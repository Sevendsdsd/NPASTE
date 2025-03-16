import os
import json
from core.encryption import generate_self_signed_cert
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

DEFAULT_CONFIG = {
    "log_file": "ngrok_clone.log",
    "cert_file": "selfsigned_cert.pem",
    "key_file": "private_key.pem",
    "server_port": 5000,
    "allowed_api_keys": ["example_api_key_123"]
}

def initialize():
    # Load configuration
    config_path = os.path.join(os.getcwd(), 'config.json')
    if not os.path.exists(config_path):
        print(f"Configuration file not found. Creating default config at {config_path}...")
        with open(config_path, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)

    config_loader = ConfigLoader(config_path)

    # Set up logger
    log_file = config_loader.get('log_file', 'ngrok_clone.log')
    logger = setup_logger('ngrok_clone', log_file)

    # Generate self-signed certificates if not present
    cert_file = config_loader.get('cert_file', 'selfsigned_cert.pem')
    key_file = config_loader.get('key_file', 'private_key.pem')
    if not os.path.exists(cert_file) or not os.path.exists(key_file):
        logger.info("Generating self-signed certificates...")
        generate_self_signed_cert(cert_file, key_file)

    # Ensure the TCP remote log file exists
    tcp_remote_log = 'tcp_remote.log'
    if not os.path.exists(tcp_remote_log):
        open(tcp_remote_log, 'w').close()
        logger.info(f"Created empty log file: {tcp_remote_log}")

    logger.info("Initialization complete.")
    return config_loader, logger

if __name__ == "__main__":
    initialize()
    print("Initialization complete. Configuration and certificates are ready.")
