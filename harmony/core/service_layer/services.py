from typing import IO, TextIO, Tuple

from harmony.color_sorting.constants import SortingStrategyName
from harmony.core.interfaces import FileReadingStrategy, WritingStrategy
from harmony.core.models import Color
from harmony.core.utils import (
    does_file_name_have_extension,
    extract_extension_from_file_path,
    get_extension_from_file_path,
)


def get_sorted_file_path(
    source_file: TextIO,
    sorting_strategy: SortingStrategyName,
    suffix: str,
) -> str:
    """Return the path to the file with the processed data

    Args:
        source_file (TextIO): original file

    Returns:
        str: path to the processed data file
    """
    if does_file_name_have_extension(source_file.name):
        return (
            f"{extract_extension_from_file_path(source_file.name)}"
            + f"_{sorting_strategy}{suffix}"
            + f"{get_extension_from_file_path(source_file.name)}"
        )

    return f"{source_file.name}_{sorting_strategy}"


class ColorReader:
    """Service for reading colors from file"""

    def __init__(self, strategy: FileReadingStrategy) -> None:
        self._strategy = strategy

    def extract_from_file(self, colors_file: IO) -> Tuple[Color, ...]:
        """Extracts a list of colors from a file

        Args:
            file_path (str): path to the file with the colors

        Returns:
            List[Color]: list of colors extracted
        """
        return self._strategy.read(colors_file)


class ColorWriter:
    """Service for writing colors to file"""

    def __init__(self, strategy: WritingStrategy):
        self._strategy = strategy

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to passed file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """

        self._strategy.write(colors, final_file_path)
