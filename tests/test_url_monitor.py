import hashlib
from unittest.mock import patch
import requests

from url_monitor import get_website_hash

def test_get_website_hash_success():
    mock_content = b"<html><body>Hello World!</body></html>"
    expected_hash = hashlib.sha256(mock_content).hexdigest()

    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = mock_content

        assert get_website_hash("http://test.com") == expected_hash

def test_get_website_hash_failure():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")
        assert get_website_hash("http://test.com") is None
