import re
from itertools import dropwhile

from harmony import color_factories, core, core_services
from harmony.core import exceptions, interfaces
from harmony.from_svg_reading.constants import CSSBasicColorNames


class HexcodeSVGReading(interfaces.StringReadingStrategy):
    """Make a color given a string with a RGB value as hexcode"""

    STRING_PATTERN = r"#[A-Za-z0-9]{3}([A-Za-z0-9]{3})?"

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_hexcode_with_auto_label(
            property_value
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None


class CSSColorNameReading(interfaces.StringReadingStrategy):
    """Make a color given a string with a CSS basic color name"""

    def do_read(self, property_value: str) -> core.Color:
        for color_data in dropwhile(
            lambda color_data: color_data.name.lower() != property_value.lower(),
            CSSBasicColorNames,
        ):
            return HexcodeSVGReading().do_read(color_data.value)

        raise exceptions.InvalidColorFormatException(
            f"'{property_value}' is not a basic color"
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        for name in filter(
            lambda name: name.lower() == property_value.lower(),
            CSSBasicColorNames.__members__.keys(),
        ):
            return bool(name)

        return False


class RGBSVGReading(interfaces.StringReadingStrategy):
    """Make a color given a string with the CSS function `RGB()` with components as
    integers"""

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_rgb_with_auto_label(
            core_services.RGBCSSFunctionReader().read(property_value)
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return (
            re.match(core_services.RGBCSSFunctionReader.STRING_PATTERN, property_value)
            is not None
        )
