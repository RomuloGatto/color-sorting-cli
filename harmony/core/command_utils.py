from typing import TextIO, Tuple

import rich
import typer

from harmony.core.interfaces import WritingStrategy
from harmony.core.models import Color
from harmony.core.service_layer.file_readings import PlainTextFileReading
from harmony.core.service_layer.services import ColorReader, ColorWriter
from harmony.core.utils import get_path_with_extension


class CommandUtils:
    """Helping methods for the entrypoints"""

    def __init__(
        self, writing_strategy: WritingStrategy, must_generate_color_names: bool = False
    ) -> None:
        self._writing_strategy = writing_strategy
        self._must_generate_color_names = must_generate_color_names

    def convert_txt_file(
        self,
        colors_file: typer.FileText,
    ) -> None:
        """Convert the text file using the passed writing strategy

        Args:
            colors_file (typer.FileText): file to be converted
            writing_strategy (WritingStrategy): strategy to use when writing the new
            file
        """
        ColorWriter(self._writing_strategy).write(
            self._get_colors_tuple_for_convertion(colors_file),
            get_path_with_extension(colors_file, self._writing_strategy.EXTENSION),
        )

        rich.print(
            "[green]File converted and saved to "
            + get_path_with_extension(colors_file, self._writing_strategy.EXTENSION)
        )

    def _get_colors_tuple_for_convertion(
        self, colors_file: TextIO
    ) -> Tuple[Color, ...]:
        return tuple(
            ColorReader(
                PlainTextFileReading(self._must_generate_color_names)
            ).extract_from_file(colors_file)
        )
