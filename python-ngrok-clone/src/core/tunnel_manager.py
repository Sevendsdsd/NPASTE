from typing import List, Dict
import random
import string

class Tunnel:
    def __init__(self, tunnel_id: str, local_address: str, public_address: str, protocol: str, port: int):
        self.tunnel_id = tunnel_id
        self.local_address = local_address
        self.public_address = public_address
        self.protocol = protocol
        self.port = port

    def to_dict(self):
        """Convert the tunnel object to a dictionary."""
        return {
            "tunnel_id": self.tunnel_id,
            "local_address": self.local_address,
            "public_address": self.public_address,
            "protocol": self.protocol,
            "port": self.port
        }

class TunnelManager:
    def __init__(self):
        """Initialize the TunnelManager with an empty dictionary of tunnels."""
        self.tunnels: Dict[str, Tunnel] = {}

    def create_tunnel(self, local_address: str, protocol: str, port: int) -> Tunnel:
        """
        Create a new tunnel with a unique ID and public address.

        Args:
            local_address (str): The local address to forward traffic to (e.g., localhost:8080).
            protocol (str): The protocol of the tunnel (e.g., HTTP, HTTPS, TCP).
            port (int): The port to listen on.

        Returns:
            Tunnel: The created tunnel object.
        """
        tunnel_id = self._generate_tunnel_id()
        public_address = self._generate_public_address(tunnel_id)
        tunnel = Tunnel(tunnel_id, local_address, public_address, protocol, port)
        self.tunnels[tunnel_id] = tunnel
        return tunnel

    def list_tunnels(self) -> List[Tunnel]:
        """
        List all active tunnels.

        Returns:
            List[Tunnel]: A list of all active tunnel objects.
        """
        return list(self.tunnels.values())

    def stop_tunnel(self, tunnel_id: str) -> bool:
        """
        Stop and remove a tunnel by its ID.

        Args:
            tunnel_id (str): The ID of the tunnel to stop.

        Returns:
            bool: True if the tunnel was successfully stopped, False otherwise.
        """
        if tunnel_id in self.tunnels:
            del self.tunnels[tunnel_id]
            return True
        return False

    def _generate_tunnel_id(self) -> str:
        """
        Generate a random tunnel ID with 50 characters.

        Returns:
            str: A unique tunnel ID.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

    def _generate_public_address(self, tunnel_id: str) -> str:
        """
        Generate a public address for the tunnel using a dynamic domain.

        Args:
            tunnel_id (str): The unique ID of the tunnel.

        Returns:
            str: The public address for the tunnel.
        """
        return f"https://{tunnel_id}.mysecuretunnel.local"