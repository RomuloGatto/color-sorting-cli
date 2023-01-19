import logging
from typing import Any, Dict, Tuple

from harmony.core.models import HSL, ColorName


class ColorNamesStorageLogger:
    """Provide the methods for logging the color names storage activity"""

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger("ColorNamesStorage")

    def log_nearest_color_found(
        self, hsl: HSL, first_color_data_found: Tuple[str, ...]
    ) -> None:
        """Trigger log informing the closer color name found to the HSL values passed"""
        self._logger.info(
            self._get_log_nearest_color_found_message(),
            self._get_log_nearest_color_found_data(hsl, first_color_data_found),
        )

    @staticmethod
    def _get_log_nearest_color_found_message() -> str:
        return (
            "Found color %(name)s"
            + "(%(found_hue)d, %(found_saturation).2f, %(found_luminosity).2f) "
            + "for HSL(%(original_hue)d, %(original_saturation).2f, "
            + "%(original_luminosity).2f)"
        )

    def _get_log_nearest_color_found_data(
        self, hsl: HSL, first_color_data_found: Tuple[str, ...]
    ) -> Dict[str, Any]:
        return {
            "name": self._get_first_name_found(first_color_data_found),
            "found_hue": self._get_first_hue_found_as_int(first_color_data_found),
            "found_saturation": self._get_first_saturation_found_as_float(
                first_color_data_found
            ),
            "found_luminosity": self._get_first_luminosity_found_as_float(
                first_color_data_found
            ),
            "original_hue": hsl.hue,
            "original_saturation": hsl.saturation,
            "original_luminosity": hsl.luminosity,
        }

    def _get_first_name_found(self, first_color_data_found: Tuple[str, ...]) -> str:
        return first_color_data_found[self._get_name_index_in_row()]

    def _get_first_hue_found_as_int(
        self, first_color_data_found: Tuple[str, ...]
    ) -> int:
        return int(self._get_first_hue_found(first_color_data_found))

    def _get_first_hue_found(self, first_color_data_found: Tuple[str, ...]) -> str:
        return first_color_data_found[self._get_hue_index_in_row()]

    def _get_first_saturation_found_as_float(
        self, first_color_data_found: Tuple[str, ...]
    ) -> float:
        return float(self._get_first_saturation_found(first_color_data_found))

    def _get_first_saturation_found(
        self, first_color_data_found: Tuple[str, ...]
    ) -> str:
        return first_color_data_found[self._get_saturation_index_in_row()]

    def _get_first_luminosity_found_as_float(
        self, first_color_data_found: Tuple[str, ...]
    ) -> float:
        return float(self._get_first_luminosity_found(first_color_data_found))

    def _get_first_luminosity_found(
        self, first_color_data_found: Tuple[str, ...]
    ) -> str:
        return first_color_data_found[self._get_luminosity_index_in_row()]

    @staticmethod
    def _get_name_index_in_row() -> int:
        return 0

    @staticmethod
    def _get_hue_index_in_row() -> int:
        return 1

    @staticmethod
    def _get_saturation_index_in_row() -> int:
        return 2

    @staticmethod
    def _get_luminosity_index_in_row() -> int:
        return 3

    def warn_error_on_recording_name(
        self, color_name_data: ColorName, exception: BaseException
    ) -> None:
        """Trigger log warning an error occurred while color name was being store in
        database"""
        self._logger.warning(
            "Error on recording name %(color_name)s: %(exception)s",
            {"color_name": color_name_data.name, "exception": str(exception)},
        )

    def log_color_name_stored(self, color_name_data: ColorName) -> None:
        """Trigger log informing the color name was stored in database"""
        self._logger.info(
            "%(name)s (%(hue)d, %(saturation).2f, %(luminosity).2f) stored",
            {
                "name": color_name_data.name,
                "hue": color_name_data.hsl.hue,
                "saturation": color_name_data.hsl.saturation,
                "luminosity": color_name_data.hsl.luminosity,
            },
        )
