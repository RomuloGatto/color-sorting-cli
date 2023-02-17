# pylint: disable=too-many-arguments,too-many-locals
from pathlib import Path

import rich

from harmony import core, core_services
from harmony.color_sorting.constants import Directions, SortCommandArguments
from harmony.color_sorting.service_layer.services import (
    ColorSorter,
    make_sorting_strategy,
)


def sort(
    file_path: Path = SortCommandArguments.file_path,
    sorting_algorithm: core.SortingStrategyName = (
        SortCommandArguments.sorting_algorithm
    ),
    direction: Directions = SortCommandArguments.direction,
    color_format: core.ColorFormat = core.CommonArguments.color_format,
    suffix: str = core.CommonArguments.suffix,
    generate_names: bool = core.CommonArguments.generate_names,
) -> None:
    """Entry point for generating a file with the sorted colors"""
    colors = core_services.FileColorReader(
        core_services.PlainTextFileReading(generate_names)
    ).extract_colors(file_path)
    sorted_colors = ColorSorter(make_sorting_strategy(sorting_algorithm)).sort(
        set(colors), direction
    )

    final_file_path = core_services.PathGenerator(suffix).get_sorted_file_path(
        file_path, sorting_algorithm
    )
    core_services.ColorWriter(core_services.PlainTextWriting(color_format)).write(
        sorted_colors, final_file_path
    )

    rich.print(f"[green]Colors sorted and saved to {final_file_path}")
