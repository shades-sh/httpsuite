####
http
####

.. code-block:: python

  from httpsuite.http import Message, Request, Response

.. automodule:: httpsuite.http

-------

.. autoclass:: httpsuite.http.Message(abc.ABC)

  .. automethod:: httpsuite.http.Message.__init__

  .. centered::
    **Parse**
  
  .. method:: httpsuite.http.Message.parse(message)

    Parses the passed ``messaged`` into a ``cls`` instance (either a :class:`Request` or :class:`Response` object).

    :param message: The primative or object to convert into a Request or Response object.

    :returns: An initialized object of class ``cls``.

    :raises RequiredAwait: Attempting to parse asynchronous object without 'await' statement.

  .. centered::
    **Properties**

  .. note::

    The ``httpsuite.http.Message.raw()`` function will return the message with proper ``\r\n`` escape characters. It can be
    used directly with ``sockets`` or any low-level communication system that requires properly formatted HTTP
    messages.

  .. autoproperty:: httpsuite.http.Message.string

  .. autoproperty:: httpsuite.http.Message.raw 

  .. centered::
    **HTTP**

  .. note::
    
    All HTTP properties are saved as an :class:`Item` type. Modification and comparissons can be done on the fly.

  .. autoproperty:: httpsuite.http.Message.protocol

  .. autoproperty:: httpsuite.http.Message.headers

  .. autoproperty:: httpsuite.http.Message.body

-------

.. autoclass:: httpsuite.http.Request(Message)

  .. automethod:: httpsuite.http.Request.__init__

  .. automethod:: httpsuite.http.Request.__str__

  .. centered::
    **HTTP**

  .. note::
    
    Note that Request is a child object of a Message and therefore has access to :py:attr:`httpsuite.http.Message.headers`, 
    :py:attr:`httpsuite.http.Message.headers`, and :py:attr:`httpsuite.http.Message.body`.

  .. autoproperty:: httpsuite.http.Request.method

  .. autoproperty:: httpsuite.http.Request.target

-------

.. autoclass:: httpsuite.http.Response

  .. automethod:: httpsuite.http.Response.__init__

  .. automethod:: httpsuite.http.Response.__str__

  .. centered::
    **HTTP**

  .. note::

    Note that Response is a child object of a Message and therefore has access to :py:attr:`httpsuite.http.Message.headers`, 
    :py:attr:`httpsuite.http.Message.headers`, and :py:attr:`httpsuite.http.Message.body`.

  .. autoproperty:: httpsuite.http.Response.status

  .. autoproperty:: httpsuite.http.Response.status_msg
