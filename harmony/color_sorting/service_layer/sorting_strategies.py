from abc import ABC, abstractmethod
from typing import Set, Tuple

from harmony.color_sorting.service_layer.calculators import HillbertIndexCalculator
from harmony.color_sorting.service_layer.converters import (
    RGBtoHSVConverter,
    RGBToLuminosityConverter,
    RGBToSteppedHueValueAndSteppedLuminosity,
)
from harmony.core import constants
from harmony.core.math_utils import quotient_between
from harmony.core.models import RGB, Color
from harmony.core.service_layer.converters import RGBToHSLConverter
from harmony.typing import Number


class SortingStrategy(ABC):
    """Interface for sorting strategies"""

    @abstractmethod
    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """


class RGBSorting(SortingStrategy):
    """Sorting strategy based on RGB values"""

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their RGB

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(key=lambda color: self._get_rgb_values(color.rgb))
        return tuple(colors_list)

    def _get_rgb_values(self, rgb: RGB) -> Tuple[int, int, int]:
        return (rgb.red, rgb.green, rgb.blue)


class HSVSorting(SortingStrategy):
    """Sorting strategy based on HSV"""

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSV

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        RGBtoHSVConverter()

        colors_list = list(colors_to_sort)
        colors_list.sort(key=lambda color: self._get_hsv_values(color.rgb))
        return tuple(colors_list)

    def _get_hsv_values(self, rgb: RGB):
        return RGBtoHSVConverter().convert(rgb)


class HSLSorting(SortingStrategy):
    """Sorting strategy based on HSL"""

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(key=lambda color: self._get_hsl_values(color.rgb))
        return tuple(colors_list)

    def _get_hsl_values(self, rgb: RGB) -> Tuple[Number, ...]:
        return RGBToHSLConverter().convert(rgb)[:3]


class LuminositySorting(SortingStrategy):
    """Sorting strategy based on perceived luminosity"""

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their perceived luminosity

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(key=lambda color: self._get_luminosity(color.rgb))
        return tuple(colors_list)

    def _get_luminosity(self, rgb: RGB) -> float:
        return RGBToLuminosityConverter().convert(rgb)[0]


class StepSorting(SortingStrategy):
    """Step sorting strategy"""

    STEPS = 8

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(
            key=lambda color: self._get_stepped_hsv_and_luminosity_values(color.rgb)
        )
        return tuple(colors_list)

    def _get_stepped_hsv_and_luminosity_values(self, rgb: RGB) -> Tuple[Number, ...]:
        hue, _, value = RGBtoHSVConverter().convert(rgb)

        return (
            round(quotient_between(hue, constants.MAXIMUM_HUE_VALUE) * self.STEPS),
            *RGBToLuminosityConverter().convert(rgb),
            round(value * self.STEPS),
        )


class AlternatedStepSorting(SortingStrategy):
    """Alternated step sorting strategy"""

    STEPS = 8

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors based on their HSL and luminosity but splitting them by
        steps

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(
            key=lambda color: self._get_stepped_alternatively_hsv_and_luminosity_values(
                color.rgb
            )
        )
        return tuple(colors_list)

    def _get_stepped_alternatively_hsv_and_luminosity_values(
        self, rgb: RGB
    ) -> Tuple[Number, ...]:
        return RGBToSteppedHueValueAndSteppedLuminosity(self.STEPS).convert(rgb)


class HillbertSorting(SortingStrategy):
    """Hillbert Curve sorting strategy"""

    def sort(self, colors_to_sort: Set[Color]) -> Tuple[Color, ...]:
        """Sort a list of colors using the Hillbert Curve algorithm

        Args:
            colors_to_sort (List[Color]): the colors to be sorted

        Returns:
            Tuple[Color]: sorted set of colors
        """
        colors_list = list(colors_to_sort)
        colors_list.sort(key=lambda color: self._get_hillbert_index(color.rgb))
        return tuple(colors_list)

    def _get_hillbert_index(self, rgb: RGB):
        return HillbertIndexCalculator().calculate(rgb)
