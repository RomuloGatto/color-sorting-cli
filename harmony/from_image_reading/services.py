import logging
import multiprocessing
from math import sqrt
from pathlib import Path
from typing import List, Tuple

from PIL import Image

from harmony import convertions, core, data_access
from harmony.core import interfaces


class ImageFileReading(interfaces.FileReadingStrategy):
    """Extract a set of colors from an image file"""

    MAXIMUM_PIXELS = 256

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def read(self, file_path: Path) -> Tuple[core.Color, ...]:
        image = self._get_image_from_file(file_path)

        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            colors: List[core.Color] = pool.map(
                self._get_color_from_pixel_tuple,
                self._get_list_of_arguments(image),
                20,
            )

        return tuple(core.extract_unique_values_from_iterable(colors))

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
    ) -> core.Color:
        return core.Color(
            rgb=self._get_rgb_from_pixel(image, x_coordinate, y_coordinate),
            hsl=self._get_hsl_from_pixel(image, x_coordinate, y_coordinate),
            hexcode=self._get_hexcode_from_pixel(image, x_coordinate, y_coordinate),
            original_format=core.ColorFormat.RGB,
            description=self._generate_color_name_from_pixel(
                image, x_coordinate, y_coordinate
            ),
        )

    def _get_hexcode_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> str:
        return core.HexcodeUtils.get_hexcode_from_rgb(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate)
        )

    def _generate_color_name_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> str:
        return self._generate_color_name(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate)
        )

    def _get_hsl_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> core.HSL:
        return convertions.RGBToHSLConverter().convert(
            self._get_rgb_from_pixel(image, x_coordinate, y_coordinate)
        )

    def _get_rgb_from_pixel(
        self, image: Image.Image, x_coordinate: int, y_coordinate: int
    ) -> core.RGB:
        return core.RGB(
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

    def _generate_color_name(self, rgb_values: core.RGB):
        return data_access.ColorNamesStorage().get_color_name_by_hsl(
            convertions.RGBToHSLConverter().convert(rgb_values)
        )

    def _get_image_from_file(self, file_path: Path) -> Image.Image:
        Image.MAX_IMAGE_PIXELS = None
        return Image.open(file_path).resize(self._get_size_to_resize(), Image.NEAREST)

    def _get_size_to_resize(self):
        return (self._image_side_length(),) * 2

    def _image_side_length(self) -> int:
        return int(sqrt(self.MAXIMUM_PIXELS))
