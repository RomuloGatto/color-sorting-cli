from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Type
from xml.etree import ElementTree

from harmony.core.interfaces import FileReadingStrategy, StringReadingStrategy
from harmony.core.models import Color
from harmony.from_svg_reading.service_layer.basic_svg_readings import (
    CSSColorNameReading,
    HexcodeSVGReading,
    RGBAReading,
    RGBSVGReading,
)
from harmony.from_svg_reading.service_layer.hsl_svg_readings import (
    HSLAReading,
    HSLSVGReading,
)
from harmony.from_svg_reading.service_layer.percentage_svg_reading import (
    PercentageRGBAReading,
    PercentageRGBReading,
)


class SVGFileReading(FileReadingStrategy):
    """Strategy for reading SVG files.

    The colors are extracted from the attributes `fill` and `stroke` as specified at
    [MDN](https://developer.mozilla.org/en-US/docs/Web/SVG/Content_type#paint), which
    possible values are specified by [W3](https://www.w3.org/TR/css-color-3/#html4)
    """

    def read(self, file_path: Path) -> Tuple[Color, ...]:
        colors: List[Color] = []

        for element in filter(
            self._validate_stroke_or_fill_if_exists,
            ElementTree.parse(file_path).iter(),
        ):
            colors.append(
                self._validate_stroke_or_fill_if_exists(
                    element  # type: ignore[arg-type]
                ),
            )

        return tuple(colors)

    def _validate_stroke_or_fill_if_exists(
        self, element: ElementTree.Element
    ) -> Optional[Color]:
        for element_property in element.keys():
            return self._get_color_if_is_color_property(
                element_property, element.get(element_property, "")
            )

        return None

    def _get_color_if_is_color_property(
        self, property_name: str, property_value: str
    ) -> Optional[Color]:
        if self._is_color_property(property_name):
            return self._get_color_if_possible(property_value.lower())

        return None

    @staticmethod
    def _is_color_property(property_name: str) -> bool:
        return property_name in ["fill", "stroke"]

    def _get_color_if_possible(self, color_value: str) -> Optional[Color]:
        for factory in filter(
            lambda factory: factory.match_pattern(color_value),
            self._iter_color_factories(),
        ):
            return factory().read(color_value)

        return None

    def _iter_color_factories(
        self,
    ) -> Iterator[Type[StringReadingStrategy]]:
        yield CSSColorNameReading
        yield HexcodeSVGReading
        yield RGBSVGReading
        yield PercentageRGBReading
        yield RGBAReading
        yield PercentageRGBAReading
        yield HSLSVGReading
        yield HSLAReading
