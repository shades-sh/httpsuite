# -*- coding: utf-8 -*-
""" Lower-level interfaces that ``httpsuite`` depedents on. """

from toolbox.collections.mapping import (
    BidirectionalDict,
    FrozenDict,
    ItemDict,
    ObjectDict,
    UnderscoreAccessDict,
)


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
        All the keys and values inside TwoWayFrozenDict are Item objects, which allows
        easy comparissions to check if an item is inside the TwoWayFrozenDict mapping.
    """


class FrozenSet(frozenset):
    """A frozen set with pretty-print."""

    def __str__(self):
        """String representation of the FrozenSet.

        Returns:
            String representation of the FrozenSet.
        """
        return str({k for k in self})
