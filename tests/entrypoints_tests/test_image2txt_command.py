import shutil
import tempfile
from pathlib import Path

import pytest
from click.testing import Result
from typer.testing import CliRunner

from harmony.harmony.main import app
from tests.helpers import TestResourceUtils


class TestImage2TextCommand:
    """Tests for the "image2txt" command"""

    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    def test_passing_file(self, runner: CliRunner) -> None:
        """Test passing valid file to CLI"""
        temporary_directory_path = Path(tempfile.mkdtemp())

        try:
            arrangement = self._get_image(temporary_directory_path)
            results = self._when_file_is_sent(runner, str(arrangement))
            self._then_should_show_success_message(results)

        finally:
            shutil.rmtree(temporary_directory_path)

    def _get_image(self, temporary_directory_path: Path) -> Path:
        self._get_image_copy_path(temporary_directory_path).write_bytes(
            self._get_test_image_path().read_bytes()
        )

        return self._get_image_copy_path(temporary_directory_path)

    def _get_image_copy_path(self, directory_path: Path) -> Path:
        return directory_path.joinpath(self._get_test_image_path().name)

    @staticmethod
    def _get_test_image_path() -> Path:
        return Path(TestResourceUtils.get_resource("image-for-reading.jpg"))

    def test_passing_directory(self, runner: CliRunner) -> None:
        """Test passing valid directory to CLI"""
        temporary_directory_path = Path(tempfile.mkdtemp())

        try:
            self._get_image(temporary_directory_path)
            results = self._when_file_is_sent(runner, str(temporary_directory_path))
            self._then_should_show_success_message(results)

        finally:
            shutil.rmtree(temporary_directory_path)

    def _then_should_show_success_message(self, results: Result):
        expected_exit_code = 0
        actual_exit_code = results.exit_code

        expected_message = "Colors extracted and saved to "
        actual_message = results.stdout

        assert expected_exit_code == actual_exit_code
        assert expected_message in actual_message

    def test_passing_invalid_file(self, runner: CliRunner):
        """Test passing invalid file to CLI"""
        arrangements = "not-a-file"
        results = self._when_file_is_sent(runner, arrangements)
        self._then_should_show_error_message(results, arrangements)

    def _when_file_is_sent(self, runner: CliRunner, arrangements: str) -> Result:
        return runner.invoke(app, ["image2txt", str(arrangements)])

    def _then_should_show_error_message(self, results: Result, source_file: str):
        expected_exit_code = 2
        actual_exit_code = results.exit_code

        assert expected_exit_code == actual_exit_code
