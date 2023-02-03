import os
import shutil
import tempfile
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import FileReadingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.typing import Number
from tests import constants


def _get_temporary_file(**kwargs) -> Tuple[int, str]:
    return tempfile.mkstemp(**kwargs)  # type: ignore[return-value]


def get_temporary_file_path(**kwargs: object) -> str:
    """Generates a temporary file

    Returns:
        str: the path to the temporary file
    """
    return _get_temporary_file(**kwargs)[  # type: ignore[return-value]
        constants.MKSTEMP_ABSOLUTE_PATH_INDEX
    ]


@contextmanager
def temporary_file_context() -> Iterator[Path]:
    """Provide the path for a temporary file and remove it after used"""

    temporary_file = get_temporary_file_path()

    try:
        yield Path(temporary_file)

    finally:
        os.remove(temporary_file)


@contextmanager
def temporary_directory_context(**kwargs) -> Iterator[Path]:
    directory = tempfile.mkdtemp(**kwargs)

    try:
        yield Path(directory)

    finally:
        shutil.rmtree(directory)


def _difference_between(expected_number: Number, actual_number: Number) -> Number:
    return expected_number - actual_number


def _absolute_difference_between(
    expected_number: Number, actual_number: Number
) -> Number:
    return abs(_difference_between(expected_number, actual_number))


def assert_real_numbers_are_equal(
    expected_number: float, actual_number: float, tolerance=10 ^ (-7)
) -> None:
    """Raises AssertionError if numbers aren't equal

    Args:
        first_number (float): first number to be compared
        second_number (float): second number to be compared
    """
    assert (
        _absolute_difference_between(expected_number, actual_number) < tolerance
    ), f"Expected {expected_number}, got {actual_number}"


class TestResourceUtils:
    """Methods for managing resources"""

    @classmethod
    def get_resource(cls, path: str) -> str:
        """Return the absolute path to the resource passed

        Args:
            path (str): path to the resource relative to the resources directory

        Returns:
            str: absolute path to the resourse
        """
        return os.path.join(cls._get_resources_directory_path(), path)

    @classmethod
    def _get_resources_directory_path(cls) -> str:
        return os.path.join(cls._get_current_directory_path(), "resources")

    @classmethod
    def _get_current_directory_path(cls) -> str:
        return os.path.abspath(os.path.dirname(__file__))


class FakeFileReadingStrategy(FileReadingStrategy):
    colors_queue: List[Color] = [
        Color(
            rgb=RGB(212, 104, 4),
            hsl=HSL(28, 0.98, 0.42),
            hexcode="#d46804",
            original_format=ColorFormat.HEXCODE,
            description="Orange",
        ),
        Color(
            rgb=RGB(red=22, green=92, blue=196),
            hsl=HSL(215, 0.89, 0.43),
            hexcode="#165cc4",
            original_format=ColorFormat.HEXCODE,
            description="Blue",
        ),
        Color(
            rgb=RGB(red=196, green=22, blue=190),
            hsl=HSL(302, 0.89, 0.43),
            hexcode="#c416be",
            original_format=ColorFormat.RGB,
            description="Magenta",
        ),
    ]

    def __init__(self) -> None:
        self.colors_queue = deepcopy(self.__class__.colors_queue)

    def read(self, file_path: Path) -> Tuple[Color, ...]:
        del file_path
        return (self.colors_queue.pop(),)


@dataclass
class ColorReadingArrangement:
    path: Path
    strategy: FileReadingStrategy


def get_directory_to_read(directory: Path) -> ColorReadingArrangement:
    directory.joinpath("fake-file1.txt").write_text("#c416be Magenta")
    directory.joinpath("fake-file2.txt").write_text("#165cc4 Blue")
    directory.joinpath("fake-folder").mkdir()
    directory.joinpath("fake-folder").joinpath("fake-file3.txt").write_text(
        "#c416be red"
    )

    return ColorReadingArrangement(directory, strategy=FakeFileReadingStrategy())
