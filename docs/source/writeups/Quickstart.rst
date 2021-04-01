##########
Quickstart
##########


**********
Installing
**********

To get started with ``httpsuite``, install the latest stable release from `PyPi <https://pypi.org/project/httpsuite/>`_:

.. code-block:: bash

  pip install httpsuite

***************
Getting Started
***************

There are two principal abstractions to be aware of it in ``httpsuite``, ``Request`` and ``Response``.

.. code-block:: python

  from httpsuite import Request, Response

These classes represent an HTTP/1.x request and response message, and offer a high-level API to :term:`modify`, 
:term:`compile`, and :term:`parse` them. The :class:`Request` and :class:`Response` can be initialized via two different
methods.

``__init__()``
==============

Create a :class:`Request` or :class:`Response` object with the given parameter.

.. code-block:: python
  
  from httpsuite import Request, Response

  request = Request(
      method="POST",
      target="/",
      protocol="HTTP/1.1",
      headers={"User-Agent": "httpsuite", "Content-Length": 12},
      body="Hello world."
  )

  response = Response(
      protocol="HTTP/1.1",
      status=200,
      status_msg="OK",
      headers={"User-Agent": "httpsuite", "Content-Length": 8},
      body="Hi back!"
  )

``.parse()``
============

Or, parse from `bytes` to create a new :class:`Request` or :class:`Response` with the given details.

``bytes``
---------

Most useful when using socket connections.

.. code-block:: python

  from httpsuite import Request, Response

  req = Request.parse(b"GET / HTTP/1.1\r\nUser-Agent: httpsuite\r\nContent-Length: 12\r\n\r\nHello world")
  resp = Response.parse(b"HTTP/1.1 200 OK\r\nUser-Agent: httpsuite\r\nContent-Length: 12\r\n\r\nHi back!")

******
Modify
******

The next probable step after initializing a :class:`Request` or :class:`Response` object is to :term:`modify` and 
:term:`compile`. Object modification is done as one would expect.

.. code-block:: python

  request.method = "POST"
  response.status = 300
  response.status_msg = b"Continue"

Notice that setting object properties is type-agnostic. Properties can be modified to either ``int``, ``str``, 
or ``bytes`` objects. Internally, ``httpsuite`` automatically converts every property of a :class:`request` or
:class:`response` into an :class:`Item`, which is a low-level interface to allow easy setting and comparissons on the
fly. Similarly to setting properties, one can be assured of type-agnostic property comparissions.

.. code-block:: python

  request.status == 300     # True
  request.status == "300"   # True
  request.status == b"300"  # True

*******
Compile
*******

After modifying a message compilation allows the :class:`Request` and :class:`Response` objects to be compiled into 
less maluable yet useful types. Those types being ``bytes`` or ``str``.

.. code-block:: python

  from httpsuite import Request, Response
  import json

  body = json.dumps({"hello": "world"})
  request = Request(
      method="POST",
      target="/post",
      protocol="HTTP/1.1",
      headers={
          "Host": "httpbin.org",
          "Connection": "close",
          "Content-Length": len(body),
          "Accept": "*/*",
      },
      body=body,
  )

``.raw``
=========

Useful to use with sockets.

.. code-block:: python

  print(request.raw)

.. code-block:: python

  b'POST /post HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\nContent-Length: 18\r\nAccept: */*\r\n\r\n{"hello": "world"}'

``__str__``
===========

Pretty print of the object.

.. code-block:: python

  print(request)

.. code-block::

  → POST /post HTTP/1.1
  → Host: httpbin.org
  → Connection: close
  → Content-Length: 18
  → Accept: */*
  → {"hello": "world"}


****
More 
****

If you finished this guide and want to continue learning more you can do so by reading the package's documentation found
on the left menu.
