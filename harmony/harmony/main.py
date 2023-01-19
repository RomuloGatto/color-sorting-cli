# pylint: disable=too-many-locals,too-many-arguments

import rich
import typer

from harmony import __version__
from harmony.color_sorting.commands import sort
from harmony.from_image_reading.commands import image2txt
from harmony.harmony.adapters import HarmonyTyper
from harmony.to_ase_convertion.commands import txt2ase
from harmony.to_clr_convertion.commands import txt2clr
from harmony.to_image_convertion.commands import txt2image

app = HarmonyTyper(pretty_exceptions_show_locals=False, rich_markup_mode="markdown")
app.command()(sort)
app.command()(txt2ase)
app.command()(txt2clr)
app.command()(txt2image)
app.command()(image2txt)


def _display_version(context: typer.Context):
    if context.invoked_subcommand:
        rich.print(
            "[bright_red] ERROR: parameter --version not compatible with other "
            + "commands"
        )
        raise typer.Exit(code=1)

    rich.print(f"Harmony {__version__}")


@app.callback(invoke_without_command=True)
def main(context: typer.Context, version: bool = False):
    """Harmony is a CLI that provides tools for managing colors"""
    if version:
        _display_version(context)


if __name__ == "__main__":
    app()
