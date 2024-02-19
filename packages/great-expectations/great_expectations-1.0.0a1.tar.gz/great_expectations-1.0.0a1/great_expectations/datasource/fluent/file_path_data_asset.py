from __future__ import annotations

import copy
import logging
import warnings
from collections import Counter
from pprint import pformat as pf
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Pattern,
    Set,
)

import great_expectations.exceptions as gx_exceptions
from great_expectations._docs_decorators import public_api
from great_expectations.compatibility import pydantic
from great_expectations.compatibility.typing_extensions import override
from great_expectations.datasource.fluent.batch_request import (
    BatchRequest,
    BatchRequestOptions,
)
from great_expectations.datasource.fluent.constants import MATCH_ALL_PATTERN
from great_expectations.datasource.fluent.data_asset.data_connector import (
    FILE_PATH_BATCH_SPEC_KEY,
)
from great_expectations.datasource.fluent.data_asset.data_connector.file_path_data_connector import (
    FilePathDataConnector,
    file_get_unfiltered_batch_definition_list_fn,
)
from great_expectations.datasource.fluent.data_asset.data_connector.regex_parser import (
    RegExParser,
)
from great_expectations.datasource.fluent.interfaces import (
    Batch,
    DataAsset,
    TestConnectionError,
)
from great_expectations.datasource.fluent.spark_generic_partitioners import (
    Partitioner,
    PartitionerColumnValue,
    PartitionerDatetimePart,
    PartitionerDividedInteger,
    PartitionerModInteger,
    PartitionerMultiColumnValue,
    PartitionerYear,
    PartitionerYearAndMonth,
    PartitionerYearAndMonthAndDay,
)

if TYPE_CHECKING:
    from typing_extensions import Self

    from great_expectations.core.batch import BatchDefinition, BatchMarkers
    from great_expectations.core.id_dict import BatchSpec
    from great_expectations.datasource.fluent.data_asset.data_connector import (
        DataConnector,
    )
    from great_expectations.datasource.fluent.interfaces import (
        BatchMetadata,
        BatchSlice,
    )
    from great_expectations.execution_engine import (
        PandasExecutionEngine,
        SparkDFExecutionEngine,
    )

logger = logging.getLogger(__name__)


class _FilePathDataAsset(DataAsset):
    _EXCLUDE_FROM_READER_OPTIONS: ClassVar[Set[str]] = {
        "type",
        "name",
        "order_by",
        "batch_metadata",
        "batching_regex",  # file_path argument
        "kwargs",  # kwargs need to be unpacked and passed separately
        "batch_metadata",  # noqa: PLW0130
        "connect_options",
        "id",
    }

    # General file-path DataAsset pertaining attributes.
    batching_regex: Pattern = (  # must use typing.Pattern for pydantic < v1.10
        MATCH_ALL_PATTERN
    )
    connect_options: Mapping = pydantic.Field(
        default_factory=dict,
        description="Optional filesystem specific advanced parameters for connecting to data assets",
    )
    partitioner: Optional[Partitioner] = None

    _unnamed_regex_param_prefix: str = pydantic.PrivateAttr(
        default="batch_request_param_"
    )
    _regex_parser: RegExParser = pydantic.PrivateAttr()

    _all_group_name_to_group_index_mapping: Dict[str, int] = pydantic.PrivateAttr()
    _all_group_index_to_group_name_mapping: Dict[int, str] = pydantic.PrivateAttr()
    _all_group_names: List[str] = pydantic.PrivateAttr()

    # `_data_connector`` should be set inside `_build_data_connector()`
    _data_connector: DataConnector = pydantic.PrivateAttr()
    # more specific `_test_connection_error_message` can be set inside `_build_data_connector()`
    _test_connection_error_message: str = pydantic.PrivateAttr(
        "Could not connect to your asset"
    )

    class Config:
        """
        Need to allow extra fields for the base type because pydantic will first create
        an instance of `_FilePathDataAsset` before we select and create the more specific
        asset subtype.
        Each specific subtype should `forbid` extra fields.
        """

        extra = pydantic.Extra.allow

    def __init__(self, **data):
        super().__init__(**data)

        self._regex_parser = RegExParser(
            regex_pattern=self.batching_regex,
            unnamed_regex_group_prefix=self._unnamed_regex_param_prefix,
        )

        self._all_group_name_to_group_index_mapping = (
            self._regex_parser.get_all_group_name_to_group_index_mapping()
        )
        self._all_group_index_to_group_name_mapping = (
            self._regex_parser.get_all_group_index_to_group_name_mapping()
        )
        self._all_group_names = self._regex_parser.get_all_group_names()

    @property
    @override
    def batch_request_options(
        self,
    ) -> tuple[str, ...]:
        """The potential keys for BatchRequestOptions.

        Example:
        ```python
        >>> print(asset.batch_request_options)
        ("day", "month", "year", "path")
        >>> options = {"year": "2023"}
        >>> batch_request = asset.build_batch_request(options=options)
        ```

        Returns:
            A tuple of keys that can be used in a BatchRequestOptions dictionary.
        """
        partitioner_options: tuple[str, ...] = tuple()
        if self.partitioner:
            partitioner_options = tuple(self.partitioner.param_names)
        return (
            tuple(self._all_group_names)
            + (FILE_PATH_BATCH_SPEC_KEY,)
            + partitioner_options
        )

    @public_api
    @override
    def build_batch_request(
        self,
        options: Optional[BatchRequestOptions] = None,
        batch_slice: Optional[BatchSlice] = None,
    ) -> BatchRequest:
        """A batch request that can be used to obtain batches for this DataAsset.

        Args:
            options: A dict that can be used to filter the batch groups returned from the asset.
                The dict structure depends on the asset type. The available keys for dict can be obtained by
                calling batch_request_options.
            batch_slice: A python slice that can be used to limit the sorted batches by index.
                e.g. `batch_slice = "[-5:]"` will request only the last 5 batches after the options filter is applied.

        Returns:
            A BatchRequest object that can be used to obtain a batch list from a Datasource by calling the
            get_batch_list_from_batch_request method.

        Note:
            Option "batch_slice" is supported for all "DataAsset" extensions of this class identically.  This mechanism
            applies to every "Datasource" type and any "ExecutionEngine" that is capable of loading data from files on
            local and/or cloud/networked filesystems (currently, Pandas and Spark backends work with files).
        """
        if options:
            for option, value in options.items():
                if (
                    option in self._all_group_name_to_group_index_mapping
                    and value
                    and not isinstance(value, str)
                ):
                    raise gx_exceptions.InvalidBatchRequestError(
                        f"All batching_regex matching options must be strings. The value of '{option}' is "
                        f"not a string: {value}"
                    )

        if options is not None and not self._valid_batch_request_options(options):
            allowed_keys = set(self.batch_request_options)
            actual_keys = set(options.keys())
            raise gx_exceptions.InvalidBatchRequestError(
                "Batch request options should only contain keys from the following set:\n"
                f"{allowed_keys}\nbut your specified keys contain\n"
                f"{actual_keys.difference(allowed_keys)}\nwhich is not valid.\n"
            )

        return BatchRequest(
            datasource_name=self.datasource.name,
            data_asset_name=self.name,
            options=options or {},
            batch_slice=batch_slice,
        )

    @override
    def _validate_batch_request(self, batch_request: BatchRequest) -> None:
        """Validates the batch_request has the correct form.

        Args:
            batch_request: A batch request object to be validated.
        """
        if not (
            batch_request.datasource_name == self.datasource.name
            and batch_request.data_asset_name == self.name
            and self._valid_batch_request_options(batch_request.options)
        ):
            options = {option: None for option in self.batch_request_options}
            expect_batch_request_form = BatchRequest(
                datasource_name=self.datasource.name,
                data_asset_name=self.name,
                options=options,
                batch_slice=batch_request._batch_slice_input,  # type: ignore[attr-defined]
            )
            raise gx_exceptions.InvalidBatchRequestError(
                "BatchRequest should have form:\n"
                f"{pf(expect_batch_request_form.dict())}\n"
                f"but actually has form:\n{pf(batch_request.dict())}\n"
            )

    @override
    def get_batch_list_from_batch_request(
        self, batch_request: BatchRequest
    ) -> List[Batch]:
        self._validate_batch_request(batch_request)

        execution_engine: PandasExecutionEngine | SparkDFExecutionEngine = (
            self.datasource.get_execution_engine()
        )

        batch_definition_list = self._get_batch_definition_list(batch_request)

        batch_list: List[Batch] = []

        batch_spec: BatchSpec
        batch_data: Any
        batch_markers: BatchMarkers
        batch_metadata: BatchMetadata
        batch: Batch
        for batch_definition in batch_definition_list:
            batch_spec = self._data_connector.build_batch_spec(
                batch_definition=batch_definition
            )
            batch_spec_options = self._batch_spec_options_from_batch_request(
                batch_request
            )
            batch_spec.update(batch_spec_options)

            batch_data, batch_markers = execution_engine.get_batch_data_and_markers(
                batch_spec=batch_spec
            )

            fully_specified_batch_request = copy.deepcopy(batch_request)
            fully_specified_batch_request.options.update(
                batch_definition.batch_identifiers
            )
            batch_metadata = self._get_batch_metadata_from_batch_request(
                batch_request=fully_specified_batch_request
            )

            batch = Batch(
                datasource=self.datasource,
                data_asset=self,
                batch_request=fully_specified_batch_request,
                data=batch_data,
                metadata=batch_metadata,
                batch_markers=batch_markers,
                batch_spec=batch_spec,
                batch_definition=batch_definition,
            )
            batch_list.append(batch)

        # TODO: <Alex>ALEX_INCLUDE_SORTERS_FUNCTIONALITY_UNDER_PYDANTIC-MAKE_SURE_SORTER_CONFIGURATIONS_ARE_VALIDATED</Alex>
        # TODO: <Alex>ALEX-MOVE_SORTING_INTO_FILE_PATH_DATA_CONNECTOR_ON_BATCH_DEFINITION_OBJECTS</Alex>
        self.sort_batches(batch_list)

        return batch_list

    def _get_batch_definition_list(
        self, batch_request: BatchRequest
    ) -> list[BatchDefinition]:
        """Generate a batch definition list from a given batch request, handling a partitioner config if present.

        Args:
            batch_request: Batch request used to generate batch definitions.

        Returns:
            List of batch definitions.
        """
        if self.partitioner:
            # Remove the partitioner kwargs from the batch_request to retrieve the batch and add them back later to the batch_spec.options
            batch_request_options_counts = Counter(self.batch_request_options)
            batch_request_copy_without_partitioner_kwargs = copy.deepcopy(batch_request)
            for param_name in self.partitioner.param_names:
                # If the option appears twice (e.g. from asset regex and from partitioner) then don't remove.
                if batch_request_options_counts[param_name] == 1:
                    batch_request_copy_without_partitioner_kwargs.options.pop(
                        param_name
                    )
                else:
                    warnings.warn(
                        f"The same option name is applied for your batch regex and partitioner config: {param_name}"
                    )
            batch_definition_list = self._data_connector.get_batch_definition_list(
                batch_request=batch_request_copy_without_partitioner_kwargs
            )
        else:
            batch_definition_list = self._data_connector.get_batch_definition_list(
                batch_request=batch_request
            )
        return batch_definition_list

    def _batch_spec_options_from_batch_request(
        self, batch_request: BatchRequest
    ) -> dict:
        """Build a set of options for use in a batch spec from a batch request.

        Args:
            batch_request: Batch request to use to generate options.

        Returns:
            Dictionary containing batch spec options.
        """
        get_reader_options_include: set[str] | None = self._get_reader_options_include()
        if not get_reader_options_include:
            # Set to None if empty set to include any additional `extra_kwargs` passed to `add_*_asset`
            get_reader_options_include = None
        batch_spec_options = {
            "reader_method": self._get_reader_method(),
            "reader_options": self.dict(
                include=get_reader_options_include,
                exclude=self._EXCLUDE_FROM_READER_OPTIONS,
                exclude_unset=True,
                by_alias=True,
                config_provider=self._datasource._config_provider,
            ),
        }

        if self.partitioner:
            batch_spec_options["partitioner_method"] = self.partitioner.method_name
            partitioner_kwargs = self.partitioner.partitioner_method_kwargs()
            partitioner_kwargs[
                "batch_identifiers"
            ] = self.partitioner.batch_request_options_to_batch_spec_kwarg_identifiers(
                batch_request.options
            )
            batch_spec_options["partitioner_kwargs"] = partitioner_kwargs

        return batch_spec_options

    @override
    def test_connection(self) -> None:
        """Test the connection for the DataAsset.

        Raises:
            TestConnectionError: If the connection test fails.
        """
        try:
            if self._data_connector.test_connection():
                return None
        except Exception as e:
            raise TestConnectionError(
                f"Could not connect to asset using {type(self._data_connector).__name__}: Got {type(e).__name__}"
            ) from e
        raise TestConnectionError(self._test_connection_error_message)

    def get_unfiltered_batch_definition_list_fn(
        self,
    ) -> Callable[[FilePathDataConnector, BatchRequest], list[BatchDefinition]]:
        """Get the asset specific function for retrieving the unfiltered list of batch definitions."""
        return file_get_unfiltered_batch_definition_list_fn

    def _get_reader_method(self) -> str:
        raise NotImplementedError(
            """One needs to explicitly provide "reader_method" for File-Path style DataAsset extensions as temporary \
work-around, until "type" naming convention and method for obtaining 'reader_method' from it are established."""
        )

    def _get_reader_options_include(self) -> set[str]:
        raise NotImplementedError(
            """One needs to explicitly provide set(str)-valued reader options for "pydantic.BaseModel.dict()" method \
to use as its "include" directive for File-Path style DataAsset processing."""
        )

    def _add_partitioner(self: Self, partitioner: Partitioner) -> Self:
        self.partitioner = partitioner
        return self

    @public_api
    def add_partitioner_year(
        self: Self,
        column_name: str,
    ) -> Self:
        """Associates a year partitioner with this data asset.
        Args:
            column_name: A column name of the date column where year will be parsed out.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerYear(method_name="partition_on_year", column_name=column_name)
        )

    @public_api
    def add_partitioner_year_and_month(
        self: Self,
        column_name: str,
    ) -> Self:
        """Associates a year, month partitioner with this asset.
        Args:
            column_name: A column name of the date column where year and month will be parsed out.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerYearAndMonth(
                method_name="partition_on_year_and_month", column_name=column_name
            )
        )

    @public_api
    def add_partitioner_year_and_month_and_day(
        self: Self,
        column_name: str,
    ) -> Self:
        """Associates a year, month, day partitioner with this asset.
        Args:
            column_name: A column name of the date column where year and month will be parsed out.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerYearAndMonthAndDay(
                method_name="partition_on_year_and_month_and_day",
                column_name=column_name,
            )
        )

    @public_api
    def add_partitioner_datetime_part(
        self: Self, column_name: str, datetime_parts: List[str]
    ) -> Self:
        """Associates a datetime part partitioner with this asset.
        Args:
            column_name: Name of the date column where parts will be parsed out.
            datetime_parts: A list of datetime parts to partition on, specified as DatePart objects or as their string equivalent e.g. "year", "month", "week", "day", "hour", "minute", or "second"
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerDatetimePart(
                method_name="partition_on_date_parts",
                column_name=column_name,
                datetime_parts=datetime_parts,
            )
        )

    @public_api
    def add_partitioner_column_value(self: Self, column_name: str) -> Self:
        """Associates a column value partitioner with this asset.
        Args:
            column_name: A column name of the column to partition on.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerColumnValue(
                method_name="partition_on_column_value",
                column_name=column_name,
            )
        )

    @public_api
    def add_partitioner_divided_integer(
        self: Self, column_name: str, divisor: int
    ) -> Self:
        """Associates a divided integer partitioner with this asset.
        Args:
            column_name: A column name of the column to partition on.
            divisor: The divisor to use when partitioning.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerDividedInteger(
                method_name="partition_on_divided_integer",
                column_name=column_name,
                divisor=divisor,
            )
        )

    @public_api
    def add_partitioner_mod_integer(self: Self, column_name: str, mod: int) -> Self:
        """Associates a mod integer partitioner with this asset.
        Args:
            column_name: A column name of the column to partition on.
            mod: The mod to use when partitioning.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerModInteger(
                method_name="partition_on_mod_integer",
                column_name=column_name,
                mod=mod,
            )
        )

    @public_api
    def add_partitioner_multi_column_values(
        self: Self, column_names: list[str]
    ) -> Self:
        """Associates a multi-column value partitioner with this asset.
        Args:
            column_names: A list of column names to partition on.
        Returns:
            This asset so we can use this method fluently.
        """
        return self._add_partitioner(
            PartitionerMultiColumnValue(
                column_names=column_names,
                method_name="partition_on_multi_column_values",
            )
        )
