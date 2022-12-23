from unittest import TestCase
from unittest.mock import patch

from clients.http import HTTPClient


class HTTPClientTest(TestCase):
    def test_get(self):

        http_client = HTTPClient()
        url = "https://www.google.com"
        headers = {"Accept": "text/plain"}

        with patch("requests.get") as patched_get:
            http_client.get(url, headers)
            patched_get.assert_called_once_with(url, headers)
