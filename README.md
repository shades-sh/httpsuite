<p align="center">

  <img src="https://i.imgur.com/LnNDqEE.png">
  <br><br>
  <a href="https://travis-ci.com/synchronizing/httpsuite">
    <img src="https://travis-ci.com/shades-sh/httpsuite.svg?branch=master">
  </a>

  <a href="https://synchronizing.github.io/httpsuite/">
    <img src="https://readthedocs.org/projects/pip/badge/?version=latest&style=flat">
  </a>

  <a href="https://coveralls.io/github/synchronizing/httpsuite?branch=master">
    <img src="https://coveralls.io/repos/github/synchronizing/httpsuite/badge.svg?branch=master">
  </a>

  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

`httpsuite` is a collection of tools to parse, manipulate, and compile raw HTTP messages. Built to be used as a dependency for larger projects that require parsing, modifying, requesting, and responding to raw HTTP requests.

## Installing

```
pip install httpsuite
```

This package was intentionally built to have no external dependencies outside of the [Python Standard Library](https://docs.python.org/3/library/). If you plan on contribute, then make sure to install the `dev-requirements.txt`.

## Documentation

Read the documentation [here](https://shades-sh.github.io/httpsuite/).

## Use

`httpsuite` provides two main objects, `Request` and `Response`. Both objects can be initialized with either `__init__` or `parse`:

```python
from httpsuite import Request, Response
import json

request = Request(
    method="GET",
    target="/",
    protocol="HTTP/1.1",
    headers={"Host": "www.google.com", "Connection": "keep-alive", "Content-Length": "18"},
    body=json.dumps({"hello": "world"}),
)

response = Response(
    protocol="HTTP/1.1",
    status=200,
    status_msg="OK",
    headers={"Host": "www.google.com", "Connection": "keep-alive", "Content-Length": "18"},
    body=json.dumps({"hello": "world"}),
)
```

or

```python
from httpsuite import Request, Response

request = Request.parse(
    (
        b"GET / HTTP/1.1\r\n"
        b"Host: www.google.com\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 18\r\n"
        b"\r\n"
        b'{"hello": "world"}'
    )
)

response = Response.parse(
    (
        b"HTTP/1.1 200 OK\r\n"
        b"Host: www.google.com\r\n"
        b"Connection: keep-alive\r\n"
        b"Content-Length: 18\r\n"
        b"\r\n"
        b'{"hello": "world"}'
    )
)
```

`Request` and `Responses` objects can be directly modified as one would expect, with no limitations as to the type:

```python
request.method = "POST"
request.headers += {"Accept": "*/*"}

response.status = 100
response.status_msg = b"Continue"
```

Internally, every item of a request or response is saved as an `Item`, a special object type that allows easy setting and comparisons on the fly:

```python
response.status == 100      # >>> True
response.status == "100"    # >>> True
response.status == b"100"   # >>> True
```

Once the object is modified to the users preference, utilizing the `Request` and `Response` object is as easy as calling a property (specifically `.raw`):

```python
print(request.raw)
# >>> b'POST / HTTP/1.1\r\nHost: www.google.com\r\nConnection: keep-alive\r\nContent-Length: 18\r\nAccept: */*\r\n\r\n{"hello": "world"}'

print(response.raw)
# >>> b'HTTP/1.1 100 Continue\r\nHost: www.google.com\r\nConnection: keep-alive\r\nContent-Length: 18\r\n\r\n{"hello": "world"}'
```

Uniquely, the `__str__` method for `Request` and `Response` return the objects with arrows to make obvious of its type:

```python
print(request)
print(response)
```

```
→ POST / HTTP/1.1
→ Host: www.google.com
→ Connection: keep-alive
→ Content-Length: 18
→ Accept: */*
→
→ {"hello": "world"}

← HTTP/1.1 100 Continue
← Host: www.google.com
← Connection: keep-alive
← Content-Length: 18
←
← {"hello": "world"}
```

For more information and examples of `httpsuite`, check out the [docs](https://synchronizing.github.io/httpsuite/).
