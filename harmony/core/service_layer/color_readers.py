import logging
import os
from pathlib import Path
from typing import List, Sized, Tuple

from harmony.core.exceptions import NoColorsFoundException
from harmony.core.interfaces import ColorReader, FileReadingStrategy
from harmony.core.models import Color


class FileColorReader(ColorReader):
    """Service for reading colors from file"""

    def __init__(self, strategy: FileReadingStrategy) -> None:
        self._strategy = strategy

    def extract_colors(self, path: Path) -> Tuple[Color, ...]:
        """Extracts a list of colors from a file

        Args:
            colors_file (IO): file with the colors

        Returns:
            Tuple[Color, ...]: tuple of colors extracted
        """
        return self._strategy.read(path)


class DirectoryColorReader(ColorReader):
    """Service for reading colors from files in a directory"""

    def __init__(self, strategy: FileReadingStrategy) -> None:
        self._strategy = strategy
        self._logger = logging.getLogger(self.__class__.__name__)

    def extract_colors(self, path: Path) -> Tuple[Color, ...]:
        """Extracts a list of colors from the files of the passed directory

        Args:
            directory (Path): path to the directory to extract the colors

        Returns:
            Tuple[Color, ...]: tuple of colors extracted
        """
        colors: List[Color] = []

        for entry in os.scandir(path):
            if entry.is_file():
                colors.extend(self._try_to_read_from_path_string(entry.path))

        self._check_if_colors_were_found(colors)

        return tuple(colors)

    def _try_to_read_from_path_string(self, path: str) -> Tuple[Color, ...]:
        try:
            return self._strategy.read(Path(path))

        except Exception as exception:
            log_message = (
                "An error occurred while extracting the colors from '%(path)s': "
                + "%(exception)s"
            )

            self._logger.debug(
                log_message,
                {"path": path, "exception": exception},
            )

            return ()

    def _check_if_colors_were_found(self, colors_found: Sized) -> None:
        if self._no_color_was_found(colors_found):
            raise NoColorsFoundException(
                "Harmony could not extract any color from the path"
            )

    @staticmethod
    def _no_color_was_found(colors_found: Sized) -> bool:
        return len(colors_found) < 1


def extract_colors_from_path(
    path: Path, strategy: FileReadingStrategy
) -> Tuple[Color, ...]:
    """Extract the colors from the given path using the given file reading strategy

    Args:
        path (Path): path where the file(s) to extract the colors are going to be found
        strategy (FileReadingStrategy): strategy to use on extracting the colors

    Returns:
        Tuple[Color, ...]: the colors extracted
    """

    if path.is_file():
        return FileColorReader(strategy).extract_colors(path)

    return DirectoryColorReader(strategy).extract_colors(path)
