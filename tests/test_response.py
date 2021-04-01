import json

import pytest
from httpsuite import Headers, Response


class Test_response_init_:
    def test_response_init_small(self):
        Response(protocol="HTTP/1.1", status=200, status_msg="OK")

    def test_response_init_large(self):
        Response(
            protocol="GET",
            status=200,
            status_msg="OK",
            headers=Headers(
                {
                    "Host": "www.google.com",
                    "Accept": "*/*",
                    "Connection": "keep-alive",
                }
            ),
            body=json.dumps({"hello": "world"}),
        )

    def test_init_wrong_type(self):
        with pytest.raises(TypeError):
            # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
            Response(method=None, target=None, protocol=None)


response = Response(
    protocol="HTTP/1.1",
    status=200,
    status_msg="OK",
    headers=Headers(
        {
            "Host": "www.google.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }
    ),
    body=json.dumps({"hello": "world"}),
)

response_raw = (
    b"HTTP/1.1 200 OK\r\n"
    b"Test: Headers\r\n"
    b"Host: www.google.com\r\n"
    b"Accept: */*\r\n"
    b"Connection: keep-alive\r\n"
    b"\r\n"
    b'{"hello": "world"}'
)


class Test_response_getters:
    def test_response_getter_protocol(self):
        for protocol in ["HTTP/1.1", b"HTTP/1.1"]:
            assert response.protocol == protocol

    def test_response_getter_status(self):
        for status in [200, "200", b"200"]:
            assert response.status == status

    def test_response_getter_status_msg(self):
        for status_msg in ["OK", b"OK"]:
            assert response.status_msg == status_msg


class Test_response_setters:
    def test_response_setter_protocol(self):
        response.protocol = "HTTP/0.9"

        for protocol in ["HTTP/0.9", b"HTTP/0.9"]:
            assert response.protocol == protocol

    def test_response_setter_status(self):
        response.status = "400"

        for status in [400, "400", b"400"]:
            assert response.status == status

    def test_response_setter_status_msg(self):
        response.status_msg = "Not Found"

        for status_msg in ["Not Found", b"Not Found"]:
            assert response.status_msg == status_msg


class Test_response_str:
    def test_request_str(self):
        assert "←" in response.__str__()


class Test_response_parse:
    def test_response_str(self):
        parsed = Response.parse(response_raw)
        assert isinstance(parsed, Response)

        assert parsed.protocol == "HTTP/1.1"
        assert parsed.status == 200
        assert parsed.status_msg == "OK"
        assert parsed.headers == Headers(
            {
                "Test": "Headers",
                "Host": "www.google.com",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }
        )
        assert parsed.body == '{"hello": "world"}'
