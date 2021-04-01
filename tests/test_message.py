import json

import pytest
from httpsuite import Headers, Request, Response
from toolbox.collections.item import ENCODE

# ====================
#       Request
# ====================
request_headers = {
    "Host": "www.google.com",
    "Accept": "*/*",
    "User-Agent": "httpsuite/1.0.0",
    "Connection": "keep-alive",
}
request_body = json.dumps({"hello": "world"})
request = Request(
    method="GET",
    target="/",
    protocol="HTTP/1.1",
    headers=Headers(request_headers),
    body=request_body,
)
request_raw = b'GET / HTTP/1.1\r\nHost: www.google.com\r\nAccept: */*\r\nUser-Agent: httpsuite/1.0.0\r\nConnection: keep-alive\r\n\r\n{"hello": "world"}'
request_first_line = b"GET / HTTP/1.1"

# ====================
#       Response
# ====================
response_headers = {
    "Host": "www.google.com",
    "Accept": "*/*",
    "Connection": "keep-alive",
    "Keep-Alive": "timeout=5, max=1000",
    "Server": "httpsuite/1.0.0",
}
response_body = json.dumps({"hello": "world"})
response = Response(
    protocol="HTTP/1.1",
    status=200,
    status_msg="OK",
    headers=response_headers,
    body=response_body,
)
response_raw = b'HTTP/1.1 200 OK\r\nHost: www.google.com\r\nAccept: */*\r\nConnection: keep-alive\r\nKeep-Alive: timeout=5, max=1000\r\nServer: httpsuite/1.0.0\r\n\r\n{"hello": "world"}'
response_first_line = b"HTTP/1.1 200 OK"

# ====================
#       Objects
# ====================
objects_headers = [request_headers, response_headers]
objects_body = [request_body, response_body]
objects = [request, response]
objects_raw = [request_raw, response_raw]
objects_first_line = [request_first_line, response_first_line]


class Test_message_getters:
    @pytest.mark.parametrize("zipped", zip(objects, objects_raw))
    def test_message_getter_string(self, zipped):
        assert zipped[0].string == zipped[1].decode(ENCODE)

    @pytest.mark.parametrize("zipped", zip(objects, objects_raw))
    def test_message_getter_raw(self, zipped):
        assert zipped[0].raw == zipped[1]

    @pytest.mark.parametrize("zipped", zip(objects, objects_first_line))
    def test_message_getter_first_line(self, zipped):
        assert zipped[0].first_line == zipped[1]

    @pytest.mark.parametrize("zipped", zip(objects, objects_headers))
    def test_message_getter_headers_valid(self, zipped):
        assert zipped[0].headers == zipped[1]
        assert zipped[0].headers == Headers(zipped[1])

    @pytest.mark.parametrize("zipped", zip(objects, objects_body))
    def test_message_getter_body(self, zipped):
        assert zipped[0].body == zipped[1]
        assert zipped[0].body == bytes(zipped[1], ENCODE)

    @pytest.mark.parametrize("message", objects)
    def test_message_getter_protocol(self, message):
        assert message.protocol == "HTTP/1.1"
        assert message.protocol == b"HTTP/1.1"


class Test_message_setters:
    def test_message_setter_request_headers_valid(self):
        request.headers = {}
        request.headers = Headers({})

    def test_message_setter_response_headers_valid(self):
        response.headers = {}
        response.headers = Headers({})

    def test_message_setter_request_headers_invalid(self):
        with pytest.raises(TypeError):
            request.headers = "NONE"

    def test_message_setter_response_headers_invalid(self):
        with pytest.raises(TypeError):
            response.headers = "NONE"

    def test_message_setter_request_body(self):
        request.body = "<html>"

    def test_message_setter_response_body(self):
        response.body = "<html>"


class Test_message_compile:
    def test_message_compile_response(self):
        with pytest.raises(TypeError):
            assert response._compile(frmt="dict")

    def test_message_compile_request(self):
        with pytest.raises(TypeError):
            assert request._compile(frmt="dict")
