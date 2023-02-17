from typing import Callable

import pytest

from harmony import convertions, core
from harmony.core import exceptions


class TestHSLToRGBConverter:
    """Tests fot the HSL to RGB converter"""

    def test_converting_hsl(self) -> None:
        """Test converting a HSL object to a RGB object"""
        arrangement = self._given_hsl()
        result = self._when_converted(arrangement)
        self._then_should_get_rgb(result)

    def _given_hsl(self) -> core.HSL:
        return core.HSL(136, 0.54, 0.43)

    def _then_should_get_rgb(self, result: core.RGB) -> None:
        assert result == core.RGB(50, 169, 82)

    def test_invalid_hue(self) -> None:
        """Test converting an invalid HSL object"""
        arrangement = self._given_invalid_hsl()

        def result() -> None:
            self._when_converted(arrangement)

        self._then_should_raise_invalid_format(result)

    def _given_invalid_hsl(self) -> core.HSL:
        return core.HSL(361, 0.54, 0.43)

    def _then_should_raise_invalid_format(self, result: Callable[[], None]) -> None:
        with pytest.raises(exceptions.InvalidColorFormatException):
            result()

    def _when_converted(self, arrangement: core.HSL) -> core.RGB:
        return convertions.HSLToRGBConverter().convert(arrangement)
