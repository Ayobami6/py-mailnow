"""HTTP client for communicating with the Mailnow API."""

from typing import Dict, Any, cast
import httpx

from mailnow.constants import API_BASE_URL, REQUEST_TIMEOUT, EMAIL_SEND_ENDPOINT
from mailnow.exceptions import (
    MailnowValidationError,
    MailnowAuthError,
    MailnowRateLimitError,
    MailnowServerError,
    MailnowConnectionError,
)


class HTTPClient:
    """
    HTTP client for making requests to the Mailnow API.

    This class handles all HTTP communication with the Mailnow API,
    including request building, response parsing, and error handling.
    """

    def __init__(self, api_key: str, base_url: str = API_BASE_URL) -> None:
        """
        Initialize HTTP client with API key and base URL.

        Args:
            api_key: The Mailnow API key for authentication
            base_url: The base URL for the Mailnow API (defaults to production URL)
        """
        self.api_key: str = api_key
        self.base_url: str = base_url
        self.client: httpx.Client = httpx.Client(timeout=httpx.Timeout(REQUEST_TIMEOUT))

    def send_email_request(self, payload: Dict[str, str]) -> Dict[str, Any]:
        """
        Make POST request to /v1/email/send endpoint.

        Args:
            payload: Dictionary containing email data (from, to, subject, html)

        Returns:
            Dict[str, Any]: Parsed JSON response from the API

        Raises:
            MailnowValidationError: For 400 status codes
            MailnowAuthError: For 401 status codes
            MailnowRateLimitError: For 429 status codes
            MailnowServerError: For 5xx status codes
            MailnowConnectionError: For network/connection errors
        """
        url = f"{self.base_url}{EMAIL_SEND_ENDPOINT}"
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }

        try:
            response = self.client.post(url, json=payload, headers=headers)

            # Handle successful responses
            if 200 <= response.status_code < 300:
                return cast(Dict[str, Any], response.json())

            # Handle error responses
            error_data = response.json() if response.text else {}
            error_message = self._extract_error_message(error_data)

            if response.status_code == 400:
                raise MailnowValidationError(error_message)
            elif response.status_code == 401:
                raise MailnowAuthError(error_message)
            elif response.status_code == 429:
                raise MailnowRateLimitError(error_message)
            elif response.status_code >= 500:
                raise MailnowServerError(error_message)
            else:
                # Fallback for other error codes
                raise MailnowServerError(
                    f"HTTP {response.status_code}: {error_message}"
                )

        except httpx.RequestError as e:
            # Handle network/connection errors
            raise MailnowConnectionError(f"Connection failed: {str(e)}")

    def _extract_error_message(self, error_data: Dict[str, Any]) -> str:
        """
        Extract error message from API error response.

        Args:
            error_data: The error response data from the API

        Returns:
            str: The extracted error message
        """
        if isinstance(error_data, dict) and "error" in error_data:
            error = error_data["error"]
            if isinstance(error, dict) and "message" in error:
                return cast(str, error["message"])
        return "An error occurred"
