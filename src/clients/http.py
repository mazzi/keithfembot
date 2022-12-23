import requests

from exceptions import HTTPError


class HTTPClient:
    """Requests encapsulation"""

    def __init__(self, http_client=None):
        self.http_client = http_client or requests

    def get(self, url, headers=None):
        """HTTP GET"""
        try:
            response = self.http_client.get(url, headers)
            response.raise_for_status()
        except self.http_client.HTTPError as exec:
            raise HTTPError(str(exec)) from exec

        return response.text
