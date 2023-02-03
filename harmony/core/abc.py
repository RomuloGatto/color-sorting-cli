import re
from abc import ABCMeta, abstractmethod

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import StringReadingStrategy
from harmony.core.models import HSL, RGB, Color
from harmony.core.utils import RegexHelper
from harmony.data_access.store import ColorNamesStorage


class ExtractLabelPatternReadingStrategy(StringReadingStrategy, metaclass=ABCMeta):
    """Interface for the object responsible for converting a color property to a Color
    object"""

    STRING_PATTERN: str
    ORIGINAL_FORMAT: ColorFormat

    def read(self, property_value: str) -> Color:
        """Convert the raw value passed into a Color object

        Args:
            property_value (str): value of the color property in a given element from a
            SVG file

        Returns:
            Color: Color result
        """
        return Color(
            rgb=self.execute_get_rgb(property_value),
            hsl=self.execute_get_hsl(property_value),
            hexcode=self.execute_get_hexcode(property_value),
            original_format=self.__class__.ORIGINAL_FORMAT,
            description=self.__get_description(property_value) or "",
        )

    def __get_description(self, property_value: str) -> str:
        return RegexHelper(self.__class__.STRING_PATTERN).get_raw_string_data(
            property_value
        )["description"]

    @abstractmethod
    def execute_get_rgb(self, property_value: str) -> RGB:
        """Overwrite this method returning a RGB object

        Args:
            property_value (str): original string passed

        Returns:
            RGB: RGB object
        """

    @abstractmethod
    def execute_get_hexcode(self, property_value: str) -> str:
        """Overwrite this method returning a hexcode string

        Args:
            property_value (str): original string passed

        Returns:
            str: hexcode string
        """

    @abstractmethod
    def execute_get_hsl(self, property_value: str) -> HSL:
        """Overwrite this method returning a HSL object

        Args:
            property_value (str): original string passed

        Returns:
            HSL: HSL object
        """

    @classmethod
    def match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None


class AutoLabelPatternReadingStrategy(StringReadingStrategy, metaclass=ABCMeta):
    """Interface for the object responsible for converting a color property to a Color
    object"""

    STRING_PATTERN: str
    ORIGINAL_FORMAT: ColorFormat

    def read(self, property_value: str) -> Color:
        """Convert the raw value passed into a Color object

        Args:
            property_value (str): value of the color property in a given element from a
            SVG file

        Returns:
            Color: Color result
        """
        return Color(
            rgb=self.execute_get_rgb(property_value),
            hsl=self.execute_get_hsl(property_value),
            hexcode=self.execute_get_hexcode(property_value),
            original_format=self.__class__.ORIGINAL_FORMAT,
            description=self.__get_description(property_value),
        )

    def __get_description(self, property_value: str) -> str:
        with ColorNamesStorage() as store:
            return store.get_color_name_by_hsl(self.execute_get_hsl(property_value))

    @abstractmethod
    def execute_get_rgb(self, property_value: str) -> RGB:
        """Overwrite this method returning a RGB object

        Args:
            property_value (str): original string passed

        Returns:
            RGB: RGB object
        """

    @abstractmethod
    def execute_get_hexcode(self, property_value: str) -> str:
        """Overwrite this method returning a hexcode string

        Args:
            property_value (str): original string passed

        Returns:
            str: hexcode string
        """

    @abstractmethod
    def execute_get_hsl(self, property_value: str) -> HSL:
        """Overwrite this method returning a HSL object

        Args:
            property_value (str): original string passed

        Returns:
            HSL: HSL object
        """

    @classmethod
    def match_pattern(cls, property_value: str) -> bool:
        return re.match(cls.STRING_PATTERN, property_value) is not None
