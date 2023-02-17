# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony import core
from harmony.commands import FromTxtCommandUtils
from harmony.to_ase_convertion.constants import TXT2ASECommandArguments
from harmony.to_ase_convertion.services import ASEWriting


def txt2ase(
    file_path: Path = core.CommonArguments.file_path,
    palette_name: str = TXT2ASECommandArguments.palette_name,
    generate_names: bool = core.CommonArguments.generate_names,
    suffix: str = core.CommonArguments.suffix,
):
    """Command to convert a text file into a ".ase" file"""
    FromTxtCommandUtils(
        ASEWriting(palette_name), suffix, generate_names
    ).convert_from_txt_file(file_path)
