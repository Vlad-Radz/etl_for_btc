"""
Here are the unit tests for the class HTTPConnection from the module api_caller.py.

They can be used as they are, just by executing the module.

These tests can be improved in various ways:
    - they should be faster
    - mock server can be probably improved
    - Execution of tests is not automated yet (for example, with Travis CI
"""
import unittest
import http
import json
from http.server import HTTPServer
from threading import Thread
import os.path
from pathlib import Path

from werkzeug.serving import make_ssl_devcert

import api_caller.app.api_caller as api_caller
from api_caller.test.mock_server import get_free_port, MockServerRequestHandler


mock_port = get_free_port()
mock_users_url = 'http://localhost:{port}/users'.format(port=mock_port)
headers = {'username': 'Vlad',
           'password': '2019'}

if not (os.path.isfile("dev.crt") and os.path.isfile("dev.key")):
    root_path = Path(__file__).resolve().parent
    make_ssl_devcert(str(root_path) + "\\dev", host='localhost')

ssl_api = {'keyfile': 'dev.key',
           'certfile': 'dev.crt'}


class TestHTTPConnection(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_server = HTTPServer(('localhost', mock_port), MockServerRequestHandler)
        self.mock_server_thread = Thread(target=self.mock_server.serve_forever)
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

        self.con1 = api_caller.HTTPConnection(mock_users_url, None, None)
        self.con2 = api_caller.HTTPConnection(mock_users_url, ssl_api, None)
        self.con3 = api_caller.HTTPConnection(mock_users_url, None, headers)

    def testReadingConnection(self):
        response_simple = self.con1.get_data()
        self.assertIsInstance(response_simple, http.client.HTTPResponse)
        response_simple_data = json.loads(response_simple.read())
        self.assertEqual(response_simple_data['status'], 'OK')

    def testSSLArgs(self):
        response_ssl = self.con2.get_data()
        self.assertIsInstance(response_ssl, http.client.HTTPResponse)
        response_ssl_data = json.loads(response_ssl.read())
        self.assertEqual(response_ssl_data['status'], 'OK')

    def testAddingHeaders(self):
        response_headers = self.con3.get_data()
        self.assertIsInstance(response_headers, http.client.HTTPResponse)
        response_headers_data = json.loads(response_headers.read())
        self.assertEqual(response_headers_data['status'], 'OK')

    def tearDown(self) -> None:
        self.mock_server.shutdown()
