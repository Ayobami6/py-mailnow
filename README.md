# Mailnow Python SDK

A simple, type-safe Python SDK for the [Mailnow](https://mailnow.xyz) email API. Send emails programmatically with just a few lines of code.

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 Simple, intuitive API
- 🔒 Type-safe with full type hints
- ✅ Comprehensive input validation
- 🎯 Detailed error handling
- 📝 Extensive documentation
- 🧪 Thoroughly tested

## Installation

Install the SDK using pip:

```bash
pip install py-mailnow
```

## Quick Start

```python
from mailnow import MailnowClient

# Initialize the client with your API key
client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

# Send an email
response = client.send_email(
    from_email="sender@example.com",
    to_email="recipient@example.com",
    subject="Hello from Mailnow!",
    html="<h1>Welcome!</h1><p>This is your first email.</p>"
)

print(f"Email sent! Message ID: {response['message_id']}")
```

## API Key Format

Your Mailnow API key must be in one of the following formats:

- **Production**: `mn_live_` followed by your unique key (e.g., `mn_live_7e59df7ce4a14545b443837804ec9722`)
- **Testing**: `mn_test_` followed by your unique key (e.g., `mn_test_abc123def456`)

You can find your API key in your [Mailnow dashboard](https://mailnow.xyz/dashboard).

## Usage Examples

### Basic Email Sending

```python
from mailnow import MailnowClient

client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

response = client.send_email(
    from_email="noreply@yourcompany.com",
    to_email="customer@example.com",
    subject="Welcome to Our Service",
    html="<h1>Welcome!</h1><p>Thanks for signing up.</p>"
)

print(response)
# Output: {'success': True, 'message_id': 'msg_abc123', 'status': 'queued'}
```

### With Error Handling

```python
from mailnow import (
    MailnowClient,
    MailnowError,
    MailnowValidationError,
    MailnowAuthError,
    MailnowRateLimitError,
    MailnowServerError,
    MailnowConnectionError
)

client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

try:
    response = client.send_email(
        from_email="sender@example.com",
        to_email="recipient@example.com",
        subject="Important Update",
        html="<p>Your account has been updated.</p>"
    )
    print(f"✓ Email sent successfully: {response['message_id']}")
    
except MailnowValidationError as e:
    print(f"✗ Validation error: {e}")
    # Handle invalid input (missing fields, invalid email format, etc.)
    
except MailnowAuthError as e:
    print(f"✗ Authentication error: {e}")
    # Handle invalid or expired API key
    
except MailnowRateLimitError as e:
    print(f"✗ Rate limit exceeded: {e}")
    # Implement exponential backoff or retry logic
    
except MailnowServerError as e:
    print(f"✗ Server error: {e}")
    # Retry the request after a delay
    
except MailnowConnectionError as e:
    print(f"✗ Connection error: {e}")
    # Check network connectivity
    
except MailnowError as e:
    print(f"✗ Unexpected error: {e}")
    # Catch any other SDK errors
```

### Sending HTML Emails

```python
from mailnow import MailnowClient

client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .header { background-color: #4CAF50; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to Our Newsletter</h1>
    </div>
    <div class="content">
        <p>Hello,</p>
        <p>Thank you for subscribing to our newsletter!</p>
        <p>Best regards,<br>The Team</p>
    </div>
</body>
</html>
"""

response = client.send_email(
    from_email="newsletter@yourcompany.com",
    to_email="subscriber@example.com",
    subject="Welcome to Our Newsletter",
    html=html_content
)
```

### Handling Multiple Recipients

```python
from mailnow import MailnowClient, MailnowError

client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

recipients = [
    "user1@example.com",
    "user2@example.com",
    "user3@example.com"
]

for recipient in recipients:
    try:
        response = client.send_email(
            from_email="notifications@yourcompany.com",
            to_email=recipient,
            subject="System Notification",
            html="<p>This is an automated notification.</p>"
        )
        print(f"✓ Sent to {recipient}: {response['message_id']}")
    except MailnowError as e:
        print(f"✗ Failed to send to {recipient}: {e}")
        continue
```

## Exception Types

The SDK provides detailed exception types for different error scenarios:

### `MailnowError`

Base exception for all Mailnow SDK errors. Catch this to handle any SDK-related error.

```python
try:
    client.send_email(...)
except MailnowError as e:
    print(f"SDK error: {e}")
```

### `MailnowValidationError`

Raised when input validation fails. This includes:
- Missing or empty required parameters (`from_email`, `to_email`, `subject`, `html`)
- Invalid email address format
- Invalid API key format
- API returns 400 Bad Request

```python
try:
    client.send_email(
        from_email="invalid-email",  # Invalid format
        to_email="user@example.com",
        subject="Test",
        html="<p>Test</p>"
    )
except MailnowValidationError as e:
    print(f"Validation error: {e}")
```

### `MailnowAuthError`

Raised when authentication fails. This includes:
- Missing or None API key
- Empty API key
- Invalid API key format (doesn't start with `mn_live_` or `mn_test_`)
- API returns 401 Unauthorized

```python
try:
    client = MailnowClient(api_key="invalid_key")
except MailnowAuthError as e:
    print(f"Authentication error: {e}")
```

### `MailnowRateLimitError`

Raised when rate limit is exceeded (API returns 429 Too Many Requests). Consider implementing exponential backoff retry logic.

```python
import time

try:
    client.send_email(...)
except MailnowRateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    time.sleep(60)  # Wait before retrying
```

### `MailnowServerError`

Raised when the Mailnow API experiences an internal error (5xx status codes). Consider retrying the request after a delay.

```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = client.send_email(...)
        break
    except MailnowServerError as e:
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
        raise
```

### `MailnowConnectionError`

Raised when network connection fails. This includes:
- Network connection cannot be established
- Request times out
- DNS resolution fails
- Any other network-level error

```python
try:
    client.send_email(...)
except MailnowConnectionError as e:
    print(f"Connection error: {e}")
    # Check network connectivity or retry
```

## Type Hints and mypy Compatibility

The Mailnow SDK is fully type-annotated and compatible with [mypy](http://mypy-lang.org/) for static type checking. All public APIs include comprehensive type hints.

### Running Type Checks

```bash
# Install mypy
pip install mypy

# Run type checking on your code
mypy your_script.py
```

### Example with Type Hints

```python
from typing import Dict, Any
from mailnow import MailnowClient

def send_welcome_email(client: MailnowClient, user_email: str) -> Dict[str, Any]:
    """Send a welcome email to a new user."""
    return client.send_email(
        from_email="welcome@yourcompany.com",
        to_email=user_email,
        subject="Welcome!",
        html="<h1>Welcome to our platform!</h1>"
    )

# mypy will catch type errors
client: MailnowClient = MailnowClient(api_key="mn_live_abc123")
response: Dict[str, Any] = send_welcome_email(client, "user@example.com")
```

## API Reference

### `MailnowClient`

Main client class for interacting with the Mailnow API.

#### `__init__(api_key: str) -> None`

Initialize the Mailnow client.

**Parameters:**
- `api_key` (str): Your Mailnow API key (format: `mn_live_*` or `mn_test_*`)

**Raises:**
- `MailnowAuthError`: If API key is invalid or missing

#### `send_email(from_email: str, to_email: str, subject: str, html: str) -> Dict[str, Any]`

Send an email via the Mailnow API.

**Parameters:**
- `from_email` (str): Sender email address (must be valid format)
- `to_email` (str): Recipient email address (must be valid format)
- `subject` (str): Email subject line (cannot be empty)
- `html` (str): HTML content of the email (cannot be empty)

**Returns:**
- `Dict[str, Any]`: Response dictionary containing:
  - `success` (bool): Whether the email was successfully queued
  - `message_id` (str): Unique identifier for the message
  - `status` (str): Current status (e.g., "queued")

**Raises:**
- `MailnowValidationError`: Invalid input parameters
- `MailnowAuthError`: Authentication failure
- `MailnowRateLimitError`: Rate limit exceeded
- `MailnowServerError`: Server error (5xx)
- `MailnowConnectionError`: Network connection error

## Requirements

- Python 3.12 or higher
- httpx >= 0.27.0

## Development

### Installing Development Dependencies

```bash
pip install py-mailnow[dev]
```

### Running Tests

```bash
pytest
```

### Running Type Checks

```bash
mypy mailnow
```

### Code Formatting

```bash
black mailnow tests
ruff check mailnow tests
```

## License

This project is licensed under the MIT License.

## Support

- **Documentation**: [GitHub README](https://github.com/mailnow/py-mailnow#readme)
- **Issues**: [GitHub Issues](https://github.com/mailnow/py-mailnow/issues)
- **Website**: [mailnow.xyz](https://mailnow.xyz)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
