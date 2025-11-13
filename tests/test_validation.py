"""Tests for Mailnow SDK validation functions."""

import pytest


class TestValidateApiKey:
    """Tests for validate_api_key function."""

    def test_validate_api_key_with_none(self):
        """Test that validate_api_key raises MailnowValidationError when api_key is None."""
        from mailnow.validation import validate_api_key
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_api_key(None)

        assert "API key is required" in str(exc_info.value)

    def test_validate_api_key_with_empty_string(self):
        """Test that validate_api_key raises MailnowValidationError when api_key is empty."""
        from mailnow.validation import validate_api_key
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_api_key("")

        assert "API key is required" in str(exc_info.value)

    def test_validate_api_key_with_whitespace_only(self):
        """Test that validate_api_key raises MailnowValidationError when api_key is whitespace."""
        from mailnow.validation import validate_api_key
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_api_key("   ")

        assert "API key is required" in str(exc_info.value)

    def test_validate_api_key_with_invalid_format(self):
        """Test that validate_api_key raises MailnowValidationError for invalid format."""
        from mailnow.validation import validate_api_key
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_api_key("invalid_key_format")

        assert "API key must start with" in str(exc_info.value)

    def test_validate_api_key_with_valid_live_key(self):
        """Test that validate_api_key accepts valid live API key."""
        from mailnow.validation import validate_api_key

        # Should not raise any exception
        validate_api_key("mn_live_7e59df7ce4a14545b443837804ec9722")

    def test_validate_api_key_with_valid_test_key(self):
        """Test that validate_api_key accepts valid test API key."""
        from mailnow.validation import validate_api_key

        # Should not raise any exception
        validate_api_key("mn_test_abc123def456")

    def test_validate_api_key_with_wrong_prefix(self):
        """Test that validate_api_key rejects keys with wrong prefix."""
        from mailnow.validation import validate_api_key
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_api_key("sk_live_wrongprefix")

        assert "API key must start with" in str(exc_info.value)


class TestValidateEmailAddress:
    """Tests for validate_email_address function."""

    def test_validate_email_with_valid_simple_email(self):
        """Test that validate_email_address accepts valid simple email."""
        from mailnow.validation import validate_email_address

        # Should not raise any exception
        validate_email_address("user@example.com")

    def test_validate_email_with_valid_subdomain(self):
        """Test that validate_email_address accepts email with subdomain."""
        from mailnow.validation import validate_email_address

        # Should not raise any exception
        validate_email_address("user@mail.example.com")

    def test_validate_email_with_plus_sign(self):
        """Test that validate_email_address accepts email with plus sign."""
        from mailnow.validation import validate_email_address

        # Should not raise any exception
        validate_email_address("user+tag@example.com")

    def test_validate_email_with_dots(self):
        """Test that validate_email_address accepts email with dots in local part."""
        from mailnow.validation import validate_email_address

        # Should not raise any exception
        validate_email_address("first.last@example.com")

    def test_validate_email_with_missing_at_symbol(self):
        """Test that validate_email_address rejects email without @ symbol."""
        from mailnow.validation import validate_email_address
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_address("userexample.com")

        assert "Invalid email address format" in str(exc_info.value)

    def test_validate_email_with_missing_domain(self):
        """Test that validate_email_address rejects email without domain."""
        from mailnow.validation import validate_email_address
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_address("user@")

        assert "Invalid email address format" in str(exc_info.value)

    def test_validate_email_with_missing_local_part(self):
        """Test that validate_email_address rejects email without local part."""
        from mailnow.validation import validate_email_address
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_address("@example.com")

        assert "Invalid email address format" in str(exc_info.value)

    def test_validate_email_with_spaces(self):
        """Test that validate_email_address rejects email with spaces."""
        from mailnow.validation import validate_email_address
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_address("user name@example.com")

        assert "Invalid email address format" in str(exc_info.value)

    def test_validate_email_with_empty_string(self):
        """Test that validate_email_address rejects empty string."""
        from mailnow.validation import validate_email_address
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_address("")

        assert "Invalid email address format" in str(exc_info.value)


class TestValidateEmailParams:
    """Tests for validate_email_params function."""

    def test_validate_email_params_with_all_valid_params(self):
        """Test that validate_email_params accepts all valid parameters."""
        from mailnow.validation import validate_email_params

        # Should not raise any exception
        validate_email_params(
            from_email="sender@example.com",
            to_email="recipient@example.com",
            subject="Test Subject",
            html="<h1>Test</h1>",
        )

    def test_validate_email_params_with_missing_from_email(self):
        """Test that validate_email_params rejects missing from_email."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="<h1>Test</h1>",
            )

        assert "from_email" in str(exc_info.value).lower()

    def test_validate_email_params_with_missing_to_email(self):
        """Test that validate_email_params rejects missing to_email."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="sender@example.com",
                to_email="",
                subject="Test Subject",
                html="<h1>Test</h1>",
            )

        assert "to_email" in str(exc_info.value).lower()

    def test_validate_email_params_with_missing_subject(self):
        """Test that validate_email_params rejects missing subject."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="sender@example.com",
                to_email="recipient@example.com",
                subject="",
                html="<h1>Test</h1>",
            )

        assert "subject" in str(exc_info.value).lower()

    def test_validate_email_params_with_missing_html(self):
        """Test that validate_email_params rejects missing html."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="sender@example.com",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="",
            )

        assert "html" in str(exc_info.value).lower()

    def test_validate_email_params_with_whitespace_only_from_email(self):
        """Test that validate_email_params rejects whitespace-only from_email."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="   ",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="<h1>Test</h1>",
            )

        assert "from_email" in str(exc_info.value).lower()

    def test_validate_email_params_with_invalid_from_email_format(self):
        """Test that validate_email_params rejects invalid from_email format."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="invalid-email",
                to_email="recipient@example.com",
                subject="Test Subject",
                html="<h1>Test</h1>",
            )

        assert "email address format" in str(exc_info.value).lower()

    def test_validate_email_params_with_invalid_to_email_format(self):
        """Test that validate_email_params rejects invalid to_email format."""
        from mailnow.validation import validate_email_params
        from mailnow.exceptions import MailnowValidationError

        with pytest.raises(MailnowValidationError) as exc_info:
            validate_email_params(
                from_email="sender@example.com",
                to_email="invalid-email",
                subject="Test Subject",
                html="<h1>Test</h1>",
            )

        assert "email address format" in str(exc_info.value).lower()
