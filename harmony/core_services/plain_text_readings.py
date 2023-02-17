import re

from harmony import color_factories, core
from harmony.core import interfaces
from harmony.core_services.css_readers import HSLCSSFunctionReader, RGBCSSFunctionReader


class HexcodeTextReading(interfaces.StringReadingStrategy):
    """Convert a raw string the with a hexcode string into a Color object"""

    STRING_PATTERN = r"(?P<hexcode>#([A-Za-z0-9]{3}){1,2})([\s](?P<description>.*))?"

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_hexcode(
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                property_value
            )["hexcode"],
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                property_value
            )["description"]
            or "",
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None


class RGBTextReading(interfaces.StringReadingStrategy):
    """Convert a raw string the with RGB components into a Color object"""

    STRING_PATTERN = (
        r"(rgb|RGB)\([\s]*(?P<red>[0-9]{1,3})[\s]*,[\s]*(?P<green>[0-9]{1,3})[\s]*"
        + r",[\s]*(?P<blue>[0-9]{1,3})[\s]*\)([\s](?P<description>.*))?"
    )

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_rgb(
            RGBCSSFunctionReader().read(property_value),
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                property_value
            )["description"]
            or "",
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None


class HSLTextReading(interfaces.StringReadingStrategy):
    """Read css HSL() function and convert to HSL object"""

    STRING_PATTERN = (
        r"(hsl|HSL)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[\s]*%[\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[\s]*%[\s]*\)([\s](?P<description>.*))?"
    )

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_hsl(
            HSLCSSFunctionReader().read(property_value),
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                property_value
            )["description"]
            or "",
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None
