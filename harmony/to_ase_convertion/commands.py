# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony.core.command_utils import CommandUtils
from harmony.core.constants import CommonArguments
from harmony.to_ase_convertion.constants import TXT2ASECommandArguments
from harmony.to_ase_convertion.services import ASEWriting


def txt2ase(
    file_path: Path = CommonArguments.file_path,
    palette_name: str = TXT2ASECommandArguments.palette_name,
    generate_names: bool = CommonArguments.generate_names,
    suffix: str = CommonArguments.suffix,
):
    """Command to convert a text file into a ".ase" file"""
    CommandUtils(ASEWriting(palette_name), suffix, generate_names).convert_txt_file(
        file_path
    )
