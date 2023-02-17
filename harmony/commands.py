import pathlib
from typing import Tuple

import rich

from harmony import core, core_services
from harmony.core import interfaces


class FromTxtCommandUtils:
    """Helping methods for entrypoints that convert a Harmony files to other formats"""

    def __init__(
        self,
        writing_strategy: interfaces.WritingStrategy,
        suffix: str,
        must_generate_color_names: bool = False,
    ) -> None:
        self.__writing_strategy = writing_strategy
        self.__must_generate_color_names = must_generate_color_names
        self.__suffix = suffix

    def convert_from_txt_file(
        self,
        file_path: pathlib.Path,
    ) -> None:
        """Convert the text file using the passed writing strategy

        Args:
            file_path (Path): file to be converted
            writing_strategy (WritingStrategy): strategy to use when writing the new
            file
        """
        core_services.ColorWriter(self.__writing_strategy).write(
            self._get_colors_tuple_for_convertion(file_path),
            core_services.PathGenerator(self.__suffix).get_path_with_extension(
                file_path, self.__writing_strategy.EXTENSION
            ),
        )

        rich.print(
            "[green]File converted and saved to "
            + core_services.PathGenerator(self.__suffix).get_path_with_extension(
                file_path, self.__writing_strategy.EXTENSION
            )
        )

    def _get_colors_tuple_for_convertion(
        self, colors_file: pathlib.Path
    ) -> Tuple[core.Color, ...]:
        return tuple(
            core_services.FileColorReader(
                core_services.PlainTextFileReading(self.__must_generate_color_names)
            ).extract_colors(colors_file)
        )


class ToTxtCommandUtils:
    """Helping methods for entrypoints that convert some file to a Harmony file"""

    def __init__(
        self,
        reading_strategy: interfaces.FileReadingStrategy,
        color_format: core.ColorFormat,
        recursively: bool,
    ) -> None:
        self.__reading_strategy = reading_strategy
        self.__color_format = color_format
        self.__recursively = recursively

    def convert_to_txt_file(self, path: pathlib.Path) -> None:
        """Convert some file to a Harmony file"""
        colors: Tuple[core.Color, ...] = core_services.extract_colors_from_path(
            path, self.__reading_strategy, self.__recursively
        )
        final_file_path = core_services.PathGenerator("").get_path_with_extension(
            path, core_services.PlainTextWriting.EXTENSION
        )
        core_services.ColorWriter(
            core_services.PlainTextWriting(self.__color_format)
        ).write(colors, final_file_path)
        rich.print(f"[green]Colors extracted and saved to {final_file_path}")
