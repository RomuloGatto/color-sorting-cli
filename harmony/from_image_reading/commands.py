# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path
from typing import Tuple

import rich
import typer

from harmony.color_sorting.service_layer.writing_strategies import PlainTextWriting
from harmony.core.constants import ColorFormat, CommonArguments
from harmony.core.models import Color
from harmony.core.service_layer.color_readers import extract_colors_from_path
from harmony.core.service_layer.services import ColorWriter, PathGenerator
from harmony.from_image_reading.constants import Image2TXTArguments
from harmony.from_image_reading.services import ImageFileReading


def image2txt(
    path: Path = Image2TXTArguments.path,
    color_format: ColorFormat = CommonArguments.color_format,
    recursively: bool = Image2TXTArguments.recursively,
) -> None:
    """Extract the colors from an image and write them into a plain text file"""
    try:
        colors: Tuple[Color, ...] = extract_colors_from_path(
            path, ImageFileReading(), recursively
        )
        final_file_path = PathGenerator("").get_path_with_extension(
            path, PlainTextWriting.EXTENSION
        )
        ColorWriter(PlainTextWriting(color_format)).write(colors, final_file_path)
        rich.print(f"[green]Colors extracted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
