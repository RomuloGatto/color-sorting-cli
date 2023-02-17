import logging
from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path
from typing import Generic, Tuple, TypeVar

from harmony.core.models import Color, ColorFormatModel


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


T = TypeVar("T", bound=ColorFormatModel)
K = TypeVar("K", bound=ColorFormatModel)


class ColorFormatConverter(Generic[T, K], metaclass=ABCMeta):
    """Interface for color format converters

    Generics:
        T: original format to be converted
        K: final format
    """

    @abstractmethod
    def convert(self, original_format: T) -> K:
        """Converts RGB to other color format"""


del T, K


class FileReadingStrategy(ABC):
    """Interface for a object that extract a set of colors from a file"""

    @abstractmethod
    def read(self, file_path: Path) -> Tuple[Color, ...]:
        """Extract a set of colors from a given file"""


class StringReadingStrategy(ABC):
    """Interface for strategies that extract a color from a given string"""

    def read(self, property_value: str) -> Color:
        """Convert the raw value passed into a Color object

        Args:
            property_value (str): value of the color property in a given element from a
            SVG file

        Returns:
            Color: Color result
        """
        self._get_logger().info("Reading '%s'", property_value)
        return self.do_read(property_value)

    @abstractmethod
    def do_read(self, property_value: str) -> Color:
        """Override this method with the logic to extract a color from the passed
        string"""

    @classmethod
    def match_pattern(cls, property_value: str) -> bool:
        """Return True if the passed string can be processed by this strategy"""
        if cls.do_match_pattern(property_value):
            cls._get_logger().info("Value '%s' does match the pattern", property_value)
            return True

        cls._get_logger().info("Value '%s' does not match the pattern", property_value)
        return False

    @classmethod
    @abstractmethod
    def do_match_pattern(cls, property_value: str) -> bool:
        """Override this method return whether the class implemented can read the
        passed string"""
        raise NotImplementedError

    @classmethod
    def _get_logger(cls) -> logging.Logger:
        return logging.getLogger(cls.__name__)
