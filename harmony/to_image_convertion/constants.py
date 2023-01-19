import typer


class TXT2ImageCommandArguments:
    """Store the "txt2clr" command arguments"""

    colors_file: typer.FileText = typer.Argument(
        ..., help="File with the colors to be represented"
    )
