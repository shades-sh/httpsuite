# -*- coding: utf-8 -*-
""" Classes for parsing, modifying, and re-compiling HTTP messages. """

import abc
from typing import Any, Type, Union

from toolbox.collections.item import Item, ItemType, ENCODE

HeadersType = Union[dict, "Headers", None]


class Headers(dict):
    """Interface for HTTP/1.x headers object."""

    def __init__(self, headers: HeadersType = None) -> None:
        """Initializes the Headers object.

        Args:
            value: Dictionary, headers, or None object that represents the headers.
        """

        if headers is None:
            headers = {}

        self._check(headers)

        if isinstance(headers, dict):
            for key, value in headers.items():
                self[Item(key)] = Item(value)

        super().__init__()

    def _compile(self, frmt: str = "bytes") -> Union[str, bytes]:
        r"""Compiles the Headers into the passed format.

        Notes:
            When the format is bytes this function will return the headers in bytes
            format with the correct HTTP escape characters "\r\n". This does **not**
            occur when string is passed as the format (new lines are created instead).

        Args:
            format: Either bytes or str. Formats the return accordingly to the passed
                format.

        Returns:
            String or bytes representation of the Headers.
        """

        if frmt == "bytes":
            data = b""
            for key, value in self.items():
                data += b"%b: %b\r\n" % (key.raw, value.raw)

        elif frmt == "string":
            data = ""
            for key, value in self.items():
                data += "{}: {}\r\n".format(key.string, value.string)

            if data[-2:] == "\r\n":
                data = data[: len(data) - 2]

        return data

    def _check(self, value: HeadersType) -> Union[None, None]:
        """Checks the item type to verify it is either Headers or dict.

        Raises:
            TypeError: Headers is not either dict or headers.
        """

        if not isinstance(value, dict) and not isinstance(value, Headers):
            raise TypeError("Headers can only be of type that inherits from 'dict'.")

    @property
    def string(self) -> str:
        """String representation of the Headers.

        Returns:
            String representation of the Headers.
        """
        return self._compile(frmt="string")

    @property
    def raw(self) -> bytes:
        r"""Bytes representation of the Headers.

        Note:
            This method will return Headers with "\r\n" escape characters.

        Returns:
            Bytes representation of the Headers.
        """
        return self._compile(frmt="bytes")

    def __add__(self, other: Union[dict, "Headers"]) -> "Headers":
        """Adds item with passed other and returns new Headers.

        Args:
            other: Headers or dictionary to be added.

        Returns:
            Headers: New resulting Headers object.
        """

        self._check(other)

        if isinstance(other, Headers):
            current = self.copy()
            current.update(other)
            return Headers(current)
        elif isinstance(other, dict):
            itemized_values = {Item(k): Item(v) for k, v in other.items()}
            copy = self.copy()
            copy.update(itemized_values)
            return copy

    def __iadd__(self, other: Union[dict, "Headers"]) -> "Headers":
        """Adds current headers with passed other and returns self.

        Args:
            other: Headers or dictionary to be added.

        Returns:
            Headers: Self after addition of other to itself.
        """

        self._check(other)

        itemized_values = {Item(k): Item(v) for k, v in other.items()}
        self.update(itemized_values)
        return self

    def __setattr__(self, key: str, value: str) -> None:
        """Sets a new attribute inside Headers.

        Notes:
            If "_" is present in the key it gets replaced with "-". This is so, example,
            "headers.User_Agent" is equivalent to "headers['User-Agent']".
        """

        key_mod = key.replace("_", "-").encode(ENCODE)
        self[Item(key_mod)] = Item(value)

    def __getattr__(self, key: str) -> Item:
        """Gets attribute inside Headers.

        Notes:
            If "_" is present in the key it gets replaced with "-". This is so the
            "headers.User_Agent" is equivalent to "headers['User-Agent']".

        Returns:
            Item corresponding to the passed key.
        """

        key_mod = key.replace("_", "-").encode(ENCODE)

        if key_mod in self:
            return self[key_mod]
        else:
            return None

    def __str__(self) -> str:
        """String representation of the Headers.

        Returns:
            String representation of the Headers.
        """
        return self.string

    def __repr__(self):
        """String representation of the Headers.

        Returns:
            String representation of the Headers.
        """
        return "Headers({})".format(self.string)


class Message(abc.ABC):
    """Abstract class that contains shared methods and properties accessible by both the
    Request and Response classes.

    Warning:
        This class is not intended to be used by itself. Note that Message is an
        abstraction that represents the shared properties and methods of both a Request
        and Response instance. All functions displayed in Message are, therefore,
        accessible by both the Request and Response classes.
    """

    __slots__ = ["_protocol", "_headers", "_body", "_first_line"]

    def __init__(
        self, protocol: ItemType, headers: HeadersType = None, body: ItemType = None
    ) -> None:
        """Initializes an HTTP Message.

        Args:
            protocol: "<major>.<minor>" numbering scheme to indicate versions of the
                protocol.
            headers: Collection of case-insensitive name followed by a colon (:).
            body: Data associated with the message.
        """
        self._first_line = None
        self._protocol = Item(protocol)

        if isinstance(headers, Headers):
            self._headers = headers
        elif headers is None:
            self._headers = Headers()
        else:
            self._headers = Headers(headers)

        self._body = Item(body)

    # ================ Parsing ================
    #           other types -> Message

    @classmethod
    def parse(cls: Union["Message", "Response", "Request"], message: Any) -> None:
        """Parses a raw HTTP message (in bytes or string) to an object instance of class 'cls'.

        Args:
            message: The primative or object to convert into a Request or Response
                object.

        Returns:
            An initialized object of class 'cls'.
        """

        if isinstance(cls, Message):
            err = "You can only use .parse() with either the Request or Response class."
            raise ValueError(err)

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
            else:
                body += line

        args = (*first_line.split(b" "), headers, body)

        try:
            return cls(*args)
        except TypeError as error:  # pragma: no cover
            err = "Error parsing the message due to {}.".format(error)
            raise TypeError(err) from error

    # ================ Compilation ================
    #             Message -> other types

    def _compile(
        self, frmt: type = Union[Type[str], Type[bytes]], arrow: str = ""
    ) -> Union[str, bytes]:
        """Compile the Message object into a useable type (str, or bytes).

        Note:
            The 'arrow' argument only works when 'frmt' is 'str'.

        Args:
            format: Type that represents the return type. Either 'str' or 'bytes'.
            arrow: String to append to the beginning of every line.

        Returns:
            String or bytes representation of the 'Message'.
        """

        if frmt is not bytes and frmt is not str:
            raise TypeError("format must either be str, or byte.")

        self._compile_first_line()

        if frmt is bytes:
            first_line = self._first_line.raw
            body = self._body.raw
            headers = b""
        elif frmt is str:
            first_line = self._first_line.string
            body = self._body.string
            headers = ""

        for key, value in self.headers.items():
            if frmt is bytes:
                headers += b"%b: %b\r\n" % (key.raw, value.raw)
            elif frmt is str:
                headers += "{}: {}\r\n".format(key.string, value.string)

        if frmt is bytes:
            msg = b"%b\r\n%b\r\n%b" % (first_line, headers, body)
        elif frmt is str:
            msg = "{}\r\n{}\r\n{}".format(first_line, headers, body)

        if frmt is str and arrow:
            arrow_msg = [
                "{} {}".format(arrow, line) for line in msg.splitlines() if line
            ]
            return "\r\n".join(arrow_msg)
        else:
            return msg

    # ----- Conversions -----

    @abc.abstractmethod
    def _compile_first_line(self) -> None:  # pragma: no cover
        """Compiles the first line of the message.

        Notes:
            Sets self._first_line to self.protocol; self.method or self.status;
            self.target or self.status_msg.
        """
        raise NotImplementedError

    # ================ Properties ================

    # Protocol, headers, and body are the three
    # shared properties between an HTTP request, and
    # response.

    @property
    def protocol(self) -> Item:
        """Protocol of the message."""
        return self._protocol

    @protocol.setter
    def protocol(self, value: ItemType) -> None:
        self._protocol = Item(value)

    @property
    def headers(self) -> Headers:
        """Headers of the message."""
        return self._headers

    @headers.setter
    def headers(self, value: Union[dict, Headers, None]) -> None:
        if not isinstance(value, dict):
            raise TypeError("can only set to type that inherits from 'dict'.")

        if isinstance(value, Headers):
            self._headers = value
        else:
            self._headers = Headers(value)

    @property
    def body(self) -> Item:
        """Body of the message."""
        return self._body

    @body.setter
    def body(self, value: ItemType) -> None:
        self._body = Item(value)

    @property
    def first_line(self) -> Item:
        """First line of the Message.

        Returns:
            The first line of the Message.
        """

        self._compile_first_line()
        return self._first_line

    @property
    def __items__(self) -> dict:
        """Fast retrieval of the Message's content.

        Returns:
            Dictionary with the message's protocol, headers, and body.
        """
        return {"protocol": self.protocol, "headers": self.headers, "body": self.body}

    # ----- Compiled Properties -----

    @property
    def string(self) -> str:
        """String representation of the Message.

        Returns:
            Message as a string, without any arrows.
        """

        return self._compile(frmt=str)

    @property
    def raw(self) -> bytes:
        """Bytes representation of the Message.

        Returns:
            Message as a bytes, without arrows, properly escaped.
        """
        return self._compile(frmt=bytes)


class Request(Message):
    __slots__ = ["_method", "_target"]

    def __init__(
        self,
        method: ItemType,
        target: ItemType,
        protocol: HeadersType,
        headers: ItemType = None,
        body: ItemType = None,
    ) -> None:
        """Python object representation of an HTTP/1.x request."

        Args:
            method: Indicates the desired action on the server's resource.
            target: Resource location in the server for which the client is requesting.
            protocol: "<major>.<minor>" numbering scheme to indicate versions of the
                protocol.
            headers: Collection of case-insensitive name followed by a colon (:).
            body: Data associated with the message.
        """

        self._method = Item(method)
        self._target = Item(target)

        super().__init__(protocol, headers, body)

        first_line = (self._method.raw, self._target.raw, self._protocol.raw)
        self._first_line = Item(b"%b %b %b" % first_line)

    # ================ Compilation ================

    def _compile_first_line(self) -> None:
        """Compiles the first line of the message.

        Notes:
            Sets self._first_line to self.protocol, self.method, self.target.
        """
        first_line = (self._method.raw, self._target.raw, self._protocol.raw)
        self._first_line = Item(b"%b %b %b" % first_line)

    # ================ Properties ================

    @property
    def method(self) -> Item:
        """Method of the HTTP request."""
        return self._method

    @method.setter
    def method(self, value: ItemType) -> None:
        self._method = Item(value)

    @property
    def target(self) -> Item:
        """Target of the HTTP request."""
        return self._target

    @target.setter
    def target(self, value: ItemType) -> None:
        self._target = Item(value)

    @property
    def __items__(self) -> dict:
        """Items corresponding to the Request."""
        return {
            **super().__items__,
            **{
                "method": self.method,
                "target": self.target,
            },
        }

    # ================ Misc ================

    def __str__(self) -> str:
        """String representation of the Request.

        Returns:
            Representation of the Request object with pretty-print (→) arrows.
        """
        return self._compile(frmt=str, arrow="→")


class Response(Message):
    __slots__ = ["_status", "_status_msg"]

    def __init__(
        self,
        protocol: ItemType,
        status: ItemType,
        status_msg: ItemType,
        headers: HeadersType = None,
        body: ItemType = None,
    ) -> None:
        """Python object representation of an HTTP/1.x response.

        Args:
            protocol: "<major>.<minor>" numbering scheme to indicate versions of the
                protocol.
            status: Numberical value designating a specific return value.
            status_msg: Message related to the status code.
            headers: Collection of case-insensitive name followed by a colon (:).
            body: Data associated with the message.
        """

        self._status = Item(status)
        self._status_msg = Item(status_msg)

        super().__init__(protocol, headers, body)

        first_line = self._protocol.raw, self._status.raw, self._status_msg.raw
        self._first_line = Item(b"%b %b %b" % first_line)

    # ================ Compilation ================

    def _compile_first_line(self) -> None:
        """Compiles the first line of the message.

        Notes:
            Sets self._first_line to self.protocol, self.status, self.status_msg.
        """
        first_line = self._protocol.raw, self._status.raw, self._status_msg.raw
        self._first_line = Item(b"%b %b %b" % first_line)

    # ================ Properties ================

    @property
    def status(self) -> Item:
        """Status of the HTTP response."""
        return self._status

    @status.setter
    def status(self, value: ItemType) -> None:
        self._status = Item(value)

    @property
    def status_msg(self) -> Item:
        """Status message of the HTTP response."""
        return self._status_msg

    @status_msg.setter
    def status_msg(self, value: ItemType) -> None:
        self._status_msg = Item(value)

    @property
    def __items__(self) -> dict:
        """Items corresponding to the Response."""

        return {
            **super().__items__,
            **{
                "status": self.status,
                "status_msg": self.status_msg,
            },
        }

    # ================ Misc ================

    def __str__(self) -> str:
        """String representation of the Response.

        Returns:
            Representation of the Response object with pretty-print (←) arrows.
        """
        return self._compile(frmt=str, arrow="←")
