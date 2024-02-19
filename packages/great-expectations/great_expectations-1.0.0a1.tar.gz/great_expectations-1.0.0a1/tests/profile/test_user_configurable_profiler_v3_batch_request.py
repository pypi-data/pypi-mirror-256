import random
import string
from unittest import mock

import pandas as pd
import pytest

from great_expectations.compatibility import sqlalchemy
from great_expectations.compatibility.sqlalchemy_compatibility_wrappers import (
    add_dataframe_to_db,
)
from great_expectations.core.batch import Batch, RuntimeBatchRequest
from great_expectations.core.util import get_or_create_spark_application
from great_expectations.data_context.types.base import ProgressBarsConfig
from great_expectations.execution_engine import SqlAlchemyExecutionEngine
from great_expectations.execution_engine.sqlalchemy_batch_data import (
    SqlAlchemyBatchData,
)
from great_expectations.profile.base import (
    OrderedProfilerCardinality,
    ProfilerSemanticTypes,
)
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)
from great_expectations.self_check.util import (
    get_sql_dialect_floating_point_infinity_value,
)
from great_expectations.validator.validator import Validator
from tests.profile.conftest import get_set_of_columns_and_expectations_from_suite

try:
    postgresqltypes = sqlalchemy.dialects.postgresql

    POSTGRESQL_TYPES = {
        "TEXT": postgresqltypes.TEXT,
        "CHAR": postgresqltypes.CHAR,
        "INTEGER": postgresqltypes.INTEGER,
        "SMALLINT": postgresqltypes.SMALLINT,
        "BIGINT": postgresqltypes.BIGINT,
        "TIMESTAMP": postgresqltypes.TIMESTAMP,
        "DATE": postgresqltypes.DATE,
        "DOUBLE_PRECISION": postgresqltypes.DOUBLE_PRECISION,
        "BOOLEAN": postgresqltypes.BOOLEAN,
        "NUMERIC": postgresqltypes.NUMERIC,
    }
except (ImportError, AttributeError):
    postgresqltypes = None
    POSTGRESQL_TYPES = {}


def get_pandas_runtime_validator(context, df):
    batch_request = RuntimeBatchRequest(
        datasource_name="my_pandas_runtime_datasource",
        data_connector_name="my_data_connector",
        data_asset_name="IN_MEMORY_DATA_ASSET",
        runtime_parameters={"batch_data": df},
        batch_identifiers={
            "an_example_key": "a",
            "another_example_key": "b",
        },
    )

    expectation_suite = context.add_expectation_suite("my_suite")

    validator = context.get_validator(
        batch_request=batch_request, expectation_suite=expectation_suite
    )

    return validator


def get_spark_runtime_validator(context, df):
    spark = get_or_create_spark_application(
        spark_config={
            "spark.sql.catalogImplementation": "hive",
            "spark.executor.memory": "450m",
            # "spark.driver.allowMultipleContexts": "true",  # This directive does not appear to have any effect.
        }
    )
    df = spark.createDataFrame(df)
    batch_request = RuntimeBatchRequest(
        datasource_name="my_spark_datasource",
        data_connector_name="my_data_connector",
        data_asset_name="IN_MEMORY_DATA_ASSET",
        runtime_parameters={"batch_data": df},
        batch_identifiers={
            "an_example_key": "a",
            "another_example_key": "b",
        },
    )

    expectation_suite = context.add_expectation_suite("my_suite")

    validator = context.get_validator(
        batch_request=batch_request, expectation_suite=expectation_suite
    )

    return validator


def get_sqlalchemy_runtime_validator_postgresql(
    df,
    postgresql_engine,
    schemas=None,
    caching=True,
    table_name=None,
):
    sa_engine_name = "postgresql"
    # noinspection PyUnresolvedReferences
    try:
        engine = postgresql_engine
    except (sqlalchemy.OperationalError, ModuleNotFoundError):
        return None

    sql_dtypes = {}

    if (
        schemas
        and sa_engine_name in schemas
        and isinstance(engine.dialect, postgresqltypes.dialect)
    ):
        schema = schemas[sa_engine_name]
        sql_dtypes = {col: POSTGRESQL_TYPES[dtype] for (col, dtype) in schema.items()}

        for col in schema:
            type_ = schema[col]
            if type_ in ["INTEGER", "SMALLINT", "BIGINT"]:
                df[col] = pd.to_numeric(df[col], downcast="signed")
            elif type_ in ["FLOAT", "DOUBLE", "DOUBLE_PRECISION"]:
                df[col] = pd.to_numeric(df[col])
                min_value_dbms = get_sql_dialect_floating_point_infinity_value(
                    schema=sa_engine_name, negative=True
                )
                max_value_dbms = get_sql_dialect_floating_point_infinity_value(
                    schema=sa_engine_name, negative=False
                )
                for api_schema_type in ["api_np", "api_cast"]:
                    min_value_api = get_sql_dialect_floating_point_infinity_value(
                        schema=api_schema_type, negative=True
                    )
                    max_value_api = get_sql_dialect_floating_point_infinity_value(
                        schema=api_schema_type, negative=False
                    )
                    df.replace(
                        to_replace=[min_value_api, max_value_api],
                        value=[min_value_dbms, max_value_dbms],
                        inplace=True,
                    )
            elif type_ in ["DATETIME", "TIMESTAMP"]:
                df[col] = pd.to_datetime(df[col])

    if table_name is None:
        table_name = "test_data_" + "".join(
            [random.choice(string.ascii_letters + string.digits) for _ in range(8)]
        )
    add_dataframe_to_db(
        df=df,
        name=table_name,
        con=engine,
        index=False,
        dtype=sql_dtypes,
        if_exists="replace",
    )
    execution_engine = SqlAlchemyExecutionEngine(caching=caching, engine=engine)
    batch_data = SqlAlchemyBatchData(
        execution_engine=execution_engine, table_name=table_name
    )
    batch = Batch(data=batch_data)

    return Validator(execution_engine=execution_engine, batches=[batch])


@pytest.fixture()
def nulls_validator(titanic_data_context_modular_api):
    df = pd.DataFrame(
        {
            "mostly_null": [i if i % 3 == 0 else None for i in range(0, 1000)],
            "mostly_not_null": [None if i % 3 == 0 else i for i in range(0, 1000)],
        }
    )

    validator = get_pandas_runtime_validator(titanic_data_context_modular_api, df)

    return validator


@pytest.fixture()
def cardinality_validator(titanic_data_context_modular_api):
    """
    What does this test do and why?
    Ensures that all available expectation types work as expected
    """
    df = pd.DataFrame(
        {
            # TODO: Uncomment assertions that use col_none when proportion_of_unique_values bug is fixed for columns
            #  that are all NULL/None
            # "col_none": [None for i in range(0, 1000)],
            "col_one": [0 for _ in range(0, 1000)],
            "col_two": [i % 2 for i in range(0, 1000)],
            "col_very_few": [i % 10 for i in range(0, 1000)],
            "col_few": [i % 50 for i in range(0, 1000)],
            "col_many": [i % 100 for i in range(0, 1000)],
            "col_very_many": [i % 500 for i in range(0, 1000)],
            "col_unique": [i for i in range(0, 1000)],
        }
    )
    return get_pandas_runtime_validator(titanic_data_context_modular_api, df)


@pytest.fixture
def taxi_data_ignored_columns():
    return [
        "pickup_location_id",
        "dropoff_location_id",
        "fare_amount",
        "extra",
        "mta_tax",
        "tip_amount",
        "tolls_amount",
        "improvement_surcharge",
        "congestion_surcharge",
        "pickup_datetime",
    ]


@pytest.fixture
def taxi_data_semantic_types():
    return {
        "numeric": ["total_amount", "passenger_count"],
        "value_set": [
            "payment_type",
            "rate_code_id",
            "store_and_fwd_flag",
            "passenger_count",
        ],
        "boolean": ["store_and_fwd_flag"],
    }


@pytest.mark.big
def test_profiler_init_no_config(
    cardinality_validator,
):
    """
    What does this test do and why?
    Confirms that profiler can initialize with no config.
    """
    profiler = UserConfigurableProfiler(cardinality_validator)
    assert profiler.primary_or_compound_key == []
    assert profiler.ignored_columns == []
    assert profiler.value_set_threshold == "MANY"
    assert not profiler.table_expectations_only
    assert profiler.excluded_expectations == []


@pytest.mark.big
def test_profiler_init_full_config_no_semantic_types(cardinality_validator):
    """
    What does this test do and why?
    Confirms that profiler initializes properly with a full config, without a semantic_types dict
    """

    profiler = UserConfigurableProfiler(
        cardinality_validator,
        primary_or_compound_key=["col_unique"],
        ignored_columns=["col_one"],
        value_set_threshold="UNIQUE",
        table_expectations_only=False,
        excluded_expectations=["expect_column_values_to_not_be_null"],
    )
    assert profiler.primary_or_compound_key == ["col_unique"]
    assert profiler.ignored_columns == [
        "col_one",
    ]
    assert profiler.value_set_threshold == "UNIQUE"
    assert not profiler.table_expectations_only
    assert profiler.excluded_expectations == ["expect_column_values_to_not_be_null"]

    assert "col_one" not in profiler.column_info


@pytest.mark.big
def test_init_with_semantic_types(cardinality_validator):
    """
    What does this test do and why?
    Confirms that profiler initializes properly with a full config and a semantic_types dict
    """

    semantic_types = {
        "numeric": ["col_few", "col_many", "col_very_many"],
        "value_set": ["col_two", "col_very_few"],
    }
    profiler = UserConfigurableProfiler(
        cardinality_validator,
        semantic_types_dict=semantic_types,
        primary_or_compound_key=["col_unique"],
        ignored_columns=["col_one"],
        value_set_threshold="unique",
        table_expectations_only=False,
        excluded_expectations=["expect_column_values_to_not_be_null"],
    )

    assert "col_one" not in profiler.column_info

    assert profiler.column_info.get("col_two") == {
        "cardinality": "TWO",
        "type": "INT",
        "semantic_types": ["VALUE_SET"],
    }
    assert profiler.column_info.get("col_very_few") == {
        "cardinality": "VERY_FEW",
        "type": "INT",
        "semantic_types": ["VALUE_SET"],
    }
    assert profiler.column_info.get("col_few") == {
        "cardinality": "FEW",
        "type": "INT",
        "semantic_types": ["NUMERIC"],
    }
    assert profiler.column_info.get("col_many") == {
        "cardinality": "MANY",
        "type": "INT",
        "semantic_types": ["NUMERIC"],
    }
    assert profiler.column_info.get("col_very_many") == {
        "cardinality": "VERY_MANY",
        "type": "INT",
        "semantic_types": ["NUMERIC"],
    }
    assert profiler.column_info.get("col_unique") == {
        "cardinality": "UNIQUE",
        "type": "INT",
        "semantic_types": [],
    }


@pytest.mark.big
def test__validate_config(cardinality_validator):
    """
    What does this test do and why?
    Tests the validate config function on the profiler
    """

    with pytest.raises(AssertionError) as e:
        # noinspection PyTypeChecker
        UserConfigurableProfiler(cardinality_validator, ignored_columns="col_name")
    assert e.typename == "AssertionError"

    with pytest.raises(AssertionError) as e:
        # noinspection PyTypeChecker
        UserConfigurableProfiler(cardinality_validator, table_expectations_only="True")
    assert e.typename == "AssertionError"


@pytest.mark.slow  # 1.18s
@pytest.mark.big
def test__validate_semantic_types_dict(cardinality_validator):
    """
    What does this test do and why?
    Tests that _validate_semantic_types_dict function errors when not formatted correctly
    """

    bad_semantic_types_dict_type = {"value_set": "col_few"}
    with pytest.raises(AssertionError) as e:
        # noinspection PyTypeChecker
        UserConfigurableProfiler(
            cardinality_validator, semantic_types_dict=bad_semantic_types_dict_type
        )
    assert e.value.args[0] == (
        "Entries in semantic type dict must be lists of column names e.g. "
        "{'semantic_types': {'numeric': ['number_of_transactions']}}"
    )

    bad_semantic_types_incorrect_type = {"incorrect_type": ["col_few"]}
    with pytest.raises(ValueError) as e:
        UserConfigurableProfiler(
            cardinality_validator, semantic_types_dict=bad_semantic_types_incorrect_type
        )
    assert e.value.args[0] == (
        f"incorrect_type is not a recognized semantic_type. Please only include one of "
        f"{[semantic_type.value for semantic_type in ProfilerSemanticTypes]}"
    )

    # Error if column is specified for both semantic_types and ignored
    working_semantic_type = {"numeric": ["col_few"]}
    with pytest.raises(ValueError) as e:
        UserConfigurableProfiler(
            cardinality_validator,
            semantic_types_dict=working_semantic_type,
            ignored_columns=["col_few"],
        )
    assert e.value.args[0] == (
        "Column col_few is specified in both the semantic_types_dict and the list of ignored columns. Please remove "
        "one of these entries to proceed."
    )


@pytest.mark.filesystem
def test_profiler_works_with_batch_object(cardinality_validator):
    profiler = UserConfigurableProfiler(cardinality_validator.active_batch)
    assert profiler.primary_or_compound_key == []
    assert profiler.ignored_columns == []
    assert profiler.value_set_threshold == "MANY"
    assert not profiler.table_expectations_only
    assert profiler.excluded_expectations == []

    assert profiler.all_table_columns == [
        "col_one",
        "col_two",
        "col_very_few",
        "col_few",
        "col_many",
        "col_very_many",
        "col_unique",
    ]


@pytest.mark.slow  # 1.18s
@pytest.mark.filesystem
def test_build_suite_with_semantic_types_dict(
    cardinality_validator,
    possible_expectations_set,
):
    """
    What does this test do and why?
    Tests that the build_suite function works as expected with a semantic_types dict
    """

    semantic_types = {
        "numeric": ["col_few", "col_many", "col_very_many"],
        "value_set": ["col_two", "col_very_few"],
    }

    profiler = UserConfigurableProfiler(
        cardinality_validator,
        semantic_types_dict=semantic_types,
        primary_or_compound_key=["col_unique"],
        ignored_columns=["col_one"],
        value_set_threshold="unique",
        table_expectations_only=False,
        excluded_expectations=["expect_column_values_to_not_be_null"],
    )
    suite = profiler.build_suite()
    (
        columns_with_expectations,
        expectations_from_suite,
    ) = get_set_of_columns_and_expectations_from_suite(suite)

    assert "column_one" not in columns_with_expectations
    assert "expect_column_values_to_not_be_null" not in expectations_from_suite
    assert expectations_from_suite.issubset(possible_expectations_set)
    assert len(suite.expectations) == 32

    value_set_expectations = [
        i
        for i in suite.expectation_configurations
        if i.expectation_type == "expect_column_values_to_be_in_set"
    ]
    value_set_columns = {i.kwargs.get("column") for i in value_set_expectations}

    assert len(value_set_columns) == 2
    assert value_set_columns == {"col_two", "col_very_few"}


@pytest.mark.filesystem
def test_build_suite_when_suite_already_exists(
    cardinality_validator,
):
    """
    What does this test do and why?
    Confirms that creating a new suite on an existing profiler wipes the previous suite
    """
    profiler = UserConfigurableProfiler(
        cardinality_validator,
        table_expectations_only=True,
        excluded_expectations=["expect_table_row_count_to_be_between"],
    )

    suite = profiler.build_suite()
    _, expectations = get_set_of_columns_and_expectations_from_suite(suite)
    assert len(suite.expectations) == 1
    assert "expect_table_columns_to_match_ordered_list" in expectations

    profiler.excluded_expectations = ["expect_table_columns_to_match_ordered_list"]
    suite = profiler.build_suite()
    _, expectations = get_set_of_columns_and_expectations_from_suite(suite)
    assert len(suite.expectations) == 1
    assert "expect_table_row_count_to_be_between" in expectations


@pytest.mark.slow  # 1.01s
@pytest.mark.filesystem
def test_primary_or_compound_key_not_found_in_columns(cardinality_validator):
    """
    What does this test do and why?
    Confirms that an error is raised if a primary_or_compound key is specified with a column not found in the validator
    """
    # regular case, should pass
    working_profiler = UserConfigurableProfiler(
        cardinality_validator, primary_or_compound_key=["col_unique"]
    )
    assert working_profiler.primary_or_compound_key == ["col_unique"]

    # key includes a non-existent column, should fail
    with pytest.raises(ValueError) as e:
        # noinspection PyUnusedLocal
        bad_key_profiler = UserConfigurableProfiler(  # noqa: F841
            cardinality_validator,
            primary_or_compound_key=["col_unique", "col_that_does_not_exist"],
        )
    assert e.value.args[0] == (
        """Column col_that_does_not_exist not found. Please ensure that this column is in the Validator if you would \
like to use it as a primary_or_compound_key.
"""
    )

    # key includes a column that exists, but is in ignored_columns, should pass
    ignored_column_profiler = UserConfigurableProfiler(
        cardinality_validator,
        primary_or_compound_key=["col_unique", "col_one"],
        ignored_columns=["col_none", "col_one"],
    )
    assert ignored_column_profiler.primary_or_compound_key == ["col_unique", "col_one"]


@pytest.mark.slow  # 1.28s
@pytest.mark.filesystem
def test_config_with_not_null_only(nulls_validator, possible_expectations_set):
    """
    What does this test do and why?
    Confirms that the not_null_only key in config works as expected.
    """

    excluded_expectations = [i for i in possible_expectations_set if "null" not in i]

    validator = nulls_validator

    profiler_without_not_null_only = UserConfigurableProfiler(
        validator, excluded_expectations, not_null_only=False
    )
    suite_without_not_null_only = profiler_without_not_null_only.build_suite()
    _, expectations = get_set_of_columns_and_expectations_from_suite(
        suite_without_not_null_only
    )
    assert expectations == {
        "expect_column_values_to_be_null",
        "expect_column_values_to_not_be_null",
    }

    profiler_with_not_null_only = UserConfigurableProfiler(
        validator, excluded_expectations, not_null_only=True
    )
    not_null_only_suite = profiler_with_not_null_only.build_suite()
    _, expectations = get_set_of_columns_and_expectations_from_suite(
        not_null_only_suite
    )
    assert expectations == {"expect_column_values_to_not_be_null"}

    no_config_profiler = UserConfigurableProfiler(validator)
    no_config_suite = no_config_profiler.build_suite()
    _, expectations = get_set_of_columns_and_expectations_from_suite(no_config_suite)
    assert "expect_column_values_to_be_null" in expectations


@pytest.mark.filesystem
def test_nullity_expectations_mostly_tolerance(
    nulls_validator, possible_expectations_set
):
    excluded_expectations = [i for i in possible_expectations_set if "null" not in i]

    validator = nulls_validator

    profiler = UserConfigurableProfiler(
        validator, excluded_expectations, not_null_only=False
    )
    suite = profiler.build_suite()

    for i in suite.expectation_configurations:
        assert i["kwargs"]["mostly"] == 0.66


@pytest.mark.slow  # 2.44s
@pytest.mark.filesystem
def test_profiled_dataset_passes_own_validation(
    cardinality_validator, titanic_data_context
):
    """
    What does this test do and why?
    Confirms that a suite created on a validator with no config will pass when validated against itself
    """
    context = titanic_data_context
    profiler = UserConfigurableProfiler(
        cardinality_validator, ignored_columns=["col_none"]
    )
    suite = profiler.build_suite()

    context.add_expectation_suite(expectation_suite=suite)
    results = context.run_validation_operator(
        "action_list_operator", assets_to_validate=[cardinality_validator]
    )

    assert results["success"]


@pytest.mark.filesystem
def test_column_cardinality_functions(cardinality_validator):
    profiler = UserConfigurableProfiler(cardinality_validator)
    # assert profiler.column_info.get("col_none").get("cardinality") == "NONE"
    assert profiler.column_info.get("col_one").get("cardinality") == "ONE"
    assert profiler.column_info.get("col_two").get("cardinality") == "TWO"
    assert profiler.column_info.get("col_very_few").get("cardinality") == "VERY_FEW"
    assert profiler.column_info.get("col_few").get("cardinality") == "FEW"
    assert profiler.column_info.get("col_many").get("cardinality") == "MANY"
    assert profiler.column_info.get("col_very_many").get("cardinality") == "VERY_MANY"

    cardinality_with_ten_num_and_no_pct = (
        OrderedProfilerCardinality.get_basic_column_cardinality(num_unique=10)
    )
    assert cardinality_with_ten_num_and_no_pct.name == "VERY_FEW"

    cardinality_with_unique_pct_and_no_num = (
        OrderedProfilerCardinality.get_basic_column_cardinality(pct_unique=1.0)
    )
    assert cardinality_with_unique_pct_and_no_num.name == "UNIQUE"

    cardinality_with_no_pct_and_no_num = (
        OrderedProfilerCardinality.get_basic_column_cardinality()
    )
    assert cardinality_with_no_pct_and_no_num.name == "NONE"

    cardinality_with_large_pct_and_no_num = (
        OrderedProfilerCardinality.get_basic_column_cardinality(pct_unique=0.5)
    )
    assert cardinality_with_large_pct_and_no_num.name == "NONE"


@mock.patch("great_expectations.profile.user_configurable_profiler.tqdm")
@pytest.mark.slow  # 1.28s
@pytest.mark.filesystem
def test_user_configurable_profiler_progress_bar_config_enabled(
    mock_tqdm, cardinality_validator
):
    semantic_types = {
        "numeric": ["col_few", "col_many", "col_very_many"],
        "value_set": ["col_two", "col_very_few"],
    }

    profiler = UserConfigurableProfiler(
        cardinality_validator,
        semantic_types_dict=semantic_types,
    )

    profiler.build_suite()

    assert mock_tqdm.called
    assert mock_tqdm.call_count == 1


@mock.patch("great_expectations.data_context.data_context.EphemeralDataContext")
@pytest.mark.slow  # 1.34s
@pytest.mark.filesystem
def test_user_configurable_profiler_progress_bar_config_disabled(
    mock_tqdm, cardinality_validator
):
    data_context = cardinality_validator.data_context
    data_context.project_config_with_variables_substituted.progress_bars = (
        ProgressBarsConfig(profilers=False)
    )

    semantic_types = {
        "numeric": ["col_few", "col_many", "col_very_many"],
        "value_set": ["col_two", "col_very_few"],
    }

    profiler = UserConfigurableProfiler(
        cardinality_validator,
        semantic_types_dict=semantic_types,
    )

    profiler.build_suite()

    assert not mock_tqdm.called
    assert mock_tqdm.call_count == 0
