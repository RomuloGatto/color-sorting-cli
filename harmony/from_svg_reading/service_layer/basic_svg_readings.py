from itertools import dropwhile

from harmony.core.abc import AutoLabelPatternReadingStrategy
from harmony.core.constants import ColorFormat
from harmony.core.exceptions import InvalidColorFormatException
from harmony.core.interfaces import StringReadingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.core.service_layer import RGBCSSFunctionReader, RGBToHSLConverter
from harmony.core.utils import HexcodeUtils, RGBUtils
from harmony.from_svg_reading.constants import CSSBasicColorNames


class HexcodeSVGReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with a RGB value as hexcode"""

    STRING_PATTERN = r"#[A-Za-z0-9]{3}([A-Za-z0-9]{3})?"
    ORIGINAL_FORMAT = ColorFormat.HEXCODE

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGBUtils.get_rgb_from_hexcode(property_value)

    def execute_get_hexcode(self, property_value: str) -> str:
        return property_value

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))


class CSSColorNameReading(StringReadingStrategy):
    """Make a color given a string with a CSS basic color name"""

    def read(self, property_value: str) -> Color:
        for color_data in dropwhile(
            lambda color_data: color_data.name.lower() != property_value.lower(),
            CSSBasicColorNames,
        ):
            return HexcodeSVGReading().read(color_data.value)

        raise InvalidColorFormatException(f"'{property_value}' is not a basic color")

    @classmethod
    def match_pattern(cls, property_value: str) -> bool:
        for name in filter(
            lambda name: name.lower() == property_value.lower(),
            CSSBasicColorNames.__members__.keys(),
        ):
            return bool(name)

        return False


class RGBSVGReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `RGB()` with components as
    integers"""

    STRING_PATTERN = (
        r"(RGB|rgb)[\s]*\([\s]*(?P<red>{0-9}{1,3})[\s]*,"
        + r"[\s]*(?P<green>{0-9}{1,3})[\s]*,[\s]*(?P<blue>{0-9}{1,3})[\s]*\)"
    )
    ORIGINAL_FORMAT = ColorFormat.RGB

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().make_hsl_from_rgb(
            self.execute_get_rgb(property_value)
        )

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGBCSSFunctionReader().read(property_value)


class RGBAReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `RGBA()` with components as
    integers"""

    STRING_PATTERN = (
        r"^(rgba|RGBA)[\s]*\([\s]*(?P<red>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<blue>[0-9]{1,3})[\s]*,[\s]*([01]?[.][0-9]+)[\s]*\)$"
    )
    ORIGINAL_FORMAT = ColorFormat.RGB

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return RGBToHSLConverter().convert(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return RGBCSSFunctionReader().read(property_value)
