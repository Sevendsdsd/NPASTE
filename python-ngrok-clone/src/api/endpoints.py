from flask import Blueprint, request, jsonify
from core.tunnel_manager import TunnelManager
from core.authentication import authenticate

api = Blueprint('api', __name__)
tunnel_manager = TunnelManager()

@api.route('/tunnels', methods=['POST'])
@authenticate
def create_tunnel():
    data = request.json
    protocol = data.get('protocol')
    local_address = data.get('local_address')
    if not protocol or not local_address:
        return jsonify({'error': 'Protocol and local address are required'}), 400
    tunnel = tunnel_manager.create_tunnel(protocol, local_address)
    return jsonify({'tunnel_id': tunnel.id, 'public_url': tunnel.public_url}), 201

@api.route('/tunnels', methods=['GET'])
@authenticate
def list_tunnels():
    tunnels = tunnel_manager.list_tunnels()
    return jsonify({'tunnels': [tunnel.to_dict() for tunnel in tunnels]}), 200

@api.route('/tunnels/<tunnel_id>', methods=['DELETE'])
@authenticate
def delete_tunnel(tunnel_id):
    success = tunnel_manager.stop_tunnel(tunnel_id)
    if not success:
        return jsonify({'error': 'Tunnel not found or could not be stopped'}), 404
    return jsonify({'message': 'Tunnel stopped successfully'}), 200

@api.route('/tunnels/traffic/<tunnel_id>', methods=['GET'])
@authenticate
def inspect_traffic(tunnel_id):
    traffic_data = tunnel_manager.get_traffic_data(tunnel_id)
    return jsonify({'traffic': traffic_data}), 200