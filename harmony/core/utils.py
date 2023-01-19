import os
import struct
from typing import IO, Iterable, List

from harmony.core.constants import ByteOrder
from harmony.core.exceptions import NoExtensionFoundException
from harmony.core.models import RGB
from harmony.typing import T


def get_path_with_extension(source_file: IO, extension: str) -> str:
    """Return the path to file with the given extension

    Args:
        source_file (TextIO): original file

    Returns:
        str: path to the converted file
    """
    if does_file_name_have_extension(source_file.name):
        return f"{extract_extension_from_file_path(source_file.name)}.{extension}"

    return f"{source_file.name}.{extension}"


class ResourceUtils:
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
        return os.path.abspath(cls._get_root_directory_path())

    @staticmethod
    def _get_root_directory_path() -> str:
        return os.path.join(os.path.dirname(__file__), "..")


class RGBUtils:
    """Methods for manipulating RGB"""

    @classmethod
    def get_rgb_from_hexcode(cls, hexcode: str):
        """Make a RGB object from a hexcode string"""
        return RGB(
            cls._get_red_from_hexcode(hexcode),
            cls._get_green_from_hexcode(hexcode),
            cls._get_blue_from_hexcode(hexcode),
        )

    @classmethod
    def _get_red_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[:2], 16)

    @classmethod
    def _get_green_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[2:4], 16)

    @classmethod
    def _get_blue_from_hexcode(cls, hexcode: str) -> int:
        return int(cls._clean_hexcode(hexcode)[4:], 16)

    @staticmethod
    def _clean_hexcode(hexcode) -> str:
        return HexcodeUtils.convert_hexcode_from_3_to_6_chars_form(hexcode).replace(
            "#", ""
        )


class HexcodeUtils:
    """Methods for manipulating hexcode"""

    @classmethod
    def convert_hexcode_from_3_to_6_chars_form(cls, hexcode: str) -> str:
        """Convert a hexcode string in 3 chars format to 6 chars format"""
        if cls._does_hexcode_have_not_7_digits(hexcode):
            hexcode = f"{hexcode}{hexcode[1:]}"

        return hexcode

    @staticmethod
    def _does_hexcode_have_not_7_digits(string_to_count) -> bool:
        return len(string_to_count) != 7

    @staticmethod
    def get_hexcode_from_rgb(rgb: RGB) -> str:
        """Return a hexcode string from a RGB object"""
        return f"{int(rgb.red):02x}{int(rgb.green):02x}{int(rgb.blue):02x}"


class BytesUtils:
    """Methods for manipulating bytes"""

    @classmethod
    def float_to_bytes(cls, value: float, byte_order: ByteOrder) -> bytes:
        """Convert a float into bytes

        Args:
            value (float): float to be converted

        Returns:
            bytes: float as an IEEE 754 binary representation
        """
        return struct.pack(f"{cls._get_byte_order_char(byte_order)}f", value)

    @staticmethod
    def _get_byte_order_char(byte_order: ByteOrder) -> str:
        return {
            ByteOrder.LITTLE: "<",
            ByteOrder.BIG: ">",
        }[byte_order]


def get_index_for_the_file_extension(file_path: str) -> int:
    """Return the index of the `.`(dot) separating the file name from the extension. If
    no extension is found, returns -1

    Args:
        file_path (str): path-like string

    Returns:
        int: index to the `.` separating extension and file name or -1
    """
    return file_path.rfind(".")


def does_file_name_have_extension(file_path: str) -> bool:
    """Return `True` if passed path-like string have extension"""
    return get_index_for_the_file_extension(file_path) >= 0


def get_extension_from_file_path(file_path: str) -> str:
    """Get extension from path-like string

    Args:
        file_path (str): path-like string

    Raises:
        NoExtensionFoundException: when string has no extension

    Returns:
        str: extension got
    """
    if does_file_name_have_extension(file_path):
        return file_path[get_index_for_the_file_extension(file_path) :]

    raise NoExtensionFoundException(f"The file path '{file_path}' has no extension")


def extract_extension_from_file_path(file_path: str) -> str:
    """Remove extension from path-like string

    Args:
        file_path (str): path-like string

    Raises:
        NoExtensionFoundException: when the file has no extension

    Returns:
        str: path-like string without extension
    """
    if does_file_name_have_extension(file_path):
        return file_path[: get_index_for_the_file_extension(file_path)]

    raise NoExtensionFoundException(f"The file path '{file_path}' has no extension")


def extract_unique_values_from_iterable(iterable: Iterable[T]) -> Iterable[T]:
    """Returns the unique values from the passed iterable without losing its order"""
    uniques: List[T] = []

    for value in iterable:
        if value not in uniques:
            uniques.append(value)

    return uniques
