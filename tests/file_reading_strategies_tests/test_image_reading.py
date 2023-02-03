import logging
import shutil
import tempfile
from pathlib import Path
from typing import List, Tuple

from harmony.core.constants import ColorFormat
from harmony.core.models import HSL, RGB, Color
from harmony.from_image_reading.services import ImageFileReading
from tests.helpers import TestResourceUtils


class TestImageReading:
    """Tests for the image file reading strategy"""

    def test_extract_from_image(self) -> None:
        """Test extracting colors from image"""
        temporary_directory_path = Path(tempfile.mkdtemp())

        try:
            arrangement = self._get_image(temporary_directory_path)
            result = self._when_image_is_passed(arrangement)
            self._then_should_extract_colors_from_image(list(result))

        finally:
            shutil.rmtree(temporary_directory_path)

    def _get_image(self, temporary_directory_path: Path) -> Path:
        self._get_image_copy_path(temporary_directory_path).write_bytes(
            self._get_test_image_path().read_bytes()
        )
        logging.debug(self._get_test_image_path().read_bytes())

        return self._get_image_copy_path(temporary_directory_path)

    def _get_image_copy_path(self, directory_path: Path) -> Path:
        return directory_path.joinpath(self._get_test_image_path().name)

    @staticmethod
    def _get_test_image_path() -> Path:
        return Path(TestResourceUtils.get_resource("image-for-reading.jpg"))

    def _when_image_is_passed(self, arrangement: Path) -> Tuple[Color, ...]:
        return ImageFileReading().read(arrangement)

    def _then_should_extract_colors_from_image(self, result: List[Color]) -> None:
        for color in self._get_colors_expected_in_image():
            assert color in result

    @staticmethod
    def _get_colors_expected_in_image() -> List[Color]:
        return [
            Color(
                rgb=RGB(red=4, green=86, blue=168),
                hsl=HSL(
                    hue=210,
                    saturation=0.97,
                    luminosity=0.33,
                ),
                hexcode="0456a8",
                original_format=ColorFormat.RGB,
                description="Cobalt",
            ),
            Color(
                rgb=RGB(red=24, green=103, blue=160),
                hsl=HSL(hue=205, saturation=0.85, luminosity=0.36),
                hexcode="1867a0",
                original_format=ColorFormat.RGB,
                description="Denim",
            ),
            Color(
                rgb=RGB(red=43, green=99, blue=150),
                hsl=HSL(
                    hue=208,
                    saturation=0.71,
                    luminosity=0.37,
                ),
                hexcode="2b6396",
                original_format=ColorFormat.RGB,
                description="Endeavour",
            ),
        ]
