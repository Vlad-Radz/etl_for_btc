"""
This program sends a request to an external service to get the actual exchange rate for 2 currencies.
Currently it gets exchange rate for USD -> EUR. It is implemented using the Flask framework, which is the most
simple framework to use in development projects for simple goals.

This program could be used more generic and get a base and a target currency as arguments from the client.

This program could be used even more generic and get the URL and the patterns for extracting required data for
the client. In this case this program could be reused in larger projects.
"""

import urllib.request
import ssl
import json
from operator import getitem
from functools import reduce
import sys
from typing import Optional

from flask import Flask


class HTTPConnection:
    """
        This class holds all the data and methods related to creating and handling the HTTP connection.

        ...

        Attributes
        ----------
        locator : str
            An URL address.
        ssl_args : Optional[Dict[str, str]]
            Data required to create a SSL connection. (if required).
            Are not being used now - is here to show how something like this could be implemented.
        headers : Optional[Dict[str, str]]
            HTTP headers (if required)
            Are not being used now - is here to show how something like this could be implemented.

        Methods
        -------
        get_data()
            Returns data from the specified URL address.
    """

    def __init__(self, locator: str, ssl_args: Optional[dict], headers: Optional[dict]):
        self.locator = locator
        self._build_connection(ssl_args, headers)

    def _build_connection(self, ssl_args: Optional[dict], headers: Optional[dict]):
        # created a request and adds SSL and headers, if necessary.
        self.req = urllib.request.Request(self.locator)
        self.context = None
        if headers:
            self._add_headers(headers)
        if ssl_args:
            self._setup_ssl(**ssl_args)

    def _add_headers(self, headers: dict):
        # headers are not being used now - is here to show how something like this could be implemented.
        for key, value in headers.items():
            self.req.add_header(key, value)

    def _setup_ssl(self, keyfile: str, certfile: str, password: Optional[str] = None, verify: Optional[bool] = None):
        # SSL is not being used now - is here to show how something like this could be implemented.
        self.context = ssl.create_default_context()
        self.context.load_cert_chain(keyfile=keyfile, certfile=certfile, password=password)
        if verify:
            self.context.load_verify_locations(verify)

    def get_data(self):
        response = urllib.request.urlopen(self.req, context=self.context)
        return response


URL = 'https://api.exchangeratesapi.io/latest?base=USD'
pattern_usd_eur = ['rates', 'EUR']

app = Flask(__name__)


@app.route('/')
def main():
    connection = HTTPConnection(URL, ssl_args=None, headers=None)
    exc_data = connection.get_data()
    response = json.loads(exc_data.read())

    value = reduce(getitem, pattern_usd_eur, response)  # fancy way to get a value from nested dict.

    return str(value)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
