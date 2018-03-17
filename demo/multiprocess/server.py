"""multiprocess server."""
import os
import sys
import socket
import signal

port = 6000

try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('127.0.0.1', port))
except Exception as error:
    print('===', error)

server.listen()

print('Server ready')


def chldhanlder(signum, stackframe):
    try:
        pid, status = os.waitpid(-1, os.WNOHANG)
    except OSError:
        pass


signal.signal(signal.SIGCHLD, chldhanlder)

try:
    while True:
        conn, addr = server.accept()
        print('Accept new conn from %s:%s' % addr)
        pid = os.fork()
        if pid == 0:
            data = conn.recv(1024)
            conn.send(data)
            conn.close()
            sys.exit()
        else:
            conn.close()
except KeyboardInterrupt:
    print('\nexit with KeyboardInterrupt')
except Exception as error:
    print(error)
    server.close()
