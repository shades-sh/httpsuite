from httpsuite import Headers
import pytest

dictionaries = [{"str": "str"}, {b"bytes": b"bytes"}]
headers = [Headers(d.copy()) for d in dictionaries]
valid_types = [{"str": "str"}, {b"bytes": b"bytes"}, *[header for header in headers]]
invalid_types = [
    "str",
    b"bytes",
    200,
    ["List"],
    ("Tuple",),
    {"Set"},
]


class Test_headers_init:
    @pytest.mark.parametrize("other", valid_types)
    def test_headers_init_valid_types(self, other):
        Headers(other)

    @pytest.mark.parametrize("other", invalid_types)
    def test_headers_init_invalid_types(self, other):
        with pytest.raises(TypeError):
            Headers(other)


class Test_headers_compile_string_raw:
    @pytest.mark.parametrize("other", headers)
    def test_headers_compile_string(self, other):
        compiled = other._compile(frmt="string")
        assert isinstance(compiled, str)
        assert compiled in ("str: str", "bytes: bytes")
        assert other.string == compiled

    @pytest.mark.parametrize("other", headers)
    def test_headers_compile_bytes(self, other):
        compiled = other._compile(frmt="bytes")
        assert isinstance(compiled, bytes)
        assert compiled in (b"str: str\r\n", b"bytes: bytes\r\n")
        assert other.raw == compiled


class Test_headers_add:
    def test_headers_add_headers(self):
        added = headers[0] + headers[1]
        assert added == Headers({"str": "str", "bytes": "bytes"})
        assert added == Headers({"str": "str", b"bytes": b"bytes"})
        assert added == Headers({b"str": b"str", "bytes": b"bytes"})
        assert added == Headers({b"str": b"str", b"bytes": b"bytes"})

    def test_headers_add_headers_uniqueness(self):
        added = headers[0] + headers[1]
        assert id(headers[0]) != id(added)
        assert id(headers[1]) != id(added)

    def test_headers_add_dict(self):
        added = headers[0] + dictionaries[1]
        assert added == Headers({"str": "str", "bytes": "bytes"})
        assert added == Headers({"str": "str", b"bytes": b"bytes"})
        assert added == Headers({b"str": b"str", "bytes": b"bytes"})
        assert added == Headers({b"str": b"str", b"bytes": b"bytes"})

    def test_headers_add_dict_uniqueness(self):
        added = headers[0] + dictionaries[1]
        assert id(headers[0]) != id(added)
        assert id(dictionaries[1]) != id(added)

    @pytest.mark.parametrize("other", invalid_types)
    def test_headers_add_invalid_type(self, other):
        added = Headers()
        with pytest.raises(TypeError):
            added + other


class Test_headers_iadd:
    def test_headers_iadd_headers(self):
        added = Headers()

        for header in headers:
            added += header

        assert added == Headers({"str": "str", "bytes": "bytes"})
        assert added == Headers({"str": "str", b"bytes": b"bytes"})
        assert added == Headers({b"str": b"str", "bytes": b"bytes"})
        assert added == Headers({b"str": b"str", b"bytes": b"bytes"})

    def test_headers_iadd_dict(self):
        added = Headers()

        for dictionary in dictionaries:
            added += dictionary

        assert added == Headers({"str": "str", "bytes": "bytes"})
        assert added == Headers({"str": "str", b"bytes": b"bytes"})
        assert added == Headers({b"str": b"str", "bytes": b"bytes"})
        assert added == Headers({b"str": b"str", b"bytes": b"bytes"})

    @pytest.mark.parametrize("other", invalid_types)
    def test_headers_iadd_invalid_types(self, other):
        added = Headers()
        with pytest.raises(TypeError):
            added += other


class Test_headers_setattr_and_getattr:
    def test_headers_setattr_and_getattr_single_word(self):
        headers = Headers()
        headers.Host = "github.com"

        assert headers.Host == "github.com"
        assert headers.Host == b"github.com"

        assert headers["Host"] == "github.com"
        assert headers["Host"] == b"github.com"
        assert headers[b"Host"] == "github.com"
        assert headers[b"Host"] == b"github.com"

    def test_headers_setattr_and_getattr_double_word(self):
        headers = Headers()
        headers.Cache_Control = "no-cache"

        assert headers.Cache_Control == "no-cache"
        assert headers.Cache_Control == b"no-cache"

        assert headers["Cache-Control"] == "no-cache"
        assert headers["Cache-Control"] == b"no-cache"
        assert headers[b"Cache-Control"] == "no-cache"
        assert headers[b"Cache-Control"] == b"no-cache"


class Test_headers_str:
    def test_headers_str(self):
        for header in headers:
            assert str(header) in ("str: str", "bytes: bytes")

    def test_headers_str_compiled(self):
        for header in headers:
            assert str(header) == header._compile(frmt="string")
