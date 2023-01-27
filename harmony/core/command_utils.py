from pathlib import Path
from typing import Tuple

import rich

from harmony.core.interfaces import WritingStrategy
from harmony.core.models import Color
from harmony.core.service_layer.color_readers import FileColorReader
from harmony.core.service_layer.file_readings import PlainTextFileReading
from harmony.core.service_layer.services import ColorWriter, PathGenerator


class CommandUtils:
    """Helping methods for the entrypoints"""

    def __init__(
        self, writing_strategy: WritingStrategy, must_generate_color_names: bool = False
    ) -> None:
        self._writing_strategy = writing_strategy
        self._must_generate_color_names = must_generate_color_names

    def convert_txt_file(
        self,
        file_path: Path,
    ) -> None:
        """Convert the text file using the passed writing strategy

        Args:
            file_path (Path): file to be converted
            writing_strategy (WritingStrategy): strategy to use when writing the new
            file
        """
        ColorWriter(self._writing_strategy).write(
            self._get_colors_tuple_for_convertion(file_path),
            PathGenerator("").get_path_with_extension(
                file_path, self._writing_strategy.EXTENSION
            ),
        )

        rich.print(
            "[green]File converted and saved to "
            + PathGenerator("").get_path_with_extension(
                file_path, self._writing_strategy.EXTENSION
            )
        )

    def _get_colors_tuple_for_convertion(self, colors_file: Path) -> Tuple[Color, ...]:
        return tuple(
            FileColorReader(
                PlainTextFileReading(self._must_generate_color_names)
            ).extract_colors(colors_file)
        )
