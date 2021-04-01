# -*- coding: utf-8 -*-
""" Lower-level interfaces that ``httpsuite`` depedents on. """

from typing import Iterable, Union

from toolbox.collections.item import ENCODE, Item
from toolbox.collections.mapping import (
    BidirectionalDict,
    FrozenDict,
    ItemDict,
    ObjectDict,
    UnderscoreAccessDict,
)

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
            When the format is bytes this function will return the headers in bytes format with the
            correct HTTP escape characters "\r\n". This does **not** occur when string is passed as
            the format (new lines are created instead).

        Args:
            format: Either bytes or str. Formats the return accordingly to the passed format.

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


class TwoWayFrozenDict(
    BidirectionalDict,
    FrozenDict,
    ItemDict,
    ObjectDict,
    UnderscoreAccessDict,
):
    """A frozen dictionary with two-way capabilities. Locks a dictionary in place after
    initilization, and provides accessability via key and value.

    Note:
        All the keys and values inside TwoWayFrozenDict are Item objects, which allows easy
        comparissions to check if an item is inside the TwoWayFrozenDict mapping.
    """


class FrozenSet(frozenset):
    """A frozen set with pretty-print. """

    def __str__(self):
        """String representation of the FrozenSet.

        Returns:
            String representation of the FrozenSet.
        """
        return str({k for k in self})
