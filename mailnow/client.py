"""Main client class for the Mailnow SDK."""

from typing import Dict, Any

from mailnow.http_client import HTTPClient
from mailnow.validation import validate_api_key
from mailnow.exceptions import MailnowAuthError


class MailnowClient:
    """
    Main client for interacting with the Mailnow email API.

    This class provides a simple interface for sending emails through the
    Mailnow service. It handles authentication, validation, and communication
    with the Mailnow API.

    Example:
        >>> from mailnow import MailnowClient
        >>> client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")
        >>> response = client.send_email(
        ...     from_email="sender@example.com",
        ...     to_email="recipient@example.com",
        ...     subject="Hello",
        ...     html="<h1>Hello World</h1>"
        ... )
        >>> print(response)
        {'success': True, 'message_id': 'msg_abc123', 'status': 'queued'}

    Attributes:
        _http_client (HTTPClient): Internal HTTP client for API communication
    """

    def __init__(self, api_key: str) -> None:
        """
        Initialize the Mailnow client.

        Creates a new MailnowClient instance with the provided API key.
        The API key is validated during initialization and must be in the
        correct format (starting with 'mn_live_' or 'mn_test_').

        Args:
            api_key (str): The Mailnow API key for authentication.
                Must start with 'mn_live_' for production or 'mn_test_' for testing.

        Raises:
            MailnowAuthError: If api_key is None, empty, or has invalid format
                (does not start with 'mn_live_' or 'mn_test_').

        Example:
            >>> client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")
            >>> # Client is now ready to send emails
        """
        try:
            validate_api_key(api_key)
        except Exception as e:
            # Convert validation errors to auth errors for API key issues
            raise MailnowAuthError(str(e))

        self._http_client: HTTPClient = HTTPClient(api_key=api_key)

    def send_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        html: str,
    ) -> Dict[str, Any]:
        """
        Send an email via the Mailnow API.

        This method validates all parameters, builds the API request payload,
        and sends the email through the Mailnow service. All parameters are
        validated before making the API request to provide immediate feedback
        on any issues.

        Args:
            from_email (str): Sender email address. Must be a valid email format
                (e.g., "sender@example.com"). Cannot be empty or whitespace-only.
            to_email (str): Recipient email address. Must be a valid email format
                (e.g., "recipient@example.com"). Cannot be empty or whitespace-only.
            subject (str): Email subject line. Cannot be empty or whitespace-only.
            html (str): HTML content of the email body. Cannot be empty or
                whitespace-only. Should be valid HTML markup.

        Returns:
            Dict[str, Any]: Response dictionary from the API containing:
                - success (bool): Whether the email was successfully queued
                - message_id (str): Unique identifier for the sent message
                - status (str): Current status of the message (e.g., "queued")
                Additional fields may be present depending on the API response.

        Raises:
            MailnowValidationError: If any parameter is missing, empty, or has
                invalid format. This includes:
                - Missing or empty from_email, to_email, subject, or html
                - Invalid email address format for from_email or to_email
                - API returns 400 Bad Request status code
            MailnowAuthError: If authentication fails due to invalid or expired
                API key. Raised when API returns 401 Unauthorized status code.
            MailnowRateLimitError: If rate limit is exceeded. Raised when API
                returns 429 Too Many Requests status code. Consider implementing
                exponential backoff retry logic.
            MailnowServerError: If the Mailnow API experiences an internal error.
                Raised when API returns 5xx status codes (500, 502, 503, 504, etc.).
                Consider retrying the request after a delay.
            MailnowConnectionError: If network connection fails, request times out,
                or any other network-level error occurs.

        Example:
            >>> client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")
            >>> try:
            ...     response = client.send_email(
            ...         from_email="sender@example.com",
            ...         to_email="recipient@example.com",
            ...         subject="Welcome to Mailnow",
            ...         html="<h1>Welcome!</h1><p>Thanks for signing up.</p>"
            ...     )
            ...     print(f"Email sent! Message ID: {response['message_id']}")
            ... except MailnowValidationError as e:
            ...     print(f"Validation error: {e}")
            ... except MailnowAuthError as e:
            ...     print(f"Authentication error: {e}")
            ... except MailnowError as e:
            ...     print(f"Error sending email: {e}")
        """
        from mailnow.validation import validate_email_params

        # Validate all email parameters
        validate_email_params(from_email, to_email, subject, html)

        # Build payload dictionary mapping parameters to API format
        payload = {
            "from": from_email,
            "to": to_email,
            "subject": subject,
            "html": html,
        }

        # Call HTTPClient to send the request
        response = self._http_client.send_email_request(payload)

        return response
