import logging
import multiprocessing
from math import sqrt
from typing import IO, List, Tuple

from PIL import Image

from harmony.core.constants import ColorFormat
from harmony.core.interfaces import FileReadingStrategy
from harmony.core.models import RGB, Color
from harmony.core.service_layer.converters import RGBToHSLConverter
from harmony.core.utils import HexcodeUtils, extract_unique_values_from_iterable
from harmony.data_access.store import ColorNamesStorage


class ImageFileReading(FileReadingStrategy):
    """Extract a set of colors from an image file"""

    MAXIMUM_PIXELS = 256

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def read(self, file: IO) -> Tuple[Color, ...]:
        image = self._get_image_from_file(file)

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            colors: List[Color] = pool.map(
                self._get_color_from_pixel_tuple,
                self._get_list_of_arguments(image),
                20,
            )

        return tuple(extract_unique_values_from_iterable(colors))

    def _get_list_of_arguments(
        self, image: Image.Image
    ) -> List[Tuple[Image.Image, int, int]]:
        arguments: List[Tuple[Image.Image, int, int]] = []

        for x_coordinate in range(image.size[0]):
            arguments.extend(self._get_list_of_arguments_for_x(image, x_coordinate))

        return arguments

    def _get_list_of_arguments_for_x(
        self, image: Image.Image, x_coordinate: int
    ) -> List[Tuple[Image.Image, int, int]]:
        arguments: List[Tuple[Image.Image, int, int]] = []

        for y_coordinate in range(image.size[1]):
            arguments.append((image, x_coordinate, y_coordinate))

        return arguments

    def _get_color_from_pixel_tuple(self, data: tuple):
        return self._get_color_from_pixel(data[0], data[1], data[2])

    def _get_color_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> Color:
        return Color(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate),
            self._get_hexcode_from_pixel(image, x_coordinate, y_coordinate),
            ColorFormat.RGB,
            self._generate_color_name_from_pixel(image, x_coordinate, y_coordinate),
        )

    def _get_hexcode_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> str:
        return HexcodeUtils.get_hexcode_from_rgb(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate)
        )

    def _generate_color_name_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> str:
        return self._generate_color_name(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate)
        )

    def _get_rgb_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> RGB:
        return RGB(
            self._get_red_from_pixel(image, x_coordinate, y_coordinate),
            self._get_green_from_pixel(image, x_coordinate, y_coordinate),
            self._get_blue_from_pixel(image, x_coordinate, y_coordinate),
        )

    def _get_red_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> int:
        return image.getpixel((x_coordinate, y_coordinate))[0]

    def _get_green_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> int:
        return image.getpixel((x_coordinate, y_coordinate))[1]

    def _get_blue_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> int:
        return image.getpixel((x_coordinate, y_coordinate))[2]

    def _generate_color_name(self, rgb_values: RGB):
        with ColorNamesStorage() as storage:
            return storage.get_color_name_by_hsl(
                RGBToHSLConverter().make_hsl_from_rgb(rgb_values)
            )

    def _get_image_from_file(self, file: IO) -> Image.Image:
        return Image.open(file).resize(self._get_size_to_resize(), Image.NEAREST)

    def _get_size_to_resize(self):
        return (self._image_side_length(),) * 2

    def _image_side_length(self) -> int:
        return int(sqrt(self.MAXIMUM_PIXELS))
