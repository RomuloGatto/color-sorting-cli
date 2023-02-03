import re
from pathlib import Path
from typing import Dict, List, Tuple, Type

from harmony.core.exceptions import InvalidColorException
from harmony.core.interfaces import FileReadingStrategy, PlainTextReadingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.core.service_layer.converters import RGBToHSLConverter
from harmony.core.service_layer.plain_text_readings import (
    HexcodeReading,
    HSLTextReading,
    RGBReading,
)
from harmony.core.utils import extract_unique_values_from_iterable
from harmony.data_access.store import ColorNamesStorage


class PlainTextFileReading(FileReadingStrategy):
    """Extract a set of colors from a plain text file"""

    def __init__(self, must_generate_color_names: bool = True):
        self._must_generate_color_names = must_generate_color_names

    def read(self, file_path: Path) -> Tuple[Color, ...]:
        with file_path.open("r") as file:
            return self._make_colors_tuple(file.readlines())

    def _make_colors_tuple(self, color_strings: List[str]) -> Tuple[Color, ...]:
        colors_list: List[Color] = []

        for color_string in color_strings:
            colors_list.append(self._make_color_from_raw_string(color_string))

        return tuple(extract_unique_values_from_iterable(colors_list))

    def _make_color_from_raw_string(self, raw_string: str) -> Color:
        return self._make_color_from_string(raw_string.replace("\n", ""))

    def _make_color_from_string(self, color_string: str) -> Color:
        for pattern, strategy in self._get_color_factory_mapping().items():
            if re.compile(pattern).match(color_string):
                return self._make_color(color_string, strategy())

        raise InvalidColorException(
            color_string.replace("\n", "") + " does not match any valid format"
        )

    def _get_color_factory_mapping(self) -> Dict[str, Type[PlainTextReadingStrategy]]:
        return {
            self._get_hexcode_pattern(): HexcodeReading,
            self._get_rgb_pattern(): RGBReading,
            self._get_hsl_pattern(): HSLTextReading,
        }

    @staticmethod
    def _get_hexcode_pattern() -> str:
        return "^[#][a-zA-Z0-9]{3}([a-zA-Z0-9]{3})?"

    @staticmethod
    def _get_rgb_pattern() -> str:
        return (
            r"(rgb|RGB)\([\s]*[0-9]{1,3}[\s]*,[\s]*[0-9]{1,3}[\s]*"
            + r",[\s]*[0-9]{1,3}[\s]*\)"
        )

    @staticmethod
    def _get_hsl_pattern() -> str:
        return (
            r"(hsl|HSL)\([\s]*[0-9]{1,3}[\s]*,[\s]*[0-9]{1,3}[\s]*%[\s]*,"
            + r"[\s]*[0-9]{1,3}[\s]*%[\s]*\)"
        )

    def _make_color(
        self,
        color_string: str,
        strategy: PlainTextReadingStrategy,
    ):
        new_color = strategy.read(color_string)

        if self._must_generate_name(new_color):
            new_color.description = self._generate_color_name(new_color.rgb)

        return new_color

    def _must_generate_name(self, color: Color) -> bool:
        return (
            self._must_generate_color_names
            and not self._does_color_already_have_name(color)
        )

    @staticmethod
    def _does_color_already_have_name(color: Color):
        return len(color.description) > 0

    def _generate_color_name(self, rgb_values: RGB) -> str:
        with ColorNamesStorage() as storage:
            return storage.get_color_name_by_hsl(self._get_hsl_from_rgb(rgb_values))

    def _get_hsl_from_rgb(self, rgb_values: RGB) -> HSL:
        return HSL.from_color_format_model(RGBToHSLConverter().convert(rgb_values))
