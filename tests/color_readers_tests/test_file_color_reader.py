import os
from pathlib import Path
from typing import List, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import FileReadingStrategy
from harmony.core.models import RGB, Color
from harmony.core.service_layer.color_readers import FileColorReader
from tests.helpers import get_temporary_file_path


class FakeFileReading(FileReadingStrategy):
    def read(self, file_path: Path) -> Tuple[Color, ...]:
        del file_path

        return (
            Color(
                rgb=RGB(red=22, green=92, blue=196),
                hexcode="#165cc4",
                original_format=ColorFormat.HEXCODE,
                description="Blue",
            ),
            Color(
                rgb=RGB(red=196, green=22, blue=190),
                hexcode="#c416be",
                original_format=ColorFormat.RGB,
                description="Magenta",
            ),
        )


class TestFileColorReader:
    """Tests for the reader of color files"""

    def test_extract_from_file(self) -> None:
        """Test extracting the colors from a valid file"""
        arrangements = self._given_file_path()

        try:
            result = self._when_file_is_passed(arrangements)
            self._then_should_extract_colors_from_text(list(result))

        finally:
            os.remove(arrangements)

    def _given_file_path(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("#165cc4 Blue\n" + "(196, 22, 190) Magenta")

        return temporary_file_path

    def _when_file_is_passed(self, file_path: str) -> Tuple[Color, ...]:
        extractor = FileColorReader(FakeFileReading())
        return extractor.extract_colors(Path(file_path))

    def _then_should_extract_colors_from_text(self, colors: List[Color]) -> None:
        expected_rgb = RGB(red=22, green=92, blue=196)
        expected_hexcode = "#c416be"
        first_expected_description = "Blue"
        second_expected_description = "Magenta"

        color_labels = [color.description for color in colors]
        color_hexcodes = [color.hexcode for color in colors]
        color_rgbs = [color.rgb for color in colors]

        assert expected_rgb in color_rgbs
        assert expected_hexcode in color_hexcodes
        assert first_expected_description in color_labels
        assert second_expected_description in color_labels
