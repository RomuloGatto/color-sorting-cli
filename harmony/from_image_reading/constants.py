from pathlib import Path

import typer


class Image2TXTArguments:
    """Store the arguments and options for `image2txt` command"""

    path: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Image to extract the colors",
    )
    recursively: bool = typer.Option(
        False,
        "--recursively",
        "-r",
        help="Whether it should read the files recursively, in case a directory was "
        + "passed",
    )
