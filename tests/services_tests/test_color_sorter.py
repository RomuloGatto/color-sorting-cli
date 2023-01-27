from typing import Set, Tuple

from harmony.color_sorting.constants import Directions
from harmony.color_sorting.service_layer.services import ColorSorter
from harmony.color_sorting.service_layer.sorting_strategies import SortingStrategy
from harmony.core.constants import ColorFormat
from harmony.core.models import RGB, Color


class FakeStrategy(SortingStrategy):
    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        return tuple(colors_to_sort)


class TestColorSorter:
    """Test for the color sorting service"""

    def test_sorting(self) -> None:
        """Test sorting set of colors"""
        self._then_should_sort_colors_forwards(self._when_passed_to_sort_forwards())

    def _when_passed_to_sort_forwards(self) -> Tuple[Color, ...]:
        return ColorSorter(FakeStrategy()).sort(
            self._given_parameters(), Directions.FORWARD
        )

    def _then_should_sort_colors_forwards(self, result: Tuple[Color, ...]) -> None:
        for index, color in enumerate(result):
            assert color == tuple(self._given_parameters())[index]

    def test_sorting_backwards(self) -> None:
        """Test sorting backwards"""
        arrangement = self._given_parameters()
        result = self._when_called_backwards_sorting(arrangement)
        self._then_should_sort_backwards(result)

    def _when_called_backwards_sorting(
        self, arrangement: Set[Color]
    ) -> Tuple[Color, ...]:
        return ColorSorter(FakeStrategy()).sort(arrangement, Directions.BACKWARD)

    def _then_should_sort_backwards(self, result: Tuple[Color, ...]) -> None:
        for index, color in enumerate(result):
            assert color == self._given_reversed_parameters()[index]

    def _given_reversed_parameters(self) -> Tuple[Color]:
        list_of_colors = list(self._given_parameters())
        list_of_colors.reverse()

        return list_of_colors

    def _given_parameters(self) -> Set[Color]:
        color1 = Color(
            rgb=RGB(235, 61, 52),
            hexcode="#eb3d34",
            original_format=ColorFormat.HEXCODE,
            description="red",
        )

        color2 = Color(
            rgb=RGB(75, 214, 47),
            hexcode="#4bd62f",
            original_format=ColorFormat.RGB,
            description="green",
        )

        color3 = Color(
            rgb=RGB(212, 104, 4),
            hexcode="#d46804",
            original_format=ColorFormat.HEXCODE,
            description="orange",
        )

        return {color1, color2, color3}
