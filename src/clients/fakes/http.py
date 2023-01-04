import config
from exceptions import HTTPError


class FakeHTTPClient:
    """Fake only to test external services (not airtime) due to the headers."""

    def __init__(self, http_client=None):
        self.http_client = http_client

    def get(self, url, headers=None):
        """HTTP GET"""

        if url == config.DADJOKE_URL:
            if not headers.keys() & {"User-Agent", "Accept"}:
                raise HTTPError("User-Agent and Accept is needed for this service.")
            return (
                "what do you call a dog that can do magic tricks?" " a labracadabrador"
            )
