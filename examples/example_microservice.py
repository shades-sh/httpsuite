""" Very primative example of a socket microservice architecture using httpsuite.

Server and Client functions are ran through the 'multiprocessing' module, so
to act as two seperate entities. For the sake of clarity, only the server function
prints anything to console. Entities are documented seperately.
"""

from httpsuite import Request, Response
from multiprocessing import Process
import socket
import time


def server():
    """Simple socket server that uses httpsuite to interpret and reply.

    1. Opens a new socket.
    2. Binds to 127.0.0.1:8080 and waits until new connection.
    3. Accepts connection from external source.
    4. Receive the data from the client.
    5. Parse the clients request.
    6. Interpret the request.
    7. Reply to the client.
    8. Close the connection with the client.
    """

    # 1. Opens a new socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Binds to 127.0.0.1:8080 and waits until new connection.
    s.bind(("127.0.0.1", 8080))
    s.listen(1)

    # 3. Accepts connection from external source.
    conn, address = s.accept()

    print("===== Connecting With New Client =====", "\n")
    print(address, "\n")

    # 4. Receive the data from the client.
    data = conn.recv(1024)

    # 5. Parse the clients request.
    request = Request.parse(data)

    print("===== Received Data From Client =====", "\n")
    print(request, "\n")

    # 6. Interpret the request.
    response = Response(protocol="HTTP/1.1", status=200, status_msg="OK")
    if request.target == "/":
        response.body = "Homepage of the microservice."
    elif request.target == "/data":
        response.body = "You are accessing the /data directory of this microservice."
    else:
        response.status = 404
        response.status_msg = "Not Found"

    print("===== Replying to Client =====", "\n")
    print(response, "\n")

    # 7. Reply to the client.
    conn.sendall(response.raw)

    print("===== Closing Connection to Client =====", "\n")

    # 8. Close the connection with the client, and the server.
    conn.close()
    s.close()


def client():
    """Simple socket client that uses httpmodule to request server resource.

    1. Opens a new socket.
    2. Connects the server.
    3. Creates a valid request to send to the server.
    4. Sends the request.
    5. Receives reply from the server.
    6. Parses the reply from the server.
    7. Closes connection with the server.
    """

    # Note: Sleeps so that the socket server can boot-up before.
    time.sleep(1)

    # 1. Opens a new socket.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. Connects the server.
    s.connect(("127.0.0.1", 8080))

    # 3. Creates a valid request to send to the server.
    request = Request(method="GET", target="/", protocol="HTTP/1.1")

    # 4. Sends the request.
    s.sendall(request.raw)

    # 5. Receives reply from the server.
    data = s.recv(1024)

    # 6. Parses the reply from the server.
    response = Response.parse(data)

    # 7. Closes connection with the server.
    s.close()


if __name__ == "__main__":
    p1 = Process(target=server)
    p2 = Process(target=client)

    p1.daemon = True
    p2.daemon = True

    p1.start()
    p2.start()

    time.sleep(3)
    raise SystemExit
