"""
This test file ensures that toolbox.Item is properly implemented for httpsuite's needs.
Note that the author of httpsuite is the same as toolbox.
"""

from toolbox import Item
import pytest

items = Item("str"), Item(b"bytes"), Item(200)
valid_types = ["str", b"bytes", 200, *[item for item in items]]
invalid_types = [["List"], ("Tuple",), {"Set"}, {"Dictionary": ""}]


class Test_item_init:
    @pytest.mark.parametrize("other", valid_types)
    def test_item_init_valid_types(self, other):
        Item(other)

    @pytest.mark.parametrize("other", invalid_types)
    def test_item_init_invalid_types(self, other):
        with pytest.raises(TypeError):
            Item(other)


class Test_item_string_and_raw:
    @pytest.mark.parametrize("other", items)
    def test_item_string(self, other):
        assert isinstance(Item(other).string, str)
        assert Item(other).string in ("str", "bytes", "200")

    @pytest.mark.parametrize("other", items)
    def test_item_raw(self, other):
        assert isinstance(Item(other).raw, bytes)
        assert Item(other).raw in (b"str", b"bytes", b"200")

    @pytest.mark.parametrize("other", items)
    def test_item_str_and_string(self, other):
        assert str(Item(other)) == Item(other).string


class Test_item_eq:
    def test_item_eq(self):
        assert Item(200) in items
        assert Item("200") in items
        assert Item(b"200") in items


class Test_item_ne:
    def test_item_str_ne(self):
        assert Item(300) not in items
        assert Item("300") not in items
        assert Item(b"300") not in items


class Test_item_add:
    def test_item_add_eq(self):
        assert Item("<html>") + Item("</html>") == Item("<html></html>")
        assert Item("<html>") + "</html>" == Item("<html></html>")
        assert Item("<html>") + b"</html>" == Item("<html></html>")
        assert Item("<html>") + 100 + "</html>" == Item("<html>100</html>")

    def test_item_add_ne(self):
        with pytest.raises(AssertionError):
            assert Item("<html>") + Item("</html>") == Item("<html>")
        with pytest.raises(AssertionError):
            assert Item("<html>") + "<html>" == Item("<html>")
        with pytest.raises(AssertionError):
            assert Item("<html>") + b"<html>" == Item("<html>")
        with pytest.raises(AssertionError):
            assert Item("<html>") + 100 + "</html>" == Item("<html>")


class Test_item_iadd:
    def test_item_iadd_eq(self):
        item = Item("<html>")

        item += Item("</html>")
        assert item == Item("<html></html>")

        item += "</html>"
        assert item == Item("<html></html></html>")

        item += b"</html>"
        assert item == Item("<html></html></html></html>")

        item += 100
        assert item == Item("<html></html></html></html>100")

    def test_item_add_ne(self):
        item = Item("<html>")

        with pytest.raises(AssertionError):
            item += Item("</html>")
            assert item == Item("")

        with pytest.raises(AssertionError):
            item += "<html>"
            assert item == Item("")

        with pytest.raises(AssertionError):
            item += b"<html>"
            assert item == Item("")

        with pytest.raises(AssertionError):
            item += 100
            assert item == Item("")


class Test_item_hash:
    def test_item_hash_eq(self):
        assert hash(Item("<html>")) == hash(Item("<html>"))

    def test_item_hash_ne(self):
        with pytest.raises(AssertionError):
            assert hash(Item("<html>")) == hash(Item("</html>"))
