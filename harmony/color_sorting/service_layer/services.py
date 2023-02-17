from typing import Dict, List, Set, Tuple, Type

from harmony import core
from harmony.color_sorting.constants import Directions
from harmony.color_sorting.service_layer import sorting_strategies

STRATEGY_MAPPING: Dict[
    core.SortingStrategyName, Type[sorting_strategies.SortingStrategy]
] = {
    core.SortingStrategyName.RGB: sorting_strategies.RGBSorting,
    core.SortingStrategyName.HSV: sorting_strategies.HSVSorting,
    core.SortingStrategyName.HSL: sorting_strategies.HSLSorting,
    core.SortingStrategyName.STEP: sorting_strategies.StepSorting,
    core.SortingStrategyName.ALTERNATED_STEP: sorting_strategies.AlternatedStepSorting,
    core.SortingStrategyName.LUMINOSITY: sorting_strategies.LuminositySorting,
    core.SortingStrategyName.HILLBERT: sorting_strategies.HillbertSorting,
}


class ColorSorter:
    """Service for sorting colors"""

    def __init__(self, strategy: sorting_strategies.SortingStrategy):
        self.strategy = strategy

    def sort(
        self, colors_to_sort: Set[core.Color], direction: Directions
    ) -> Tuple[core.Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color, ...]: sorted set of colors
        """
        return {
            Directions.FORWARD: lambda: self.strategy.sort(colors_to_sort),
            Directions.BACKWARD: lambda: self._sort_backwards(colors_to_sort),
        }[direction]()

    def _sort_backwards(
        self, colors_to_sort: Set[core.Color]
    ) -> Tuple[core.Color, ...]:
        colors_sorted_backwards: List[core.Color] = []

        for color in reversed(self.strategy.sort(colors_to_sort)):
            colors_sorted_backwards.append(color)

        return tuple(colors_sorted_backwards)


def make_sorting_strategy(
    strategy_name: core.SortingStrategyName,
) -> sorting_strategies.SortingStrategy:
    """Given a strategy name, make the correspondent sorting strategy

    Args:
        strategy_name (SortingStrategyName): name of the strategy to be made

    Returns:
        sorting_strategies.SortingStrategy: correspondent sorting strategy
    """
    return STRATEGY_MAPPING[strategy_name]()
