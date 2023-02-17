from typing import Tuple

from harmony import core
from harmony.core import exceptions, interfaces


class PlainTextWriting(interfaces.WritingStrategy):
    """Writting strategy that results in a simple text file"""

    EXTENSION = "txt"

    def __init__(self, color_format):
        self._color_string_getter_dict = {
            core.ColorFormat.HEXCODE: self._get_hexcode_string,
            core.ColorFormat.RGB: self._get_rgb_string,
            core.ColorFormat.HSL: self._get_hsl_string,
            core.ColorFormat.SAME_AS_INPUT: self._get_color_as_input_format,
        }

        self._get_color_string = self._color_string_getter_dict[color_format]

    def write(self, colors: Tuple[core.Color, ...], final_file_path: str):
        """Write colors to a text file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """
        with open(final_file_path, "w", encoding="utf8") as final_file:
            final_file.write(self._get_file_content(colors))

    def _get_file_content(self, colors: Tuple[core.Color, ...]) -> str:
        file_content: str = ""

        for color in colors:
            file_content += self._get_color_string(color)

        return file_content

    def _get_color_as_input_format(self, color: core.Color) -> str:
        if self._color_original_format_is_invalid(color):
            raise exceptions.InvalidColorException(
                f"Original color format can not be {color.original_format}"
            )

        return self._color_string_getter_dict[color.original_format](color)

    @staticmethod
    def _color_original_format_is_invalid(color) -> bool:
        return color.original_format == core.ColorFormat.SAME_AS_INPUT

    @staticmethod
    def _is_input_format_as_hexcode(color: core.Color) -> bool:
        return color.original_format == core.ColorFormat.HEXCODE

    def _get_hexcode_string(self, color: core.Color) -> str:
        return f"{color.hexcode} {color.description}\n"

    def _get_rgb_string(self, color: core.Color) -> str:
        return (
            f"RGB({color.rgb_red}, {color.rgb_green}, {color.rgb_blue}) "
            + f"{color.description}\n"
        )

    def _get_hsl_string(self, color: core.Color) -> str:
        return (
            f"HSL({color.hsl_hue}, "
            + f"{self._get_percentage_as_integer(color.hsl_saturation)}%, "
            + f"{self._get_percentage_as_integer(color.hsl_luminosity)}%) "
            + f"{color.description}\n"
        )

    def _get_percentage_as_integer(self, value: float) -> int:
        return int(value * 100)
