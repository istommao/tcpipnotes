# https://pymotw.com/3/socket/tcp.html
# socket_echo_client.py
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:
    # Send data
    sock.sendall(b'hello world')
    data = sock.recv(1024)
    print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
