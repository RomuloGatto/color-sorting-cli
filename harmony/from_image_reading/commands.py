import rich
import typer

from harmony.color_sorting.service_layer.writing_strategies import PlainTextWriting
from harmony.core.constants import ColorFormat, CommonArguments
from harmony.core.service_layer.services import ColorReader, ColorWriter
from harmony.core.utils import get_path_with_extension
from harmony.from_image_reading.constants import Image2TXTArguments
from harmony.from_image_reading.services import ImageFileReading


def image2txt(
    image_file: typer.FileBinaryRead = Image2TXTArguments.image_file,
    color_format: ColorFormat = CommonArguments.color_format,
) -> None:
    """Extract the colors from an image and write them into a plain text file"""
    try:
        colors = ColorReader(ImageFileReading()).extract_from_file(image_file)
        final_file_path = get_path_with_extension(
            image_file, PlainTextWriting.EXTENSION
        )
        ColorWriter(PlainTextWriting(color_format)).write(
            tuple(colors), final_file_path
        )

        rich.print(f"[green]Colors extracted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
