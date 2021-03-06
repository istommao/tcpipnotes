"""tcp server."""
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

response = """HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n\r\nHello world!"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8060

server.bind(('127.0.0.1', port))

server.listen()


print('Server listen http://127.0.0.1:{}/'.format(port))

try:
    while True:
        conn, addr = server.accept()

        print('Accept new connection from %s:%s' % addr)

        request = b''
        while EOL1 not in request and EOL2 not in request:
            request += conn.recv(2048)

        print(request.decode())

        conn.send(response.encode())
        conn.close()
except KeyboardInterrupt:
    pass
finally:
    server.close()
