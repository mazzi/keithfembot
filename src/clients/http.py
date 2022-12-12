import requests

from exceptions import HTTPError


class HTTPClient:
    def __init__(self, http_client=None):
        self.http_client = http_client or requests

    def get(self, service_url, headers=None):
        """HTTP GET"""
        try:
            response = self.http_client.get(service_url, headers)
            response.raise_for_status()
        except self.http_client.HTTPError as exec:
            raise HTTPError(str(exec)) from exec

        return response.text

    def post(self):
        """HTTP POST"""
        # TBD
        pass

    def delete(self):
        """HTTP DELETE"""
        # TBD
        pass
