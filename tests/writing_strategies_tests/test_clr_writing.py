import os
from typing import Callable, Tuple

import pytest

from harmony.core.constants import ColorFormat
from harmony.core.exceptions import InvalidFileException
from harmony.core.models import HSL, RGB, Color
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
        return (
            Color(
                rgb=RGB(235, 61, 52),
                hsl=HSL(2, 0.78, 0.56),
                hexcode="#eb3d34",
                original_format=ColorFormat.HEXCODE,
                description="red",
            ),
            Color(
                rgb=RGB(75, 214, 47),
                hsl=HSL(109, 0.78, 0.51),
                hexcode="#4bd62f",
                original_format=ColorFormat.RGB,
                description="green",
            ),
            Color(
                rgb=RGB(212, 104, 4),
                hsl=HSL(28, 0.98, 0.42),
                hexcode="#d46804",
                original_format=ColorFormat.HEXCODE,
                description="orange",
            ),
        )

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
