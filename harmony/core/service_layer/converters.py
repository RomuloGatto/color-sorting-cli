import logging
from typing import Any, Callable, Dict

from harmony.core.calculation_models import HueData, SaturationData
from harmony.core.core_utils import deprecate
from harmony.core.exceptions import InvalidColorFormatException
from harmony.core.interfaces import ColorFormatConverter
from harmony.core.math_utils import (
    absolute_difference_between,
    difference_between,
    division_between,
    multiplication_between,
)
from harmony.core.models import HSL, RGB
from harmony.core.service_layer.calculators import HueCalculator, SaturationCalculator


class RGBToHSLConverter(ColorFormatConverter[RGB, HSL]):
    """Converter to convert RGB to HSL"""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.make_hsl_from_rgb = deprecate(self.convert)

    def convert(self, original_format: RGB) -> HSL:
        self._logger.info(
            self._get_converted_log_message(),
            self._get_converted_log_data(original_format),
        )

        return HSL(
            self._get_hue_from_rgb_as_integer(original_format),
            SaturationCalculator().calculate(SaturationData.from_rgb(original_format)),
            self.calculate_luminosity(original_format),
        )

    def _get_hue_from_rgb_as_integer(self, rgb: RGB) -> int:
        return int(self._get_hue_from_rgb(rgb))

    @staticmethod
    def _get_hue_from_rgb(rgb: RGB) -> float:
        return HueCalculator().calculate(HueData.from_rgb(rgb))

    @staticmethod
    def _get_saturation_from_rgb(rgb: RGB) -> float:
        return SaturationCalculator().calculate(SaturationData.from_rgb(rgb))

    @staticmethod
    def _get_converted_log_message() -> str:
        return (
            "RGB(%(red)d, %(green)d, %(blue)d) converted to "
            + "HSL(%(hue)d, %(saturation).2f, %(luminosity).2f)"
        )

    def _get_converted_log_data(self, rgb: RGB) -> Dict[str, Any]:
        return {
            "red": rgb.red,
            "green": rgb.green,
            "blue": rgb.blue,
            "hue": HueCalculator().calculate(HueData.from_rgb(rgb)),
            "saturation": SaturationCalculator().calculate(
                SaturationData.from_rgb(rgb)
            ),
            "luminosity": self.calculate_luminosity(rgb),
        }

    def calculate_luminosity(self, rgb: RGB) -> float:
        """Calculate the component "luminosity" from HSL

        Args:
            rgb (RGB): RGB of the color to calculate luminosity

        Returns:
            float: luminosity value
        """
        return self._sum_of_biggest_and_the_smallest(rgb) / 2

    def _sum_of_biggest_and_the_smallest(self, rgb: RGB) -> float:
        return self._get_biggest_value(rgb) + self._get_smallest_value(rgb)

    def _get_biggest_value(self, rgb: RGB) -> float:
        return max(
            rgb.red_as_percentage,
            rgb.green_as_percentage,
            rgb.blue_as_percentage,
        )

    def _get_smallest_value(self, rgb: RGB) -> float:
        return min(
            rgb.red_as_percentage,
            rgb.green_as_percentage,
            rgb.blue_as_percentage,
        )


class HSLToRGBConverter(ColorFormatConverter[HSL, RGB]):
    """Converts HSL objects into RGB objects"""

    def convert(self, original_format: HSL) -> RGB:
        for is_condition_true, convert in self._get_rgb_factory_mapping().items():
            if is_condition_true(original_format.hue):
                return convert(original_format)

        raise InvalidColorFormatException(
            f"Hue must be between 0 and 360, got {original_format.hue}"
        )

    def _get_rgb_factory_mapping(
        self,
    ) -> Dict[Callable[[int], bool], Callable[[HSL], RGB]]:
        return {
            lambda hue: 0 <= hue < 60: self._calculate_ba0,
            lambda hue: 60 <= hue < 120: self._calculate_ab0,
            lambda hue: 120 <= hue < 180: self._calculate_0ba,
            lambda hue: 180 <= hue < 240: self._calculate_0ab,
            lambda hue: 240 <= hue < 300: self._calculate_a0b,
            lambda hue: 300 <= hue < 360: self._calculate_b0a,
        }

    def _calculate_ba0(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
        )

    def _calculate_ab0(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
        )

    def _calculate_0ba(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
        )

    def _calculate_0ab(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
        )

    def _calculate_a0b(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
        )

    def _calculate_b0a(self, hsl_values: HSL) -> RGB:
        return RGB(
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
        )

    def _get_rounded_a_as_component(self, hsl_values: HSL) -> int:
        return round(self._get_variable_a_as_component(hsl_values))

    def _get_variable_a_as_component(self, hsl_values: HSL) -> float:
        return multiplication_between(self._get_a_plus_c(hsl_values), 255)

    def _get_a_plus_c(self, hsl_values: HSL) -> float:
        return self._get_variable_a(hsl_values) + self._get_variable_c(hsl_values)

    def _get_rounded_b_as_component(self, hsl_values: HSL) -> int:
        return round(self._get_variable_b_as_component(hsl_values))

    def _get_variable_b_as_component(self, hsl_values: HSL) -> float:
        return self._get_b_plus_c(hsl_values) * 255

    def _get_b_plus_c(self, hsl_values: HSL) -> float:
        return self._get_variable_b(hsl_values) + self._get_variable_c(hsl_values)

    def _get_rounded_0_as_component(self, hsl_values: HSL) -> int:
        return round(self._get_0_as_component(hsl_values))

    def _get_0_as_component(self, hsl_values: HSL) -> float:
        return self._get_0_plus_c(hsl_values) * 255

    def _get_0_plus_c(self, hsl_values: HSL) -> float:
        return 0 + self._get_variable_c(hsl_values)

    def _get_variable_c(self, hsl_values: HSL) -> float:
        return hsl_values.luminosity - self._get_half_b(hsl_values)

    def _get_half_b(self, hsl_values: HSL) -> float:
        return division_between(self._get_variable_b(hsl_values), 2)

    def _get_variable_a(self, hsl_values: HSL) -> float:
        return multiplication_between(
            self._get_variable_b(hsl_values),
            self._get_1_minus_hue_mod_diff(hsl_values.hue),
        )

    def _get_1_minus_hue_mod_diff(self, hue: int) -> float:
        return 1 - self._get_hue_mod_diff(hue)

    def _get_hue_mod_diff(self, hue: int) -> float:
        return absolute_difference_between(self._get_hue_mod(hue), 1)

    @staticmethod
    def _get_hue_mod(hue: int) -> float:
        return division_between(hue, 60) % 2

    def _get_variable_b(self, hsl_values: HSL) -> float:
        return multiplication_between(
            self._get_1_minus_double_luminosity_diff(hsl_values.luminosity),
            hsl_values.saturation,
        )

    def _get_1_minus_double_luminosity_diff(self, luminosity: float) -> float:
        return difference_between(
            1,
            self._get_double_luminosity_diff(luminosity),
        )

    @staticmethod
    def _get_double_luminosity_diff(
        luminosity: float,
    ) -> float:
        return absolute_difference_between(multiplication_between(luminosity, 2), 1)
