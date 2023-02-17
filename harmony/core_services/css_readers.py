from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, TypeVar

from harmony import core

T = TypeVar("T")


def _percentage_to_rgb_value(percentage: int) -> int:
    return round((percentage / 100) * 255)


class CSSFunctionReader(Generic[T], metaclass=ABCMeta):
    """Interface for CSS functions interpreters"""

    @abstractmethod
    def read(self, css_function: str) -> T:
        """Read the css function and convert to a ColorFormatModel

        Args:
            css_function (str): CSS function to interpret

        Returns:
            T: ColorFormatModel result
        """


class RGBCSSFunctionReader(CSSFunctionReader[core.RGB]):
    """Reader for CSS RGB() and RGBA() functions (with integer components)"""

    STRING_PATTERN = (
        r"(RGB|rgb|RGBA|rgba)[\s]*\([\s]*(?P<red>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[\s]*,[\s]*(?P<blue>[0-9]{1,3})[\s]*"
    )

    def read(self, css_function: str) -> core.RGB:
        return core.RGB(
            self._get_red_from_rgb_string(css_function),
            self._get_green_from_rgb_string(css_function),
            self._get_blue_from_rgb_string(css_function),
        )

    def _get_red_from_rgb_string(self, css_function: str) -> int:
        return int(
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["red"]
        )

    def _get_green_from_rgb_string(self, css_function: str) -> int:
        return int(
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["green"]
        )

    def _get_blue_from_rgb_string(self, css_function: str) -> int:
        return int(
            core.RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["blue"]
        )


class PercentageRGBCSSFunctionReader(CSSFunctionReader[core.RGB]):
    """Reader for CSS RGB() and RGBA() functions (with percentage components)"""

    STRING_PATTERN = (
        r"^(rgba|RGBA)\([\s]*(?P<red>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[%][\s]*,"
        + r"[\s]*(?P<blue>[0-9]{1,3})[%][\s]*"
    )

    def read(self, css_function: str) -> core.RGB:
        return core.RGB(
            self._get_red_from_rgb_as_percentage(css_function),
            self._get_green_from_rgb_as_percentage(css_function),
            self._get_blue_from_rgb_as_percentage(css_function),
        )

    def _get_red_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["red"]
        )

    def _get_green_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["green"]
        )

    def _get_blue_from_rgb_as_percentage(self, rgb_string: str) -> int:
        return _percentage_to_rgb_value(
            self._get_raw_string_data_cleaned(rgb_string)["blue"]
        )

    def _get_raw_string_data_cleaned(self, raw_string: str) -> Dict[str, int]:
        return {
            key: int(component)
            for key, component in core.RegexHelper(self.__class__.STRING_PATTERN)
            .get_raw_string_data(raw_string)
            .items()
        }


class HSLCSSFunctionReader(CSSFunctionReader[core.HSL]):
    """Reader for CSS HSL() and HSLA() functions"""

    STRING_PATTERN = (
        r"(hsl|HSL|hsla|HSLA)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[\s]*%[\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[\s]*%[\s]*"
    )

    def read(self, css_function: str) -> core.HSL:
        return core.HSL(
            self._get_hue_from_hsl_string(css_function),
            self._get_saturation_from_hsl_string(css_function),
            self._get_luminosity_from_hsl_string(css_function),
        )

    def _get_hue_from_hsl_string(self, css_function: str) -> int:
        return self._get_raw_string_data_cleaned(css_function)["hue"]

    def _get_saturation_from_hsl_string(self, css_function: str) -> float:
        return self._get_raw_string_data_cleaned(css_function)["saturation"] / 100

    def _get_luminosity_from_hsl_string(self, css_function: str) -> float:
        return self._get_raw_string_data_cleaned(css_function)["luminosity"] / 100

    def _get_raw_string_data_cleaned(self, css_function: str) -> Dict[str, int]:
        return {
            key: int(component)
            for key, component in core.RegexHelper(self.STRING_PATTERN)
            .get_raw_string_data(css_function)
            .items()
        }
