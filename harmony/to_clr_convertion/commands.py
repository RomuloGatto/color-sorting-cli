# pylint: disable=too-many-arguments,too-many-locals
import rich
import typer

from harmony.core.command_utils import CommandUtils
from harmony.core.constants import CommonArguments
from harmony.to_clr_convertion.constants import TXT2CLRCommandArguments
from harmony.to_clr_convertion.services import CLRWriting


def txt2clr(
    colors_file: typer.FileText = TXT2CLRCommandArguments.colors_file,
    generate_names: bool = CommonArguments.generate_names,
):
    """Command to convert a text file into a ".clr" file"""
    try:
        CommandUtils(CLRWriting(), generate_names).convert_txt_file(colors_file)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
