from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import requests

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Forward the request to the local service
        local_service_url = f'http://localhost:8000{self.path}'
        response = requests.get(local_service_url)
        
        # Send response back to the client
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)

    def do_POST(self):
        # Forward the request to the local service
        local_service_url = f'http://localhost:8000{self.path}'
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        response = requests.post(local_service_url, data=post_data, headers=self.headers)
        
        # Send response back to the client
        self.send_response(response.status_code)
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response.content)

def run_http_proxy(server_class=HTTPServer, handler_class=ProxyHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting HTTP proxy on port {port}...')
    httpd.serve_forever()

def start_http_proxy_thread(port=8080):
    thread = threading.Thread(target=run_http_proxy, args=(HTTPServer, ProxyHTTPRequestHandler, port))
    thread.daemon = True
    thread.start()

# This function can be called to start the HTTP proxy
start_http_proxy_thread()