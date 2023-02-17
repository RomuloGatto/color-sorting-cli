import re

from harmony import color_factories, core
from harmony.core import interfaces
from harmony.core_services.css_readers import PercentageRGBCSSFunctionReader


class PercentageRGBReading(interfaces.StringReadingStrategy):
    """Make a color given a string with the CSS function `RGB()` with the components as
    percentage"""

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_rgb_with_auto_label(
            PercentageRGBCSSFunctionReader().read(property_value),
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return (
            re.match(PercentageRGBCSSFunctionReader.STRING_PATTERN, property_value)
            is not None
        )
