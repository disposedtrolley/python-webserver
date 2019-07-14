import socket
import argparse
import errno
import os

SERVER_ADDRESS = "localhost", 8888
REQUEST = b"""\
GET /hello HTTP/1.1
Host: localhost:8888

"""


def main(max_clients, max_conns):
    socks = []
    for client_num in range(max_clients):
        pid = os.fork()
        if pid == 0:
            for connection_num in range(max_conns):
                # Create a socket and connect to a server.
                # Unlike the server, the client does not need to call
                # bind or accept. This is because the client doesn't
                # care about its local IP and port; the kernel will
                # automatically assign an ephemeral port.
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(SERVER_ADDRESS)
                sock.sendall(REQUEST)
                socks.append(sock)
                print(connection_num)
                os._exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test client.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--max-conns",
        type=int,
        default=1024,
        help="Maximum number of connections per client."
    )
    parser.add_argument(
        "--max-clients",
        type=int,
        default=1,
        help="Maximum number of clients."
    )
    args = parser.parse_args()
    main(args.max_clients, args.max_conns)
