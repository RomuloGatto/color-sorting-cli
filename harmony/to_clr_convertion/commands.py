# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

from harmony import core
from harmony.commands import FromTxtCommandUtils
from harmony.to_clr_convertion.services import CLRWriting


def txt2clr(
    file_path: Path = core.CommonArguments.file_path,
    generate_names: bool = core.CommonArguments.generate_names,
    suffix: str = core.CommonArguments.suffix,
):
    """Command to convert a text file into a ".clr" file"""
    FromTxtCommandUtils(CLRWriting(), suffix, generate_names).convert_from_txt_file(
        file_path
    )
