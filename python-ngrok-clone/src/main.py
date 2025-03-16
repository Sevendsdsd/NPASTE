from flask import Flask
import argparse
from core.tunnel_manager import TunnelManager
from utils.logger import setup_logger
from init import initialize
from protocols.tcp_remote import TCPRemoteControl
from web.dashboard import start_dashboard

app = Flask(__name__)

# Initialize configuration and logger
config_loader, logger = initialize()

tunnel_manager = TunnelManager()

@app.route('/tunnels', methods=['GET'])
def list_tunnels():
    return tunnel_manager.list_tunnels()

@app.route('/tunnels', methods=['POST'])
def create_tunnel():
    return tunnel_manager.create_tunnel()

@app.route('/tunnels/<tunnel_id>', methods=['DELETE'])
def stop_tunnel(tunnel_id):
    return tunnel_manager.stop_tunnel(tunnel_id)

def main():
    parser = argparse.ArgumentParser(description='Start the ngrok clone server.')
    parser.add_argument('--port', type=int, default=config_loader.get('server_port', 5000), help='Port to run the server on.')
    parser.add_argument('--tcp-remote', action='store_true', help='Enable TCP remote control.')
    parser.add_argument('--tcp-port', type=int, default=9000, help='Port for TCP remote control.')
    parser.add_argument('--local-port', type=int, default=8080, help='Local port to forward TCP traffic to.')
    parser.add_argument('--dashboard', action='store_true', help='Enable the dashboard.')
    args = parser.parse_args()

    if args.dashboard:
        start_dashboard()
    elif args.tcp_remote:
        logger.info(f"Starting TCP Remote Control on port {args.tcp_port}...")
        remote_control = TCPRemoteControl('0.0.0.0', args.tcp_port, 'localhost', args.local_port)
        try:
            remote_control.start()
        except KeyboardInterrupt:
            remote_control.stop()
    else:
        logger.info(f"Starting server on port {args.port}...")
        app.run(host='0.0.0.0', port=args.port)

if __name__ == '__main__':
    main()