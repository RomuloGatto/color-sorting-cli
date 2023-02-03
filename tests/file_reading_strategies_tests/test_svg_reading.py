from pathlib import Path
from typing import List, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB, Color
from harmony.from_svg_reading.service_layer.svg_file_reading import SVGFileReading
from tests.helpers import TestResourceUtils


class TestSVGReading:
    """Tests for SVG files reading strategy"""

    def test_reading_svg(self) -> None:
        """Test reading a valid SVG file"""
        arrangement = self._given_valid_svg_file()
        result = self._when_readed(arrangement)
        self._then_should_extract_its_colors(result)

    def _given_valid_svg_file(self) -> Path:
        return Path(TestResourceUtils.get_resource("svg-to-read.svg"))

    def _when_readed(self, arrangement: Path) -> Tuple[Color, ...]:
        print(SVGFileReading().read(arrangement))
        return SVGFileReading().read(arrangement)

    def _then_should_extract_its_colors(self, result: Tuple[Color, ...]) -> None:
        for color in self._get_expected_colors():
            assert color in result

    @staticmethod
    def _get_expected_colors() -> List[Color]:
        return [
            Color(
                rgb=RGB(red=255, green=255, blue=255),
                hsl=HSL(hue=0, saturation=0.0, luminosity=1.0),
                hexcode="#FFFFFF",
                original_format=ColorFormat.HEXCODE,
                description="White",
            ),
            Color(
                rgb=RGB(red=128, green=181, blue=219),
                hsl=HSL(hue=205, saturation=0.56, luminosity=0.68),
                hexcode="#80b5db",
                original_format=ColorFormat.HSL,
                description="Maya Blue",
            ),
            Color(
                rgb=RGB(red=230, green=36, blue=36),
                hsl=HSL(
                    hue=0, saturation=0.8434782608695651, luminosity=0.5215686274509804
                ),
                hexcode="#e62424",
                original_format=ColorFormat.RGB,
                description="Fire Brick",
            ),
            Color(
                rgb=RGB(red=255, green=115, blue=129),
                hsl=HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=ColorFormat.HEXCODE,
                description="Froly",
            ),
            Color(
                rgb=RGB(red=255, green=115, blue=129),
                hsl=HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=ColorFormat.RGB,
                description="Froly",
            ),
            Color(
                rgb=RGB(red=255, green=115, blue=129),
                hsl=HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=ColorFormat.HEXCODE,
                description="Froly",
            ),
        ]
