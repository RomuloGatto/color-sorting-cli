import typer

from harmony.core.constants import DefaultParameters


class TXT2ASECommandArguments:
    """Store the "txt2ase" command arguments"""

    palette_name: str = typer.Option(
        DefaultParameters.PALETTE_NAME,
        "--palette-name",
        "-n",
        help='Name of the palette to be written in to the ".ase" file',
    )
