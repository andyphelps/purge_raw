import os
import tempfile

import pytest
import purgeraw.main
import purgeraw.purge_orchestrator

from unittest.mock import patch
from click.testing import CliRunner
from contextlib import contextmanager


class TestMain:

    @contextmanager
    def make_test_dir(self):
        tempdir = None
        try:
            tempdir = tempfile.mkdtemp("_purgeraw")
            yield tempdir
        finally:
            if tempdir is not None:
                os.rmdir(tempdir)

    @pytest.fixture
    def runner(self):
        yield CliRunner()

    def test_when_missing_input_dir_then_fails(self, runner):
        result = runner.invoke(purgeraw.main.main, [])

        assert result.exit_code == 2
        assert "Error: Missing option '-i' / '--input'." in result.output

    def test_when_input_dir_not_exists_then_fails(self, runner):
        result = runner.invoke(purgeraw.main.main, ["-i", "/flibble1212"])

        assert result.exit_code == 2
        assert "Path '/flibble1212' does not exist." in result.output

    @patch("purgeraw.purge_orchestrator.PurgeOrchestrator.purge")
    def test_when_input_dir_present_then_purge_called(self, purge, runner):
        with self.make_test_dir() as dirname:
            result = runner.invoke(purgeraw.main.main, ["-i", dirname])

            assert result.exit_code == 0
            assert purge.called
            assert purge.call_args.args == (dirname, False)

    @patch("purgeraw.purge_orchestrator.PurgeOrchestrator.purge")
    def test_when_input_dir_present_with_dry_run_then_purge_called(self, purge, runner):
        with self.make_test_dir() as dirname:
            result = runner.invoke(purgeraw.main.main, ["-i", dirname, "-d"])

            assert result.exit_code == 0
            assert purge.called
            assert purge.call_args.args == (dirname, True)

    @patch("purgeraw.purge_orchestrator.PurgeOrchestrator.purge")
    def test_when_input_dir_present_then_purge_called_long_params(self, purge, runner):
        with self.make_test_dir() as dirname:
            result = runner.invoke(purgeraw.main.main, ["--input", dirname])

            assert result.exit_code == 0
            assert purge.called
            assert purge.call_args.args == (dirname, False)

    @patch("purgeraw.purge_orchestrator.PurgeOrchestrator.purge")
    def test_when_input_dir_present_with_dry_run_then_purge_called_long_params(self, purge, runner):
        with self.make_test_dir() as dirname:
            result = runner.invoke(purgeraw.main.main, ["--input", dirname, "--dryrun"])

            assert result.exit_code == 0
            assert purge.called
            assert purge.call_args.args == (dirname, True)
