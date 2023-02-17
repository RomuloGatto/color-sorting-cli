from pathlib import Path

from harmony import core
from harmony.commands import ToTxtCommandUtils
from harmony.from_svg_reading.service_layer.svg_file_reading import SVGFileReading


def svg2txt(
    path: Path = core.CommonArguments.file_or_dir_path,
    color_format: core.ColorFormat = core.CommonArguments.color_format,
    recursively: bool = core.CommonArguments.recursively,
) -> None:
    """Extract the colors from an SVG file and write them into a plain text file"""
    ToTxtCommandUtils(SVGFileReading(), color_format, recursively).convert_to_txt_file(
        path
    )
