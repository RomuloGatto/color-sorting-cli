import logging

from harmony.core.calculation_models import HueData, SaturationData
from harmony.core.math_utils import (
    are_almost_equal,
    difference_between,
    quotient_between,
)


class HueCalculator:
    """Provide method calculating the hue"""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def calculate(self, data: HueData) -> float:
        """Calculate the hue for a color from the data passed

        Args:
            data (HueData): data to calculate hue

        Returns:
            float: hue value
        """
        if are_almost_equal(data.difference_between_biggest_and_smallest, 0):
            self._logger.info(  # pylint: disable=logging-not-lazy
                "Hue is zero because the difference between the biggest and the "
                + "smallest is zero"
            )
            return 0

        return self._calculate_hue(data) * 60

    def _calculate_hue(self, data: HueData) -> float:
        return (
            lambda: self._calculate_case1(data),
            lambda: self._calculate_case2(data),
            lambda: self._calculate_case3(data),
        )[self._get_index_of_the_biggest_value(data)]()

    def _get_index_of_the_biggest_value(self, data: HueData) -> int:
        return [
            are_almost_equal(difference, 0)
            for difference in data.differences_from_biggest_value
        ].index(True)

    def _calculate_case1(self, data: HueData) -> float:
        self._logger.info("Calculating case 1, cause red value is the biggest")

        return (
            quotient_between(
                difference_between(data.green_as_percentage, data.blue_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            % 6
        )

    def _calculate_case2(self, data: HueData) -> float:
        self._logger.info("Calculating case 2, cause green value is the biggest")

        return (
            quotient_between(
                difference_between(data.blue_as_percentage, data.red_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            + 2
        )

    def _calculate_case3(self, data: HueData) -> float:
        self._logger.info("Calculating case 3, cause blue value is the biggest")

        return (
            quotient_between(
                difference_between(data.red_as_percentage, data.green_as_percentage),
                data.difference_between_biggest_and_smallest,
            )
            + 4
        )


class SaturationCalculator:
    """Provide method for calculating the color saturation"""

    def calculate(self, data: SaturationData) -> float:
        """Calculate the saturation value for a color

        Args:
            data (SaturationData): data to calculate saturation

        Returns:
            float: saturation value
        """
        if not are_almost_equal(data.biggest_value, 0):
            return data.difference_between_biggest_and_smallest / data.biggest_value

        return 0.0
