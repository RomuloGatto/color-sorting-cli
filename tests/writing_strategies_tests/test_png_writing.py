import os
from typing import Tuple

from harmony import core
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
        self, arrangement: Tuple[core.Color, ...]
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

    def _given_colors(self) -> Tuple[core.Color, ...]:
        return (
            core.Color(
                rgb=core.RGB(235, 61, 52),
                hsl=core.HSL(2, 0.78, 0.56),
                hexcode="#eb3d34",
                original_format=core.ColorFormat.HEXCODE,
                description="red",
            ),
            core.Color(
                rgb=core.RGB(75, 214, 47),
                hsl=core.HSL(109, 0.78, 0.51),
                hexcode="#4bd62f",
                original_format=core.ColorFormat.RGB,
                description="green",
            ),
            core.Color(
                rgb=core.RGB(212, 104, 4),
                hsl=core.HSL(28, 0.98, 0.42),
                hexcode="#d46804",
                original_format=core.ColorFormat.HEXCODE,
                description="orange",
            ),
        )
