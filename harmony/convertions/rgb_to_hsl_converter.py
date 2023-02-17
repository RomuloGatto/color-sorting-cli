import logging
from typing import Any, Dict

from harmony import core
from harmony.convertions.calculators import HueCalculator, SaturationCalculator
from harmony.core import interfaces


class RGBToHSLConverter(interfaces.ColorFormatConverter[core.RGB, core.HSL]):
    """Converter to convert RGB to HSL"""

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self.make_hsl_from_rgb = core.deprecate(self.convert)

    def convert(self, original_format: core.RGB) -> core.HSL:
        self._logger.info(
            self._get_converted_log_message(),
            self._get_converted_log_data(original_format),
        )

        return core.HSL(
            self._get_hue_from_rgb_as_integer(original_format),
            SaturationCalculator().calculate(
                core.SaturationData.from_rgb(original_format)
            ),
            self.calculate_luminosity(original_format),
        )

    def _get_hue_from_rgb_as_integer(self, rgb: core.RGB) -> int:
        return int(self._get_hue_from_rgb(rgb))

    @staticmethod
    def _get_hue_from_rgb(rgb: core.RGB) -> float:
        return HueCalculator().calculate(core.HueData.from_rgb(rgb))

    @staticmethod
    def _get_saturation_from_rgb(rgb: core.RGB) -> float:
        return SaturationCalculator().calculate(core.SaturationData.from_rgb(rgb))

    @staticmethod
    def _get_converted_log_message() -> str:
        return (
            "RGB(%(red)d, %(green)d, %(blue)d) converted to "
            + "HSL(%(hue)d, %(saturation).2f, %(luminosity).2f)"
        )

    def _get_converted_log_data(self, rgb: core.RGB) -> Dict[str, Any]:
        return {
            "red": rgb.red,
            "green": rgb.green,
            "blue": rgb.blue,
            "hue": HueCalculator().calculate(core.HueData.from_rgb(rgb)),
            "saturation": SaturationCalculator().calculate(
                core.SaturationData.from_rgb(rgb)
            ),
            "luminosity": self.calculate_luminosity(rgb),
        }

    def calculate_luminosity(self, rgb: core.RGB) -> float:
        """Calculate the component "luminosity" from HSL

        Args:
            rgb (RGB): RGB of the color to calculate luminosity

        Returns:
            float: luminosity value
        """
        return self._sum_of_biggest_and_the_smallest(rgb) / 2

    def _sum_of_biggest_and_the_smallest(self, rgb: core.RGB) -> float:
        return self._get_biggest_value(rgb) + self._get_smallest_value(rgb)

    def _get_biggest_value(self, rgb: core.RGB) -> float:
        return max(
            rgb.red_as_percentage,
            rgb.green_as_percentage,
            rgb.blue_as_percentage,
        )

    def _get_smallest_value(self, rgb: core.RGB) -> float:
        return min(
            rgb.red_as_percentage,
            rgb.green_as_percentage,
            rgb.blue_as_percentage,
        )
