import uuid
from enum import Enum

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
    SUFFIX: str = "_sorted"


class ColorFormat(str, Enum):
    """Constants for the color formats"""

    SAME_AS_INPUT: str = "input"
    RGB: str = "rgb"
    HEXCODE: str = "hexcode"


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
