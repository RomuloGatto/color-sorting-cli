import os
from pathlib import Path
from typing import Tuple

from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB, Color
from harmony.to_ase_convertion.services import ASEWriting
from tests.helpers import TestResourceUtils, get_temporary_file_path


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
        strategy = ASEWriting("test")

        strategy.write(arrangement, temporary_file)

        colors_file_content: bytes

        with open(temporary_file, "rb") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_ase_file(self, result: bytes) -> None:
        assert (
            result == Path(TestResourceUtils.get_resource("correct.ase")).read_bytes()
        )

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
