from httpsuite.interface import FrozenSet, TwoWayFrozenDict
from toolbox import Item

status = TwoWayFrozenDict({100: "Continue"})
protocols = FrozenSet({"GET"})


class Test_misc_TwoWayFrozenDict:
    def test_misc_TwoWayFrozenDict_init(self):
        assert status

    def test_misc_TwoWayFrozenDict_get_attribute(self):
        assert status._100 == "Continue"
        assert status._100 == b"Continue"

        assert status[100] == "Continue"
        assert status[100] == b"Continue"
        assert status["100"] == "Continue"
        assert status["100"] == b"Continue"
        assert status[b"100"] == "Continue"
        assert status[b"100"] == b"Continue"

        assert status.Continue == 100
        assert status.Continue == "100"
        assert status.Continue == b"100"

        assert status["Continue"] == 100
        assert status[b"Continue"] == 100
        assert status["Continue"] == "100"
        assert status[b"Continue"] == "100"
        assert status["Continue"] == b"100"
        assert status[b"Continue"] == b"100"

    def test_misc_TwoWayFrozenDict_iter(self):
        for item in status:
            assert isinstance(item, Item)

    def test_misc_TwoWayFrozenDict_len(self):
        assert len(status) == status.__len__()

    def test_misc_TwoWayFrozenDict_get_item_in(self):
        assert "100" in status
        assert b"100" in status
        assert 100 in status

        assert "Continue" in status
        assert b"Continue" in status

    def test_misc_TwoWayFrozenDict_get_not_in(self):
        assert "NONE" not in status
        assert not status.__contains__("NONE")


class Test_misc_FrozenSet:
    def test_misc_FrozenSet_init(self):
        assert protocols

    def test_misc_FrozenSet_str(self):
        protocols_str = protocols.__str__()
        assert "<" not in protocols_str and ">" not in protocols_str
