from unittest.mock import patch

from django.test import SimpleTestCase
from httpx import HTTPStatusError

from src.utils.http import send_external_api_request


@patch("src.utils.http.httpx.Client.request")
class TestSendExternalApiRequest(SimpleTestCase):
    def test_send_external_api_request_success(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.text = "OK"
        response = send_external_api_request("GET", "http://test.com")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "OK")

    def test_send_external_api_request_failure(self, mock_request):
        mock_request.return_value.status_code = 400
        mock_request.return_value.text = "Not Found"
        mock_request.return_value.raise_for_status.side_effect = HTTPStatusError(
            "Error message", request=None, response=mock_request.return_value
        )

        with self.assertRaises(HTTPStatusError):
            send_external_api_request("GET", "http://test.com")
