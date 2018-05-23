"""epoll server."""
import socket
import select

EOL1 = b'\n\n'
EOL2 = b'\n\r\n'


response = """HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Lenght:13\r\n\r\nHello world!"""

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

port = 8080
server.bind(('0.0.0.0', port))
server.listen()
server.setblocking(0)

epoll = select.epoll()
epoll.register(server.fileno(), select.EPOLLIN)

print('Server listen http://127.0.0.1:{}/'.format(port))

try:
    conns = {}
    requests = {}
    responses = {}

    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == server.fileno():
                conn, addr = server.accept()
                conn.setblocking(0)
                epoll.register(conn.fileno(), select.EPOLLIN)
                conns[conn.fileno()] = conn
                requests[conn.fileno()] = b''
                responses[conn.fileno()] = response
            elif event & select.EPOLLIN:
                if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                    epoll.modify(fileno, select.EPOLLOUT)
                    print('-' * 40 + '\n' + requests[fileno].decode()[:-2])
            elif event & select.EPOLLOUT:
                bytesdata = conns[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][bytesdata:]
                if len(responses[fileno]) == 0:
                    epoll.modify(fileno, 0)
                    conns[fileno].shutdown(socket.SHUT_RDWR)
            elif event & select.EPOLLHUP:
                epoll.unregister(fileno)
                conns[fileno].close()
                del conns[fileno]
except KeyboardInterrupt:
    pass
finally:
    epoll.unregister(server.fileno())
    epoll.close()
    server.close()
