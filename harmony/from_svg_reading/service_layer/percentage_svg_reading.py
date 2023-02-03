from typing import Dict

from harmony.core.abc import AutoLabelPatternReadingStrategy
from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB
from harmony.core.service_layer import RGBToHSLConverter
from harmony.core.utils import HexcodeUtils, RegexHelper


def _percentage_to_rgb_value(percentage: int) -> int:
    return round((percentage / 100) * 255)


class PercentageRGBReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `RGB()` with the components as
    percentage"""

    STRING_PATTERN = (
        r"^(rgb|RGB)\([\s]*(?P<red>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<blue>[0-9]{1,3})[%][\s]*\)$"
    )
    ORIGINAL_FORMAT = ColorFormat.RGB

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGB(
            self._get_red_from_rgb_as_percentage(property_value),
            self._get_green_from_rgb_as_percentage(property_value),
            self._get_blue_from_rgb_as_percentage(property_value),
        )

    def _get_red_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["red"]
        )

    def _get_green_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["green"]
        )

    def _get_blue_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["blue"]
        )

    def _get_raw_string_data_cleaned(self, raw_string: str) -> Dict[str, int]:
        return {
            key: int(component)
            for key, component in RegexHelper(self.__class__.STRING_PATTERN)
            .get_raw_string_data(raw_string)
            .items()
        }


class PercentageRGBAReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `RGBA()` with the components as
    percentage"""

    STRING_PATTERN = (
        r"^(rgba|RGBA)\([\s]*(?P<red>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<blue>[0-9]{1,3})[%][\s]*,[\s]*([01]?[.][0-9]+)[\s]*\)$"
    )
    ORIGINAL_FORMAT = ColorFormat.RGB

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGB(
            self._get_red_from_rgba_as_percentage(property_value),
            self._get_green_from_rgba_as_percentage(property_value),
            self._get_blue_from_rgba_as_percentage(property_value),
        )

    def _get_red_from_rgba_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["red"]
        )

    def _get_green_from_rgba_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["green"]
        )

    def _get_blue_from_rgba_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["blue"]
        )

    def _get_raw_string_data_cleaned(self, raw_string: str) -> Dict[str, int]:
        return {
            key: int(component)
            for key, component in RegexHelper(self.__class__.STRING_PATTERN)
            .get_raw_string_data(raw_string)
            .keys()
        }
