from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Tuple, Type
from xml.etree import ElementTree

from harmony import core
from harmony.core import interfaces
from harmony.from_svg_reading.service_layer.basic_svg_readings import (
    CSSColorNameReading,
    HexcodeSVGReading,
    RGBSVGReading,
)
from harmony.from_svg_reading.service_layer.hsl_svg_readings import HSLSVGReading
from harmony.from_svg_reading.service_layer.percentage_svg_reading import (
    PercentageRGBReading,
)


class SVGFileReading(interfaces.FileReadingStrategy):
    """Strategy for reading SVG files.

    The colors are extracted from the attributes `fill` and `stroke` as specified at
    [MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Content_type#paint), which
    possible values are specified by [W3](https://www.w3.org/TR/css-color-3/#html4)
    """

    def read(self, file_path: Path) -> Tuple[core.Color, ...]:
        colors: List[core.Color] = []

        for element in ElementTree.parse(file_path).iter():
            colors.extend(
                value
                for value in self.__iterate_possible_colors(element)
                if value is not None
            )

        return tuple(colors)

    def __iterate_possible_colors(
        self, element: ElementTree.Element
    ) -> Iterable[Optional[core.Color]]:
        for element_property in filter(
            self.__is_color_property,
            element.keys(),
        ):
            yield self.__get_color_if_possible(element.get(element_property, ""))

    @staticmethod
    def __is_color_property(property_name: str) -> bool:
        return property_name in ["fill", "stroke"]

    def __get_color_if_possible(self, color_value: str) -> Optional[core.Color]:
        for factory in filter(
            lambda factory: factory.match_pattern(color_value),
            self.__iter_color_factories(),
        ):
            return factory().read(color_value)

        return None

    def __iter_color_factories(
        self,
    ) -> Iterator[Type[interfaces.StringReadingStrategy]]:
        yield CSSColorNameReading
        yield HexcodeSVGReading
        yield RGBSVGReading
        yield PercentageRGBReading
        yield HSLSVGReading
