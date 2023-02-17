import pathlib
from typing import Callable, Tuple

import pytest

from harmony import core, core_services
from harmony.core import exceptions
from tests.helpers import (
    ColorReadingArrangement,
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

    def _then_should_get_colors(self, result: Tuple[core.Color, ...]) -> None:
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
        self, directory: pathlib.Path
    ) -> ColorReadingArrangement:
        return ColorReadingArrangement(directory, FakeFileReadingStrategy())

    def _then_should_raise_no_color_found(self, result: Callable[[], None]) -> None:
        with pytest.raises(exceptions.NoColorsFoundException):
            result()

    def test_reading_directory_recursively(self) -> None:
        """Test reading the colors from all files in directory recursively"""
        with temporary_directory_context() as directory:
            arrangement = get_directory_to_read(directory)
            result = self._when_directory_readed(arrangement, True)
        self._then_should_read_recursively(result)

    def _then_should_read_recursively(self, result: Tuple[core.Color, ...]) -> None:
        assert len(result) == 3

        for color in result:
            assert color in FakeFileReadingStrategy.colors_queue

    def _when_directory_readed(
        self, arrangement: ColorReadingArrangement, should_be_recursively: bool = False
    ) -> Tuple[core.Color, ...]:
        return core_services.DirectoryColorReader(
            arrangement.strategy, should_be_recursively
        ).extract_colors(arrangement.path)
