import socket
import signal
import os

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def grim_reaper(signum, frame):
    while True:
        try:
            pid, status = os.waitpid(
                -1,         # Wait for any child processes
                os.WNOHANG  # Do not block and return EWOULDBLOCK error
            )
        except OSError:
            return

        if pid == 0:    # No more zombies
            return


def handle_request(client_connection):
    request_data = client_connection.recv(1024)
    print(
        "Child PID: {pid}. Parent PID: {ppid}".format(
            pid=os.getpid(),
            ppid=os.getppid(),
        ))
    print(request_data.decode("utf-8"))

    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print("Serving HTTP on port {port} ...".format(port=PORT))
    print("Parent PID (PPID): {pid}\n".format(pid=os.getpid()))

    signal.signal(signal.SIGCHLD, grim_reaper)

    while True:
        """
        try:
            client_connection, client_address = listen_socket.accept()
        except IOError as e:
            code, msg = e.args
            # restart 'accept' if it was interrupted
            if code == errno.EINTR:
                continue
            else:
                raise
        """
        client_connection, client_address = listen_socket.accept()

        # fork() returns twice; once in the parent process and once in the
        # child. We can check which process the code is running in by examining
        # the PID. Child processes are assigned PID 0, while the parent retains
        # the PID assigned when the script is first run.
        pid = os.fork()
        if pid == 0:    # child
            # Close the child copy of listen_socket because the child doesn't
            # care about accepting new connections
            listen_socket.close()
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)     # child exits here
        else:
            client_connection.close()   # close parent copy


if __name__ == "__main__":
    serve_forever()
