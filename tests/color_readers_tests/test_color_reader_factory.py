from typing import Tuple

from harmony.core.interfaces import ColorReader
from harmony.core.models import Color
from harmony.core.service_layer.color_readers import extract_colors_from_path
from tests.helpers import (
    ColorReadingArrangement,
    FakeFileReadingStrategy,
    get_directory_to_read,
    temporary_directory_context,
    temporary_file_context,
)


class TestColorReaderFactory:
    """Tests for the color reader factory"""

    def test_making_reader_for_directory(self) -> None:
        """Test making color reader for a directory path"""
        with temporary_directory_context() as directory:
            arrangement = get_directory_to_read(directory)
            result = self._when_reader_made(arrangement)
        self._then_should_get_directory_reader(result)

    def _then_should_get_directory_reader(self, result: Tuple[Color, ...]) -> None:
        assert len(result) > 1

    def test_making_reader_for_file(self) -> None:
        """Test making color reader for a file path"""
        with temporary_file_context() as file:
            arrangement = ColorReadingArrangement(file, FakeFileReadingStrategy())
            result = self._when_reader_made(arrangement)
            self._then_should_get_file_reader(result)

    def _then_should_get_file_reader(self, result: Tuple[Color, ...]) -> None:
        assert len(result) == 1

    def _when_reader_made(self, arrangement: ColorReadingArrangement) -> ColorReader:
        return extract_colors_from_path(arrangement.path, arrangement.strategy, False)
