import socket
import json
from http.server import BaseHTTPRequestHandler

import requests


class MockServerRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(requests.codes.ok)

        # Add response headers.
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()

        # Add response content.
        response_content = json.dumps({'status': 'OK'})
        self.wfile.write(response_content.encode('utf-8'))
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port
