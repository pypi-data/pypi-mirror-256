from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union

from great_expectations.core.evaluation_parameters import (
    EvaluationParameterDict,  # noqa: TCH001
)
from great_expectations.expectations.expectation import (
    ColumnMapExpectation,
)
from great_expectations.render import RenderedStringTemplateContent
from great_expectations.render.components import LegacyRendererType
from great_expectations.render.renderer.renderer import renderer
from great_expectations.render.util import num_to_str, substitute_none_for_missing

if TYPE_CHECKING:
    from great_expectations.core import (
        ExpectationConfiguration,
    )
    from great_expectations.core.expectation_validation_result import (
        ExpectationValidationResult,
    )


class ExpectColumnValuesToNotMatchLikePattern(ColumnMapExpectation):
    """Expect the column entries to be strings that do NOT match a given like pattern expression.

    expect_column_values_to_not_match_like_pattern is a \
    [Column Map Expectation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_map_expectations).

    Args:
        column (str): \
            The column name.
        like_pattern (str): \
            The like pattern expression the column entries should NOT match.

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

    See Also:
        [expect_column_values_to_match_regex](https://greatexpectations.io/expectations/expect_column_values_to_match_regex)
        [expect_column_values_to_match_regex_list](https://greatexpectations.io/expectations/expect_column_values_to_match_regex_list)
        [expect_column_values_to_not_match_regex](https://greatexpectations.io/expectations/expect_column_values_to_not_match_regex)
        [expect_column_values_to_not_match_regex_list](https://greatexpectations.io/expectations/expect_column_values_to_not_match_regex_list)
        [expect_column_values_to_match_like_pattern](https://greatexpectations.io/expectations/expect_column_values_to_match_like_pattern)
        [expect_column_values_to_match_like_pattern_list](https://greatexpectations.io/expectations/expect_column_values_to_match_like_pattern_list)
        [expect_column_values_to_not_match_like_pattern_list](https://greatexpectations.io/expectations/expect_column_values_to_not_match_like_pattern_list)
    """

    like_pattern: Union[str, EvaluationParameterDict]

    library_metadata = {
        "maturity": "production",
        "tags": ["core expectation", "column map expectation"],
        "contributors": [
            "@great_expectations",
        ],
        "requirements": [],
        "has_full_test_suite": True,
        "manually_reviewed_code": True,
    }

    map_metric = "column_values.not_match_like_pattern"
    success_keys = (
        "mostly",
        "like_pattern",
    )
    args_keys = (
        "column",
        "like_pattern",
    )

    @classmethod
    @renderer(renderer_type=LegacyRendererType.PRESCRIPTIVE)
    def _prescriptive_renderer(
        cls,
        configuration: Optional[ExpectationConfiguration] = None,
        result: Optional[ExpectationValidationResult] = None,
        runtime_configuration: Optional[dict] = None,
        **kwargs,
    ) -> List[RenderedStringTemplateContent]:
        runtime_configuration = runtime_configuration or {}
        _ = False if runtime_configuration.get("include_column_name") is False else True
        styling = runtime_configuration.get("styling")

        params = substitute_none_for_missing(
            configuration.kwargs,
            ["column", "like_pattern", "mostly"],
        )
        if params["mostly"] is not None:
            params["mostly_pct"] = num_to_str(
                params["mostly"] * 100, no_scientific=True
            )
        mostly_str = (
            ""
            if params.get("mostly") is None
            else ", at least $mostly_pct % of the time"
        )

        like_pattern = params.get("like_pattern")  # noqa: F841

        template_str = (
            f"Values must not match like pattern : $like_pattern {mostly_str} "
        )

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
