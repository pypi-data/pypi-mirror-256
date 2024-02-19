from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, List, Optional, Union

from great_expectations._docs_decorators import public_api
from great_expectations.core.evaluation_parameters import (
    EvaluationParameterDict,  # noqa: TCH001
)
from great_expectations.exceptions import InvalidExpectationConfigurationError
from great_expectations.expectations.expectation import (
    ColumnMapExpectation,
    render_evaluation_parameter_string,
)
from great_expectations.render import (
    LegacyRendererType,
    RenderedBulletListContent,
    RenderedGraphContent,
    RenderedStringTemplateContent,
    RenderedTableContent,
)
from great_expectations.render.renderer.renderer import renderer
from great_expectations.render.renderer_configuration import (
    RendererConfiguration,
    RendererValueType,
)
from great_expectations.render.util import (
    handle_strict_min_max,
    num_to_str,
    parse_row_condition_string_pandas_engine,
    substitute_none_for_missing,
)

try:
    import sqlalchemy as sa  # noqa: F401, TID251
except ImportError:
    pass

if TYPE_CHECKING:
    from great_expectations.core import (
        ExpectationValidationResult,
    )
    from great_expectations.expectations.expectation_configuration import (
        ExpectationConfiguration,
    )
    from great_expectations.render.renderer_configuration import AddParamArgs


class ExpectColumnValueLengthsToBeBetween(ColumnMapExpectation):
    """Expect the column entries to be strings with length between a minimum value and a maximum value (inclusive).

    This expectation only works for string-type values. Invoking it on ints or floats will raise a TypeError.

    expect_column_value_lengths_to_be_between is a \
    [Column Map Expectation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_map_expectations).

    Args:
        column (str): \
            The column name.
        min_value (int or None): \
            The minimum value for a column entry length.
        max_value (int or None): \
            The maximum value for a column entry length.

    Keyword Args:
        mostly (None or a float between 0 and 1): \
            Successful if at least mostly fraction of values match the expectation. \
            For more detail, see [mostly](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#mostly).

    Other Parameters:
        result_format (str or None): \
            Which output mode to use: BOOLEAN_ONLY, BASIC, COMPLETE, or SUMMARY. \
            For more detail, see [result_format](https://docs.greatexpectations.io/docs/reference/expectations/result_format).
        catch_exceptions (boolean or None): \
            If True, then catch exceptions and include them as part of the result object. \
            For more detail, see [catch_exceptions](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#catch_exceptions).
        meta (dict or None): \
            A JSON-serializable dictionary (nesting allowed) that will be included in the output without \
            modification. For more detail, see [meta](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#meta).

    Returns:
        An [ExpectationSuiteValidationResult](https://docs.greatexpectations.io/docs/terms/validation_result)

        Exact fields vary depending on the values passed to result_format, catch_exceptions, and meta.

    Notes:
        * min_value and max_value are both inclusive.
        * If min_value is None, then max_value is treated as an upper bound, and the number of acceptable rows has \
          no minimum.
        * If max_value is None, then min_value is treated as a lower bound, and the number of acceptable rows has \
          no maximum.

    See Also:
        [expect_column_value_lengths_to_equal](https://greatexpectations.io/expectations/expect_column_value_lengths_to_equal)
    """

    min_value: Union[int, EvaluationParameterDict, datetime, None] = None
    max_value: Union[int, EvaluationParameterDict, datetime, None] = None
    strict_min: bool = False
    strict_max: bool = False

    # This dictionary contains metadata for display in the public gallery
    library_metadata = {
        "maturity": "production",
        "tags": ["core expectation", "column map expectation"],
        "contributors": ["@great_expectations"],
        "requirements": [],
        "has_full_test_suite": True,
        "manually_reviewed_code": True,
    }

    map_metric = "column_values.value_length.between"
    success_keys = (
        "min_value",
        "max_value",
        "strict_min",
        "strict_max",
        "mostly",
    )

    args_keys = (
        "column",
        "min_value",
        "max_value",
    )

    @public_api
    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration] = None
    ) -> None:
        """Validates the configuration of an Expectation.

        For `expect_column_value_lengths_to_be_between` it is required that the `configuration.kwargs` contain
        `min_value` and/or `max_value`; both cannot be None.  Both `min_value` and `max_value` may be either an integer
        or a `dict`; if a `dict`, it must include `$PARAMETER` as a key.

         The configuration will also be validated using each of the `validate_configuration` methods in its Expectation
         superclass hierarchy.

        Args:
            configuration: An `ExpectationConfiguration` to validate. If no configuration is provided, it will be pulled
                from the configuration attribute of the Expectation instance.

        Raises:
            InvalidExpectationConfigurationError: The configuration does not contain the values required by the
                Expectation.
        """
        super().validate_configuration(configuration)

        configuration = configuration or self.configuration

        try:
            assert (
                configuration.kwargs.get("min_value") is not None
                or configuration.kwargs.get("max_value") is not None
            ), "min_value and max_value cannot both be None"
            if configuration.kwargs.get("min_value"):
                assert (
                    isinstance(configuration.kwargs["min_value"], dict)
                    or float(configuration.kwargs.get("min_value")).is_integer()
                ), "min_value and max_value must be integers"
                if isinstance(configuration.kwargs.get("min_value"), dict):
                    assert "$PARAMETER" in configuration.kwargs.get(
                        "min_value"
                    ), 'Evaluation Parameter dict for min_value kwarg must have "$PARAMETER" key.'

            if configuration.kwargs.get("max_value"):
                assert (
                    isinstance(configuration.kwargs["max_value"], dict)
                    or float(configuration.kwargs.get("max_value")).is_integer()
                ), "min_value and max_value must be integers"
                if isinstance(configuration.kwargs.get("max_value"), dict):
                    assert "$PARAMETER" in configuration.kwargs.get(
                        "max_value"
                    ), 'Evaluation Parameter dict for max_value kwarg must have "$PARAMETER" key.'
        except AssertionError as e:
            raise InvalidExpectationConfigurationError(str(e))

    @classmethod
    def _prescriptive_template(  # noqa: PLR0912
        cls,
        renderer_configuration: RendererConfiguration,
    ) -> RendererConfiguration:
        add_param_args: AddParamArgs = (
            ("column", RendererValueType.STRING),
            ("min_value", [RendererValueType.NUMBER, RendererValueType.DATETIME]),
            ("max_value", [RendererValueType.NUMBER, RendererValueType.DATETIME]),
            ("mostly", RendererValueType.NUMBER),
            ("strict_min", RendererValueType.BOOLEAN),
            ("strict_max", RendererValueType.BOOLEAN),
        )
        for name, param_type in add_param_args:
            renderer_configuration.add_param(name=name, param_type=param_type)

        params = renderer_configuration.params

        if not params.min_value and not params.max_value:
            template_str = "values may have any length."
        else:
            at_least_str = "greater than or equal to"
            if params.strict_min:
                at_least_str = cls._get_strict_min_string(
                    renderer_configuration=renderer_configuration
                )
            at_most_str = "less than or equal to"
            if params.strict_max:
                at_most_str = cls._get_strict_max_string(
                    renderer_configuration=renderer_configuration
                )

            if params.mostly and params.mostly.value < 1.0:  # noqa: PLR2004
                renderer_configuration = cls._add_mostly_pct_param(
                    renderer_configuration=renderer_configuration
                )
                if params.min_value and params.max_value:
                    template_str = f"values must be {at_least_str} $min_value and {at_most_str} $max_value characters long, at least $mostly_pct % of the time."
                elif not params.min_value:
                    template_str = f"values must be {at_most_str} $max_value characters long, at least $mostly_pct % of the time."
                else:
                    template_str = f"values must be {at_least_str} $min_value characters long, at least $mostly_pct % of the time."
            else:  # noqa: PLR5501
                if params.min_value and params.max_value:
                    template_str = f"values must always be {at_least_str} $min_value and {at_most_str} $max_value characters long."
                elif not params.min_value:
                    template_str = f"values must always be {at_most_str} $max_value characters long."
                else:
                    template_str = f"values must always be {at_least_str} $min_value characters long."

        if renderer_configuration.include_column_name:
            template_str = f"$column {template_str}"

        renderer_configuration.template_str = template_str

        return renderer_configuration

    @classmethod
    @renderer(renderer_type=LegacyRendererType.PRESCRIPTIVE)
    @render_evaluation_parameter_string
    def _prescriptive_renderer(
        cls,
        configuration: Optional[ExpectationConfiguration] = None,
        result: Optional[ExpectationValidationResult] = None,
        runtime_configuration: Optional[dict] = None,
        **kwargs,
    ) -> List[
        Union[
            dict,
            str,
            RenderedStringTemplateContent,
            RenderedTableContent,
            RenderedBulletListContent,
            RenderedGraphContent,
            Any,
        ]
    ]:
        runtime_configuration = runtime_configuration or {}
        include_column_name = (
            False if runtime_configuration.get("include_column_name") is False else True
        )
        styling = runtime_configuration.get("styling")
        params = substitute_none_for_missing(
            configuration.kwargs,
            [
                "column",
                "min_value",
                "max_value",
                "mostly",
                "row_condition",
                "condition_parser",
                "strict_min",
                "strict_max",
            ],
        )

        if (params["min_value"] is None) and (params["max_value"] is None):
            template_str = "values may have any length."
        else:
            at_least_str, at_most_str = handle_strict_min_max(params)

            if params["mostly"] is not None and params["mostly"] < 1.0:  # noqa: PLR2004
                params["mostly_pct"] = num_to_str(
                    params["mostly"] * 100, no_scientific=True
                )
                # params["mostly_pct"] = "{:.14f}".format(params["mostly"]*100).rstrip("0").rstrip(".")
                if params["min_value"] is not None and params["max_value"] is not None:
                    template_str = f"values must be {at_least_str} $min_value and {at_most_str} $max_value characters long, at least $mostly_pct % of the time."

                elif params["min_value"] is None:
                    template_str = f"values must be {at_most_str} $max_value characters long, at least $mostly_pct % of the time."

                elif params["max_value"] is None:
                    template_str = f"values must be {at_least_str} $min_value characters long, at least $mostly_pct % of the time."
            else:  # noqa: PLR5501
                if params["min_value"] is not None and params["max_value"] is not None:
                    template_str = f"values must always be {at_least_str} $min_value and {at_most_str} $max_value characters long."

                elif params["min_value"] is None:
                    template_str = f"values must always be {at_most_str} $max_value characters long."

                elif params["max_value"] is None:
                    template_str = f"values must always be {at_least_str} $min_value characters long."

        if include_column_name:
            template_str = f"$column {template_str}"

        if params["row_condition"] is not None:
            (
                conditional_template_str,
                conditional_params,
            ) = parse_row_condition_string_pandas_engine(params["row_condition"])
            template_str = f"{conditional_template_str}, then {template_str}"
            params.update(conditional_params)

        return [
            RenderedStringTemplateContent(
                **{
                    "content_block_type": "string_template",
                    "string_template": {
                        "template": template_str,
                        "params": params,
                        "styling": styling,
                    },
                }
            )
        ]
