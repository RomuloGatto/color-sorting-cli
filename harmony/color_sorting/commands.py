# pylint: disable=too-many-arguments,too-many-locals
import rich
import typer

from harmony.color_sorting.constants import (
    Directions,
    SortCommandArguments,
    SortingStrategyName,
)
from harmony.color_sorting.service_layer.services import ColorSorter
from harmony.color_sorting.service_layer.writing_strategies import PlainTextWriting
from harmony.core.constants import ColorFormat, CommonArguments
from harmony.core.service_layer.file_readings import PlainTextFileReading
from harmony.core.service_layer.services import (
    ColorReader,
    ColorWriter,
    get_sorted_file_path,
)


def sort(
    colors_file: typer.FileText = SortCommandArguments.colors_file,
    sorting_algorithm: SortingStrategyName = SortCommandArguments.sorting_algorithm,
    direction: Directions = SortCommandArguments.direction,
    color_format: ColorFormat = CommonArguments.color_format,
    suffix: str = SortCommandArguments.suffix,
    generate_names: bool = CommonArguments.generate_names,
) -> None:
    """Entry point for generating a file with the sorted colors"""
    try:
        colors = ColorReader(PlainTextFileReading(generate_names)).extract_from_file(
            colors_file
        )
        sorted_colors = ColorSorter(sorting_algorithm).sort(set(colors), direction)

        final_file_path = get_sorted_file_path(colors_file, sorting_algorithm, suffix)
        ColorWriter(PlainTextWriting(color_format)).write(
            sorted_colors, final_file_path
        )

        rich.print(f"[green]Colors sorted and saved to {final_file_path}")

    except Exception as exception:
        rich.print(f"[bright_red] ERROR: {exception}")
        raise typer.Exit(code=1)
