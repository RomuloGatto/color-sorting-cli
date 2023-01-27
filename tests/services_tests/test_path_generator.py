from dataclasses import dataclass
from pathlib import Path

from harmony.color_sorting.constants import SortingStrategyName
from harmony.core.service_layer.services import PathGenerator


class PathGenerationArrangement:
    suffix: str


@dataclass
class SortedFileArrangement:
    suffix: str
    source_file: Path
    sorting_strategy: SortingStrategyName


@dataclass
class ChangeExtensionArrangement:
    suffix: str
    source_file: Path
    extension: str


class TestPathGenerator:
    """Tests for the file path generator"""

    def test_getting_sorted_file_path_with_extension(self) -> None:
        """Test getting file path to color sorting output file"""
        arrangement = self._given_file_path_with_extension()
        result = self._when_passed_sorting_parameters(arrangement)
        self._then_should_generate_path_with_extension(result)

    def _given_file_path_with_extension(self) -> SortedFileArrangement:
        return SortedFileArrangement(
            "_test", self._get_path_with_extension(), SortingStrategyName.HILLBERT
        )

    def _then_should_generate_path_with_extension(self, result: str) -> None:
        assert f"{self._get_path_without_extension()}_hillbert_test.txt" == result

    def test_getting_sorted_file_path_without_extension(self) -> None:
        """Test getting file path to color sorting output file"""
        arrangement = self._given_file_path_without_extension()
        result = self._when_passed_sorting_parameters(arrangement)
        self._then_should_generate_path_without_extension(result)

    def _given_file_path_without_extension(self) -> SortedFileArrangement:
        return SortedFileArrangement(
            "_test", self._get_path_without_extension(), SortingStrategyName.HILLBERT
        )

    def _then_should_generate_path_without_extension(self, result: str) -> None:
        assert f"{self._get_path_without_extension()}_hillbert_test" == result

    def _when_passed_sorting_parameters(
        self, arrangement: SortedFileArrangement
    ) -> str:
        return PathGenerator(arrangement.suffix).get_sorted_file_path(
            arrangement.source_file, arrangement.sorting_strategy
        )

    def test_generating_path_changing_extension(self) -> None:
        """Test generating path changing the extension for the passed one"""
        arrangement = self._given_file_and_extension()
        result = self._when_generating_path_for_extension(arrangement)
        self._then_should_get_path_with_passed_extension(result)

    def _given_file_and_extension(self) -> ChangeExtensionArrangement:
        return ChangeExtensionArrangement(
            "_test", self._get_path_with_extension(), "ase"
        )

    def test_generating_path_adding_extension(self) -> None:
        """Test generating path adding the extension for the passed one"""
        arrangement = self._given_file_without_extension_and_extension()
        result = self._when_generating_path_for_extension(arrangement)
        self._then_should_get_path_with_passed_extension(result)

    def _given_file_without_extension_and_extension(self) -> ChangeExtensionArrangement:
        return ChangeExtensionArrangement(
            "_test", self._get_path_without_extension(), "ase"
        )

    def _when_generating_path_for_extension(
        self, arrangement: ChangeExtensionArrangement
    ) -> str:
        return PathGenerator(arrangement.suffix).get_path_with_extension(
            arrangement.source_file, arrangement.extension
        )

    def _then_should_get_path_with_passed_extension(self, result: str) -> None:
        assert f"{self._get_path_without_extension()}_test.ase" == result

    @staticmethod
    def _get_path_with_extension() -> Path:
        return Path("some_folder/some_file.txt")

    @staticmethod
    def _get_path_without_extension() -> Path:
        return Path("some_folder/some_file")
