import re

from harmony import color_factories, core, core_services
from harmony.core import interfaces


class HSLSVGReading(interfaces.StringReadingStrategy):
    """Make a color given a string with the CSS function `HSL()`"""

    def do_read(self, property_value: str) -> core.Color:
        return color_factories.ColorFactory().make_from_hsl_with_auto_label(
            core_services.HSLCSSFunctionReader().read(property_value)
        )

    @classmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        return (
            re.match(core_services.HSLCSSFunctionReader.STRING_PATTERN, property_value)
            is not None
        )
