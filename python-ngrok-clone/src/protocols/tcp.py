from socket import socket, AF_INET, SOCK_STREAM
import threading

class TCPProxy:
    def __init__(self, local_host, local_port, remote_host, remote_port):
        self.local_host = local_host
        self.local_port = local_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.server = None

    def start(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.local_host, self.local_port))
        self.server.listen(5)
        print(f"Listening on {self.local_host}:{self.local_port}")

        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        remote_socket = socket(AF_INET, SOCK_STREAM)
        remote_socket.connect((self.remote_host, self.remote_port))

        def forward(source, destination):
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)

        threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
        threading.Thread(target=forward, args=(remote_socket, client_socket)).start()

    def stop(self):
        if self.server:
            self.server.close()
            print("Server stopped.")

# Example usage:
# if __name__ == "__main__":
#     proxy = TCPProxy('localhost', 8080, 'remote.server.com', 80)
#     try:
#         proxy.start()
#     except KeyboardInterrupt:
#         proxy.stop()