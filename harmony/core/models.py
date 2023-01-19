from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Tuple

from harmony.core import constants


@dataclass
class RGB:
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


@dataclass
class Color:
    """Model for the color"""

    rgb: RGB
    hexcode: str
    original_format: str
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

    def __hash__(self) -> int:
        return hash((self.rgb_red, self.rgb_green, self.rgb_blue))


@dataclass
class HSL:
    """Store the data of the HSL of a color"""

    hue: int
    saturation: float
    luminosity: float


class DataModel(ABC):
    """Interface for the data table models"""


@dataclass
class ColorName(DataModel):
    """Store the data of the color name"""

    name: str
    hsl: HSL


@dataclass
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
