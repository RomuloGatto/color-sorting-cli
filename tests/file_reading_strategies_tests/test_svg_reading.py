from pathlib import Path
from typing import List, Tuple

from harmony import core
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

    def _when_readed(self, arrangement: Path) -> Tuple[core.Color, ...]:
        print(SVGFileReading().read(arrangement))
        return SVGFileReading().read(arrangement)

    def _then_should_extract_its_colors(self, result: Tuple[core.Color, ...]) -> None:
        for color in self._get_expected_colors():
            assert color in result

    @staticmethod
    def _get_expected_colors() -> List[core.Color]:
        return [
            core.Color(
                rgb=core.RGB(red=255, green=255, blue=255),
                hsl=core.HSL(hue=0, saturation=0.0, luminosity=1.0),
                hexcode="#FFFFFF",
                original_format=core.ColorFormat.HEXCODE,
                description="White",
            ),
            core.Color(
                rgb=core.RGB(red=128, green=181, blue=219),
                hsl=core.HSL(hue=205, saturation=0.56, luminosity=0.68),
                hexcode="#80b5db",
                original_format=core.ColorFormat.HSL,
                description="Maya Blue",
            ),
            core.Color(
                rgb=core.RGB(red=130, green=16, blue=16),
                hsl=core.HSL(
                    hue=0, saturation=0.8769230769230769, luminosity=0.28627450980392155
                ),
                hexcode="#821010",
                original_format=core.ColorFormat.RGB,
                description="Falu Red",
            ),
            core.Color(
                rgb=core.RGB(red=255, green=115, blue=129),
                hsl=core.HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=core.ColorFormat.HEXCODE,
                description="Froly",
            ),
            core.Color(
                rgb=core.RGB(red=255, green=115, blue=129),
                hsl=core.HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=core.ColorFormat.RGB,
                description="Froly",
            ),
            core.Color(
                rgb=core.RGB(red=255, green=115, blue=129),
                hsl=core.HSL(
                    hue=354,
                    saturation=0.5490196078431373,
                    luminosity=0.7254901960784313,
                ),
                hexcode="#ff7381",
                original_format=core.ColorFormat.HEXCODE,
                description="Froly",
            ),
        ]
