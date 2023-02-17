from pathlib import Path
from typing import Iterator, List, Tuple, Type

from harmony import convertions, core, data_access
from harmony.core import exceptions, interfaces
from harmony.core_services.plain_text_readings import (
    HexcodeTextReading,
    HSLTextReading,
    RGBTextReading,
)


class PlainTextFileReading(interfaces.FileReadingStrategy):
    """Extract a set of colors from a plain text file"""

    def __init__(self, must_generate_color_names: bool = True):
        self._must_generate_color_names = must_generate_color_names

    def read(self, file_path: Path) -> Tuple[core.Color, ...]:
        with file_path.open("r") as file:
            return self._make_colors_tuple(file.readlines())

    def _make_colors_tuple(self, color_strings: List[str]) -> Tuple[core.Color, ...]:
        colors_list: List[core.Color] = []

        for color_string in color_strings:
            colors_list.append(self._make_color_from_raw_string(color_string))

        return tuple(core.extract_unique_values_from_iterable(colors_list))

    def _make_color_from_raw_string(self, raw_string: str) -> core.Color:
        return self._make_color_from_string(raw_string.replace("\n", ""))

    def _make_color_from_string(self, color_string: str) -> core.Color:
        for factory in filter(
            lambda factory: factory.match_pattern(color_string),
            self._get_color_factories(),
        ):
            return self._make_color(color_string, factory())

        raise exceptions.InvalidColorException(
            color_string.replace("\n", "") + " does not match any valid format"
        )

    def _get_color_factories(
        self,
    ) -> Iterator[Type[interfaces.StringReadingStrategy]]:
        yield HexcodeTextReading
        yield RGBTextReading
        yield HSLTextReading

    def _make_color(
        self,
        color_string: str,
        strategy: interfaces.StringReadingStrategy,
    ):
        new_color = strategy.read(color_string)

        if self._must_generate_name(new_color):
            new_color.description = self._generate_color_name(new_color.rgb)

        return new_color

    def _must_generate_name(self, color: core.Color) -> bool:
        return (
            self._must_generate_color_names
            and not self._does_color_already_have_name(color)
        )

    @staticmethod
    def _does_color_already_have_name(color: core.Color):
        return len(color.description) > 0

    def _generate_color_name(self, rgb_values: core.RGB) -> str:
        return data_access.ColorNamesStorage().get_color_name_by_hsl(
            self._get_hsl_from_rgb(rgb_values)
        )

    def _get_hsl_from_rgb(self, rgb_values: core.RGB) -> core.HSL:
        return core.HSL.from_color_format_model(
            convertions.RGBToHSLConverter().convert(rgb_values)
        )
