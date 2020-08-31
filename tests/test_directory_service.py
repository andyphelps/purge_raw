from unittest.mock import patch, Mock
from purgeraw.directory_service import directory_walker
from typing import List


class TestDirectoryRepository:

    @patch("os.walk")
    def test_when_empty_dir_then_empty_lists_returned(self, walk_mock: Mock) -> None:
        walk_mock.return_value = []

        files: List[str] = directory_walker([])("mydir")

        assert files == []

    @patch("os.walk")
    def test_when_chosen_ext_then_only_files_matching_are_returned_case_insensitive(self, walk_mock: Mock) -> None:
        walk_mock.return_value = [("mydir", [], ["IMG_0001.CR3", "IMG_0002.Cr3", "IMG_0003.jpg"])]

        files: List[str] = directory_walker(["cr3"])("mydir")

        assert files == ["mydir/IMG_0001.CR3", "mydir/IMG_0002.Cr3"]

    @patch("os.walk")
    def test_when_chosen_exts_then_only_files_matching_are_returned_nested_dirs(self, walk_mock: Mock) -> None:
        walk_mock.return_value = [("mydir", ["00Processed", "junk"], ["IMG_0001.CR3", "IMG_0002.Cr3", "wibble.txt"]),
                                  ("mydir/00Processed", [], ["IMG_0001.jpg", "IMG_0003.jpg", "flibble.csv"]),
                                  ("mydir/junk", [], [])]

        files: List[str] = directory_walker(["cr3", "jpg"])("mydir")

        assert files == ["mydir/IMG_0001.CR3", "mydir/IMG_0002.Cr3",
                         "mydir/00Processed/IMG_0001.jpg", "mydir/00Processed/IMG_0003.jpg"]
