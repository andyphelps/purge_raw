from unittest.mock import patch, Mock

from purgeraw.deletion import fake_deleter, deleter


class TestDeletion:

    @patch("os.remove")
    def test_when_fake_delete_then_remove_not_called(self, remove: Mock) -> None:
        fake_deleter(["/flibble45"])

        assert remove.call_count == 0

    @patch("os.remove")
    def test_when_delete_then_called_correctly(self, remove: Mock) -> None:
        deleter(["/flibble56", "/flibble67"])

        assert remove.call_count == 2
        assert remove.call_args_list[0].args == ("/flibble56",)
        assert remove.call_args_list[1].args == ("/flibble67",)
