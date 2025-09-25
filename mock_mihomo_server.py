#!/usr/bin/env python3
"""
Mock Mihomo API server for testing purposes.
"""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time


class MockMihomoHandler(BaseHTTPRequestHandler):
    """Handler for mock Mihomo API requests."""
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == "/configs":
            # Health check endpoint
            response = {"mode": "rule", "port": 7890}
        elif path == "/rules":
            # Rules endpoint
            response = {
                "rules": [
                    {
                        "type": "DOMAIN",
                        "payload": "example.com",
                        "proxy": "Proxy"
                    },
                    {
                        "type": "DOMAIN-SUFFIX",
                        "payload": "google.com",
                        "proxy": "Proxy"
                    },
                    {
                        "type": "IP-CIDR",
                        "payload": "192.168.0.0/16",
                        "proxy": "DIRECT"
                    }
                ]
            }
        elif path == "/proxies":
            # Proxies endpoint
            response = {
                "proxies": {
                    "Proxy": {
                        "type": "Selector",
                        "now": "Proxy2",
                        "all": ["Proxy1", "Proxy2"]
                    },
                    "Proxy1": {
                        "type": "Shadowsocks",
                        "server": "server1.com",
                        "port": 8388
                    },
                    "Proxy2": {
                        "type": "VMess",
                        "server": "server2.com",
                        "port": 8443
                    },
                    "DIRECT": {
                        "type": "Direct"
                    }
                }
            }
        elif path == "/providers/rules":
            # Rule providers endpoint
            response = {
                "providers": {
                    "provider1": {
                        "name": "provider1",
                        "type": "http",
                        "updatedAt": "2023-01-01T00:00:00Z",
                        "vehicleType": "HTTP"
                    }
                }
            }
        else:
            # Default response
            response = {"message": "Mock Mihomo API"}
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to suppress default logging."""
        return


class MockMihomoServer:
    """Mock Mihomo API server."""
    
    def __init__(self, host='127.0.0.1', port=9091):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the mock server in a separate thread."""
        self.server = HTTPServer((self.host, self.port), MockMihomoHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        print(f"Mock Mihomo server started at http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the mock server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join()


if __name__ == "__main__":
    # Create and start the mock server
    mock_server = MockMihomoServer()
    mock_server.start()
    
    try:
        # Keep the server running
        print("Press Ctrl+C to stop the server")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping mock server...")
        mock_server.stop()
        print("Mock server stopped")