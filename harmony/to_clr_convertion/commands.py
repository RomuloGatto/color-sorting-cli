# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony.core.command_utils import CommandUtils
from harmony.core.constants import CommonArguments
from harmony.to_clr_convertion.services import CLRWriting


def txt2clr(
    file_path: Path = CommonArguments.file_path,
    generate_names: bool = CommonArguments.generate_names,
    suffix: str = CommonArguments.suffix,
):
    """Command to convert a text file into a ".clr" file"""
    CommandUtils(CLRWriting(), suffix, generate_names).convert_txt_file(file_path)
