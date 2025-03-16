import socket
import threading
import random
import string
from utils.logger import setup_logger
from core.authentication import is_token_valid
import time
from collections import defaultdict

class TCPRemoteControl:
    def __init__(self, server_host, server_port, local_host, local_port, auth_token=None, rate_limit=100, max_connections=10):
        self.server_host = server_host
        self.server_port = server_port
        self.local_host = local_host
        self.local_port = local_port
        self.auth_token = auth_token
        self.rate_limit = rate_limit  # Max connections per minute
        self.max_connections = max_connections
        self.blocked_ips = set()
        self.connection_attempts = defaultdict(int)  # Track connection attempts by IP
        self.server_socket = None
        self.active_connections = 0
        self.logger = setup_logger('tcp_remote', 'tcp_remote.log')

    def generate_random_url(self):
        """Generate a random URL for the tunnel."""
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"https://{random_string}.ngrok-clone.io"

    def start(self):
        """Start the TCP server to handle remote connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_host, self.server_port))
        self.server_socket.listen(5)
        self.logger.info(f"TCP Remote Control Server listening on {self.server_host}:{self.server_port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_ip = client_address[0]

            # Check if IP is blocked
            if client_ip in self.blocked_ips:
                self.logger.warning(f"Blocked IP {client_ip} attempted to connect.")
                client_socket.close()
                continue

            # Check rate limit
            if self.active_connections >= self.max_connections:
                self.logger.warning("Max connections reached. Closing connection.")
                client_socket.close()
                continue

            # Track connection attempts
            self.connection_attempts[client_ip] += 1
            if self.connection_attempts[client_ip] > 5:  # Block IP after 5 failed attempts
                self.logger.warning(f"Blocking IP {client_ip} due to suspicious activity.")
                self.blocked_ips.add(client_ip)
                client_socket.close()
                continue

            # Authenticate client
            if self.auth_token:
                try:
                    token = client_socket.recv(1024).decode()
                    if not is_token_valid(token):
                        self.logger.warning(f"Invalid token from {client_ip}. Closing connection.")
                        client_socket.close()
                        continue
                except Exception as e:
                    self.logger.error(f"Error during authentication: {e}")
                    client_socket.close()
                    continue

            self.active_connections += 1
            threading.Thread(target=self.handle_client, args=(client_socket, client_ip)).start()

    def handle_client(self, client_socket, client_ip):
        """Handle the communication between the remote client and the local device."""
        try:
            local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            local_socket.connect((self.local_host, self.local_port))
            self.logger.info(f"Connected to local device at {self.local_host}:{self.local_port}")

            # Start forwarding data between the client and the local device
            threading.Thread(target=self.forward, args=(client_socket, local_socket)).start()
            threading.Thread(target=self.forward, args=(local_socket, client_socket)).start()
        except Exception as e:
            self.logger.error(f"Error handling client {client_ip}: {e}")
            client_socket.close()
        finally:
            self.active_connections -= 1

    def forward(self, source, destination):
        """Forward data from source to destination."""
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)
        except Exception as e:
            self.logger.error(f"Error during forwarding: {e}")
        finally:
            source.close()
            destination.close()

    def stop(self):
        """Stop the TCP server."""
        if self.server_socket:
            self.server_socket.close()
            self.logger.info("TCP Remote Control Server stopped.")
