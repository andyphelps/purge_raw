from typing import cast, Callable, List, Tuple
from unittest.mock import Mock

import pytest  # type: ignore

from purgeraw.purger import purge

RAW_EXTS = ["cr3", "xmp"]


class TestPurger:

    @pytest.fixture
    def indexes_mock(self) -> Mock:
        return Mock()

    def test_when_purge_empty_folder_nothing_done(self, indexes_mock: Callable[[str], List[Tuple[str, str]]]) -> None:
        to_remove: List[str] = purge(RAW_EXTS, indexes_mock, [])

        assert to_remove == []

    def test_when_purge_folder_with_nothing_to_delete_nothing_done(self, indexes_mock: Mock) -> None:
        indexes_mock.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001.jpg")],
            [("00002", "/mydir/00Processed/IMG_00002.jpg")]
        )

        to_remove: List[str] = purge(RAW_EXTS, cast("Callable[[str], List[Tuple[str, str]]]", indexes_mock), [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/00Processed/IMG_00001.jpg",
            "/mydir/00Processed/IMG_00002.jpg"
        ])

        assert to_remove == []

    def test_when_purge_folder_with_one_to_delete_then_deleted(self, indexes_mock: Mock) -> None:
        indexes_mock.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001.jpg")]
        )

        to_remove: List[str] = purge(RAW_EXTS, cast("Callable[[str], List[Tuple[str, str]]]", indexes_mock), [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/00Processed/IMG_00001.jpg"
        ])

        assert to_remove == ["/mydir/IMG_00002.cr3"]

    def test_when_multi_processed_to_delete_then_correct_deletion(self, indexes_mock: Mock) -> None:
        indexes_mock.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00003", "/mydir/IMG_00003.cr3")],
            [("00004", "/mydir/IMG_00004.cr3")],
            [("00005", "/mydir/IMG_00005.cr3")],
            [("00001", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00002", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00003", "/mydir/00Processed/IMG_00001-00003.jpg")],
        )

        to_remove: List[str] = purge(RAW_EXTS, cast("Callable[[str], List[Tuple[str, str]]]", indexes_mock), [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00002.cr3",
            "/mydir/IMG_00003.cr3",
            "/mydir/IMG_00004.cr3",
            "/mydir/IMG_00005.cr3",
            "/mydir/00Processed/IMG_00001-00003.jpg"
        ])

        assert to_remove == ["/mydir/IMG_00004.cr3", "/mydir/IMG_00005.cr3"]

    def test_when_multi_processed_to_delete_with_xmp_then_correct_deletion(self, indexes_mock: Mock) -> None:
        indexes_mock.side_effect = (
            [("00001", "/mydir/IMG_00001.cr3")],
            [("00001", "/mydir/IMG_00001.xmp")],
            [("00002", "/mydir/IMG_00002.cr3")],
            [("00002", "/mydir/IMG_00002.xmp")],
            [("00003", "/mydir/IMG_00003.cr3")],
            [("00003", "/mydir/IMG_00003.xmp")],
            [("00004", "/mydir/IMG_00004.xmp")],
            [("00004", "/mydir/IMG_00004.cr3")],
            [("00005", "/mydir/IMG_00005.cr3")],
            [("00005", "/mydir/IMG_00005.xmp")],
            [("00001", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00002", "/mydir/00Processed/IMG_00001-00003.jpg"),
             ("00003", "/mydir/00Processed/IMG_00001-00003.jpg")],
        )

        to_remove: List[str] = purge(RAW_EXTS, cast("Callable[[str], List[Tuple[str, str]]]", indexes_mock), [
            "/mydir/IMG_00001.cr3",
            "/mydir/IMG_00001.xmp",
            "/mydir/IMG_00002.cr3",
            "/mydir/IMG_00002.xmp",
            "/mydir/IMG_00003.cr3",
            "/mydir/IMG_00003.xmp",
            "/mydir/IMG_00004.cr3",
            "/mydir/IMG_00004.xmp",
            "/mydir/IMG_00005.cr3",
            "/mydir/IMG_00005.xmp",
            "/mydir/00Processed/IMG_00001-00003.jpg"
        ])

        assert to_remove == [
            "/mydir/IMG_00004.cr3",
            "/mydir/IMG_00004.xmp",
            "/mydir/IMG_00005.cr3",
            "/mydir/IMG_00005.xmp"
        ]
