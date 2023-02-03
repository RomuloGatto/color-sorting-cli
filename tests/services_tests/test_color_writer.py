from typing import TextIO, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import WritingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.core.service_layer.services import ColorWriter
from tests.helpers import temporary_file_context


class FakeWriting(WritingStrategy):
    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        with open(final_file_path, "w") as file:
            self._for_each_color_write_description(file, colors)

    def _for_each_color_write_description(
        self, file: TextIO, colors: Tuple[Color, ...]
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

    def _when_written(self, arrangement: Tuple[Color, ...]) -> str:
        with temporary_file_context() as file_path:
            ColorWriter(FakeWriting()).write(arrangement, str(file_path))

            return file_path.read_text()

    def _then_should_write_to_passed_path(self, result: str) -> None:
        assert self._get_expected_content() == result

    @staticmethod
    def _get_expected_content() -> str:
        return "red\ngreen\norange"

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
                hexcode=RGB(212, 104, 4),
                original_format=ColorFormat.HEXCODE,
                description="orange",
            ),
        )
