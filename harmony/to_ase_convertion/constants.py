# pylint: disable=too-few-public-methods

import typer

from harmony import core


class TXT2ASECommandArguments:
    """Store the "txt2ase" command arguments"""

    palette_name: str = typer.Option(
        core.DefaultParameters.PALETTE_NAME,
        "--palette-name",
        "-n",
        help='Name of the palette to be written in to the ".ase" file',
    )
