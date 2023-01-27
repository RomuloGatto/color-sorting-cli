import typer


class Image2TXTArguments:
    """Store the arguments and options for `image2txt` command"""

    path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Image to extract the colors",
    )
