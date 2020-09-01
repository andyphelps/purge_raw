from purgeraw.indexer_service import indexer


class TestIndexerService:

    def test_when_empty_filename_then_empty_list(self) -> None:
        assert indexer("") == []

    def test_when_file_not_matching_then_empty_list(self) -> None:
        assert indexer("IMG_ab12.cr3") == []

    def test_when_file_matching_then_list_returns_single_entry(self) -> None:
        assert indexer("/flibble/IMG_1234.cr3") == [("1234", "/flibble/IMG_1234.cr3")]

    def test_when_range_file_matching_then_list_returns_entries(self) -> None:
        assert indexer("/flibble/IMG_01234-01236.cr3") == [
            ("01234", "/flibble/IMG_01234-01236.cr3"),
            ("01235", "/flibble/IMG_01234-01236.cr3"),
            ("01236", "/flibble/IMG_01234-01236.cr3"),
        ]

    def test_when_over_200_range_file_matching_then_empty_list(self) -> None:
        assert indexer("/flibble/IMG_01234-01435.cr3") == []

    def test_when_reversed_range_file_matching_then_empty_list(self) -> None:
        assert indexer("/flibble/IMG_01234-01232.cr3") == []

    def test_when_size_mismatched_range_file_matching_then_empty_list(self) -> None:
        assert indexer("/flibble/IMG_01234-001236.cr3") == []
