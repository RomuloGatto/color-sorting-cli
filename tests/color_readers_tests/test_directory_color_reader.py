from pathlib import Path
from typing import Callable, Tuple

import pytest

from harmony.core.exceptions import NoColorsFoundException
from harmony.core.models import Color
from harmony.core.service_layer.color_readers import DirectoryColorReader
from tests.color_readers_tests.test_color_reader_factory import ColorReadingArrangement
from tests.helpers import (
    FakeFileReadingStrategy,
    get_directory_to_read,
    temporary_directory_context,
)


class TestDirectoryColorReader:
    """Tests for the color reader for directories"""

    def test_reading_colors_from_directory(self) -> None:
        """Test reading colors from directory"""
        with temporary_directory_context() as directory:
            arrangement = get_directory_to_read(directory)
            result = self._when_directory_readed(arrangement)

        self._then_should_get_colors(result)

    def _then_should_get_colors(self, result: Tuple[Color, ...]) -> None:
        assert len(result) == 2

        for color in result:
            assert color in FakeFileReadingStrategy.colors_queue

    def test_reading_colors_from_invalid_directory(self) -> None:
        """Test reading colors from directory without a color file"""
        with temporary_directory_context() as directory:
            arrangement = self._given_directory_without_colors(directory)

            def result() -> None:
                self._when_directory_readed(arrangement)

            self._then_should_raise_no_color_found(result)

    def _given_directory_without_colors(
        self, directory: Path
    ) -> ColorReadingArrangement:
        return ColorReadingArrangement(directory, FakeFileReadingStrategy())

    def _then_should_raise_no_color_found(self, result: Callable[[], None]) -> None:
        with pytest.raises(NoColorsFoundException):
            result()

    def test_reading_directory_recursively(self) -> None:
        """Test reading the colors from all files in directory recursively"""
        with temporary_directory_context() as directory:
            arrangement = get_directory_to_read(directory)
            result = self._when_directory_readed(arrangement, True)
        self._then_should_read_recursively(result)

    def _then_should_read_recursively(self, result: Tuple[Color, ...]) -> None:
        assert len(result) == 3

        for color in result:
            assert color in FakeFileReadingStrategy.colors_queue

    def _when_directory_readed(
        self, arrangement: ColorReadingArrangement, should_be_recursively: bool = False
    ) -> Tuple[Color, ...]:
        return DirectoryColorReader(
            arrangement.strategy, should_be_recursively
        ).extract_colors(arrangement.path)
