"""epoll server."""
import socket

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'

response = """HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Lenght:13\r\n\r\nHello world!"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8080

server.bind(('127.0.0.1', port))

server.listen(1)


print('Server listen http://127.0.0.1:{}/'.format(port))


conn, addr = server.accept()

print('Accept new connection from %s:%s' % addr)

request = b''
while EOL1 not in request and EOL2 not in request:
    request += conn.recv(1024)

print(request.decode())
conn.send(response.encode())
conn.close()
