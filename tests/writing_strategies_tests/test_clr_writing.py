import os
from typing import Callable, Tuple

import pytest

from harmony.core.constants import ColorFormat
from harmony.core.exceptions import InvalidFileException
from harmony.core.models import RGB, Color
from harmony.to_clr_convertion.services import CLRWriting
from tests.helpers import get_temporary_file_path


class TestCLRWriting:
    """Tests for the CLR writing strategy"""

    def test_write_as_clr_file(self) -> None:
        """Test writting ".clr" file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_clr(arrangement)
        self._then_should_write_to_clr_file(result)

    def _then_should_write_to_clr_file(self, result: bytes) -> None:
        expected_color_bytes1 = b"\x83\xec\xebk?\x83\xf5\xf4t>\x83\xd1\xd0P>\x01\x86"
        expected_color_bytes2 = b"\x83\x97\x96\x96>\x83\xd7\xd6V?\x83\xbd\xbc<>\x01\x86"

        assert expected_color_bytes1 in result
        assert expected_color_bytes2 in result

    def test_writing_zero_colors(self) -> None:
        """Test writing a CLR file with zero colors"""
        arrangement = self._given_zero_colors()

        def result() -> None:
            self._when_colors_are_passed_writing_as_clr(arrangement)

        self._then_should_raise_invalid_file(result)

    def _given_zero_colors(self) -> Tuple[Color, ...]:
        return ()

    def _then_should_raise_invalid_file(self, result: Callable[[], None]) -> None:
        with pytest.raises(InvalidFileException):
            result()

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

    def _when_colors_are_passed_writing_as_clr(
        self, arrangement: Tuple[Color, ...]
    ) -> bytes:
        temporary_file = get_temporary_file_path(suffix=".clr")
        strategy = CLRWriting()

        strategy.write(arrangement, temporary_file)

        colors_file_content: bytes

        with open(temporary_file, "rb") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content
