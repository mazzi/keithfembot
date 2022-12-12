import config
from exceptions import HTTPError


class FakeHTTPClient:
    def __init__(self, http_client=None):
        self.http_client = http_client

    def get(self, service_url, headers=None):
        """HTTP GET"""

        match service_url:
            case config.DADJOKE_URL:
                if not headers.keys() & {"User-Agent", "Accept"}:
                    raise HTTPError("User-Agent and Accept is needed for this service.")
                return (
                    "what do you call a dog that can do magic tricks?"
                    " a labracadabrador"
                )
            case config.KEITHFEM_BASE_URL:
                return ""

    def post(self):
        """HTTP POST"""
        # TBD
        pass

    def delete(self):
        """HTTP DELETE"""
        # TBD
        pass
