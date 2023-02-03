import re
from typing import Dict, List, Optional, Tuple, no_type_check

from harmony.core.constants import MAXIMUM_RGB_VALUE, ColorFormat
from harmony.core.exceptions import InvalidFileException
from harmony.core.interfaces import PlainTextReadingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.core.service_layer.converters import HSLToRGBConverter, RGBToHSLConverter
from harmony.core.utils import HexcodeUtils, RGBUtils


class HexcodeReading(PlainTextReadingStrategy):
    """Convert a raw string the with a hexcode string into a Color object"""

    def read(self, raw_string: str) -> Color:
        description = ""

        if self._there_is_whitespace_in(raw_string):
            raw_string, description = self._split_hexcode_and_description(raw_string)

        return Color(
            rgb=RGBUtils.get_rgb_from_hexcode(raw_string),
            hsl=self._get_hsl_from_hexcode(raw_string),
            hexcode=HexcodeUtils.convert_hexcode_from_3_to_6_chars_form(
                raw_string
            ).lower(),
            original_format=ColorFormat.HEXCODE,
            description=description,
        )

    def _split_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> Tuple[str, str]:
        return (
            self._get_hexcode_from_hexcode_and_description(hexcode_and_description),
            self._get_description_from_hexcode_and_description(hexcode_and_description),
        )

    def _get_hsl_from_hexcode(self, hexcode: str) -> HSL:
        return RGBToHSLConverter().convert(RGBUtils.get_rgb_from_hexcode(hexcode))

    def _get_hexcode_from_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> str:
        return hexcode_and_description[
            : self._get_hexcode_and_description_split_index(hexcode_and_description)
        ]

    def _get_description_from_hexcode_and_description(
        self, hexcode_and_description: str
    ) -> str:
        return hexcode_and_description[
            self._get_description_start_index(hexcode_and_description) :
        ].strip()

    def _there_is_whitespace_in(self, string_to_verify: str) -> bool:
        return self._get_hexcode_and_description_split_index(string_to_verify) > 0

    def _get_description_start_index(self, hexcode_and_description: str) -> int:
        return (
            self._get_hexcode_and_description_split_index(hexcode_and_description) + 1
        )

    @staticmethod
    def _get_hexcode_and_description_split_index(hexcode_and_description: str) -> int:
        return hexcode_and_description.find(" ")


class RGBReading(PlainTextReadingStrategy):
    """Convert a raw string the with RGB components into a Color object"""

    def read(self, raw_string: str) -> Color:
        for amount in self._get_components_from_rgb_and_description(raw_string):
            self._check_rgb_amount(amount)

        return Color(
            rgb=self._get_rgb_from_rgb_and_description(raw_string),
            hsl=self._get_hsl_from_rgb_and_description(raw_string),
            hexcode=self._get_and_clean_hexcode_from_rgb_and_description(raw_string),
            original_format=ColorFormat.RGB,
            description=self._get_description_from_rgb_and_description(raw_string),
        )

    def _get_hsl_from_rgb_and_description(self, rgb_and_description: str) -> HSL:
        return RGBToHSLConverter().convert(
            self._get_rgb_from_rgb_and_description(rgb_and_description)
        )

    def _get_description_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return rgb_and_description[
            self._get_description_start_index(rgb_and_description) :
        ].strip()

    def _get_description_start_index(self, rgb_and_description: str) -> int:
        return self._get_rgb_and_description_split_index(rgb_and_description) + 1

    @staticmethod
    def _get_rgb_and_description_split_index(rgb_and_description: str) -> int:
        return rgb_and_description.index(")") + 1

    def _get_and_clean_hexcode_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return (
            "#"
            + self._get_hexcode_from_rgb_and_description(rgb_and_description).lower()
        )

    def _get_hexcode_from_rgb_and_description(self, rgb_and_description: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(
            self._get_rgb_from_rgb_and_description(rgb_and_description)
        )

    def _get_rgb_from_rgb_and_description(self, rgb_and_description: str) -> RGB:
        # pylint: disable=no-value-for-parameter
        return RGB(*self._get_components_from_rgb_and_description(rgb_and_description))

    def _get_components_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> Tuple[int, ...]:
        components: List[int] = []

        for component in self._get_and_clean_rgb_from_rgb_and_description(
            rgb_and_description
        ).split(","):
            components.append(int(component))

        return tuple(components)

    def _get_and_clean_rgb_from_rgb_and_description(
        self, rgb_and_description: str
    ) -> str:
        return self._clean_rgb_string(
            self._get_rgb_string_from_rgb_and_description(rgb_and_description)
        )

    def _get_rgb_string_from_rgb_and_description(self, rgb_and_description: str) -> str:
        return rgb_and_description[
            : self._get_rgb_and_description_split_index(rgb_and_description)
        ]

    def _clean_rgb_string(self, string_to_clean: str) -> str:
        return (
            self._get_components_from_string_to_clean(string_to_clean)["red"]
            + ","
            + self._get_components_from_string_to_clean(string_to_clean)["green"]
            + ","
            + self._get_components_from_string_to_clean(string_to_clean)["blue"]
        )

    def _get_components_from_string_to_clean(
        self, string_to_clean: str
    ) -> Dict[str, str]:
        if self._get_match_from_rgb_string(string_to_clean) is None:
            raise InvalidFileException(
                f"'{string_to_clean}' is not a valid color string"
            )

        return self._get_match_from_rgb_string(  # type:ignore[union-attr]
            string_to_clean
        ).groupdict()

    def _get_match_from_rgb_string(self, rgb_string: str) -> Optional[re.Match]:
        return re.match(
            r"(rgb|RGB)\([\s]*(?P<red>[0-9]{1,3})[\s]*,[\s]*(?P<green>[0-9]{1,3})[\s]*"
            + r",[\s]*(?P<blue>[0-9]{1,3})[\s]*\)",
            rgb_string,
        )

    def _check_rgb_amount(self, amount: int) -> None:
        """Raise exception if amount not between 0 and 255"""
        if self._is_amount_not_between_zero_and_255(amount):
            raise InvalidFileException(
                "The amount of red, green and blue needs to be between 0 and 255, "
                + f"{amount} is invalid"
            )

    def _is_amount_not_between_zero_and_255(self, amount: int) -> bool:
        return not (
            self._is_amount_greater_or_equal_to_zero(amount)
            and self._is_amount_less_than_maximum_rgb_value(amount)
        )

    @staticmethod
    def _is_amount_greater_or_equal_to_zero(amount: int) -> bool:
        return amount >= 0

    @staticmethod
    def _is_amount_less_than_maximum_rgb_value(amount: int) -> bool:
        return amount <= MAXIMUM_RGB_VALUE


class HSLTextReading(PlainTextReadingStrategy):
    """Read css HSL() function and convert to HSL object"""

    def read(self, raw_string: str) -> Color:
        return Color(
            rgb=self._get_rgb_from_raw(raw_string),
            hsl=self._get_hsl_from_raw(raw_string),
            hexcode="#" + self._get_hexcode_from_raw(raw_string),
            original_format=ColorFormat.HSL,
            description=self._get_hsl_data_from_raw(raw_string).get("description")
            or "",
        )

    def _get_hexcode_from_raw(self, raw: str) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(self._get_rgb_from_raw(raw))

    def _get_rgb_from_raw(self, raw: str) -> RGB:
        return HSLToRGBConverter().convert(self._get_hsl_from_raw(raw))

    def _get_hsl_from_raw(self, raw: str) -> HSL:
        return HSL(
            self._get_hue_from_raw(raw),
            self._get_saturation_from_raw(raw),
            self._get_luminosity_from_raw(raw),
        )

    def _get_hue_from_raw(self, raw: str) -> int:
        return int(self._get_hsl_data_from_raw(raw)["hue"])

    def _get_saturation_as_decimal_from_raw(self, raw: str) -> float:
        return self._get_saturation_from_raw(raw)

    def _get_saturation_from_raw(self, raw: str) -> float:
        return self._get_saturation_as_int_from_raw(raw) / 100

    def _get_saturation_as_int_from_raw(self, raw: str) -> float:
        return float(self._get_hsl_data_from_raw(raw)["saturation"])

    def _get_luminosity_from_raw(self, raw: str) -> float:
        return self._get_luminosity_as_int_from_raw(raw) / 100

    def _get_luminosity_as_int_from_raw(self, raw: str) -> float:
        return float(self._get_hsl_data_from_raw(raw)["luminosity"])

    @no_type_check
    def _get_hsl_data_from_raw(self, raw: str) -> Dict[str, str]:
        if self._get_raw_re_match(raw) is None:
            raise InvalidFileException(f"'{raw}' is not a valid HSL string")

        return self._get_raw_re_match(raw).groupdict()

    def _get_raw_re_match(self, raw: str) -> Optional[re.Match]:
        return re.match(
            r"(hsl|HSL)\([\s]*(?P<hue>[0-9]{1,3})[\s]*,"
            + r"[\s]*(?P<saturation>[0-9]{1,3})[\s]*%[\s]*,"
            + r"[\s]*(?P<luminosity>[0-9]{1,3})[\s]*%[\s]*\)([\s](?P<description>.*))?",
            raw,
        )
