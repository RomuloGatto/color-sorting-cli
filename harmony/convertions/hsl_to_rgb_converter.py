from itertools import dropwhile
from typing import Callable, Iterator, Tuple

from harmony import core
from harmony.core import exceptions, interfaces


class HSLToRGBConverter(interfaces.ColorFormatConverter[core.HSL, core.RGB]):
    """Converts HSL objects into RGB objects"""

    def convert(self, original_format: core.HSL) -> core.RGB:
        for _, convert in dropwhile(
            lambda item: not item[0](original_format.hue),
            self._get_rgb_factory_mapping(),
        ):
            return convert(original_format)

        raise exceptions.InvalidColorFormatException(
            f"Hue must be between 0 and 360, got {original_format.hue}"
        )

    def _get_rgb_factory_mapping(
        self,
    ) -> Iterator[Tuple[Callable[[int], bool], Callable[[core.HSL], core.RGB]]]:
        yield lambda hue: 0 <= hue < 60, self._calculate_ba0
        yield lambda hue: 60 <= hue < 120, self._calculate_ab0
        yield lambda hue: 120 <= hue < 180, self._calculate_0ba
        yield lambda hue: 180 <= hue < 240, self._calculate_0ab
        yield lambda hue: 240 <= hue < 300, self._calculate_a0b
        yield lambda hue: 300 <= hue < 360, self._calculate_b0a

    def _calculate_ba0(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
        )

    def _calculate_ab0(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
        )

    def _calculate_0ba(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
        )

    def _calculate_0ab(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
        )

    def _calculate_a0b(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_a_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_b_as_component(hsl_values),
        )

    def _calculate_b0a(self, hsl_values: core.HSL) -> core.RGB:
        return core.RGB(
            self._get_rounded_b_as_component(hsl_values),
            self._get_rounded_0_as_component(hsl_values),
            self._get_rounded_a_as_component(hsl_values),
        )

    def _get_rounded_a_as_component(self, hsl_values: core.HSL) -> int:
        return round(self._get_variable_a_as_component(hsl_values))

    def _get_variable_a_as_component(self, hsl_values: core.HSL) -> float:
        return core.multiplication_between(self._get_a_plus_c(hsl_values), 255)

    def _get_a_plus_c(self, hsl_values: core.HSL) -> float:
        return self._get_variable_a(hsl_values) + self._get_variable_c(hsl_values)

    def _get_rounded_b_as_component(self, hsl_values: core.HSL) -> int:
        return round(self._get_variable_b_as_component(hsl_values))

    def _get_variable_b_as_component(self, hsl_values: core.HSL) -> float:
        return self._get_b_plus_c(hsl_values) * 255

    def _get_b_plus_c(self, hsl_values: core.HSL) -> float:
        return self._get_variable_b(hsl_values) + self._get_variable_c(hsl_values)

    def _get_rounded_0_as_component(self, hsl_values: core.HSL) -> int:
        return round(self._get_0_as_component(hsl_values))

    def _get_0_as_component(self, hsl_values: core.HSL) -> float:
        return self._get_0_plus_c(hsl_values) * 255

    def _get_0_plus_c(self, hsl_values: core.HSL) -> float:
        return 0 + self._get_variable_c(hsl_values)

    def _get_variable_c(self, hsl_values: core.HSL) -> float:
        return hsl_values.luminosity - self._get_half_b(hsl_values)

    def _get_half_b(self, hsl_values: core.HSL) -> float:
        return core.division_between(self._get_variable_b(hsl_values), 2)

    def _get_variable_a(self, hsl_values: core.HSL) -> float:
        return core.multiplication_between(
            self._get_variable_b(hsl_values),
            self._get_1_minus_hue_mod_diff(hsl_values.hue),
        )

    def _get_1_minus_hue_mod_diff(self, hue: int) -> float:
        return 1 - self._get_hue_mod_diff(hue)

    def _get_hue_mod_diff(self, hue: int) -> float:
        return core.absolute_difference_between(self._get_hue_mod(hue), 1)

    @staticmethod
    def _get_hue_mod(hue: int) -> float:
        return core.division_between(hue, 60) % 2

    def _get_variable_b(self, hsl_values: core.HSL) -> float:
        return core.multiplication_between(
            self._get_1_minus_double_luminosity_diff(hsl_values.luminosity),
            hsl_values.saturation,
        )

    def _get_1_minus_double_luminosity_diff(self, luminosity: float) -> float:
        return core.difference_between(
            1,
            self._get_double_luminosity_diff(luminosity),
        )

    @staticmethod
    def _get_double_luminosity_diff(
        luminosity: float,
    ) -> float:
        return core.absolute_difference_between(
            core.multiplication_between(luminosity, 2), 1
        )
