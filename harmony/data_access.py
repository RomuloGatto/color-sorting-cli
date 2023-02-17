import json
from typing import Iterable, List, Mapping, TextIO

from harmony import convertions, core
from harmony.typing import Number


class ColorNamesStorage:
    """Provide methods for accessing the color names table in the database"""

    def get_color_name_by_hsl(self, hsl: core.HSL) -> str:
        """Get the name of the nearest color in database

        Args:
            hsl (HSL): HSL of the color to name

        Returns:
            str: name found
        """
        color_names = self.__color_names
        color_names.sort(
            key=lambda current_hsl: self.__calc_color_proximity(current_hsl.hsl, hsl)
        )

        return color_names[0].name

    def __calc_color_proximity(self, current_hsl: core.HSL, goal_hsl: core.HSL) -> int:
        return sum(
            self.__calc_proximity_factors(  # type: ignore[arg-type]
                current_hsl, goal_hsl
            )
        )

    def __calc_proximity_factors(
        self, current_hsl: core.HSL, goal_hsl: core.HSL
    ) -> Iterable[Number]:
        return [
            self.__calc_hue_factor(current_hsl, goal_hsl),
            core.absolute_difference_between(
                goal_hsl.saturation, current_hsl.saturation
            ),
            core.absolute_difference_between(
                goal_hsl.luminosity, current_hsl.luminosity
            ),
        ]

    def __calc_hue_factor(self, current_hsl: core.HSL, goal_hsl: core.HSL) -> Number:
        return core.multiplication_between(
            self.__calc_hue_abs_diff_rate(current_hsl, goal_hsl),
            3,
        )

    def __calc_hue_abs_diff_rate(
        self, current_hsl: core.HSL, goal_hsl: core.HSL
    ) -> Number:
        return core.division_between(
            core.absolute_difference_between(goal_hsl.hue, current_hsl.hue),
            core.MAXIMUM_HUE_VALUE,
        )

    @property
    def __color_names(self) -> List[core.ColorName]:
        with open(
            core.ResourceUtils.get_resource(core.Resources.COLOR_NAMES_JSON),
            "r",
            encoding="utf8",
        ) as json_file:
            return list(self.__yield_color_names(json_file))

    def __yield_color_names(self, json_file: TextIO) -> Iterable[core.ColorName]:
        """Extract and yield the data from the json file"""
        return map(self.__make_color_name, json.loads(json_file.read()))

    def __make_color_name(self, color_name_data: Mapping[str, str]) -> core.ColorName:
        return core.ColorName(
            color_name_data["name"],
            self.__make_hsl_from_data(color_name_data),
        )

    def __make_hsl_from_data(self, color_name_data: Mapping[str, str]) -> core.HSL:
        return convertions.RGBToHSLConverter().convert(
            self.__make_rgb_from_data(color_name_data)
        )

    def __make_rgb_from_data(self, color_name_data: Mapping[str, str]) -> core.RGB:
        return core.RGBUtils.get_rgb_from_hexcode(color_name_data["color"])
