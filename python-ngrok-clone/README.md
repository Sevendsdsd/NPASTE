# python-ngrok-clone

## Overview
This project is a Python-based implementation of a secure tunneling service, similar to ngrok. It allows users to expose local services to the internet through secure tunnels, supporting HTTP, HTTPS, and TCP protocols.

## Features
- Secure tunneling from a public endpoint to local services
- Support for HTTP, HTTPS, and TCP protocols
- End-to-end encryption with TLS
- Token-based authentication system
- Real-time traffic observability
- Compatible with Kali Linux and Windows systems

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-ngrok-clone.git
   cd python-ngrok-clone
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Generate default configuration and certificates:
   ```
   python src/init.py
   ```

## Usage
To start the application, run the following command:
```
python src/main.py --port 5000
```

## TCP Remote Control
To enable TCP remote control, use the `--tcp-remote` flag. This allows remote devices to connect to a public TCP port and forward traffic to a local device.

### Example
Start the TCP remote control server:
```
python src/main.py --tcp-remote --tcp-port 9000 --local-port 8080
```

This will forward traffic from `0.0.0.0:9000` to `localhost:8080`.

## Configuration
The application uses a `config.json` file for settings. You can modify this file to adjust logging, certificates, and server settings.

### Example Configuration
```json
{
    "log_file": "ngrok_clone.log",
    "cert_file": "selfsigned_cert.pem",
    "key_file": "private_key.pem",
    "server_port": 5000,
    "allowed_api_keys": ["example_api_key_123"]
}
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.