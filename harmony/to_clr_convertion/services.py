import logging
from typing import Any, Dict, List, Tuple

from harmony.core.constants import MAXIMUM_8_BIT_UNSIGNED_INTEGER_VALUE, ByteOrder
from harmony.core.exceptions import InvalidFileException
from harmony.core.interfaces import WritingStrategy
from harmony.core.models import RGB, Color
from harmony.core.utils import BytesUtils
from harmony.to_clr_convertion.constants import CLRSpecialBytes
from harmony.to_clr_convertion.utils import (
    is_8_bit_signed_integer,
    is_clr_color_component_near_one,
    is_clr_color_component_near_zero,
    is_clr_color_count_valid,
)


class CLRWriting(WritingStrategy):
    """Writting strategy that results into an ".clr" file"""

    EXTENSION = "clr"
    BYTE_ORDER = ByteOrder.LITTLE

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def write(self, colors: Tuple[Color, ...], final_file_path: str):
        """Write colors to a ".clr" file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed

        Raises:
            InvalidCLRFileException: when a CLR file is tried to be written with less
            then 1 color
        """
        with open(final_file_path, "wb") as final_file:
            final_file.write(self._get_file_content(colors))

    def _get_file_content(self, colors: Tuple[Color, ...]) -> bytes:
        file_content = bytearray()

        for item in self._get_bytes_to_add_to_the_file(colors):
            file_content.extend(item)

        return file_content

    def _get_bytes_to_add_to_the_file(
        self, colors: Tuple[Color, ...]
    ) -> Tuple[bytes, ...]:
        colors_list = list(colors)
        first_color_bytes = self._get_first_color_bytes(colors_list.pop(0))

        return (
            CLRSpecialBytes.get_file_start(),
            self._get_color_count_chunk_from_collection(colors),
            first_color_bytes,
            self._get_colors_bytes(colors_list),
        )

    def _get_color_count_chunk_from_collection(
        self, colors: Tuple[Color, ...]
    ) -> bytes:
        return self._get_color_count_chunk(len(colors))

    def _get_color_count_chunk(self, color_count: int) -> bytearray:
        if is_clr_color_count_valid(color_count):
            color_chunk = bytearray(CLRSpecialBytes.COLOR_COUNT_CHUNK_START)
            color_chunk.extend(self._get_color_count_bytes(color_count))

            return color_chunk

        raise InvalidFileException(
            f"CLR files must have at least one color, but {color_count} was passed"
        )

    def _get_color_count_bytes(self, color_count: int) -> bytearray:
        if is_8_bit_signed_integer(color_count):
            return bytearray(color_count.to_bytes(1, "little"))

        color_count_data_bytes = bytearray(CLRSpecialBytes.INTEGER_16_BYTE)
        color_count_data_bytes.extend(color_count.to_bytes(2, "little"))

        return color_count_data_bytes

    def _declare_map_value_type(self) -> bytearray:
        map_value_type_bytes = bytearray(self._declare_class(b"NSColor"))
        map_value_type_bytes.extend(CLRSpecialBytes.NULL_BYTE)
        map_value_type_bytes.extend(CLRSpecialBytes.INHERITANCE_DECLARATION_BYTES)
        map_value_type_bytes.extend(CLRSpecialBytes.NSOBJECT_CLASS_NAME_COUNT)
        map_value_type_bytes.extend(CLRSpecialBytes.NSOBJECT_CLASS_NAME)
        map_value_type_bytes.extend(CLRSpecialBytes.NULL_BYTE)

        return map_value_type_bytes

    def _get_first_color_bytes(self, first_color: Color) -> bytearray:
        first_color_bytes = bytearray(CLRSpecialBytes.NEW_COLOR_MAP)
        first_color_bytes.extend(self._declare_map_value_type())
        first_color_bytes.extend(CLRSpecialBytes.COLORS_COMPONENTS_CHUNK_START)
        first_color_bytes.extend(self._convert_rgb_to_bytes(first_color.rgb))
        first_color_bytes.extend(self._declare_map_keys_type())
        first_color_bytes.extend(CLRSpecialBytes.COLORS_NAMES_CHUNK_START)
        first_color_bytes.extend(
            self._convert_color_name_to_bytes(first_color.description)
        )

        return first_color_bytes

    def _declare_map_keys_type(self) -> bytearray:
        return self._declare_class(CLRSpecialBytes.NSSTRING_TYPE_NAME)

    def _declare_class(self, class_name: bytes) -> bytearray:
        class_declaration_bytes = bytearray(CLRSpecialBytes.CLASS_DECLARATION_BYTES)
        class_declaration_bytes.extend(len(class_name).to_bytes(1, "little"))
        class_declaration_bytes.extend(class_name)

        return class_declaration_bytes

    def _get_colors_bytes(self, colors: List[Color]) -> bytearray:
        colors_chunk_bytes = bytearray()

        for color in colors:
            colors_chunk_bytes.extend(CLRSpecialBytes.COLOR_ITEM_START)
            colors_chunk_bytes.extend(self._convert_rgb_to_bytes(color.rgb))
            colors_chunk_bytes.extend(CLRSpecialBytes.COLOR_DESCRIPTION_START)
            colors_chunk_bytes.extend(
                self._convert_color_name_to_bytes(color.description)
            )

        return colors_chunk_bytes

    def _convert_rgb_to_bytes(self, rgb: RGB) -> bytearray:
        rgba_bytes = bytearray(self._get_color_component_bytes(rgb.red_as_percentage))
        rgba_bytes.extend(self._get_color_component_bytes(rgb.green_as_percentage))
        rgba_bytes.extend(self._get_color_component_bytes(rgb.blue_as_percentage))
        rgba_bytes.extend(self._get_alpha_bytes())
        rgba_bytes.extend(CLRSpecialBytes.END_OF_DATA_BYTE)

        self._logger.info(
            "RGB components %(rgb)s converted to %(rgba_bytes)s",
            self._get_rgb_converted_log_data(rgb, rgba_bytes),
        )

        return rgba_bytes

    @staticmethod
    def _get_rgb_converted_log_data(rgb: RGB, rgba_bytes: bytes) -> Dict[str, Any]:
        return {
            "rgb": str(rgb),
            "rgba_bytes": rgba_bytes,
        }

    @staticmethod
    def _get_alpha_bytes() -> bytes:
        return CLRSpecialBytes.MAXIMUM_COMPONENT_VALUE

    def _get_color_component_bytes(self, component_as_decimal: float) -> bytes:
        if is_clr_color_component_near_one(component_as_decimal):
            return CLRSpecialBytes.MAXIMUM_COMPONENT_VALUE

        return self._calculate_color_component_if_not_one(component_as_decimal)

    def _calculate_color_component_if_not_one(
        self, component_as_decimal: float
    ) -> bytes:
        if is_clr_color_component_near_zero(component_as_decimal):
            return CLRSpecialBytes.MINIMUM_COMPONENT_VALUE

        component_bytes = bytearray(CLRSpecialBytes.FLOAT_BYTE)
        component_bytes.extend(
            BytesUtils.float_to_bytes(component_as_decimal, self.BYTE_ORDER)
        )

        return component_bytes

    def _convert_color_name_to_bytes(self, name: str) -> bytearray:
        color_name_bytes = bytes(name, encoding="utf8")

        if self._is_color_name_bigger_than_allowed(name):
            color_name_bytes = color_name_bytes[: self._get_last_char_allowed_index()]

        color_name_chunk_bytes = bytearray(len(color_name_bytes).to_bytes(1, "little"))
        color_name_chunk_bytes.extend(color_name_bytes)
        color_name_chunk_bytes.extend(CLRSpecialBytes.END_OF_DATA_BYTE)

        return color_name_chunk_bytes

    @staticmethod
    def _is_color_name_bigger_than_allowed(name):
        return len(bytes(name, encoding="utf8")) > MAXIMUM_8_BIT_UNSIGNED_INTEGER_VALUE

    @staticmethod
    def _get_last_char_allowed_index() -> int:
        return MAXIMUM_8_BIT_UNSIGNED_INTEGER_VALUE + 1
