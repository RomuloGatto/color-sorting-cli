from dataclasses import dataclass

from harmony.core.models import RGB


@dataclass
class HueData:
    """Store the data to calculate the hue for the HSV format"""

    red_as_percentage: float
    green_as_percentage: float
    blue_as_percentage: float

    @classmethod
    def from_rgb(cls, rgb: RGB) -> "HueData":
        """Make a HueData object from the data of a RGB object"""
        return cls(
            rgb.red_as_percentage, rgb.green_as_percentage, rgb.blue_as_percentage
        )

    @property
    def difference_between_biggest_and_smallest(self) -> float:
        """Return the difference between the biggest and the smallest values between the
        components"""
        return self.biggest_value - self._get_smallest_value()

    @property
    def biggest_value(self) -> float:
        """Return the biggest value between the components"""
        return max(
            self.red_as_percentage, self.green_as_percentage, self.blue_as_percentage
        )

    def _get_smallest_value(self) -> float:
        return min(
            self.red_as_percentage, self.green_as_percentage, self.blue_as_percentage
        )

    @property
    def difference_of_red_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.red_as_percentage - self.biggest_value)

    @property
    def difference_of_green_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.green_as_percentage - self.biggest_value)

    @property
    def difference_of_blue_from_biggest_value(self):
        """Return the difference from red to the biggest value"""
        return abs(self.blue_as_percentage - self.biggest_value)

    @property
    def differences_from_biggest_value(self):
        """Return the differences from the values to the biggest value"""
        return (
            self.difference_of_red_from_biggest_value,
            self.difference_of_green_from_biggest_value,
            self.difference_of_blue_from_biggest_value,
        )


@dataclass
class SaturationData:
    """Store the data needed to calculate the saturation data"""

    biggest_value: float
    difference_between_biggest_and_smallest: float

    @classmethod
    def from_hue_data(cls, hue_data: HueData) -> "SaturationData":
        """Make a SaturationData object from the data in a HueData object"""
        return cls(
            hue_data.biggest_value, hue_data.difference_between_biggest_and_smallest
        )

    @classmethod
    def from_rgb(cls, rgb: RGB) -> "SaturationData":
        """Make a SaturationData object from the data in a RGB object"""
        return cls.from_hue_data(HueData.from_rgb(rgb))
