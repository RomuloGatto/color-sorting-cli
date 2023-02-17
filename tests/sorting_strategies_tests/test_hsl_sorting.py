from typing import List, Tuple

from harmony import core
from harmony.color_sorting.service_layer.sorting_strategies import HSLSorting


class TestHSLSorting:
    """Tests for HSL sorting strategy"""

    def test_sorting_with_hsl_strategy(self) -> None:
        """Test sorting colors on their HSL values"""
        arrangement = self._given_parameters()
        result = self._when_sorter_set_to_hsl_strategy(arrangement)
        self._then_should_hsl_sort(result)

    def _when_sorter_set_to_hsl_strategy(
        self, arrangement: List[core.Color]
    ) -> Tuple[core.Color, ...]:
        return HSLSorting().sort(set(arrangement))

    def _then_should_hsl_sort(self, result: Tuple[core.Color, ...]) -> None:
        expected_first_color = core.Color(
            rgb=core.RGB(235, 61, 52),
            hsl=core.HSL(2, 0.78, 0.56),
            hexcode="#eb3d34",
            original_format=core.ColorFormat.HEXCODE,
            description="red",
        )
        actual_first_color = result[0]

        expected_second_color = core.Color(
            rgb=core.RGB(212, 104, 4),
            hsl=core.HSL(28, 0.98, 0.42),
            hexcode="#d46804",
            original_format=core.ColorFormat.HEXCODE,
            description="orange",
        )
        actual_second_color = result[1]

        assert expected_first_color == actual_first_color
        assert expected_second_color == actual_second_color

    def _given_parameters(self) -> List[core.Color]:
        return [
            core.Color(
                rgb=core.RGB(235, 61, 52),
                hsl=core.HSL(2, 0.78, 0.56),
                hexcode="#eb3d34",
                original_format=core.ColorFormat.HEXCODE,
                description="red",
            ),
            core.Color(
                rgb=core.RGB(75, 214, 47),
                hsl=core.HSL(109, 0.78, 0.51),
                hexcode="#4bd62f",
                original_format=core.ColorFormat.RGB,
                description="green",
            ),
            core.Color(
                rgb=core.RGB(212, 104, 4),
                hsl=core.HSL(28, 0.98, 0.42),
                hexcode="#d46804",
                original_format=core.ColorFormat.HEXCODE,
                description="orange",
            ),
        ]
