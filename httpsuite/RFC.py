# -*- coding: utf-8 -*-
""" Collection of RFC specifications related to HTTP requests and responses.

Every item in this file is commented with it's specific specification, chapter, and section number.
To access these specifications, utilize the URL https://tools.ietf.org/html/<id>.
"""

from .interface import FrozenSet, TwoWayFrozenDict

# Core Rules
# rfc5234#appendix-B.1
CR = b"\r"
LF = b"\n"


# Protocols
PROTOCOLS = FrozenSet(
    {
        "HTTP/0.9",  # rfc1945#section-3.1
        "HTTP/1.0",  # rfc1945#section-3.1
        "HTTP/1.1",  # rfc7231
        "HTTP/2.0",  # rfc7540
        "HTTP/3.0",  # draft-ietf-quic-http-27
    }
)


# Request Method Definitions
# rfc7231#section-4
REQUEST_METHODS = FrozenSet(
    {
        "GET",  # rfc7231#section-4.3.1
        "HEAD",  # rfc7231#section-4.3.2
        "POST",  # rfc7231#section-4.3.3
        "PUT",  # rfc7231#section-4.3.4
        "DELETE",  # rfc7231#section-4.3.5
        "CONNECT",  # rfc7231#section-4.3.6
        "OPTIONS",  # rfc7231#section-4.3.7
        "TRACE",  # rfc7231#section-4.3.8
    }
)

# Request Header Fields
# rfc7231#section-5
REQUEST_HEADERS = FrozenSet(
    {
        # Control
        # rfc7231#section-4
        "Cache-Control",  # rfc7234#section-5.2
        "Except",  # rfc7231#section-5.1.1
        "Host",  # rfc7230#section-5.4
        "Max-Forwards",  # rfc7231#section-5.1.2
        "Pragma",  # rfc7234#section-5.4
        "Range",  # rfc7233#section-3.1"
        "TE",  # rfc7230#section-4.3
        # Conditionals
        # rfc7231#section-5.2
        "If-Match",  # rfc7232#section-3.1
        "If-None-Match",  # rfc7232#section-3.2
        "If-Modified-Since",  # rfc7232#section-3.3
        "If-Unmodified-Since",  # rfc7232#section-3.4
        "If-Range",  # rfc7233#section-3.2
        # Content Negotiation
        # rfc7231#section-5.3
        "Accept",  # rfc7231#section-5.3.2
        "Accept-Charset",  # rfc7231#section-5.3.3
        "Accept-Encoding",  # rfc7231#section-5.3.4
        "Accept-Language",  # rfc7231#section-5.3.5
        # Authentication Credentials
        # rfc7231#section-5.4
        "Authorization",
        "Proxy-Authorization",
        # Request Context
        # rfc7231#section-5.5
        "From",  # rfc7231#section-5.5.1
        "Referer",  # rfc7231#section-5.5.2
        "User-Agent",  # rfc7231#section-5.5.3
    }
)

# Response Status Code
# rfc7231#section-6
RESPONSE_STATUS = TwoWayFrozenDict(
    {
        # Informational 1xx
        # rfc7231#section-6.2
        100: "Continue",  # rfc7231#section-6.2.1
        101: "Switching Protocols",  # rfc7231#section-6.2.2
        # Successful 2xx
        # rfc7231#section-6.3
        200: "OK",  # rfc7231#section-6.3.1
        201: "Created",  # rfc7231#section-6.3.2
        202: "Accepted",  # rfc7231#section-6.3.3
        203: "Non-Authoritative Information",  # rfc7231#section-6.3.4
        204: "No Content",  # rfc7231#section-6.3.5
        205: "Reset Content",  # rfc7231#section-6.3.6
        206: "Partial Content",  # rfc7233#section-4.1
        # Redirection 3xx
        # rfc7231#section-6.4
        300: "Multiple Choices",  # rfc7231#section-6.4.1
        301: "Moved Permanently",  # rfc7231#section-6.4.2
        302: "Found",  # rfc7231#section-6.4.3
        303: "See Other",  # rfc7231#section-6.4.4
        304: "Not Modified",  # rfc7232#section-4.1
        305: "Use Proxy",  # rfc7231#section-6.4.5
        307: "Temporary Redirect",  # rfc7231#section-6.4.7
        # Client Error 4xx
        # rfc7231#section-6.5
        400: "Bad Request",  # rfc7231#section-6.5.1
        401: "Unauthorized",  # rfc7235#section-3.1
        402: "Payment Required",  # rfc7231#section-6.5.2
        403: "Forbidden",  # rfc7231#section-6.5.3
        404: "Not Found",  # rfc7231#section-6.5.4
        405: "Method Not Allowed",  # rfc7231#section-6.5.5
        406: "Not Acceptable",  # rfc7231#section-6.5.6
        407: "Proxy Authentication Required",  # rfc7235#section-3.2
        408: "Request Timeout",  # rfc7231#section-6.5.7
        409: "Conflict",  # rfc7231#section-6.5.8
        410: "Gone",  # rfc7231#section-6.5.9
        411: "Length Required",  # rfc7231#section-6.5.10
        412: "Precondition Failed",  # rfc7232#section-4.2
        413: "Payload Too Large",  # rfc7231#section-6.5.11
        414: "URI Too Long",  # rfc7231#section-6.5.12
        415: "Unsupported Media Type",  # rfc7231#section-6.5.13
        416: "Range Not Satisfiable",  # rfc7233#section-4.4
        417: "Expectation Failed",  # rfc7231#section-6.5.14
        426: "Upgrade Required",  # rfc7231#section-6.5.15
        # Server Error 5xx
        # rfc7231#section-6.6
        500: "Internal Server Error",  # rfc7231#section-6.6.1
        501: "Not Implemented",  # rfc7231#section-6.6.2
        502: "Bad Gateway",  # rfc7231#section-6.6.3
        503: "Service Unavailable",  # rfc7231#section-6.6.4
        504: "Gateway Timeout",  # rfc7231#section-6.6.5
        505: "HTTP Version Not Supported",  # rfc7231#section-6.6.6
    }
)

# Response Header Fields
# rfc7231#section-7
RESPONSE_HEADER = FrozenSet(
    {
        # Control Data
        # rfc7231#section-7.1
        "Age",  # rfc7234#section-5.1
        "Cache-Control",  # rfc7234#section-5.2
        "Expires",  # rfc7234#section-5.3
        "Date",  # rfc7231#section-7.1.1.2
        "Location",  # rfc7231#section-7.1.2
        "Retry-After",  # rfc7231#section-7.1.3
        "Vary",  # rfc7231#section-7.1.4
        "Warning",  # rfc7234#section-5.5
        # Validator Header Fields
        # rfc7231#section-7.2
        "ETag",  # rfc7232#section-2.3
        "Last-Modified",  # rfc7232#section-2.2
        # Authentication Challenges
        # rfc7231#section-7.3
        "WWW-Authenticate",  # rfc7235#section-4.1
        "Proxy-Authenticate",  # rfc7235#section-4.3
        # Response Context
        # rfc7231#section-7.4
        "Accept-Ranges",  # rfc7233#section-2.3
        "Allow",  # rfc7231#section-7.4.1
        "Server",  # rfc7231#section-7.4.2
    }
)
