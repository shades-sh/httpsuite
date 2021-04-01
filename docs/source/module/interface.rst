#########
interface
#########

.. code-block:: python

  from httpsuite.interface import Item, Headers, TwoWayFrozenDict, FrozenSet

.. automodule:: httpsuite.interface

-------

.. autoclass:: Headers
  
  .. automethod:: Headers.__init__

  .. centered::
    **Properties**

  .. autoproperty:: Headers.string

  .. autoproperty:: Headers.raw

  .. centered::
    **Operations**

  All of the operations below evaluate to true unless specificed.

  .. method:: Headers.__add__

    .. code-block:: python

      Headers({"hello": "world"}) + {"hey": "you"} == {"hello": "world", "hey": "you"}

  .. method:: Headers.__iadd__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h += {"hey": "you"}
      h == {"hello": "world", "hey": "you"}

  Setting and getting attributes automatically uses ``_`` as the same as ``-``.

  .. method:: Headers.__setattr__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h['hello-world'] = 'ola mundo'
      
  .. method:: Headers.__getattr__

    .. code-block:: python

      h = Headers({"hello": "world"})
      h['hello-world'] = 'ola mundo'
      h['hello-world'] == h.hello_world

  .. method:: Headers.__str__

    .. code-block:: python

      str(Headers({"hello": "world"})) # 'hello: world'

  .. method:: Headers.__repr__

    .. code-block:: python

      repr(Headers({"hello": "world"})) # 'Headers(hello: world)'

-------

.. autoclass:: TwoWayFrozenDict
  :members:

-------

.. autoclass:: FrozenSet
  :members:
