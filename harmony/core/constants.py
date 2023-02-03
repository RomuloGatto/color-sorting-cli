import uuid
from enum import Enum
from pathlib import Path
from typing import Any

import typer

MAXIMUM_RGB_VALUE = 255
MAXIMUM_HUE_VALUE = 360
MAXIMUM_8_BIT_UNSIGNED_INTEGER_VALUE = 255
MAXIMUM_8_BIT_SIGNED_INTEGER_VALUE = 127
MINIMUM_8_BIT_SIGNED_INTEGER_VALUE = -MAXIMUM_8_BIT_SIGNED_INTEGER_VALUE


class Resources:
    """Constants for the package resources"""

    COLOR_NAMES_CSV = "color-names.csv"
    SQLITE_DATABASE = "db.sqlite3"


class DefaultParameters:
    """Constants for the default subjective parameters"""

    PALETTE_NAME: str = f"Palette {uuid.uuid4()} sorted by Harmony"


class ColorFormat(str, Enum):
    """Constants for the color formats"""

    SAME_AS_INPUT = "input"
    RGB = "rgb"
    HEXCODE = "hexcode"
    HSL = "hsl"


class ByteOrder(str, Enum):
    """Constants for the byte orders"""

    LITTLE: str = "little"
    BIG: str = "big"


class TableNames:
    """Constants for the database tables names"""

    COLOR_NAME = "namegeneration_colorname"


class QueryConstants:
    """Constants for query sintax elements"""

    ALL_COLUMNS = ["*"]


class FloatComparisonTolerance(float, Enum):
    """Constants for tolerance on float comparison"""

    THREE_DECIMAL_PLACES = 10 ** (-3)
    SEVEN_DECIMAL_PLACES = 10 ** (-7)


class ImageModesForPIL:
    """Contants for the image modes for Pillow package"""

    RGB_MODE = "RGB"


def make_file_path_argument(helping_text: str) -> Any:
    """Returns a typer argument for a file path with the passed helping text"""
    return typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
        help=helping_text,
    )


def make_file_or_dir_path_argument(helping_text: str) -> Any:
    """Returns a typer argument for a file path with the passed helping text"""
    return typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help=helping_text,
    )


class CommonArguments:
    """Store the arguments common to more than one command"""

    generate_names: bool = typer.Option(
        True,
        "--no-generate-color-names",
        "-G",
        help="Disables the color name generation for the unlabelled colors.",
    )
    color_format: ColorFormat = typer.Option(
        ColorFormat.SAME_AS_INPUT.value,
        "--color-format",
        "-f",
        case_sensitive=False,
        help="The format the colors will be written in the output file",
    )
    file_path: Path = make_file_path_argument("File to be converted")
    file_or_dir_path: Path = make_file_or_dir_path_argument(
        "File or directory to extract the colors from"
    )
    suffix: str = typer.Option(
        "",
        "--suffix",
        "-s",
        help="Suffix to add to the name of the output file",
    )
    recursively: bool = typer.Option(
        False,
        "--recursively",
        "-r",
        help="Whether it should read the files recursively, in case a directory was "
        + "passed",
    )
