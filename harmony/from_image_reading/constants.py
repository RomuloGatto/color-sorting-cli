import typer


class Image2TXTArguments:
    """Store the arguments and options for `image2txt` command"""

    image_file = typer.Argument(..., help="Image to extract the colors")
