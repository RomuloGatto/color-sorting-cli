# pylint: disable=too-many-arguments,too-many-locals
import rich
import typer

from harmony.core.command_utils import CommandUtils
from harmony.core.constants import CommonArguments
from harmony.to_ase_convertion.constants import TXT2ASECommandArguments
from harmony.to_ase_convertion.services import ASEWriting


def txt2ase(
    colors_file: typer.FileText = TXT2ASECommandArguments.colors_file,
    palette_name: str = TXT2ASECommandArguments.palette_name,
    generate_names: bool = CommonArguments.generate_names,
):
    """Command to convert a text file into a ".ase" file"""
    try:
        CommandUtils(ASEWriting(palette_name), generate_names).convert_txt_file(
            colors_file
        )

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
