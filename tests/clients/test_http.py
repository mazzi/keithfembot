from unittest import TestCase
from unittest.mock import patch

import pytest
import requests

from clients.http import HTTPClient
from exceptions import HTTPError


class HTTPClientTest(TestCase):
    def test_get(self):

        http_client = HTTPClient()
        url = "https://www.google.com"
        headers = {"Accept": "text/plain"}

        with patch("requests.get") as patched_get:
            http_client.get(url, headers)
            patched_get.assert_called_once_with(url, headers)

    def test_get_throws_exception(self):
        http_client = HTTPClient()
        url = "https://www.google.com"
        headers = {"Accept": "text/plain"}

        with patch("requests.get") as patched_get:
            patched_get.side_effect = requests.exceptions.ConnectionError()
            with pytest.raises(HTTPError) as exc_info:
                http_client.get(url, headers)
                assert "Connection Error" in exc_info.value

            patched_get.assert_called_once_with(url, headers)
