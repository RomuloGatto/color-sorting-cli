from harmony import core
from harmony.color_sorting.service_layer.services import make_sorting_strategy
from harmony.color_sorting.service_layer.sorting_strategies import (
    AlternatedStepSorting,
    SortingStrategy,
)


class TestSortingStrategyFactory:
    """Tests for the sorting strategy factory"""

    def test_making_strategy(self) -> None:
        """Test making sorting strategy"""
        arrangement = self._given_strategy_name()
        result = self._when_requested_strategy(arrangement)
        self._then_should_make_strategy(result)

    def _given_strategy_name(self) -> core.SortingStrategyName:
        return core.SortingStrategyName.ALTERNATED_STEP

    def _when_requested_strategy(
        self, arrangement: core.SortingStrategyName
    ) -> SortingStrategy:
        return make_sorting_strategy(arrangement)

    def _then_should_make_strategy(self, result: SortingStrategy) -> None:
        assert isinstance(result, AlternatedStepSorting)
