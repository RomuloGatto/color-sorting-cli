# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony import core
from harmony.commands import ToTxtCommandUtils
from harmony.from_image_reading.services import ImageFileReading


def image2txt(
    path: Path = core.CommonArguments.file_or_dir_path,
    color_format: core.ColorFormat = core.CommonArguments.color_format,
    recursively: bool = core.CommonArguments.recursively,
) -> None:
    """Extract the colors from an image and write them into a plain text file"""
    ToTxtCommandUtils(
        ImageFileReading(), color_format, recursively
    ).convert_to_txt_file(path)
