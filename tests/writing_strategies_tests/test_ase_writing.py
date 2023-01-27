import os
from typing import Tuple

from harmony.core.constants import ColorFormat
from harmony.core.models import RGB, Color
from harmony.to_ase_convertion.services import ASEWriting
from tests.helpers import get_temporary_file_path


class TestASEWriting:
    """Test ASE writing strategy"""

    def test_write_as_ase_file(self) -> None:
        """Test writting ".ase" file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writting_as_ase(arrangement)
        self._then_should_write_to_ase_file(result)

    def _when_colors_are_passed_writting_as_ase(
        self, arrangement: Tuple[Color, ...]
    ) -> bytes:
        temporary_file = get_temporary_file_path(suffix=".ase")
        strategy = ASEWriting("")

        strategy.write(arrangement, temporary_file)

        colors_file_content: bytes

        with open(temporary_file, "rb") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_ase_file(self, result: bytes) -> None:
        expected_color_bytes1 = b"RGB ?k\xeb\xec>t\xf4\xf5>P\xd0\xd1\x00\x02"
        expected_color_bytes2 = b"RGB >\x96\x96\x97?V\xd6\xd7><\xbc\xbd\x00\x02"

        assert expected_color_bytes1 in result
        assert expected_color_bytes2 in result

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
