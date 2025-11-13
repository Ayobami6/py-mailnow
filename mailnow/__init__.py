"""
Mailnow Python SDK.

A lightweight Python client library for the Mailnow email API.
Provides a simple interface for sending emails programmatically with
comprehensive error handling and type safety.

Example:
    >>> from mailnow import MailnowClient
    >>> client = MailnowClient(api_key="mn_live_your_api_key")
    >>> response = client.send_email(
    ...     from_email="sender@example.com",
    ...     to_email="recipient@example.com",
    ...     subject="Hello",
    ...     html="<h1>Hello World</h1>"
    ... )
"""

__version__: str = "0.1.0"

from mailnow.client import MailnowClient
from mailnow.exceptions import (
    MailnowError,
    MailnowValidationError,
    MailnowAuthError,
    MailnowRateLimitError,
    MailnowServerError,
    MailnowConnectionError,
)

__all__ = [
    "MailnowClient",
    "MailnowError",
    "MailnowValidationError",
    "MailnowAuthError",
    "MailnowRateLimitError",
    "MailnowServerError",
    "MailnowConnectionError",
]
