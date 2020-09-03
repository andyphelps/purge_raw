import os
import tempfile

import pytest  # type: ignore
import purgeraw.main

from unittest.mock import patch, Mock, call
from click.testing import CliRunner, Result
from contextlib import contextmanager
from typing import Generator, Optional
from purgeraw.index_extraction import indexer


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

    @patch.object(purgeraw.main, purgeraw.main.directory_walker.__name__)
    @patch.object(purgeraw.main, purgeraw.main.purge.__name__)
    @patch.object(purgeraw.main, purgeraw.main.fake_deleter.__name__)
    def test_when_input_dir_present_then_walker_purger_and_fake_deleter_called(self,
                                                                               deleter_mock: Mock,
                                                                               purger_mock: Mock,
                                                                               walker_mock: Mock,
                                                                               runner: CliRunner) -> None:

        walker_mock.side_effect = [walker_mock, ["/some/dir/fred.cr3"]]
        purger_mock.side_effect = [purger_mock, ["/some/dir/fred.cr3"]]

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname])

        assert result.exit_code == 0
        assert walker_mock.call_args_list == [call(["cr3", "xmp", "jpg"]),
                                              call(dirname)
                                              ]
        assert purger_mock.call_args_list == [call(["cr3", "xmp"], indexer),
                                              call(["/some/dir/fred.cr3"])
                                              ]
        assert deleter_mock.call_args.args[0] == ["/some/dir/fred.cr3"]

    @patch.object(purgeraw.main, purgeraw.main.directory_walker.__name__)
    @patch.object(purgeraw.main, purgeraw.main.purge.__name__)
    @patch.object(purgeraw.main, purgeraw.main.deleter.__name__)
    def test_when_input_dir_present_with_delete_then_walker_purger_and_deleter_called(self,
                                                                                      deleter_mock: Mock,
                                                                                      purger_mock: Mock,
                                                                                      walker_mock: Mock,
                                                                                      runner: CliRunner) -> None:
        walker_mock.side_effect = [walker_mock, ["/some/dir/fred.cr3"]]
        purger_mock.side_effect = [purger_mock, ["/some/dir/fred.cr3"]]

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-d"])

        assert result.exit_code == 0
        assert walker_mock.call_args_list == [call(["cr3", "xmp", "jpg"]),
                                              call(dirname)
                                              ]
        assert purger_mock.call_args_list == [call(["cr3", "xmp"], indexer),
                                              call(["/some/dir/fred.cr3"])
                                              ]
        assert deleter_mock.call_args.args[0] == ["/some/dir/fred.cr3"]

    @patch.object(purgeraw.main, purgeraw.main.directory_walker.__name__)
    @patch.object(purgeraw.main, purgeraw.main.purge.__name__)
    def test_when_input_dir_present_with_raw_extensions_then_purge_called(self,
                                                                          purger_mock: Mock,
                                                                          walker_mock: Mock,
                                                                          runner: CliRunner) -> None:
        walker_mock.side_effect = [walker_mock, ["/some/dir/fred.cr3"]]
        purger_mock.side_effect = [purger_mock, ["/some/dir/fred.cr3"]]

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-r", "cr2", "-r", "raw"])

        assert result.exit_code == 0
        assert walker_mock.call_args_list[0] == call(["cr2", "raw", "jpg"])
        assert purger_mock.call_args_list[0] == call(["cr2", "raw"], indexer)

    @patch.object(purgeraw.main, purgeraw.main.directory_walker.__name__)
    @patch.object(purgeraw.main, purgeraw.main.purge.__name__)
    def test_when_input_dir_present_with_processed_extensions_then_purge_called(self,
                                                                                purger_mock: Mock,
                                                                                walker_mock: Mock,
                                                                                runner: CliRunner) -> None:
        walker_mock.side_effect = [walker_mock, ["/some/dir/fred.cr3"]]
        purger_mock.side_effect = [purger_mock, ["/some/dir/fred.cr3"]]

        dirname: str
        with self.make_test_dir() as dirname:
            result: Result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-p", "png"])

        assert result.exit_code == 0
        assert walker_mock.call_args_list[0] == call(["cr3", "xmp", "png"])
