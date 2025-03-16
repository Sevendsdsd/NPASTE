from flask import Flask, render_template, jsonify, request
from core.tunnel_manager import TunnelManager
from utils.logger import setup_logger
from core.authentication import validate_api_key
from init import config_loader

app = Flask(__name__)
tunnel_manager = TunnelManager()
logger = setup_logger('web_interface', 'web_interface.log')

@app.route('/')
def index():
    """Render the web interface."""
    return render_template('web_interface.html')

@app.route('/api/tunnels', methods=['GET'])
def list_tunnels():
    """API endpoint to list active tunnels."""
    tunnels = tunnel_manager.list_tunnels()
    return jsonify({'tunnels': [tunnel.to_dict() for tunnel in tunnels]})

@app.route('/api/tunnels', methods=['POST'])
def create_tunnel():
    """API endpoint to create a new tunnel."""
    data = request.json
    api_key = request.headers.get('Authorization')
    if not validate_api_key(api_key, set(config_loader.get('allowed_api_keys', []))):
        logger.warning(f"Unauthorized attempt to create tunnel with API key: {api_key}")
        return jsonify({'error': 'Unauthorized'}), 401

    local_address = data.get('local_address')
    protocol = data.get('protocol', 'http')
    port = data.get('port', 80)
    if not local_address:
        return jsonify({'error': 'Local address is required'}), 400
    tunnel = tunnel_manager.create_tunnel(local_address, protocol, port)
    logger.info(f"Created tunnel: {tunnel.to_dict()}")
    return jsonify(tunnel.to_dict()), 201

@app.route('/api/tunnels/<tunnel_id>', methods=['DELETE'])
def delete_tunnel(tunnel_id):
    """API endpoint to delete a tunnel."""
    success = tunnel_manager.stop_tunnel(tunnel_id)
    if not success:
        return jsonify({'error': 'Tunnel not found'}), 404
    logger.info(f"Stopped tunnel: {tunnel_id}")
    return jsonify({'message': 'Tunnel stopped successfully'}), 200

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """API endpoint to fetch logs."""
    with open('web_interface.log', 'r') as log_file:
        logs = log_file.readlines()
    return jsonify({'logs': logs})

def start_web_interface():
    """Start the web interface server."""
    logger.info("Starting web interface on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001)
