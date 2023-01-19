import typer

from harmony.core.constants import DefaultParameters


class TXT2ASECommandArguments:
    """Store the "txt2ase" command arguments"""

    colors_file: typer.FileText = typer.Argument(..., help="File to be converted")
    palette_name: str = typer.Option(
        DefaultParameters.PALETTE_NAME,
        "--palette-name",
        "-n",
        help='Name of the palette to be written in to the ".ase" file',
    )
