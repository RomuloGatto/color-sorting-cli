from math import sqrt

from harmony.core import constants
from harmony.core.calculation_models import HueData, SaturationData
from harmony.core.interfaces import ColorFormatConverter
from harmony.core.math_utils import division_between
from harmony.core.models import (
    HSV,
    RGB,
    PerceivedLuminosity,
    SteppedHueValuePerceivedLuminosity,
)
from harmony.core.service_layer.calculators import HueCalculator, SaturationCalculator


class RGBtoHSVConverter(ColorFormatConverter[RGB, HSV]):
    """Converter to convert RGB to HSV"""

    def convert(self, original_format: RGB) -> HSV:
        """Converts a RGB object into a tuple with its corresponding HSV values

        Args:
            rgb (RGB): RGB to be converted

        Returns:
            Tuple[float, float, float]: the HSV values
        """
        return HSV(
            self._calculate_rounded_hue_from_rgb(original_format),
            self._calculate_saturation_from_rgb(original_format),
            self.calculate_value_from_rgb(original_format),
        )

    def _calculate_rounded_hue_from_rgb(self, rgb: RGB) -> int:
        return round(self._calculate_hue_from_rgb(rgb))

    @staticmethod
    def _calculate_hue_from_rgb(rgb: RGB) -> float:
        return HueCalculator().calculate(HueData.from_rgb(rgb))

    def _calculate_saturation_from_rgb(self, rgb: RGB) -> float:
        return self._calculate_saturation_from_hue_data(HueData.from_rgb(rgb))

    @staticmethod
    def _calculate_saturation_from_hue_data(hue_data: HueData) -> float:
        return SaturationCalculator().calculate(SaturationData.from_hue_data(hue_data))

    @staticmethod
    def calculate_value_from_rgb(rgb: RGB) -> float:
        """Calculate "value" component from HSV related to the RGB passed

        Args:
            rgb (RGB): RGB to be converted

        Returns:
            float: "value" value
        """
        return HueData.from_rgb(rgb).biggest_value


class RGBToLuminosityConverter(ColorFormatConverter[RGB, PerceivedLuminosity]):
    """Converter to convert RGB to perceived luminosity"""

    def convert(self, original_format: RGB) -> PerceivedLuminosity:
        return PerceivedLuminosity(
            self._square_root_from_the_sum_of_factors(original_format)
        )

    def _square_root_from_the_sum_of_factors(self, rgb: RGB) -> float:
        return sqrt(self._get_sum_of_factors(rgb))

    def _get_sum_of_factors(self, rgb: RGB) -> float:
        return (
            self._get_red_factor(rgb.red)
            + self._get_green_factor(rgb.green)
            + self._get_blue_factor(rgb.blue)
        )

    @staticmethod
    def _get_red_factor(red: float) -> float:
        return 0.241 * red

    @staticmethod
    def _get_green_factor(green: float) -> float:
        return 0.691 * green

    @staticmethod
    def _get_blue_factor(blue: float) -> float:
        return 0.068 * blue


class RGBToSteppedHueValueAndSteppedLuminosity(
    ColorFormatConverter[RGB, SteppedHueValuePerceivedLuminosity]
):
    """Converter to convert RGB to the stepped hue, "value" and stepped luminosity
    values"""

    def __init__(self, steps: int) -> None:
        self._steps = steps

    def convert(self, original_format: RGB) -> SteppedHueValuePerceivedLuminosity:
        luminosity = RGBToLuminosityConverter().convert(original_format).value
        stepped_value = self._get_stepped_value(original_format)

        if self._is_stepped_hue_odd(original_format):
            stepped_value = self._steps - stepped_value
            luminosity = self._steps - luminosity

        return SteppedHueValuePerceivedLuminosity(
            self._get_stepped_hue(original_format), luminosity, stepped_value
        )

    def _is_stepped_hue_odd(self, rgb: RGB) -> bool:
        return self._get_stepped_hue(rgb) % 2 == 1

    def _get_stepped_hue(self, rgb: RGB) -> int:
        return round(self._get_hue_as_decimal_times_steps(self._get_hue(rgb)))

    def _get_hue(self, rgb: RGB) -> float:
        return HueCalculator().calculate(HueData.from_rgb(rgb))

    def _get_hue_as_decimal_times_steps(self, hue) -> float:
        return division_between(hue, constants.MAXIMUM_HUE_VALUE) * self._steps

    def _get_stepped_value(self, rgb: RGB) -> int:
        return round(self._get_value_times_steps(rgb))

    def _get_value_times_steps(self, rgb: RGB) -> float:
        return RGBtoHSVConverter().calculate_value_from_rgb(rgb) * self._steps
