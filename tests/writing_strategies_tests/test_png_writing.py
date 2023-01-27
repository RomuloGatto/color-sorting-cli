import os
from typing import Tuple

from harmony.core.constants import ColorFormat
from harmony.core.models import RGB, Color
from harmony.to_image_convertion.services import PNGWritting
from tests.helpers import get_temporary_file_path


class TestPNGWriting:
    """Test PNG writing strategy"""

    def test_write_as_png_file(self) -> None:
        """Test writting ".png" file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writting_as_png(arrangement)
        self._then_should_write_to_png_file(result)

    def _when_colors_are_passed_writting_as_png(
        self, arrangement: Tuple[Color, ...]
    ) -> bytes:
        temporary_file = get_temporary_file_path(suffix=".png")
        strategy = PNGWritting()

        strategy.write(arrangement, temporary_file)

        colors_file_content: bytes

        with open(temporary_file, "rb") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_png_file(self, result: bytes) -> None:
        assert len(result) > 0
        assert result.find(b"\x89PNG\r\n\x1a\n") == 0

    def _given_colors(self) -> Tuple[Color, ...]:
        rgb1 = RGB(235, 61, 52)
        hexcode1 = "#eb3d34"
        color1 = Color(
            rgb=rgb1,
            hexcode=hexcode1,
            original_format=ColorFormat.HEXCODE,
            description="red",
        )

        rgb2 = RGB(75, 214, 47)
        hexcode2 = "#4bd62f"
        color2 = Color(
            rgb=rgb2,
            hexcode=hexcode2,
            original_format=ColorFormat.RGB,
            description="green",
        )

        rgb3 = RGB(212, 104, 4)
        hexcode3 = "#d46804"
        color3 = Color(
            rgb=rgb3,
            hexcode=hexcode3,
            original_format=ColorFormat.HEXCODE,
            description="orange",
        )

        return (color1, color2, color3)
