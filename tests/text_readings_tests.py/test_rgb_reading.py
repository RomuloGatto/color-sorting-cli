from typing import Callable

import pytest

from harmony import core, core_services
from harmony.core import exceptions


class TestRGBReading:
    """Tests for the hexcode lines reading strategy"""

    def test_reading_rgb_without_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_rgb_without_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_without_description(result)

    def _given_rgb_without_description(self) -> str:
        return "RGB(102,144,206)"

    def _then_should_get_color_without_description(self, result: core.Color) -> None:
        assert result.hexcode == "#6690ce"
        assert result.rgb == core.RGB(red=102, green=144, blue=206)
        assert result.description == ""

    def test_reading_rgb_with_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_rgb_with_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_with_description(result)

    def _given_rgb_with_description(self) -> str:
        return "rgb(102,144,206) Danube"

    def _then_should_get_color_with_description(self, result: core.Color) -> None:
        assert result.hexcode == "#6690ce"
        assert result.rgb == core.RGB(red=102, green=144, blue=206)
        assert result.description == "Danube"

    def test_reading_invalid_rgb(self) -> None:
        """Test reading a RGB raw string with component value bigger out of the 0-255
        range"""
        arrangement = self._given_invalid_rgb()

        def result() -> None:
            self._when_read(arrangement)

        self._then_should_raise_invalid_regex(result)

    def _given_invalid_rgb(self) -> str:
        return "rgb(722,323,-23)"

    def _then_should_raise_invalid_regex(self, result: Callable[[], None]) -> None:
        with pytest.raises(exceptions.InvalidRegexException):
            result()

    def _when_read(self, arrangement: str) -> core.Color:
        return core_services.RGBTextReading().do_read(arrangement)
