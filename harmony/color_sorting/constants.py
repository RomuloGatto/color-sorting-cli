# pylint: disable=too-few-public-methods,too-many-ancestors

from enum import Enum
from pathlib import Path

import typer

from harmony import core


class Directions(str, Enum):
    """Constants for the direction of the sorting"""

    FORWARD: str = "forward"
    BACKWARD: str = "backward"


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
    sorting_algorithm: core.SortingStrategyName = typer.Option(
        core.SortingStrategyName.HILLBERT.value,
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
