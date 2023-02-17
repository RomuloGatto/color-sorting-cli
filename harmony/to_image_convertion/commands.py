# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony import core
from harmony.commands import FromTxtCommandUtils
from harmony.to_image_convertion.constants import TXT2ImageCommandArguments
from harmony.to_image_convertion.services import PNGWritting


def txt2image(
    file_path: Path = TXT2ImageCommandArguments.file_path,
    suffix: str = core.CommonArguments.suffix,
):
    """Command to generate a color palette with the visual representation of the colors
    especified in the passed file"""
    FromTxtCommandUtils(PNGWritting(), suffix).convert_from_txt_file(file_path)
