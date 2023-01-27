from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

from harmony.core.models import RGB, Color


class ColorReader(ABC):
    """Interface for objects capable of extracting colors from a passed path"""

    @abstractmethod
    def extract_colors(self, path: Path) -> Tuple[Color, ...]:
        """Extract colors given a path"""


class WritingStrategy(ABC):
    """Interface for output file writting strategies"""

    EXTENSION: str = ""

    @abstractmethod
    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write the sorted colors to a new file

        Args:
            colors (Tuple[Color, ...]): colors to written
            final_file_path (str): path to the new file
        """


class ColorFormatConverter(ABC):
    """Interface for color format converters"""

    @abstractmethod
    def convert(self, rgb: RGB) -> Tuple[float, ...]:
        """Converts RGB to other color format"""


class FileReadingStrategy(ABC):
    """Interface for a object that extract a set of colors from a file"""

    @abstractmethod
    def read(self, file_path: Path) -> Tuple[Color, ...]:
        """Extract a set of colors from a given file"""


class PlainTextReadingStrategy(ABC):
    """Interface for a object resposible for converting a string to a Color object"""

    @abstractmethod
    def read(self, raw_string) -> Color:
        """Convert a raw string containing the data of the color to a Color object"""
