"""tcp server."""
import socket

port = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('', port))

# 最大连接数 1
server.listen(1)

print('Server ready')

while True:
    conn, addr = server.accept()
    print('Accept new conn from %s:%s' % addr)
    req = conn.recv(1024)

    content = req.upper()
    conn.send(content)
    conn.close()
