from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, TypeVar

from harmony.core.models import HSL, RGB
from harmony.core.utils import RegexHelper

T = TypeVar("T")


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


class RGBCSSFunctionReader(CSSFunctionReader[RGB]):
    """Reader for CSS RGB() and RGBA() functions (with integer components)"""

    STRING_PATTERN = (
        r"(RGB|rgb|RGBA|rgba)[\s]*\([\s]*(?P<red>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<green>[0-9]{1,3})[\s]*,[\s]*(?P<blue>[0-9]{1,3})[\s]*"
    )

    def read(self, css_function: str) -> RGB:
        return RGB(
            self._get_red_from_rgb_string(css_function),
            self._get_green_from_rgb_string(css_function),
            self._get_blue_from_rgb_string(css_function),
        )

    def _get_red_from_rgb_string(self, css_function: str) -> int:
        return int(
            RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["red"]
        )

    def _get_green_from_rgb_string(self, css_function: str) -> int:
        return int(
            RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["green"]
        )

    def _get_blue_from_rgb_string(self, css_function: str) -> int:
        return int(
            RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
                css_function
            )["blue"]
        )


class HSLCSSFunctionReader(CSSFunctionReader[HSL]):
    """Reader for CSS HSL() and HSLA() functions"""

    STRING_PATTERN = (
        r"(hsl|HSL|hsla|HSLA)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
        + r"[\s]*(?P<saturation>[0-9]{1,3})[\s]*%[\s]*,"
        + r"[\s]*(?P<luminosity>[0-9]{1,3})[\s]*%[\s]*"
    )

    def read(self, css_function: str) -> HSL:
        return HSL(
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
            for key, component in RegexHelper(self.STRING_PATTERN)
            .get_raw_string_data(css_function)
            .items()
        }
