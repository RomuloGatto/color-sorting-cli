from typing import TextIO, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import WritingStrategy
from harmony.core.models import RGB, Color
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
        rgb1 = RGB(235, 61, 52)
        hexcode1 = "#eb3d34"
        color1 = Color(
            rgb=rgb1,
            hexcode=hexcode1,
            original_format=ColorFormat.HEXCODE,
            description="red",
        )

        rgb2 = RGB(75, 214, 47)
        hexcode2 = "#4bd62f"
        color2 = Color(
            rgb=rgb2,
            hexcode=hexcode2,
            original_format=ColorFormat.RGB,
            description="green",
        )

        rgb3 = RGB(212, 104, 4)
        hexcode3 = "#d46804"
        color3 = Color(
            rgb=rgb3,
            hexcode=hexcode3,
            original_format=ColorFormat.HEXCODE,
            description="orange",
        )

        return (color1, color2, color3)
