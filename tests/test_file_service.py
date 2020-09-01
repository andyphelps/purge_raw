from unittest.mock import patch, Mock

from purgeraw.file_service import fake_delete, delete, raw_determinator


class TestFileService:

    @patch("os.remove")
    def test_when_fake_delete_then_remove_not_called(self, remove: Mock) -> None:
        fake_delete("/flibble45")

        assert remove.call_count == 0

    @patch("os.remove")
    def test_when_delete_then_called_correctly(self, remove: Mock) -> None:
        delete("/flibble56")

        assert remove.call_count == 1
        assert remove.call_args.args == ("/flibble56",)

    def test_when_is_raw_with_matching_extension_then_returns_true(self) -> None:
        raw_checker = raw_determinator(["cr3", "raw"])
        assert raw_checker("/flibble12/IMG_0001.cr3")
        assert raw_checker("/flibble12/IMG_0002.raw")

    def test_when_is_raw_with_matching_extension_without_dot_then_returns_false(self) -> None:
        raw_checker = raw_determinator(["cr3"])
        assert not raw_checker("/flibble12/IMG_0001cr3")

    def test_when_is_raw_with_none_matching_extension_then_returns_false(self) -> None:
        raw_checker = raw_determinator(["cr3"])
        assert not raw_checker("/flibble12/IMG_0001.cr2")
