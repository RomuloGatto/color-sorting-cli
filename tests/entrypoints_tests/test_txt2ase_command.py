import os

import pytest
from click.testing import Result
from typer.testing import CliRunner

from harmony.harmony.main import app
from tests.helpers import get_temporary_file_path


class TestTXT2ASECommand:
    """Tests for the "txt2ase" command"""

    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    def test_passing_file(self, runner: CliRunner) -> None:
        """Test passing valid file to CLI"""
        arrangements = self._given_valid_file()

        try:
            results = self._when_file_is_sent(runner, arrangements)
            self._then_should_show_success_message(results)

        finally:
            os.remove(arrangements)

    def _given_valid_file(self) -> str:
        return get_temporary_file_path()

    def _then_should_show_success_message(self, results: Result):
        expected_exit_code = 0
        actual_exit_code = results.exit_code

        expected_message = "File converted and saved to "
        actual_message = results.stdout

        assert expected_exit_code == actual_exit_code
        assert expected_message in actual_message

    def test_passing_invalid_file(self, runner: CliRunner):
        """Test passing invalid file to CLI"""
        arrangements = "not-a-file"
        results = self._when_file_is_sent(runner, arrangements)
        self._then_should_show_error_message(results, arrangements)

    def _when_file_is_sent(self, runner: CliRunner, arrangements: str) -> Result:
        return runner.invoke(app, ["txt2ase", arrangements])

    def _then_should_show_error_message(self, results: Result, source_file: str):
        expected_exit_code = 2
        actual_exit_code = results.exit_code

        assert expected_exit_code == actual_exit_code
