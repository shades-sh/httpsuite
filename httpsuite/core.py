""" Interfaces to parse, manipulate, and compile raw HTTP messages. """

from __future__ import annotations

import abc
from typing import NoReturn, Union

from httpsuite.helpers import Headers, Item


class Message(abc.ABC):
    """Base class representing an HTTP message.

    Note:
        ``Messages`` is an abstract class that both ``Request`` and ``Response``
        inherit from. ``Message`` should not be used directly.

    Args:
        first_line: Union[str, bytes, Item, None]: First line of the the request or response
                                                   message; either the request line or the
                                                   status line, respectfully.
        headers: Union[dict, Headers, None]: Dictionary or ``Headers`` that represents
                                             the requests or response's headers.
        body: Union[str, bytes, Item, None]: Body of the message.
    """

    __slots__ = ["_first_line", "_headers", "_body"]

    def __init__(
        self,
        first_line: Union[str, bytes, Item, None],
        headers: Union[dict, Headers, None] = None,
        body: Union[str, bytes, Item, None] = None,
    ) -> None:
        self._first_line = Item(first_line)

        if isinstance(headers, Headers):
            self._headers = headers
        elif headers == None:
            self._headers = Headers()
        else:
            self._headers = Headers(headers)

        self._body = Item(body)

    def _compile(self, format: str = "bytes", arrow: str = "") -> str:
        """Compiles the ``Message`` into the given format.

        Note:
            The ``arrow`` argument only works when ``format`` is ``string``.

        Args:
            format (str): Format that represents the return type. Either ``string``
                          or ``bytes``.
            arrow (str): String to append to the beginning of every line.

        Returns:
            Union[str, bytes]: String or bytes representation of the ``Message``.
        """

        if format not in ("str", "bytes"):
            raise TypeError("format must either be str, or byte.")

        self._compile_first_line()

        if format == "bytes":
            first_line = self._first_line.raw
            body = self._body.raw
            headers = b""
        elif format == "str":
            first_line = self._first_line.string
            body = self._body.string
            headers = ""

        for k, v in self.headers.items():
            if format == "bytes":
                headers += b"%b: %b\r\n" % (k.raw, v.raw)
            elif format == "str":
                headers += "{}: {}\r\n".format(k.string, v.string)

        if format == "bytes":
            msg = b"%b\r\n%b\r\n%b" % (first_line, headers, body)
        elif format == "str":
            msg = "{}\r\n{}\r\n{}".format(first_line, headers, body)

        if format == "str" and arrow:
            arrow_msg = [
                "{} {}".format(arrow, line) for line in msg.splitlines() if line
            ]
            return "\r\n".join(arrow_msg)
        else:
            return msg

    @property
    def headers(self) -> Headers:
        r"""HTTP headers of the ``Message``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Headers`, :class:`None`): New headers of the message.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Headers`: A ``Headers`` object that represents the HTTP header.

        Example:
            .. code-block:: python

               r.headers = {"Accept": "*/*"}
               r.headers += {"Host": "google.com"}
               r.headers.Host = "www.google.com"
               print(r.headers)
               print(r.headers.raw)

            .. code-block::

                Accept: */*
                Host: www.google.com

                b'Accept: */*\r\nHost: www.google.com\r\n'
        """

        return self._headers

    @property
    def body(self) -> Item:
        """Body of the ``Message``.

        **Setter**:
            *Args*:
                value (:class:`str`, :class:`bytes`, :class:`int`, :class:`httpsuite.helpers.Item`, :class:`None`): New body of the ``Message``.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP body.

        Example:
            .. code-block:: python

               r.body = "<html>Hello World</html>"
               print(r.body)
               print(r.body.raw)

            .. code-block:: python

                <html>Hello World</html>
                b'<html>Hello World</html>'
        """

        return self._body

    @property
    def string(self) -> str:
        """String representation of the ``Message``.

        Returns:
            str: String representation of the ``Message``.
        """

        return self._compile(format="str")

    @property
    def raw(self) -> bytes:
        r"""Bytes representation of the ``Message``.

        Note:
            This method will return ``Message`` with ``\r\n`` escape characters.

        Returns:
            bytes: Bytes representation of the ``Message``.
        """
        return self._compile(format="bytes")

    @property
    def first_line(self) -> Item:
        """First line of the ``Message``.

        Returns:
            Item: The first line of the ``Message``.
        """

        self._compile_first_line()
        return self._first_line

    @headers.setter
    def headers(self, value: Union[dict, Headers, None]) -> None:
        if not isinstance(value, dict):
            raise TypeError("can only set to type that inherits from 'dict'.")

        if isinstance(value, Headers):
            self._headers = value
        else:
            self._headers = Headers(value)

    @body.setter
    def body(self, value: Union[str, bytes, int, Item, None]) -> None:
        self._body = Item(value)

    @first_line.setter
    def first_line(self, value: Union[str, bytes]) -> None:
        self._first_line = Item(value)
        self._parse_first_line()

    @abc.abstractmethod
    def _compile_first_line(self) -> NoReturn:  # pragma: no cover
        """ Compiles the first line of the message. """
        raise NotImplementedError

    def _parse_first_line(self) -> NoReturn:  # pragma: no cover
        """ Parses the first line of the message. """
        raise NotImplementedError

    @classmethod
    def parse(
        cls: Union[Response, Request], message: Union[str, bytes]
    ) -> Union[Request, Response]:
        """Parses a raw ``Message``.

        Args:
            message (Union[str, bytes]): The raw string or bytes representation of a
                                     HTTP request or response.

        Returns:
            Union[Request, Response]: A ``Request`` or ``Response`` object.
        """

        if not isinstance(message, Item):
            message = Item(message)

        first_line = b""
        headers = Headers({})
        body = b""

        top_frame = True
        for index, line in enumerate(message.raw.splitlines()):
            if line == b"":
                top_frame = False

            if top_frame:
                if index == 0:
                    first_line = line
                elif b":" in line:
                    key, value = line.split(b":", 1)
                    headers += {key: value.lstrip(b" ")}
            elif line != b"":
                body += line

        args = (*first_line.split(b" "), headers, body)

        try:
            instance = cls(*args)
        except TypeError:  # pragma: no cover
            err = "You cannot use parse with type Message. Use Request or Response."
            raise TypeError(err)

        return instance

    def _string(self, arrow: str) -> str:
        """String representation of the ``Message``.

        Args:
            arrow (str): String to append to the beginning of every line of the
                         return.

        Returns:
            str: String representation of the ``Message``.
        """

        return self._compile(format="str", arrow=arrow)


class Request(Message):
    """Object representation of an HTTP request.

    Note:
        ``__init__`` should *not* be used to *parse* a raw HTTP request.
        Instead, one should use ``Request.parse(raw_msg)``.

    Args:
        method (Union[str, bytes, Item]): HTTP request method (i.e. ``GET``, ``POST``, etc).
        target (Union[str, bytes, Item]): HTTP request target (i.e. ``/index.html``).
        protocol (Union[str, bytes, Item]): HTTP request protocol (i.e. ``HTTP/1.1``).
        headers (Union[dict, Headers, None]): HTTP request headers.
        body (Union[str, bytes, Item, None]): HTTP request body.
    """

    __slots__ = ["_method", "_target", "_protocol"]

    def __init__(
        self,
        method: Union[str, bytes, Item, None],
        target: Union[str, bytes, Item, None],
        protocol: Union[str, bytes, Item, None],
        headers: Union[dict, Headers, None] = None,
        body: Union[str, bytes, Item, None] = None,
    ) -> None:
        self._method = Item(method)
        self._target = Item(target)
        self._protocol = Item(protocol)

        first_line = (self._method.raw, self._target.raw, self._protocol.raw)
        super().__init__(b"%b %b %b" % first_line, headers, body)

    def _compile_first_line(self) -> None:
        """ Sets the ``Request`` first line to ``method target protocol`` values. """
        first_line = (self._method.raw, self._target.raw, self._protocol.raw)
        self._first_line = Item(b"%b %b %b" % first_line)

    def _parse_first_line(self) -> None:
        """ Sets the ``Request`` first line values ``method target protocol`` to that of the first line."""
        first_line = self._first_line.raw.split(b" ")
        self.method, self.target, self.protocol = first_line

    @property
    def method(self) -> Item:
        r"""HTTP method of the ``Request``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New method of the request.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP request method.

        Example:
            .. code-block:: python

               r = Request(method="GET", target="/", protocol="HTTP/1.1")
               r.method = "POST"
               print(r)

            .. code-block::

                → POST / HTTP/1.1
        """
        return self._method

    @property
    def target(self) -> Item:
        r"""HTTP target of the ``Request``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New target of the request.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP request method.

        Example:
            .. code-block:: python

               r = Request(method="GET", target="/", protocol="HTTP/1.1")
               r.target = "/index.html"
               print(r)

            .. code-block::

                → GET /index.html HTTP/1.1
        """
        return self._target

    @property
    def protocol(self) -> Item:
        r"""HTTP protocol of the ``Request``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New protocol of the request.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP request protocol.

        Example:
            .. code-block:: python

               r = Request(method="GET", target="/", protocol="HTTP/1.1")
               r.protocol = "HTTP/1.0"
               print(r)

            .. code-block::

                → GET / HTTP/1.0
        """
        return self._protocol

    @method.setter
    def method(self, value: Union[str, bytes, Item, None]) -> None:
        self._method = Item(value)

    @target.setter
    def target(self, value: Union[str, bytes, Item, None]) -> None:
        self._target = Item(value)

    @protocol.setter
    def protocol(self, value: Union[str, bytes, Item, None]) -> None:
        self._protocol = Item(value)

    def __str__(self) -> str:
        r"""String representation of the ``Request``.

        Returns:
            str: Representation of the ``Request`` object.


        Example:
            .. code-block:: python

               r = Request(
                   method="GET",
                   target="/",
                   protocol="HTTP/1.1",
                   headers={"Host": "www.google.com", "Connection": "keep-alive",},
                   body=json.dumps({"hello": "world"}),
               )
               print(r)

            .. code-block::

                → GET / HTTP/1.1
                → Host: www.google.com
                → Connection: keep-alive
                → {"hello": "world"}
        """
        return super()._string("→")


class Response(Message):
    """Object representation of an HTTP response.

    Note:
        ``__init__`` should *not* be used to *parse* a raw HTTP response.
        Instead, one should use ``Response.parse(raw_msg)``.

    Args:
        protocol (Union[str, bytes, Item]): HTTP request protocol (i.e. ``HTTP/1.1``).
        status (Union[str, bytes, Item]): HTTP status (i.e. ``200``).
        status_msg (Union[str, bytes, Item]): HTTP status message (i.e. ``OK``).
        headers (Union[dict, Headers, None]): HTTP request headers.
        body (Union[str, bytes, Item, None]): HTTP request body.
    """

    __slots__ = ["_protocol", "_status", "_status_msg"]

    def __init__(
        self,
        protocol: Union[str, bytes, Item, None],
        status: Union[str, bytes, int, Item, None],
        status_msg: Union[str, bytes, Item, None],
        headers: Union[dict, Headers, None] = None,
        body: Union[str, bytes, Item, None] = None,
    ) -> None:
        self._protocol = Item(protocol)
        self._status = Item(status)
        self._status_msg = Item(status_msg)

        first_line = self._protocol.raw, self._status.raw, self._status_msg.raw
        super().__init__(b"%b %b %b" % first_line, headers, body)

    def _compile_first_line(self) -> None:
        """Sets the ``Response`` first line to ``protocol status status_msg``
        values.
        """
        first_line = self._protocol.raw, self._status.raw, self._status_msg.raw
        self._first_line = Item(b"%b %b %b" % first_line)

    def _parse_first_line(self) -> None:
        """Sets the ``Response`` first line values ``protocol status status_msg``
        to that of the first line.
        """
        first_line = self._first_line.raw.split(b" ")
        self.protocol, self.status, self.status_msg = first_line

    @property
    def protocol(self) -> Item:
        r"""HTTP protocol of the ``Response``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New protocol of the response.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP response protocol.

        Example:
            .. code-block:: python

               r = Response(protocol="HTTP/1.1", status=200, status_msg="OK")
               r.protocol = "HTTP/1.0"
               print(r)

            .. code-block::

                ← HTTP/1.0 200 OK
        """
        return self._protocol

    @property
    def status(self) -> Item:
        r"""HTTP status of the ``Response``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New status of the response.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP response status.

        Example:
            .. code-block:: python

               r = Response(protocol="HTTP/1.1", status=200, status_msg="OK")
               r.status = 300
               r.status_msg = "Continue"
               print(r)

            .. code-block::

                ← HTTP/1.1 300 Continue
        """
        return self._status

    @property
    def status_msg(self) -> Item:
        r"""HTTP status message of the ``Response``.

        **Setter**:
            *Args*:
                value (:class:`dict`, :class:`httpsuite.helpers.Item`, :class:`None`): New status message of the response.
        **Getter**:
            *Returns*:
                :class:`httpsuite.helpers.Item`: A ``Item`` object that represents the HTTP response status message.

        Example:
            .. code-block:: python

               r = Response(protocol="HTTP/1.1", status=200, status_msg="OK")
               r.status = 300
               r.status_msg = "Continue"
               print(r)

            .. code-block::

                ← HTTP/1.0 300 Continue
        """
        return self._status_msg

    @protocol.setter
    def protocol(self, value: Union[str, bytes, Item, None]) -> None:
        self._protocol = Item(value)

    @status.setter
    def status(self, value: Union[str, bytes, Item, None]) -> None:
        self._status = Item(value)

    @status_msg.setter
    def status_msg(self, value: Union[str, bytes, Item, None]) -> None:
        self._status_msg = Item(value)

    def __str__(self) -> str:
        r"""String representation of the ``Response``.

        Returns:
            str: Representation of the ``Response`` object.

        Example:
            .. code-block:: python

               r = Response(
                   protocol="HTTP/1.1",
                   status=200,
                   status_msg="OK",
                   headers={"Host": "www.google.com", "Connection": "keep-alive",},
                   body=json.dumps({"hello": "world"}),
               )
               print(r)

            .. code-block::

                ← HTTP/1.1 200 OK
                ← Host: www.google.com
                ← Connection: keep-alive
                ← {"hello": "world"}
        """
        return super()._string("←")
