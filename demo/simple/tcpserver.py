"""tcp server."""
import socket
import time

port = 6000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('127.0.0.1', port))

server.listen()

print('Server ready')

while True:
    conn, addr = server.accept()
    print('Accept new conn from %s:%s' % addr)
    req = conn.recv(1024)

    content = req.upper()
    conn.send(content)
    conn.close()
