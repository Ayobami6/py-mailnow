"""Validation functions for the Mailnow SDK."""

import re
from typing import Optional

from mailnow.exceptions import MailnowValidationError


def validate_api_key(api_key: Optional[str]) -> None:
    """
    Validate API key format.

    Args:
        api_key: The API key to validate

    Raises:
        MailnowValidationError: If API key is None, empty, or has invalid format
    """
    if api_key is None or not api_key.strip():
        raise MailnowValidationError("API key is required")

    if not (api_key.startswith("mn_live_") or api_key.startswith("mn_test_")):
        raise MailnowValidationError("API key must start with 'mn_live_' or 'mn_test_'")


def validate_email_address(email: str) -> None:
    """
    Validate email address format.

    Args:
        email: The email address to validate

    Raises:
        MailnowValidationError: If email format is invalid
    """
    # Basic email regex pattern
    # Matches: local-part@domain.tld
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if not email or not re.match(email_pattern, email):
        raise MailnowValidationError(f"Invalid email address format: {email}")


def validate_email_params(
    from_email: str, to_email: str, subject: str, html: str
) -> None:
    """
    Validate all email parameters.

    Args:
        from_email: Sender email address
        to_email: Recipient email address
        subject: Email subject line
        html: HTML content

    Raises:
        MailnowValidationError: If any parameter is missing, empty, or invalid
    """
    # Check for missing or empty parameters
    if not from_email or not from_email.strip():
        raise MailnowValidationError("from_email is required and cannot be empty")

    if not to_email or not to_email.strip():
        raise MailnowValidationError("to_email is required and cannot be empty")

    if not subject or not subject.strip():
        raise MailnowValidationError("subject is required and cannot be empty")

    if not html or not html.strip():
        raise MailnowValidationError("html is required and cannot be empty")

    # Validate email address formats
    validate_email_address(from_email)
    validate_email_address(to_email)
