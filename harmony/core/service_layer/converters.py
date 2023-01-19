import logging
from typing import Any, Dict, Tuple

from harmony.core.calculation_models import HueData, SaturationData
from harmony.core.interfaces import ColorFormatConverter
from harmony.core.models import HSL, RGB
from harmony.core.service_layer.calculators import HueCalculator, SaturationCalculator


class RGBToHSLConverter(ColorFormatConverter):
    """Converter to convert RGB to HSL"""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def convert(self, rgb: RGB) -> Tuple[float, ...]:
        self._logger.info(
            self._get_converted_log_message(),
            self._get_converted_log_data(rgb),
        )

        return (
            HueCalculator().calculate(HueData.from_rgb(rgb)),
            SaturationCalculator().calculate(SaturationData.from_rgb(rgb)),
            self.calculate_luminosity(rgb),
        )

    def make_hsl_from_rgb(self, rgb: RGB) -> HSL:
        """Make HSL object from a RGB object

        Args:
            rgb (RGB): RGB of the color to get the HSL data

        Returns:
            HSL: HSL related to the RGB
        """
        return HSL(
            self._get_hue_from_rgb_as_integer(rgb),
            self._get_saturation_from_rgb(rgb),
            RGBToHSLConverter().calculate_luminosity(rgb),
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
