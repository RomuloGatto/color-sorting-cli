from typing import Set, Tuple

from harmony import core
from harmony.color_sorting.constants import Directions
from harmony.color_sorting.service_layer.services import ColorSorter
from harmony.color_sorting.service_layer.sorting_strategies import SortingStrategy


class FakeStrategy(SortingStrategy):
    def sort(self, colors_to_sort: Set[core.Color]) -> Tuple[core.Color, ...]:
        return tuple(colors_to_sort)


class TestColorSorter:
    """Test for the color sorting service"""

    def test_sorting(self) -> None:
        """Test sorting set of colors"""
        self._then_should_sort_colors_forwards(self._when_passed_to_sort_forwards())

    def _when_passed_to_sort_forwards(self) -> Tuple[core.Color, ...]:
        return ColorSorter(FakeStrategy()).sort(
            self._given_parameters(), Directions.FORWARD
        )

    def _then_should_sort_colors_forwards(self, result: Tuple[core.Color, ...]) -> None:
        for index, color in enumerate(result):
            assert color == tuple(self._given_parameters())[index]

    def test_sorting_backwards(self) -> None:
        """Test sorting backwards"""
        arrangement = self._given_parameters()
        result = self._when_called_backwards_sorting(arrangement)
        self._then_should_sort_backwards(result)

    def _when_called_backwards_sorting(
        self, arrangement: Set[core.Color]
    ) -> Tuple[core.Color, ...]:
        return ColorSorter(FakeStrategy()).sort(arrangement, Directions.BACKWARD)

    def _then_should_sort_backwards(self, result: Tuple[core.Color, ...]) -> None:
        for index, color in enumerate(result):
            assert color == self._given_reversed_parameters()[index]

    def _given_reversed_parameters(self) -> Tuple[core.Color]:
        list_of_colors = list(self._given_parameters())
        list_of_colors.reverse()

        return list_of_colors

    def _given_parameters(self) -> Set[core.Color]:
        color1 = core.Color(
            rgb=core.RGB(235, 61, 52),
            hsl=core.HSL(2, 0.78, 0.56),
            hexcode="#eb3d34",
            original_format=core.ColorFormat.HEXCODE,
            description="red",
        )

        color2 = core.Color(
            rgb=core.RGB(75, 214, 47),
            hsl=core.HSL(109, 0.78, 0.51),
            hexcode="#4bd62f",
            original_format=core.ColorFormat.RGB,
            description="green",
        )

        color3 = core.Color(
            rgb=core.RGB(212, 104, 4),
            hsl=core.HSL(28, 0.98, 0.42),
            hexcode="#d46804",
            original_format=core.ColorFormat.HEXCODE,
            description="orange",
        )

        return {color1, color2, color3}
