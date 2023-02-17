from typing import Iterable, List, Sized, Tuple

from PIL import Image, ImageDraw

from harmony import core
from harmony.core import interfaces


class PNGWritting(interfaces.WritingStrategy):
    """Writing strategy that write a PNG file with the visual representation of the
    passed colors"""

    EXTENSION = "png"
    IMAGE_MODE = core.ImageModesForPIL.RGB_MODE
    IMAGE_WIDTH = 640
    COLOR_SLICE_HEIGHT = 100

    def write(self, colors: Tuple[core.Color, ...], final_file_path: str):
        palette = Image.new(
            self.IMAGE_MODE, (self.IMAGE_WIDTH, self._get_image_height(colors)), None
        )
        self._draw_color_palette(colors, palette)
        palette.save(final_file_path)

    def _draw_color_palette(
        self, colors: Iterable[core.Color], raw_palette: Image.Image
    ) -> None:
        for color_counter, color in enumerate(colors):
            self._get_drawer(raw_palette).rectangle(
                self._get_slice_starting_and_ending(color_counter),
                f"rgb({color.rgb_red},{color.rgb_green},{color.rgb_blue})",
            )

    def _get_drawer(self, raw_palette: Image.Image) -> ImageDraw.ImageDraw:
        return ImageDraw.Draw(raw_palette)

    def _get_image_height(self, colors: Sized) -> int:
        return len(colors) * self.COLOR_SLICE_HEIGHT

    def _get_slice_starting_and_ending(self, counter: int) -> List[Tuple[int, int]]:
        return [
            self._get_slice_starting_coordinate(counter),
            self._get_slice_ending_coordinate(counter),
        ]

    def _get_slice_starting_coordinate(self, counter: int) -> Tuple[int, int]:
        return (
            self._get_starting_x(),
            self._get_slice_starting_y(counter),
        )

    def _get_slice_ending_coordinate(self, counter: int) -> Tuple[int, int]:
        return (
            self.IMAGE_WIDTH,
            self._get_slice_starting_y(counter) + self.COLOR_SLICE_HEIGHT,
        )

    def _get_slice_starting_y(self, counter: int) -> int:
        return counter * self.COLOR_SLICE_HEIGHT

    @staticmethod
    def _get_starting_x() -> int:
        return 0
