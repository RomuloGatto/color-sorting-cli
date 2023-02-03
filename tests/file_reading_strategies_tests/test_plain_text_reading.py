import os
from pathlib import Path
from typing import Callable, List, Tuple

import pytest

from harmony.core.exceptions import InvalidColorException
from harmony.core.models import RGB, Color
from harmony.core.service_layer.file_readings import PlainTextFileReading
from tests.helpers import get_temporary_file_path


class TestPlainTextFileReading:
    """Tests for the plain text file reading strategy"""

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
            colors_file.write("#165cc4 Blue\n" + "rgb(196, 22, 190) Magenta")

        return temporary_file_path

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

    def test_extracting_colors_from_invalid_format(self) -> None:
        arrangements = self._given_file_with_invalid_formats()

        try:

            def results() -> None:
                self._when_file_is_passed(arrangements)

            self._then_should_raise_invalid_color(results)

        finally:
            os.remove(arrangements)

    def _given_file_with_invalid_formats(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("adasdkajlsdka\n" + "djaisdljaksa")

        return temporary_file_path

    def _then_should_raise_invalid_color(self, result: Callable[[], None]):
        with pytest.raises(InvalidColorException):
            result()

    def test_extract_from_file_without_color_names(self) -> None:
        """Test generating names for the colors in a file"""
        arrangement = self._given_file_without_color_names()
        result = self._when_file_is_passed(arrangement)
        self._then_should_give_names_to_colors(result)

    def _given_file_without_color_names(self) -> str:
        temporary_file_path = get_temporary_file_path()

        with open(temporary_file_path, "w", encoding="utf8") as colors_file:
            colors_file.write("RGB(255, 0, 0)\n" + "#0500A5\n" + "rgb(219, 0, 76)")

        return temporary_file_path

    def _then_should_give_names_to_colors(self, result: Tuple[Color, ...]) -> None:
        expected_color_names = ["Red", "New Midnight Blue", "Razzmatazz"]
        actual_color_names = [color.description for color in result]

        for expected_name in expected_color_names:
            assert expected_name in actual_color_names

    def _when_file_is_passed(self, file_path: str) -> Tuple[Color, ...]:
        strategy = PlainTextFileReading(True)
        return strategy.read(Path(file_path))
