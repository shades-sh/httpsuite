# -*- coding: utf-8 -*-
""" Collection of helper classes used through the project.

This module contain helper classes that are used throughout ``httpsuite``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Iterable, Union

from . import __ENCODE__


class Item:
    """Item provides an interface for ``string``, ``byte``, ``int``, and ``None``.

    Item is an interface between the original object (``str``, ``bytes``, ``int``,
    ``None``) that allows the user to do object-agnostic equality checks
    (i.e. ``Item(200) == Item("200") == Item(b"200")``), as well as retrieve the
    original item as either a ``string`` or ``bytes`` object.

    Note:
        ``Item`` will automatically convert the passed item into a ``bytes``
        object internally.

    Args:
        item (Union[str, bytes, int, Item]): input to be stored.
    """

    __slots__ = ["_item"]

    def __init__(self, item: Union[str, bytes, int, None, Item]) -> None:

        if (
            not isinstance(item, str)
            and not isinstance(item, bytes)
            and not type(item) is int  # isinstance(True, int) is True.
            and not item is None
            and not isinstance(item, Item)
        ):
            raise TypeError("item must inherit from str, bytes, or int.")
        elif isinstance(item, str):
            self._item = item.encode(__ENCODE__)
        elif isinstance(item, bytes):
            self._item = item
        elif isinstance(item, int):
            self._item = b"%d" % item
        elif item is None:
            self._item = b""
        elif isinstance(item, Item):
            self._item = item.raw

    @property
    def string(self) -> str:
        """String representation of the ``Item``.

        Returns:
            str: String representation of the ``Item`` object.
        """
        return self._item.decode(__ENCODE__)

    @property
    def raw(self) -> bytes:
        """Bytes representation of the ``Item``.

        Returns:
            bytes: Bytes representation of the ``Item`` object.
        """
        return self._item

    def __eq__(self, other: Union[str, bytes, int, Item]) -> bool:
        """Compares ``Item`` with passed ``other``.

        Args:
            other (Union[str, bytes, int, Item]): ``Item`` to be compared.

        Returns:
            bool: Represents if the ``Item`` is equal to ``other``.
        """
        if isinstance(other, str):
            item = other.encode(__ENCODE__)
        elif isinstance(other, int):
            item = str(other).encode(__ENCODE__)
        else:
            item = other

        return self._item == item

    def __add__(self, other: Union[str, bytes, int, Item]) -> Item:
        """Adds ``Item`` with passed ``other`` and returns new ``Item``.

        Args:
            other (Union[str, bytes, int, Item]): ``Item`` to be added.

        Return:
            Item: Returns new ``Item`` that is the addition of the current, and
            the passed.
        """
        if isinstance(other, str):
            item = other.encode(__ENCODE__)
        elif isinstance(other, int):
            item = str(other).encode(__ENCODE__)
        elif isinstance(other, Item):
            item = other._item
        else:
            item = other

        return Item(self._item + item)

    def __iadd__(self, other: Union[str, bytes, int, Item]) -> Item:
        """Adds ``Item`` with passed ``other`` and returns ``self`` after addition.

        Args:
            other (Union[str, bytes, int, Item]): ``Item`` to be added.

        Returns:
            Item: Returns current ``Item`` after addition with the passed.
        """
        if isinstance(other, str):
            item = other.encode(__ENCODE__)
        elif isinstance(other, int):
            item = str(other).encode(__ENCODE__)
        elif isinstance(other, Item):
            item = other._item
        else:
            item = other

        self._item += item
        return self

    def __hash__(self) -> int:
        """Hash representation of the current ``Item``.

        Returns:
            int: Hash representation of the ``Item``.
        """
        return hash(self._item)

    def __bool__(self) -> bool:
        """Boolean representation of the current ``Item``.

        Returns:
            bool: Bool representation of the ``Item``.
        """
        return bool(self._item)

    def __str__(self) -> str:
        """String representation of the ``Item`` object.

        Returns:
            str: String representation of the `Item` object.
        """
        return self.string


class Headers(dict):
    r"""Representation of a HTTP request or response headers object.

    ``Headers``, similiar to ``Item``, provides an interface for a HTTP request and
    response header, allowing easy manipulation, parsing, adding, and returning
    ``str`` and ``bytes`` version of itself. ``bytes`` version is escaped with ``\r\n``.

    Args:
        value (Union[dict, Headers]): `Headers` value in dictionary or
                                      `Headers` object.
    """

    def __init__(self, value: Union[None, dict, Headers] = None) -> None:
        if value is None:
            value = {}

        if not isinstance(value, dict) and not isinstance(value, Headers):
            raise TypeError("headers can only be of type that inherits from 'dict'.")

        if isinstance(value, dict):
            for key, value in value.items():
                self[Item(key)] = Item(value)

        super().__init__()

    def _compile(self, frmt: str = "bytes") -> Union[str, bytes]:
        r"""Compiles the ``Headers`` into the passed format.

        Notes:
            When the format is ``bytes`` this function will return the headers
            in bytes format with the correct HTTP escape characters ``\r\n``.
            This does **not** occur when ``string`` is passed as the format (new
            lines are created instead).

        Args:
            format (str): Either ``bytes`` or ``string``. Formats the return
                          accordingly to the passed format.

        Returns:
            Union[str, bytes]: String or bytes representation of the ``Headers``.
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

    @property
    def string(self) -> str:
        """String representation of the ``Headers``.

        Returns:
            str: String representation of the ``Headers``.
        """
        return self._compile(frmt="string")

    @property
    def raw(self) -> bytes:
        r"""Bytes representation of the ``Headers``.

        Note:
            This method will return ``Headers`` with ``\r\n`` escape characters.

        Returns:
            bytes: Bytes representation of the ``Headers``.
        """
        return self._compile(frmt="bytes")

    def __add__(self, other: Union[dict, Headers]) -> Headers:
        """Adds item with passed ``other`` and returns new ``Headers``.

        Args:
            other (Union[dict, Headers]): ``Headers`` or ``dict`` to be added.

        Returns:
            Headers: New resulting ``Headers`` object.
        """

        if not isinstance(other, dict) and not isinstance(other, Headers):
            raise TypeError("can only add with type that inherits from 'dict'.")

        if isinstance(other, Headers):
            current = self.copy()
            current.update(other)
            return Headers(current)
        elif isinstance(other, dict):
            itemized_values = {Item(k): Item(v) for k, v in other.items()}
            copy = self.copy()
            copy.update(itemized_values)
            return copy

    def __iadd__(self, other: Union[dict, Headers]) -> Headers:
        """Adds current headers with passed `other` and returns self.

        Args:
            other (Union[dict, Headers]): ``Headers`` or ``dict`` to be added.

        Returns:
            Headers: Self after addition to itself.
        """

        if not isinstance(other, dict) and not isinstance(other, Headers):
            raise TypeError("can only add with type that inherits from 'dict'.")

        itemized_values = {Item(k): Item(v) for k, v in other.items()}
        self.update(itemized_values)
        return self

    def __setattr__(self, key: str, value: str) -> None:
        """Sets a new attribute inside ``Headers``.

        Notes:
            If ``_`` is present in the key it gets replaced with ``-``. This is
            so the ``headers.User_Agent`` is equivalent to ``headers['User-Agent']``.
        """

        key_mod = key.replace("_", "-").encode(__ENCODE__)
        self[Item(key_mod)] = Item(value)

    def __getattr__(self, key: str) -> Item:
        """Gets attribute inside ``Headers``.

        Notes:
            If ``_`` is present in the key it gets replaced with ``-``. This is
            so the ``headers.User_Agent`` is equivalent to ``headers['User-Agent']``.

        Returns:
            Item: `Item` corresponding to the passed key.
        """

        key_mod = key.replace("_", "-").encode(__ENCODE__)

        if key_mod in self:
            return self[key_mod]
        else:
            return None

    def __str__(self) -> str:
        """String representation of the ``Headers``.

        Returns:
            str: String representation of the ``Headers``.
        """
        return self.string


@dataclass(frozen=True)
class TwoWayFrozenDict(Mapping):
    """A frozen dictionary with two-way capabilities.

    Interface that locks a dictionary in place after initilization, and provides
    accessability via key and value.

    Note:
        All the keys and values inside ``TwoWayFrozenDict`` are ``Item`` objects,
        which allows easy comparissions to check if an item is inside
        the ``TwoWayFrozenDict`` mapping.

    Args:
        data (dict): Dictionary that will use this interface.
    """

    def __init__(self, data: dict) -> None:
        self.__dict__.update({Item(k): Item(v) for k, v in data.items()})
        self.__dict__.update({Item(v): Item(k) for k, v in data.items()})

    def __getattribute__(self, key: str) -> Item:
        """Gets attribute inside ``Headers``.

        Notes:
            If ``_`` is present in the key it gets replaced with a blank space.
            This is so the ``frozendict.No_Content`` is equivalent to
            ``frozendict['No Content']``. The only exception is when it is an
            integer following ``_``, ``frozendict._200``, which will be interpret
            as ``frozendict[200]``.

        Returns:
            Item: ``Item`` corresponding to the passed key.
        """

        if not key.startswith("__"):
            status_message = key.replace("_", " ")
            status_code = key.replace("_", "")

            if status_message in self.__dict__:
                return self.__getitem__(status_message)
            elif status_code in self.__dict__:
                return self.__getitem__(status_code)

        return super().__getattribute__(key)

    def __contains__(self, key: str) -> bool:
        """Checks if the key is inside ``TwoWayFrozenDict``.

        Returns:
            bool: Boolean corresponding to if the passed key is inside the
            ``TwoWayFrozenDict``.
        """

        if Item(key) in self.__dict__:
            return True
        else:
            return False

    def __getitem__(self, key: str) -> Item:
        """Retrieves item that's mapped with the passed key.

        Returns:
            Item: ``Item`` corresponding to the passed key.
        """
        return self.__dict__[Item(key)]

    def __iter__(self) -> Iterable[Item]:
        """Returns an iterable representation of the ``TwoWayFrozenDict``.

        Returns:
            Iterable[Item]: Iterable of items.
        """
        return iter(self.__dict__)

    def __len__(self) -> int:
        """Returns the length of the ``TwoWayFrozenDict``.

        Returns:
            int: Length of the ``TwoWayFrozenDict``.
        """

        return len(self.__dict__)

    def __str__(self) -> str:
        """String representation of the ``TwoWayFrozenDict``.

        Returns:
            str: String representation of the ``TwoWayFrozenDict``.
        """
        return str({k.string: v.string for k, v in self.__dict__.items()})


class FrozenSet(frozenset):
    """ A frozen set with pretty-print. """

    def __str__(self):
        """String representation of the ``FrozenSet``.

        Returns:
            str: String representation of the ``FrozenSet``.
        """
        return str({k for k in self})
