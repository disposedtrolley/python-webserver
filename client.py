import socket

# Create a socket and connect to a server.
# Unlike the server, the client does not need to call
# bind or accept. This is because the client doesn't
# care about its local IP and port; the kernel will
# automatically assign an ephemeral port.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 8888))

# Send and receive some data
sock.sendall(b"test")
data = sock.recv(1024)
print(data.decode())

