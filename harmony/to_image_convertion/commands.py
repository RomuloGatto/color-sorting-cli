# pylint: disable=too-many-arguments,too-many-locals
import rich
import typer

from harmony.core.command_utils import CommandUtils
from harmony.to_image_convertion.constants import TXT2ImageCommandArguments
from harmony.to_image_convertion.services import PNGWritting


def txt2image(
    colors_file: typer.FileText = TXT2ImageCommandArguments.colors_file,
):
    """Command to generate a color palette with the visual representation of the colors
    especified in the passed file"""
    try:
        CommandUtils(PNGWritting()).convert_txt_file(colors_file)

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
