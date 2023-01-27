from harmony.core.models import RGB, Color
from harmony.core.service_layer.plain_text_readings import HexcodeReading


class TestHexcodeReading:
    """Tests for the hexcode lines reading strategy"""

    def test_reading_hexcode_without_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_hexcode_without_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_without_description(result)

    def _given_hexcode_without_description(self) -> str:
        return "#6690ce"

    def _then_should_get_color_without_description(self, result: Color) -> None:
        assert result.hexcode == "#6690ce"
        assert result.rgb == RGB(red=102, green=144, blue=206)
        assert result.description == ""

    def test_reading_hexcode_with_description(self) -> None:
        """Test reading a valid raw string without description"""
        arrangement = self._given_hexcode_with_description()
        result = self._when_read(arrangement)
        self._then_should_get_color_with_description(result)

    def _given_hexcode_with_description(self) -> str:
        return "#6690ce Danube"

    def _then_should_get_color_with_description(self, result: Color) -> None:
        assert result.hexcode == "#6690ce"
        assert result.rgb == RGB(red=102, green=144, blue=206)
        assert result.description == "Danube"

    def _when_read(self, arrangement: str) -> Color:
        return HexcodeReading().read(arrangement)
