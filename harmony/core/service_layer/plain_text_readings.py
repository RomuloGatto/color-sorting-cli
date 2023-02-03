from harmony.core.abc import ExtractLabelPatternReadingStrategy
from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB
from harmony.core.service_layer import (
    HSLCSSFunctionReader,
    HSLToRGBConverter,
    RGBCSSFunctionReader,
    RGBToHSLConverter,
)
from harmony.core.utils import HexcodeUtils, RegexHelper, RGBUtils


class HexcodeTextReading(ExtractLabelPatternReadingStrategy):
    """Convert a raw string the with a hexcode string into a Color object"""

    STRING_PATTERN = r"(?P<hexcode>#([A-Za-z0-9]{3}){1,2})([\s](?P<description>.*))?"
    ORIGINAL_FORMAT = ColorFormat.HEXCODE

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGBUtils.get_rgb_from_hexcode(self.execute_get_hexcode(property_value))

    def execute_get_hexcode(self, property_value: str) -> str:
        return RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
            property_value
        )["hexcode"]


class RGBTextReading(ExtractLabelPatternReadingStrategy):
    """Convert a raw string the with RGB components into a Color object"""

    STRING_PATTERN = (
        r"(rgb|RGB)\([\s]*(?P<red>[0-9]{1,3})[\s]*,[\s]*(?P<green>[0-9]{1,3})[\s]*"
        + r",[\s]*(?P<blue>[0-9]{1,3})[\s]*\)([\s](?P<description>.*))?"
    )
    ORIGINAL_FORMAT = ColorFormat.RGB

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGBCSSFunctionReader().read(property_value)


class HSLTextReading(ExtractLabelPatternReadingStrategy):
    """Read css HSL() function and convert to HSL object"""

    STRING_PATTERN = (
        r"(hsl|HSL)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[\s]*%[\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[\s]*%[\s]*\)([\s](?P<description>.*))?"
    )
    ORIGINAL_FORMAT = ColorFormat.HSL

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return HSLToRGBConverter().convert(self.execute_get_hsl(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return HSLCSSFunctionReader().read(property_value)
