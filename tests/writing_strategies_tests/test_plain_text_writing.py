import os
from typing import Tuple

from harmony import core
from harmony.core_services.writing_strategies import PlainTextWriting
from tests.helpers import get_temporary_file_path


class TestPlainTextWriting:
    """Tests for the plain text writing strategy"""

    def test_write_colors_as_rgb(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_rgb(arrangement)
        self._then_should_write_to_new_file_as_rgb(result)

    def _when_colors_are_passed_writing_as_rgb(
        self, arrangement: Tuple[core.Color, ...]
    ) -> str:
        temporary_file = get_temporary_file_path()
        strategy = PlainTextWriting(core.ColorFormat.RGB)

        strategy.write(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_rgb(self, result: str) -> None:
        expected_color_string = "(75, 214, 47)"
        unexpected_color_string = "#4bd62f"

        assert expected_color_string in result
        assert unexpected_color_string not in result

    def test_write_colors_as_hexcode(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_hexcode(arrangement)
        self._then_should_write_to_new_file_as_hexcode(result)

    def _when_colors_are_passed_writing_as_hexcode(
        self, arrangement: Tuple[core.Color, ...]
    ) -> str:
        temporary_file = get_temporary_file_path()
        strategy = PlainTextWriting(core.ColorFormat.HEXCODE)

        strategy.write(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_hexcode(self, result: str) -> None:
        expected_color_string = "#4bd62f"
        unexpected_color_string = "(75, 214, 47)"

        assert expected_color_string in result
        assert unexpected_color_string not in result

    def test_writing_as_hsl(self) -> None:
        """Test writing colors as HSL"""
        arrangement = self._given_colors()
        result = self._when_passed_writing_as_hsl(arrangement)
        self._then_should_write_as_hsl(result)

    def _when_passed_writing_as_hsl(self, arrangement: Tuple[core.Color, ...]) -> str:
        temporary_file = get_temporary_file_path()
        strategy = PlainTextWriting(core.ColorFormat.HSL)

        strategy.write(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_as_hsl(self, result: str) -> None:
        expected_color_string = "HSL(2, 78%, 56%)"
        unexpected_color_string1 = "RGB(235, 61, 52)"
        unexpected_color_string2 = "#eb3d34"

        assert expected_color_string in result
        assert unexpected_color_string1 not in result
        assert unexpected_color_string2 not in result

    def test_write_colors_as_same_as_input(self) -> None:
        """Test writing colors to file"""
        arrangement = self._given_colors()
        result = self._when_colors_are_passed_writing_as_same_as_input(arrangement)
        self._then_should_write_to_new_file_as_same_as_input(result)

    def _when_colors_are_passed_writing_as_same_as_input(
        self, arrangement: Tuple[core.Color, ...]
    ) -> str:
        temporary_file = get_temporary_file_path()
        strategy = PlainTextWriting(core.ColorFormat.SAME_AS_INPUT)

        strategy.write(arrangement, temporary_file)

        colors_file_content: str

        with open(temporary_file, "r", encoding="utf8") as colors_file:
            colors_file_content = colors_file.read()

        os.remove(temporary_file)

        return colors_file_content

    def _then_should_write_to_new_file_as_same_as_input(self, result: str) -> None:
        expected_color_string1 = "#eb3d34 red\n"
        unexpected_color_string1 = "RGB(235, 61, 52) red\n"

        expected_color_string2 = "RGB(75, 214, 47) green\n"
        unexpected_color_string2 = "HSL(109, 78%, 51%) green\n"

        expected_color_string3 = "HSL(28, 98%, 42%) orange\n"
        unexpected_color_string3 = "#d46804 orange\n"

        assert expected_color_string1 in result
        assert unexpected_color_string1 not in result

        assert expected_color_string2 in result
        assert unexpected_color_string2 not in result

        assert expected_color_string3 in result
        assert unexpected_color_string3 not in result

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
                original_format=core.ColorFormat.HSL,
                description="orange",
            ),
        )
