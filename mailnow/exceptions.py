"""Custom exception classes for the Mailnow SDK."""


class MailnowError(Exception):
    """
    Base exception for all Mailnow SDK errors.

    All custom exceptions in the Mailnow SDK inherit from this base class,
    allowing users to catch all SDK-related errors with a single except clause.

    Example:
        try:
            client.send_email(...)
        except MailnowError as e:
            print(f"Mailnow SDK error: {e}")
    """

    pass


class MailnowValidationError(MailnowError):
    """
    Raised when input validation fails.

    This exception is raised when:
    - Required parameters are missing or empty
    - Email addresses have invalid format
    - API key format is invalid
    - The API returns a 400 Bad Request status code

    Example:
        try:
            client.send_email(from_email="", to_email="user@example.com", ...)
        except MailnowValidationError as e:
            print(f"Validation error: {e}")
    """

    pass


class MailnowAuthError(MailnowError):
    """
    Raised when authentication fails.

    This exception is raised when:
    - API key is missing or None
    - API key is empty
    - API key has invalid format (doesn't start with mn_live_ or mn_test_)
    - The API returns a 401 Unauthorized status code

    Example:
        try:
            client = MailnowClient(api_key="invalid_key")
        except MailnowAuthError as e:
            print(f"Authentication error: {e}")
    """

    pass


class MailnowRateLimitError(MailnowError):
    """
    Raised when rate limit is exceeded.

    This exception is raised when the API returns a 429 Too Many Requests
    status code, indicating that the client has sent too many requests in
    a given time period.

    Example:
        try:
            client.send_email(...)
        except MailnowRateLimitError as e:
            print(f"Rate limit exceeded: {e}")
            # Consider implementing exponential backoff retry logic
    """

    pass


class MailnowServerError(MailnowError):
    """
    Raised when server returns a 5xx error.

    This exception is raised when the Mailnow API experiences an internal
    error and returns a 5xx status code (500, 502, 503, 504, etc.).

    Example:
        try:
            client.send_email(...)
        except MailnowServerError as e:
            print(f"Server error: {e}")
            # Consider retrying the request after a delay
    """

    pass


class MailnowConnectionError(MailnowError):
    """
    Raised when network connection fails.

    This exception is raised when:
    - Network connection cannot be established
    - Request times out
    - DNS resolution fails
    - Any other network-level error occurs

    Example:
        try:
            client.send_email(...)
        except MailnowConnectionError as e:
            print(f"Connection error: {e}")
            # Check network connectivity
    """

    pass
