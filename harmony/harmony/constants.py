# pylint: disable=too-few-public-methods
import typer


class MainArguments:
    """Store the core arguments"""

    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Display the current installed version of the CLI",
    )
