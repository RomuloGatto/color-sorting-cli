from pathlib import Path
from typing import Tuple

import rich

from harmony.color_sorting.service_layer.writing_strategies import PlainTextWriting
from harmony.core.constants import ColorFormat, CommonArguments
from harmony.core.models import Color
from harmony.core.service_layer.color_readers import extract_colors_from_path
from harmony.core.service_layer.services import ColorWriter, PathGenerator
from harmony.from_svg_reading.service_layer.svg_file_reading import SVGFileReading


def svg2txt(
    path: Path = CommonArguments.file_or_dir_path,
    color_format: ColorFormat = CommonArguments.color_format,
    recursively: bool = CommonArguments.recursively,
) -> None:
    """Extract the colors from an SVG file and write them into a plain text file"""
    colors: Tuple[Color, ...] = extract_colors_from_path(
        path, SVGFileReading(), recursively
    )
    final_file_path = PathGenerator("").get_path_with_extension(
        path, PlainTextWriting.EXTENSION
    )
    ColorWriter(PlainTextWriting(color_format)).write(colors, final_file_path)
    rich.print(f"[green]Colors extracted and saved to {final_file_path}")
