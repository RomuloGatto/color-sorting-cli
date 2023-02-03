# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony.core.command_utils import CommandUtils
from harmony.core.constants import CommonArguments
from harmony.to_image_convertion.constants import TXT2ImageCommandArguments
from harmony.to_image_convertion.services import PNGWritting


def txt2image(
    file_path: Path = TXT2ImageCommandArguments.file_path,
    suffix: str = CommonArguments.suffix,
):
    """Command to generate a color palette with the visual representation of the colors
    especified in the passed file"""
    CommandUtils(PNGWritting(), suffix).convert_txt_file(file_path)
