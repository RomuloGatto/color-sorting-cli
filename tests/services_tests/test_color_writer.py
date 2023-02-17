from typing import TextIO, Tuple

from harmony import core, core_services
from harmony.core import interfaces
from tests.helpers import temporary_file_context


class FakeWriting(interfaces.WritingStrategy):
    def write(self, colors: Tuple[core.Color, ...], final_file_path: str):
        with open(final_file_path, "w") as file:
            self._for_each_color_write_description(file, colors)

    def _for_each_color_write_description(
        self, file: TextIO, colors: Tuple[core.Color, ...]
    ):
        for index, color in enumerate(colors):
            file.write(color.description)

            if index < len(colors) - 1:
                file.write("\n")


class TestColorsWriter:
    """Tests for the colors writer"""

    def test_writing_colors_to_file(self) -> None:
        """Test writing the valid passed colors to file"""
        arrangement = self._given_colors()
        result = self._when_written(arrangement)
        self._then_should_write_to_passed_path(result)

    def _when_written(self, arrangement: Tuple[core.Color, ...]) -> str:
        with temporary_file_context() as file_path:
            core_services.ColorWriter(FakeWriting()).write(arrangement, str(file_path))

            return file_path.read_text()

    def _then_should_write_to_passed_path(self, result: str) -> None:
        assert self._get_expected_content() == result

    @staticmethod
    def _get_expected_content() -> str:
        return "red\ngreen\norange"

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
                original_format=core.ColorFormat.HEXCODE,
                description="orange",
            ),
        )
