from abc import ABC
from dataclasses import dataclass

from harmony.core.models import HSL


class DataModel(ABC):
    """Interface for the data table models"""


@dataclass
class ColorName(DataModel):
    """Store the data of the color name"""

    name: str
    hsl: HSL
