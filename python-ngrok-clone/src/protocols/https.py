from flask import Flask, request, jsonify
import ssl
import socket
import threading

class HTTPSProtocol:
    def __init__(self, local_port, public_port, certfile, keyfile):
        self.local_port = local_port
        self.public_port = public_port
        self.certfile = certfile
        self.keyfile = keyfile
        self.app = Flask(__name__)

        @self.app.route('/', methods=['GET', 'POST'])
        def handle_request():
            if request.method == 'POST':
                return self.forward_request(request)
            return "HTTPS Tunnel is active."

    def forward_request(self, request):
        local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_socket.connect(('localhost', self.local_port))
        local_socket.sendall(request.data)
        response = local_socket.recv(4096)
        local_socket.close()
        return response

    def start(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
        self.app.run(port=self.public_port, ssl_context=context)

def run_https_tunnel(local_port, public_port, certfile, keyfile):
    https_tunnel = HTTPSProtocol(local_port, public_port, certfile, keyfile)
    https_tunnel.start()

def start_tunnel_thread(local_port, public_port, certfile, keyfile):
    tunnel_thread = threading.Thread(target=run_https_tunnel, args=(local_port, public_port, certfile, keyfile))
    tunnel_thread.start()