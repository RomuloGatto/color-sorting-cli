from enum import Enum
from pathlib import Path

import typer

from harmony.core.constants import DefaultParameters


class Directions(str, Enum):
    """Constants for the direction of the sorting"""

    FORWARD: str = "forward"
    BACKWARD: str = "backward"


class SortingStrategyName(str, Enum):
    """Constants for the sorting strategies"""

    RGB: str = "rgb"
    HSV: str = "hsv"
    HSL: str = "hsl"
    LUMINOSITY: str = "luminosity"
    STEP: str = "step"
    ALTERNATED_STEP: str = "stepalt"
    HILLBERT: str = "hillbert"


class SortCommandArguments:
    """Store the "sort" command arguments"""

    file_path: Path = typer.Argument(
        ...,
        help="File with the colors to be sorted",
        exists=True,
        file_okay=True,
        readable=True,
        resolve_path=True,
    )
    sorting_algorithm: SortingStrategyName = typer.Option(
        SortingStrategyName.HILLBERT.value,
        "--sorting-algorithm",
        "-a",
        case_sensitive=False,
        help="Algorithm to be used for sorting the colors",
    )
    direction: Directions = typer.Option(
        Directions.FORWARD.value,
        "--direction",
        "-d",
        case_sensitive=False,
        help="If the colors will be sorted forward or backward",
    )
    suffix: str = typer.Option(
        DefaultParameters.SUFFIX,
        "--suffix",
        "-s",
        help="Suffix to add to the name of the output file",
    )
