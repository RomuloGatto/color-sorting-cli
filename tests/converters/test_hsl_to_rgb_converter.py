from typing import Callable

import pytest

from harmony.core.exceptions import InvalidColorFormatException
from harmony.core.models import HSL, RGB
from harmony.core.service_layer.converters import HSLToRGBConverter


class TestHSLToRGBConverter:
    """Tests fot the HSL to RGB converter"""

    def test_converting_hsl(self) -> None:
        """Test converting a HSL object to a RGB object"""
        arrangement = self._given_hsl()
        result = self._when_converted(arrangement)
        self._then_should_get_rgb(result)

    def _given_hsl(self) -> HSL:
        return HSL(136, 0.54, 0.43)

    def _then_should_get_rgb(self, result: RGB) -> None:
        assert result == RGB(50, 169, 82)

    def test_invalid_hue(self) -> None:
        """Test converting an invalid HSL object"""
        arrangement = self._given_invalid_hsl()

        def result() -> None:
            self._when_converted(arrangement)

        self._then_should_raise_invalid_format(result)

    def _given_invalid_hsl(self) -> HSL:
        return HSL(361, 0.54, 0.43)

    def _then_should_raise_invalid_format(self, result: Callable[[], None]) -> None:
        with pytest.raises(InvalidColorFormatException):
            result()

    def _when_converted(self, arrangement: HSL) -> RGB:
        return HSLToRGBConverter().convert(arrangement)
