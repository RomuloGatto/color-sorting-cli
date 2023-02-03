from harmony.core.abc import AutoLabelPatternReadingStrategy
from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB
from harmony.core.service_layer import HSLToRGBConverter
from harmony.core.service_layer.css_readers import HSLCSSFunctionReader
from harmony.core.utils import HexcodeUtils


class HSLSVGReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `HSL()`"""

    STRING_PATTERN = (
        r"^(hsl|HSL)[\s]*\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[%][\s]*\)$"
    )
    ORIGINAL_FORMAT = ColorFormat.HSL

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return HSLToRGBConverter().convert(self.execute_get_hsl(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return HSLCSSFunctionReader().read(property_value)


class HSLAReading(AutoLabelPatternReadingStrategy):
    """Make a color given a string with the CSS function `HSLA()`"""

    STRING_PATTERN = (
        r"^(hsl|HSL)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[%][\s]*,[\s]*(1|[0]?[.][0-9]+)[\s]*\)$"
    )
    ORIGINAL_FORMAT = ColorFormat.HSL

    def execute_get_hexcode(self, property_value: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self.execute_get_rgb(property_value))

    def execute_get_rgb(self, property_value: str) -> RGB:
        return HSLToRGBConverter().convert(self.execute_get_hsl(property_value))

    def execute_get_hsl(self, property_value: str) -> HSL:
        return HSLCSSFunctionReader().read(property_value)
