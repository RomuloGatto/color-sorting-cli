from typing import Callable

import pytest

from harmony import core, core_services
from harmony.core import exceptions


class TestHSLReading:
    """Tests for the HSL text reading strategy"""

    def test_reading_hsl_without_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_hsl_without_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_without_description(result)

    def _given_hsl_without_description(self) -> str:
        return "HSL(102, 44%, 6%)"

    def _then_should_get_color_without_description(self, result: core.Color) -> None:
        assert result.hexcode == "#0d1609"
        assert result.rgb == core.RGB(red=13, green=22, blue=9)
        assert result.hsl == core.HSL(hue=102, saturation=0.44, luminosity=0.06)
        assert result.description == ""

    def test_reading_hsl_with_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_hsl_with_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_with_description(result)

    def _given_hsl_with_description(self) -> str:
        return "hsl(102, 44%, 6%) Danube"

    def _then_should_get_color_with_description(self, result: core.Color) -> None:
        assert result.hexcode == "#0d1609"
        assert result.hsl == core.HSL(hue=102, saturation=0.44, luminosity=0.06)
        assert result.description == "Danube"

    def test_reading_invalid_hsl(self) -> None:
        """Test reading a RGB raw string with component value bigger out of the 0-255
        range"""
        arrangement = self._given_invalid_hsl()

        def result() -> None:
            self._when_read(arrangement)

        self._then_should_raise_invalid_regex(result)

    def _given_invalid_hsl(self) -> str:
        return "hsl(722, 323%, -23%)"

    def _then_should_raise_invalid_regex(self, result: Callable[[], None]) -> None:
        with pytest.raises(exceptions.InvalidRegexException):
            result()

    def _when_read(self, arrangement: str) -> core.Color:
        return core_services.HSLTextReading().do_read(arrangement)
