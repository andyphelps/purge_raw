import os
import tempfile

import pytest  # type: ignore
import purgeraw.main

from unittest.mock import patch, Mock
from click.testing import CliRunner, Result
from contextlib import contextmanager
from typing import Generator, Optional

from purgeraw.file_service import delete, fake_delete


class TestMain:

    @contextmanager
    def make_test_dir(self) -> Generator[str, None, None]:
        tempdir: Optional[str] = None
        try:
            tempdir = tempfile.mkdtemp("_purgeraw")
            yield tempdir
        finally:
            if tempdir is not None:
                os.rmdir(tempdir)

    @pytest.fixture
    def runner(self) -> CliRunner:
        return CliRunner()

    def test_when_missing_input_dir_then_fails(self, runner: CliRunner) -> None:
        result: Result = runner.invoke(purgeraw.main.main, [])

        assert result.exit_code == 2
        assert "Error: Missing option '-i' / '--input'." in result.output

    def test_when_input_dir_not_exists_then_fails(self, runner: CliRunner) -> None:
        result: Result = runner.invoke(purgeraw.main.main, ["-i", "/flibble1212"])

        assert result.exit_code == 2
        assert "Path '/flibble1212' does not exist." in result.output

    @patch("purgeraw.main.raw_determinator")
    @patch("purgeraw.main.directory_walker")
    @patch("purgeraw.main.purger")
    def test_when_input_dir_present_then_purge_called(self,
                                                      purger_mock: Mock,
                                                      walker_mock: Mock,
                                                      raw_determinator_mock: Mock,
                                                      runner: CliRunner) -> None:
        walk_mock: Mock = Mock()
        is_raw_mock: Mock = Mock()
        walker_mock.return_value = walk_mock
        raw_determinator_mock.return_value = is_raw_mock

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname])

            assert result.exit_code == 0

            assert walker_mock.call_args.args[0] == ["cr3", "jpg"]
            assert raw_determinator_mock.call_args.args == (("cr3",), ("jpg",))
            assert purger_mock.call_args.args == (walk_mock, delete, is_raw_mock)

    @patch("purgeraw.main.raw_determinator")
    @patch("purgeraw.main.directory_walker")
    @patch("purgeraw.main.purger")
    def test_when_input_dir_present_with_dry_run_then_purge_called(self,
                                                                   purger_mock: Mock,
                                                                   walker_mock: Mock,
                                                                   raw_determinator_mock: Mock,
                                                                   runner: CliRunner) -> None:
        walk_mock: Mock = Mock()
        is_raw_mock: Mock = Mock()
        walker_mock.return_value = walk_mock
        raw_determinator_mock.return_value = is_raw_mock

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-d"])

            assert result.exit_code == 0

            assert purger_mock.call_args.args == (walk_mock, fake_delete, is_raw_mock)

    @patch("purgeraw.main.raw_determinator")
    @patch("purgeraw.main.directory_walker")
    @patch("purgeraw.main.purger")
    def test_when_input_dir_present_with_raw_extensions_then_purge_called(self,
                                                                          purger_mock: Mock,
                                                                          walker_mock: Mock,
                                                                          raw_determinator_mock: Mock,
                                                                          runner: CliRunner) -> None:
        walk_mock: Mock = Mock()
        is_raw_mock: Mock = Mock()
        walker_mock.return_value = walk_mock
        raw_determinator_mock.return_value = is_raw_mock

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-r", "cr3", "-r", "raw"])

            assert result.exit_code == 0

            assert walker_mock.call_args.args[0] == ["cr3", "raw", "jpg"]
            assert raw_determinator_mock.call_args.args == (("cr3", "raw"), ("jpg",))
            assert purger_mock.call_args.args == (walk_mock, delete, is_raw_mock)

    @patch("purgeraw.main.raw_determinator")
    @patch("purgeraw.main.directory_walker")
    @patch("purgeraw.main.purger")
    def test_when_input_dir_present_with_processed_extensions_then_purge_called(self,
                                                                                purger_mock: Mock,
                                                                                walker_mock: Mock,
                                                                                raw_determinator_mock: Mock,
                                                                                runner: CliRunner) -> None:
        walk_mock: Mock = Mock()
        is_raw_mock: Mock = Mock()
        walker_mock.return_value = walk_mock
        raw_determinator_mock.return_value = is_raw_mock

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-p", "png"])

            assert result.exit_code == 0

            assert walker_mock.call_args.args[0] == ["cr3", "png"]
            assert raw_determinator_mock.call_args.args == (("cr3",), ("png",))
            assert purger_mock.call_args.args == (walk_mock, delete, is_raw_mock)
