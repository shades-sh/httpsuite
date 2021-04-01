import json

import pytest
from httpsuite import Headers, Request


class Test_request_init_:
    def test_request_init_small(self):
        Request(
            method="GET",
            target="google.com:80",
            protocol="HTTP/1.1",
        )

    def test_request_init_medium(self):
        Request(
            method="GET",
            target="google.com:80",
            protocol="HTTP/1.1",
            headers=None,
            body=None,
        )

    def test_request_init_large(self):
        Request(
            method="GET",
            target="/",
            protocol="HTTP/1.1",
            headers=Headers(
                {
                    "Host": "www.google.com",
                    "Accept": "*/*",
                    "User-Agent": "httpsuite/1.0.0",
                    "Connection": "keep-alive",
                }
            ),
            body=json.dumps({"hello": "world"}),
        )

    def test_init_wrong_type(self):
        with pytest.raises(TypeError):
            Request(method={}, target={}, protocol={})


request = Request(
    method="GET",
    target="/",
    protocol="HTTP/1.1",
    headers=Headers(
        {
            "Host": "www.google.com",
            "Accept": "*/*",
            "User-Agent": "httpsuite/1.0.0",
            "Connection": "keep-alive",
        }
    ),
    body=json.dumps({"hello": "world"}),
)

request_raw = (
    b"POST / HTTP/1.1\r\n"
    b"Host: www.google.com\r\n"
    b"Accept: */*\r\n"
    b"User-Agent: httpsuite/1.0.0\r\n"
    b"Connection: keep-alive\r\n"
    b"\r\n"
    b'{"hello": "world"}'
)


class Test_request_getters:
    def test_request_getter_method(self):
        for method in ["GET", b"GET"]:
            assert request.method == method

    def test_request_getter_target(self):
        for target in ["/", b"/"]:
            assert request.target == target

    def test_request_getter_protocol(self):
        for protocol in ["HTTP/1.1", b"HTTP/1.1"]:
            assert request.protocol == protocol


class Test_request_setters:
    def test_request_setter_method(self):
        request.method = "POST"

        for method in ["POST", b"POST"]:
            assert request.method == method

    def test_request_setter_target(self):
        request.target = "/index.html"

        for target in ["/index.html", b"/index.html"]:
            assert request.target == target

    def test_request_setter_protocol(self):
        request.protocol = "HTTP/0.9"

        for protocol in ["HTTP/0.9", b"HTTP/0.9"]:
            assert request.protocol == protocol


class Test_request_str:
    def test_request_str(self):
        assert "→" in request.__str__()


class Test_request_parse:
    def test_request_str(self):
        parsed = Request.parse(request_raw)
        assert isinstance(parsed, Request)

        assert parsed.method == "POST"
        assert parsed.target == "/"
        assert parsed.protocol == "HTTP/1.1"
        assert parsed.headers == Headers(
            {
                "Host": "www.google.com",
                "Accept": "*/*",
                "User-Agent": "httpsuite/1.0.0",
                "Connection": "keep-alive",
            }
        )
        assert parsed.body == '{"hello": "world"}'
