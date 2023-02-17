from dataclasses import dataclass

from harmony.core.models import HSL


@dataclass
class ColorName:
    """Store the data of the color name"""

    name: str
    hsl: HSL
