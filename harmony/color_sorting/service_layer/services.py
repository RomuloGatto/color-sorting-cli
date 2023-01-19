from typing import Dict, List, Set, Tuple, Type

from harmony.color_sorting.constants import Directions, SortingStrategyName
from harmony.color_sorting.service_layer import sorting_strategies
from harmony.core.models import Color


class ColorSorter:
    """Service for sorting colors"""

    STRATEGY_MAPPING: Dict[
        SortingStrategyName, Type[sorting_strategies.SortingStrategy]
    ] = {
        SortingStrategyName.RGB: sorting_strategies.RGBSorting,
        SortingStrategyName.HSV: sorting_strategies.HSVSorting,
        SortingStrategyName.HSL: sorting_strategies.HSLSorting,
        SortingStrategyName.STEP: sorting_strategies.StepSorting,
        SortingStrategyName.ALTERNATED_STEP: sorting_strategies.AlternatedStepSorting,
        SortingStrategyName.LUMINOSITY: sorting_strategies.LuminositySorting,
        SortingStrategyName.HILLBERT: sorting_strategies.HillbertSorting,
    }

    def __init__(self, strategy_name: SortingStrategyName):
        self.strategy: sorting_strategies.SortingStrategy = self.STRATEGY_MAPPING[
            strategy_name
        ]()

    def sort(
        self, colors_to_sort: Set[Color], direction: Directions
    ) -> Tuple[Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        return {
            Directions.FORWARD: lambda: self.strategy.sort(colors_to_sort),
            Directions.BACKWARD: lambda: self._sort_backwards(colors_to_sort),
        }[direction]()

    def _sort_backwards(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        colors_sorted_backwards: List[Color] = []

        for color in reversed(self.strategy.sort(colors_to_sort)):
            colors_sorted_backwards.append(color)

        return tuple(colors_sorted_backwards)
