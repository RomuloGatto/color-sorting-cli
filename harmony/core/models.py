import dataclasses
from abc import ABC
from functools import total_ordering
from typing import Any, Dict, List, Tuple, no_type_check

import pydantic

from harmony.core import constants
from harmony.typing import Number, T


@total_ordering
class ColorFormatModel(ABC):
    """Interface for the color format models"""

    def __hash__(self) -> int:
        return hash(self.get_field_values())

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.get_field_values() == other.get_field_values()

        raise TypeError(f"'==' not supported between {type(other)} and {type(self)}")

    def __lt__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.get_field_values() < other.get_field_values()

        raise TypeError(f"'<' not supported between {type(other)} and {type(self)}")

    def get_field_values(self) -> Tuple[Number, ...]:
        """Return all values from all numeric field in the model"""
        field_values: List[Number] = self._get_integer_fields()
        field_values.extend(self._get_float_fields())
        return tuple(field_values)

    def _get_integer_fields(self) -> List[Number]:
        field_values: List[Number] = []

        for field in filter(
            self._is_field_integer,
            vars(self.__class__)["__dataclass_fields__"].keys(),
        ):
            field_values.append(getattr(self, field))

        return field_values

    def _get_float_fields(self) -> List[Number]:
        field_values: List[Number] = []

        for field in filter(
            self._is_field_float,
            vars(self.__class__)["__dataclass_fields__"].keys(),
        ):
            field_values.append(self._get_decimal_field_as_int(field))

        return field_values

    def _is_field_integer(self, field: Any) -> bool:
        return isinstance(getattr(self, field), int)

    def _is_field_float(self, field: Any) -> bool:
        return isinstance(getattr(self, field), float)

    def _get_decimal_field_as_int(self, field: str) -> int:
        return int(getattr(self, field) * 100)

    @no_type_check
    @classmethod
    def from_color_format_model(cls: T, value: "ColorFormatModel") -> T:
        """Convert a generic ColorFormatModel to a specific one

        Args:
            cls (T): specific ColorFormatModel to convert to
            value (ColorFormatModel): generic ColorFormatModel

        Raises:
            TypeError: when the convertion is not possible

        Returns:
            T: the converted object
        """
        if isinstance(value, cls):
            return value

        raise TypeError(f"Unable to convert {type(value)} to {cls.__name__}")


@dataclasses.dataclass(eq=False)
class SteppedHueValuePerceivedLuminosity(ColorFormatModel):
    """Model for the stepped hue, perceived luminosity and stepped value"""

    stepped_hue: int
    perceived_luminosity: float
    stepped_value: int

    def __hash__(self) -> int:
        return hash((self.stepped_hue, self.perceived_luminosity, self.stepped_value))


@dataclasses.dataclass(eq=False)
class HSV(ColorFormatModel):
    """Model for the HSV values of a color"""

    hue: int
    saturation: float
    value: float


@dataclasses.dataclass(eq=False)
class PerceivedLuminosity(ColorFormatModel):
    """Model for the perceived luminosity of the color"""

    value: float


@dataclasses.dataclass(eq=False)
class RGB(ColorFormatModel):
    """Model for the RGB format of color"""

    red: int
    green: int
    blue: int

    def __str__(self):
        return f"RGB({self.red}, {self.green}, {self.blue})"

    @property
    def red_as_percentage(self) -> float:
        """Return the red component as percentage"""
        return self.red / constants.MAXIMUM_RGB_VALUE

    @property
    def green_as_percentage(self) -> float:
        """Return the green component as percentage"""
        return self.green / constants.MAXIMUM_RGB_VALUE

    @property
    def blue_as_percentage(self) -> float:
        """Return the blue component as percentage"""
        return self.blue / constants.MAXIMUM_RGB_VALUE


@dataclasses.dataclass(eq=False)
class HSL(ColorFormatModel):
    """Store the data of the HSL of a color"""

    hue: int
    saturation: float
    luminosity: float


class Color(pydantic.BaseModel):  # pylint: disable=no-member
    """Model for the color"""

    rgb: RGB
    hsl: HSL
    hexcode: str
    original_format: constants.ColorFormat
    description: str

    @property
    def rgb_red(self) -> int:
        """Return the value of red from the RGB of the color"""
        return self.rgb.red

    @property
    def rgb_green(self) -> int:
        """Return the value of green from the RGB of the color"""
        return self.rgb.green

    @property
    def rgb_blue(self) -> int:
        """Return the value of blue from the RGB of the color"""
        return self.rgb.blue

    @property
    def hsl_hue(self) -> int:
        """Return the value of hue from the HSL of the color"""
        return self.hsl.hue

    @property
    def hsl_saturation(self) -> float:
        """Return the value of saturation from the HSL of the color"""
        return self.hsl.saturation

    @property
    def hsl_luminosity(self) -> float:
        """Return the value of luminosity from the HSL of the color"""
        return self.hsl.luminosity

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.rgb == other.rgb and self.hsl == other.hsl

        raise TypeError(f"'==' not supported between {type(other)} and {type(self)}")

    def __hash__(self) -> int:
        return hash((self.rgb_red, self.rgb_green, self.rgb_blue))


@dataclasses.dataclass
class InsertQueryData:
    """Store the data needed to form a INSERT SQL query"""

    table_name: str
    data_to_insert: Dict[str, Any]

    @property
    def columns(self) -> Tuple[str, ...]:
        """Return the name of the columns related to the passed values"""
        return tuple(self.data_to_insert.keys())

    @property
    def values_to_insert(self) -> Tuple[Any, ...]:
        """Return the values passed for the new table registry"""
        return tuple(self.data_to_insert.values())
