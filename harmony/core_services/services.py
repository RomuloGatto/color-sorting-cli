import logging
from pathlib import Path
from typing import Any, Dict, Tuple

from harmony import core
from harmony.core import interfaces


class PathGenerator:
    """Provide methods for generating"""

    def __init__(self, suffix: str):
        self._suffix = suffix

    def get_sorted_file_path(
        self,
        source_file: Path,
        sorting_strategy: core.SortingStrategyName,
    ) -> str:
        """Return the path to the file with the processed data

        Args:
            source_file (TextIO): original file

        Returns:
            str: path to the processed data file
        """
        if core.does_file_name_have_extension(str(source_file)):
            self._log_sorted_path_generated_with_extension(
                source_file, sorting_strategy
            )
            return self._get_path_with_suffix_strategy_and_extension(
                source_file, sorting_strategy
            )

        self._log_sorted_path_generated_without_extension(source_file, sorting_strategy)
        return self._get_path_with_strategy_and_suffix(source_file, sorting_strategy)

    def get_path_with_extension(self, file_path: Path, extension: str) -> str:
        """Return the path to file with the given extension

        Args:
            source_file (TextIO): original file

        Returns:
            str: path to the converted file
        """
        if core.does_file_name_have_extension(str(file_path)):
            self._log_changed_extension(file_path, extension)
            return self._get_path_with_changed_extension(file_path, extension)

        self._log_added_extension(file_path, extension)
        return self._get_path_with_added_extension(file_path, extension)

    def _log_sorted_path_generated_with_extension(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> None:
        return self._logger.info(
            "sorted file path generated is %(final_path)s",
            self._get_sorted_path_with_extension_log_data(
                source_file, sorting_strategy
            ),
        )

    def _get_sorted_path_with_extension_log_data(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> Dict[str, Any]:
        return {
            "final_path": self._get_path_with_suffix_strategy_and_extension(
                source_file, sorting_strategy
            )
        }

    def _log_sorted_path_generated_without_extension(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> None:
        return self._logger.info(
            "sorted file path generated is %(final_path)s",
            self._get_sorted_path_without_extension_log_data(
                source_file, sorting_strategy
            ),
        )

    def _get_sorted_path_without_extension_log_data(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> Dict[str, Any]:
        return {
            "final_path": self._get_path_with_strategy_and_suffix(
                source_file, sorting_strategy
            )
        }

    def _get_path_with_suffix_strategy_and_extension(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> str:
        return (
            f"{core.extract_extension_from_file_path(str(source_file))}"
            + f"_{sorting_strategy}{self._suffix}"
            + f"{core.get_extension_from_file_path(str(source_file))}"
        )

    def _get_path_with_strategy_and_suffix(
        self, source_file: Path, sorting_strategy: core.SortingStrategyName
    ) -> str:
        return f"{str(source_file)}_{sorting_strategy}{self._suffix}"

    def _log_changed_extension(self, file_path: Path, extension: str) -> None:
        self._logger.info(
            "Path with extension changed to the passed one %(final_path)s",
            self._get_path_with_changed_extension_log_data(file_path, extension),
        )

    def _get_path_with_changed_extension_log_data(
        self, file_path: Path, extension: str
    ) -> Dict[str, str]:
        return {
            "final_path": self._get_path_with_changed_extension(file_path, extension)
        }

    def _log_added_extension(self, file_path: Path, extension: str) -> None:
        self._logger.info(
            "Path with passed extension added %(final_path)s",
            self._get_path_with_added_extension_log_data(file_path, extension),
        )

    def _get_path_with_added_extension_log_data(
        self, file_path: Path, extension: str
    ) -> Dict[str, str]:
        return {"final_path": self._get_path_with_added_extension(file_path, extension)}

    def _get_path_with_changed_extension(self, file_path: Path, extension: str) -> str:
        return (
            f"{core.extract_extension_from_file_path(str(file_path))}{self._suffix}."
            + extension
        )

    def _get_path_with_added_extension(self, file_path: Path, extension: str) -> str:
        return f"{str(file_path)}{self._suffix}.{extension}"

    @property
    def _logger(self) -> logging.Logger:
        return logging.getLogger(self.__class__.__name__)


class ColorWriter:
    """Service for writing colors to file"""

    def __init__(self, strategy: interfaces.WritingStrategy):
        self._strategy = strategy

    def write(self, colors: Tuple[core.Color, ...], final_file_path: str):
        """Write colors to passed file

        Args:
            colors (Tuple[Color, ...]): colors to be written
            final_file_path (str): path to the file where the colors will be passed
        """

        self._strategy.write(colors, final_file_path)
