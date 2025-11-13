"""Tests for the HTTP client module."""

import httpx
import pytest

from mailnow.http_client import HTTPClient
from mailnow.constants import API_BASE_URL, REQUEST_TIMEOUT


class TestHTTPClientInitialization:
    """Tests for HTTPClient initialization."""

    def test_init_with_api_key_and_default_base_url(self) -> None:
        """Test HTTPClient initialization with API key and default base URL."""
        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        assert client.api_key == api_key
        assert client.base_url == API_BASE_URL
        assert isinstance(client.client, httpx.Client)

    def test_init_with_api_key_and_custom_base_url(self) -> None:
        """Test HTTPClient initialization with API key and custom base URL."""
        api_key = "mn_test_abc456"
        custom_url = "https://custom.api.example.com"
        client = HTTPClient(api_key=api_key, base_url=custom_url)

        assert client.api_key == api_key
        assert client.base_url == custom_url
        assert isinstance(client.client, httpx.Client)

    def test_httpx_client_configured_with_timeout(self) -> None:
        """Test that httpx client is properly configured with timeout."""
        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        # Verify the httpx client has the correct timeout configuration
        assert client.client.timeout == httpx.Timeout(REQUEST_TIMEOUT)


class TestSendEmailRequest:
    """Tests for HTTPClient send_email_request method."""

    def test_successful_post_request_with_proper_headers_and_payload(self) -> None:
        """Test successful POST request with proper headers and payload."""
        import respx
        from mailnow.constants import EMAIL_SEND_ENDPOINT

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test Subject",
            "html": "<h1>Test</h1>",
        }

        expected_response = {
            "success": True,
            "message_id": "msg_abc123",
            "status": "queued",
        }

        with respx.mock:
            route = respx.post(f"{API_BASE_URL}{EMAIL_SEND_ENDPOINT}").mock(
                return_value=httpx.Response(200, json=expected_response)
            )

            response = client.send_email_request(payload)

            assert response == expected_response
            assert route.called

            # Verify headers
            request = route.calls.last.request
            assert request.headers["Content-Type"] == "application/json"
            assert request.headers["X-API-Key"] == api_key

    def test_successful_response_parsing_2xx(self) -> None:
        """Test successful response parsing for 2xx status codes."""
        import respx

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        expected_response = {"success": True, "message_id": "msg_xyz"}

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                return_value=httpx.Response(201, json=expected_response)
            )

            response = client.send_email_request(payload)
            assert response == expected_response

    def test_http_400_maps_to_validation_error(self) -> None:
        """Test HTTP 400 maps to MailnowValidationError."""
        import respx
        from mailnow.exceptions import MailnowValidationError

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "invalid-email",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        error_response = {
            "error": {"code": "validation_error", "message": "Invalid email address"}
        }

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                return_value=httpx.Response(400, json=error_response)
            )

            with pytest.raises(MailnowValidationError) as exc_info:
                client.send_email_request(payload)

            assert "Invalid email address" in str(exc_info.value)

    def test_http_401_maps_to_auth_error(self) -> None:
        """Test HTTP 401 maps to MailnowAuthError."""
        import respx
        from mailnow.exceptions import MailnowAuthError

        api_key = "invalid_key"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        error_response = {"error": {"code": "auth_error", "message": "Invalid API key"}}

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                return_value=httpx.Response(401, json=error_response)
            )

            with pytest.raises(MailnowAuthError) as exc_info:
                client.send_email_request(payload)

            assert "Invalid API key" in str(exc_info.value)

    def test_http_429_maps_to_rate_limit_error(self) -> None:
        """Test HTTP 429 maps to MailnowRateLimitError."""
        import respx
        from mailnow.exceptions import MailnowRateLimitError

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        error_response = {
            "error": {"code": "rate_limit_error", "message": "Rate limit exceeded"}
        }

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                return_value=httpx.Response(429, json=error_response)
            )

            with pytest.raises(MailnowRateLimitError) as exc_info:
                client.send_email_request(payload)

            assert "Rate limit exceeded" in str(exc_info.value)

    def test_http_5xx_maps_to_server_error(self) -> None:
        """Test HTTP 5xx maps to MailnowServerError."""
        import respx
        from mailnow.exceptions import MailnowServerError

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        error_response = {
            "error": {"code": "server_error", "message": "Internal server error"}
        }

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                return_value=httpx.Response(500, json=error_response)
            )

            with pytest.raises(MailnowServerError) as exc_info:
                client.send_email_request(payload)

            assert "Internal server error" in str(exc_info.value)

    def test_network_errors_map_to_connection_error(self) -> None:
        """Test network errors map to MailnowConnectionError."""
        import respx
        from mailnow.exceptions import MailnowConnectionError

        api_key = "mn_live_test123"
        client = HTTPClient(api_key=api_key)

        payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test",
            "html": "<p>Test</p>",
        }

        with respx.mock:
            respx.post(f"{API_BASE_URL}/v1/email/send").mock(
                side_effect=httpx.ConnectError("Connection failed")
            )

            with pytest.raises(MailnowConnectionError) as exc_info:
                client.send_email_request(payload)

            assert "Connection failed" in str(exc_info.value)
