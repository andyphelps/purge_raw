from unittest.mock import Mock, call

import pytest  # type: ignore
from purgeraw.directory_service import directory_walker
from purgeraw.file_service import raw_determinator, delete
from purgeraw.indexer_service import indexer
from purgeraw.purge_service import purger
from typing import cast, Callable


class TestPurgeService:
    class PurgerMockingFixture:

        def __init__(self):
            self.walk_mock: Mock = Mock()
            self.delete_mock: Mock = Mock()
            self.is_raw_mock: Callable[[str], bool] = raw_determinator(["cr3"])
            self.indexer: Mock = Mock()
            self.purge: Callable[[str], None] = purger(
                cast(directory_walker, self.walk_mock),
                cast(delete, self.delete_mock),
                cast(raw_determinator, self.is_raw_mock),
                cast(indexer, self.indexer))

    @pytest.fixture
    def purger_fixture(self) -> PurgerMockingFixture:
        return TestPurgeService.PurgerMockingFixture()

    def test_when_purge_empty_folder_nothing_done(self, purger_fixture: PurgerMockingFixture) -> None:
        purger_fixture.walk_mock.return_value = []

        purger_fixture.purge("/mydir")

        assert not purger_fixture.delete_mock.called

    def test_when_purge_folder_with_nothing_to_delete_nothing_done(self, purger_fixture: PurgerMockingFixture) -> None:
        purger_fixture.walk_mock.return_value = [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/00Processed/IMG_00001.jpg",
            "/mydir/00Processed/IMG_00002.jpg"
        ]
        purger_fixture.indexer.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001.jpg")],
            [("00002", "/mydir/00Processed/IMG_00002.jpg")]
        )

        purger_fixture.purge("/mydir")

        assert not purger_fixture.delete_mock.called

    def test_when_purge_folder_with_one_to_delete_then_deleted(self, purger_fixture: PurgerMockingFixture) -> None:
        purger_fixture.walk_mock.return_value = [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/00Processed/IMG_00001.jpg"
        ]
        purger_fixture.indexer.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001.jpg")]
        )
        purger_fixture.delete_mock.return_value = None

        purger_fixture.purge("/mydir")

        assert purger_fixture.delete_mock.called
        assert purger_fixture.delete_mock.call_args.args[0] == "/mydir/IMG_00002.cr3"

    def test_when_multi_processed_to_delete_then_correct_deletion(self, purger_fixture: PurgerMockingFixture) -> None:
        purger_fixture.walk_mock.return_value = [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/IMG_00003.cr3",
            "/mydir/IMG_00004.cr3",
            "/mydir/IMG_00005.cr3",
            "/mydir/00Processed/IMG_00001-00003.jpg"
        ]
        purger_fixture.indexer.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00003", "/mydir/IMG_00003.cr3")],
            [("00004", "/mydir/IMG_00004.cr3")],
            [("00005", "/mydir/IMG_00005.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00002", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00003", "/mydir/00Processed/IMG_00001-00003.jpg")],
        )

        purger_fixture.purge("/mydir")

        assert purger_fixture.delete_mock.call_count == 2
        assert call("/mydir/IMG_00004.cr3") in purger_fixture.delete_mock.call_args_list
        assert call("/mydir/IMG_00005.cr3") in purger_fixture.delete_mock.call_args_list
