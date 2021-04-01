####
http
####

.. code-block:: python

  from httpsuite.http import Message, Request, Response

.. automodule:: httpsuite.http

-------

.. autoclass:: Message(abc.ABC)

  .. automethod:: Message.__init__

  .. centered::
    **Parse**
  
  .. method:: Message.parse(message)

    Parses the passed ``messaged`` into a ``cls`` instance (either a :class:`Request` or :class:`Response` object).

    :param message: The primative or object to convert into a Request or Response object.

    :returns: An initialized object of class ``cls``.

    :raises RequiredAwait: Attempting to parse asynchronous object without 'await' statement.

  .. centered::
    **Properties**

  .. note::

    The ``Message.raw()`` function will return the message with proper ``\r\n`` escape characters. It can be
    used directly with ``sockets`` or any low-level communication system that requires properly formatted HTTP
    messages.

  .. autoproperty:: Message.string

  .. autoproperty:: Message.raw 

  .. centered::
    **HTTP**

  .. note::
    
    All HTTP properties are saved as an :class:`Item` type. Modification and comparissons can be done on the fly.

  .. autoproperty:: Message.protocol

  .. autoproperty:: Message.headers

  .. autoproperty:: Message.body

-------

.. autoclass:: Request(Message)

  .. automethod:: Request.__init__

  .. automethod:: Request.__str__

  .. centered::
    **HTTP**

  .. note::
    
    Note that Request is a child object of a Message and therefore has access to :py:attr:`Message.headers`, 
    :py:attr:`Message.headers`, and :py:attr:`Message.body`.

  .. autoproperty:: Request.method

  .. autoproperty:: Request.target

-------

.. autoclass:: httpsuite.http.Response

  .. automethod:: Response.__init__

  .. automethod:: Response.__str__

  .. centered::
    **HTTP**

  .. note::

    Note that Response is a child object of a Message and therefore has access to :py:attr:`Message.headers`, 
    :py:attr:`Message.headers`, and :py:attr:`Message.body`.

  .. autoproperty:: Response.status

  .. autoproperty:: Response.status_msg
