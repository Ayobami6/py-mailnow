"""Tests for Mailnow SDK client."""

import pytest


class TestMailnowClientInitialization:
    """Tests for MailnowClient initialization."""

    def test_init_with_none_api_key(self):
        """Test that MailnowClient raises MailnowAuthError when api_key is None."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowAuthError

        with pytest.raises(MailnowAuthError) as exc_info:
            MailnowClient(api_key=None)

        assert "API key" in str(exc_info.value)

    def test_init_with_empty_api_key(self):
        """Test that MailnowClient raises MailnowAuthError when api_key is empty."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowAuthError

        with pytest.raises(MailnowAuthError) as exc_info:
            MailnowClient(api_key="")

        assert "API key" in str(exc_info.value)

    def test_init_with_invalid_format_api_key(self):
        """Test that MailnowClient raises MailnowAuthError for invalid API key format."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowAuthError

        with pytest.raises(MailnowAuthError) as exc_info:
            MailnowClient(api_key="invalid_key_format")

        assert "API key must start with" in str(exc_info.value)

    def test_init_with_valid_live_api_key(self):
        """Test that MailnowClient initializes successfully with valid live API key."""
        from mailnow.client import MailnowClient

        # Should not raise any exception
        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")
        assert client is not None

    def test_init_with_valid_test_api_key(self):
        """Test that MailnowClient initializes successfully with valid test API key."""
        from mailnow.client import MailnowClient

        # Should not raise any exception
        client = MailnowClient(api_key="mn_test_abc123def456")
        assert client is not None

    def test_init_creates_http_client_instance(self):
        """Test that MailnowClient creates an HTTPClient instance during initialization."""
        from mailnow.client import MailnowClient
        from mailnow.http_client import HTTPClient

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        # Verify HTTPClient instance is created
        assert hasattr(client, "_http_client")
        assert isinstance(client._http_client, HTTPClient)

    def test_init_stores_api_key_in_http_client(self):
        """Test that MailnowClient passes API key to HTTPClient."""
        from mailnow.client import MailnowClient

        api_key = "mn_live_7e59df7ce4a14545b443837804ec9722"
        client = MailnowClient(api_key=api_key)

        # Verify API key is stored in HTTPClient
        assert client._http_client.api_key == api_key


class TestMailnowClientSendEmail:
    """Tests for MailnowClient send_email method."""

    def test_send_email_with_valid_parameters(self):
        """Test that send_email successfully sends email with valid parameters."""
        from mailnow.client import MailnowClient
        from unittest.mock import Mock

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        # Mock the HTTPClient's send_email_request method
        mock_response = {"success": True, "message_id": "msg_abc123"}
        client._http_client.send_email_request = Mock(return_value=mock_response)

        response = client.send_email(
            from_email="sender@example.com",
            to_email="recipient@example.com",
            subject="Test Subject",
            html="<h1>Test Email</h1>",
        )

        # Verify response is returned correctly
        assert response == mock_response
        assert response["success"] is True
        assert response["message_id"] == "msg_abc123"

    def test_send_email_builds_correct_payload(self):
        """Test that send_email builds the correct payload for HTTPClient."""
        from mailnow.client import MailnowClient
        from unittest.mock import Mock

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        # Mock the HTTPClient's send_email_request method
        mock_response = {"success": True}
        client._http_client.send_email_request = Mock(return_value=mock_response)

        client.send_email(
            from_email="sender@example.com",
            to_email="recipient@example.com",
            subject="Test Subject",
            html="<h1>Test Email</h1>",
        )

        # Verify the correct payload was passed to HTTPClient
        expected_payload = {
            "from": "sender@example.com",
            "to": "recipient@example.com",
            "subject": "Test Subject",
            "html": "<h1>Test Email</h1>",
        }
        client._http_client.send_email_request.assert_called_once_with(expected_payload)

    def test_send_email_with_missing_from_email(self):
        """Test that send_email raises MailnowValidationError for missing from_email."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="<h1>Test Email</h1>",
            )

        assert "from_email" in str(exc_info.value).lower()

    def test_send_email_with_missing_to_email(self):
        """Test that send_email raises MailnowValidationError for missing to_email."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="sender@example.com",
                to_email="",
                subject="Test Subject",
                html="<h1>Test Email</h1>",
            )

        assert "to_email" in str(exc_info.value).lower()

    def test_send_email_with_missing_subject(self):
        """Test that send_email raises MailnowValidationError for missing subject."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="sender@example.com",
                to_email="recipient@example.com",
                subject="",
                html="<h1>Test Email</h1>",
            )

        assert "subject" in str(exc_info.value).lower()

    def test_send_email_with_missing_html(self):
        """Test that send_email raises MailnowValidationError for missing html."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="sender@example.com",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="",
            )

        assert "html" in str(exc_info.value).lower()

    def test_send_email_with_invalid_from_email_format(self):
        """Test that send_email raises MailnowValidationError for invalid from_email format."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="invalid-email",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="<h1>Test Email</h1>",
            )

        assert "email address format" in str(exc_info.value).lower()

    def test_send_email_with_invalid_to_email_format(self):
        """Test that send_email raises MailnowValidationError for invalid to_email format."""
        from mailnow.client import MailnowClient
        from mailnow.exceptions import MailnowValidationError

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        with pytest.raises(MailnowValidationError) as exc_info:
            client.send_email(
                from_email="sender@example.com",
                to_email="invalid-email",
                subject="Test Subject",
                html="<h1>Test Email</h1>",
            )

        assert "email address format" in str(exc_info.value).lower()

    def test_send_email_returns_response_from_http_client(self):
        """Test that send_email returns the response from HTTPClient."""
        from mailnow.client import MailnowClient
        from unittest.mock import Mock

        client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

        # Mock different response structures
        mock_response = {
            "success": True,
            "message_id": "msg_xyz789",
            "status": "queued",
        }
        client._http_client.send_email_request = Mock(return_value=mock_response)

        response = client.send_email(
            from_email="sender@example.com",
            to_email="recipient@example.com",
            subject="Test Subject",
            html="<h1>Test Email</h1>",
        )

        # Verify the exact response is returned
        assert response == mock_response
        assert response["message_id"] == "msg_xyz789"
        assert response["status"] == "queued"
