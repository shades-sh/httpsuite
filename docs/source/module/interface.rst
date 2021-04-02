#########
interface
#########

.. code-block:: python

  from httpsuite.interface import Item, Headers, TwoWayFrozenDict, FrozenSet

.. automodule:: httpsuite.interface

-------

.. autoclass:: httpsuite.interface.Headers
  
  .. automethod:: httpsuite.interface.Headers.__init__

  .. centered::
    **Properties**

  .. autoproperty:: httpsuite.interface.Headers.string

  .. autoproperty:: httpsuite.interface.Headers.raw

  .. centered::
    **Operations**

  All of the operations below evaluate to true unless specificed.

  .. method:: httpsuite.interface.Headers.__add__

    .. code-block:: python

      Headers({"hello": "world"}) + {"hey": "you"} == {"hello": "world", "hey": "you"}

  .. method:: httpsuite.interface.Headers.__iadd__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h += {"hey": "you"}
      h == {"hello": "world", "hey": "you"}

  Setting and getting attributes automatically uses ``_`` as the same as ``-``.

  .. method:: httpsuite.interface.Headers.__setattr__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h['hello-world'] = 'ola mundo'
      
  .. method:: httpsuite.interface.Headers.__getattr__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h['hello-world'] = 'ola mundo'
      h['hello-world'] == h.hello_world

  .. method:: httpsuite.interface.Headers.__str__

    .. code-block:: python

      str(Headers({"hello": "world"})) # 'hello: world'

  .. method:: httpsuite.interface.Headers.__repr__

    .. code-block:: python

      repr(Headers({"hello": "world"})) # 'Headers(hello: world)'

-------

.. autoclass:: httpsuite.interface.TwoWayFrozenDict
  :members:

-------

.. autoclass:: httpsuite.interface.FrozenSet
  :members:
