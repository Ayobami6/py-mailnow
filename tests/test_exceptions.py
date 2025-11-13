"""Tests for Mailnow SDK exception classes."""

import pytest


class TestMailnowError:
    """Tests for the base MailnowError exception."""

    def test_mailnow_error_is_exception(self):
        """Test that MailnowError inherits from Exception."""
        from mailnow.exceptions import MailnowError

        assert issubclass(MailnowError, Exception)

    def test_mailnow_error_with_message(self):
        """Test that MailnowError can be created with a message."""
        from mailnow.exceptions import MailnowError

        error = MailnowError("Test error message")
        assert str(error) == "Test error message"

    def test_mailnow_error_can_be_raised(self):
        """Test that MailnowError can be raised and caught."""
        from mailnow.exceptions import MailnowError

        with pytest.raises(MailnowError) as exc_info:
            raise MailnowError("Test error")

        assert str(exc_info.value) == "Test error"


class TestMailnowValidationError:
    """Tests for MailnowValidationError exception."""

    def test_inherits_from_mailnow_error(self):
        """Test that MailnowValidationError inherits from MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowValidationError

        assert issubclass(MailnowValidationError, MailnowError)

    def test_validation_error_with_message(self):
        """Test that MailnowValidationError can be created with a message."""
        from mailnow.exceptions import MailnowValidationError

        error = MailnowValidationError("Invalid email address")
        assert str(error) == "Invalid email address"

    def test_validation_error_can_be_raised(self):
        """Test that MailnowValidationError can be raised and caught."""
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            raise MailnowValidationError("Validation failed")

        assert str(exc_info.value) == "Validation failed"

    def test_can_be_caught_as_mailnow_error(self):
        """Test that MailnowValidationError can be caught as MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowValidationError

        with pytest.raises(MailnowError):
            raise MailnowValidationError("Validation failed")


class TestMailnowAuthError:
    """Tests for MailnowAuthError exception."""

    def test_inherits_from_mailnow_error(self):
        """Test that MailnowAuthError inherits from MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowAuthError

        assert issubclass(MailnowAuthError, MailnowError)

    def test_auth_error_with_message(self):
        """Test that MailnowAuthError can be created with a message."""
        from mailnow.exceptions import MailnowAuthError

        error = MailnowAuthError("Invalid API key")
        assert str(error) == "Invalid API key"

    def test_auth_error_can_be_raised(self):
        """Test that MailnowAuthError can be raised and caught."""
        from mailnow.exceptions import MailnowAuthError

        with pytest.raises(MailnowAuthError) as exc_info:
            raise MailnowAuthError("Authentication failed")

        assert str(exc_info.value) == "Authentication failed"

    def test_can_be_caught_as_mailnow_error(self):
        """Test that MailnowAuthError can be caught as MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowAuthError

        with pytest.raises(MailnowError):
            raise MailnowAuthError("Authentication failed")


class TestMailnowRateLimitError:
    """Tests for MailnowRateLimitError exception."""

    def test_inherits_from_mailnow_error(self):
        """Test that MailnowRateLimitError inherits from MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowRateLimitError

        assert issubclass(MailnowRateLimitError, MailnowError)

    def test_rate_limit_error_with_message(self):
        """Test that MailnowRateLimitError can be created with a message."""
        from mailnow.exceptions import MailnowRateLimitError

        error = MailnowRateLimitError("Rate limit exceeded")
        assert str(error) == "Rate limit exceeded"

    def test_rate_limit_error_can_be_raised(self):
        """Test that MailnowRateLimitError can be raised and caught."""
        from mailnow.exceptions import MailnowRateLimitError

        with pytest.raises(MailnowRateLimitError) as exc_info:
            raise MailnowRateLimitError("Too many requests")

        assert str(exc_info.value) == "Too many requests"

    def test_can_be_caught_as_mailnow_error(self):
        """Test that MailnowRateLimitError can be caught as MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowRateLimitError

        with pytest.raises(MailnowError):
            raise MailnowRateLimitError("Rate limit exceeded")


class TestMailnowServerError:
    """Tests for MailnowServerError exception."""

    def test_inherits_from_mailnow_error(self):
        """Test that MailnowServerError inherits from MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowServerError

        assert issubclass(MailnowServerError, MailnowError)

    def test_server_error_with_message(self):
        """Test that MailnowServerError can be created with a message."""
        from mailnow.exceptions import MailnowServerError

        error = MailnowServerError("Internal server error")
        assert str(error) == "Internal server error"

    def test_server_error_can_be_raised(self):
        """Test that MailnowServerError can be raised and caught."""
        from mailnow.exceptions import MailnowServerError

        with pytest.raises(MailnowServerError) as exc_info:
            raise MailnowServerError("Server error occurred")

        assert str(exc_info.value) == "Server error occurred"

    def test_can_be_caught_as_mailnow_error(self):
        """Test that MailnowServerError can be caught as MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowServerError

        with pytest.raises(MailnowError):
            raise MailnowServerError("Server error")


class TestMailnowConnectionError:
    """Tests for MailnowConnectionError exception."""

    def test_inherits_from_mailnow_error(self):
        """Test that MailnowConnectionError inherits from MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowConnectionError

        assert issubclass(MailnowConnectionError, MailnowError)

    def test_connection_error_with_message(self):
        """Test that MailnowConnectionError can be created with a message."""
        from mailnow.exceptions import MailnowConnectionError

        error = MailnowConnectionError("Connection failed")
        assert str(error) == "Connection failed"

    def test_connection_error_can_be_raised(self):
        """Test that MailnowConnectionError can be raised and caught."""
        from mailnow.exceptions import MailnowConnectionError

        with pytest.raises(MailnowConnectionError) as exc_info:
            raise MailnowConnectionError("Network error")

        assert str(exc_info.value) == "Network error"

    def test_can_be_caught_as_mailnow_error(self):
        """Test that MailnowConnectionError can be caught as MailnowError."""
        from mailnow.exceptions import MailnowError, MailnowConnectionError

        with pytest.raises(MailnowError):
            raise MailnowConnectionError("Connection failed")


class TestExceptionHierarchy:
    """Tests for the complete exception hierarchy."""

    def test_all_exceptions_inherit_from_mailnow_error(self):
        """Test that all custom exceptions inherit from MailnowError."""
        from mailnow.exceptions import (
            MailnowError,
            MailnowValidationError,
            MailnowAuthError,
            MailnowRateLimitError,
            MailnowServerError,
            MailnowConnectionError,
        )

        assert issubclass(MailnowValidationError, MailnowError)
        assert issubclass(MailnowAuthError, MailnowError)
        assert issubclass(MailnowRateLimitError, MailnowError)
        assert issubclass(MailnowServerError, MailnowError)
        assert issubclass(MailnowConnectionError, MailnowError)

    def test_all_exceptions_inherit_from_exception(self):
        """Test that all custom exceptions ultimately inherit from Exception."""
        from mailnow.exceptions import (
            MailnowError,
            MailnowValidationError,
            MailnowAuthError,
            MailnowRateLimitError,
            MailnowServerError,
            MailnowConnectionError,
        )

        assert issubclass(MailnowError, Exception)
        assert issubclass(MailnowValidationError, Exception)
        assert issubclass(MailnowAuthError, Exception)
        assert issubclass(MailnowRateLimitError, Exception)
        assert issubclass(MailnowServerError, Exception)
        assert issubclass(MailnowConnectionError, Exception)
