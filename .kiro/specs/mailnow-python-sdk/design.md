# Design Document

## Overview

The Mailnow Python SDK is a lightweight, user-friendly client library that wraps the Mailnow email API. The design follows Python best practices with strong typing throughout and Test-Driven Development (TDD) methodology. The SDK provides a simple, intuitive interface for sending emails using a class-based architecture with clear separation between the client interface, HTTP communication, validation, and error handling.

## Architecture

The SDK follows a layered architecture:

```
┌─────────────────────────────────┐
│   Customer Application Code    │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│     MailnowClient (Public)      │
│  - send_email()                 │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   Validation & Serialization    │
│  - validate_email()             │
│  - validate_api_key()           │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      HTTP Client Layer          │
│  - make_request()               │
│  - handle_response()            │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│      Mailnow API Service        │
│  https://api.mailnow.xyz        │
└─────────────────────────────────┘
```

## Components and Interfaces

### 1. MailnowClient Class

The main entry point for customers. This class handles initialization and provides the public API.

**Location:** `mailnow/client.py`

**Interface:**
```python
from typing import Dict, Any

class MailnowClient:
    def __init__(self, api_key: str) -> None:
        """
        Initialize the Mailnow client.
        
        Args:
            api_key: The Mailnow API key (format: mn_live_* or mn_test_*)
            
        Raises:
            MailnowAuthError: If api_key is invalid or missing
        """
        
    def send_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        html: str
    ) -> Dict[str, Any]:
        """
        Send an email via the Mailnow API.
        
        Args:
            from_email: Sender email address
            to_email: Recipient email address
            subject: Email subject line
            html: HTML content of the email
            
        Returns:
            Dict[str, Any]: Response from the API containing status and message details
            
        Raises:
            MailnowValidationError: If any parameter is invalid
            MailnowAuthError: If authentication fails
            MailnowRateLimitError: If rate limit is exceeded
            MailnowServerError: If server error occurs
            MailnowConnectionError: If network error occurs
        """
```

### 2. Validation Module

Handles input validation before making API requests.

**Location:** `mailnow/validation.py`

**Functions:**
```python
from typing import Optional

def validate_api_key(api_key: Optional[str]) -> None:
    """
    Validate API key format.
    
    Args:
        api_key: The API key to validate
        
    Raises:
        MailnowValidationError: If API key is None, empty, or has invalid format
    """
    
def validate_email_address(email: str) -> None:
    """
    Validate email address format.
    
    Args:
        email: The email address to validate
        
    Raises:
        MailnowValidationError: If email format is invalid
    """
    
def validate_email_params(
    from_email: str, 
    to_email: str, 
    subject: str, 
    html: str
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
```

### 3. HTTP Client Module

Manages HTTP communication with the Mailnow API.

**Location:** `mailnow/http_client.py`

**Interface:**
```python
from typing import Dict, Any
import httpx

class HTTPClient:
    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://api.mailnow.xyz"
    ) -> None:
        """
        Initialize HTTP client with API key and base URL.
        
        Args:
            api_key: The Mailnow API key
            base_url: The base URL for the Mailnow API
        """
        
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
```

### 4. Exception Classes

Custom exceptions for different error scenarios.

**Location:** `mailnow/exceptions.py`

**Classes:**
```python
class MailnowError(Exception):
    """Base exception for all Mailnow SDK errors."""

class MailnowValidationError(MailnowError):
    """Raised when input validation fails."""

class MailnowAuthError(MailnowError):
    """Raised when authentication fails."""

class MailnowRateLimitError(MailnowError):
    """Raised when rate limit is exceeded."""

class MailnowServerError(MailnowError):
    """Raised when server returns 5xx error."""

class MailnowConnectionError(MailnowError):
    """Raised when network connection fails."""
```

## Data Models

### Email Request Payload

```python
{
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email subject",
    "html": "<h1>Email content</h1>"
}
```

### API Response (Success)

```python
{
    "success": true,
    "message_id": "msg_abc123",
    "status": "queued"
}
```

### API Response (Error)

```python
{
    "error": {
        "code": "validation_error",
        "message": "Invalid email address",
        "details": {...}
    }
}
```

## Error Handling

### Error Mapping Strategy

The SDK maps HTTP status codes to specific exceptions:

- **400 Bad Request** → `MailnowValidationError`
- **401 Unauthorized** → `MailnowAuthError`
- **429 Too Many Requests** → `MailnowRateLimitError`
- **5xx Server Errors** → `MailnowServerError`
- **Network/Connection Errors** → `MailnowConnectionError`

### Error Response Parsing

When the API returns an error, the SDK will:
1. Parse the JSON error response
2. Extract the error message and details
3. Create an appropriate exception with the error information
4. Include the HTTP status code in the exception

### Validation Error Handling

Client-side validation occurs before making API requests:
1. Check for missing required parameters
2. Validate email address format using regex
3. Validate API key format
4. Raise `MailnowValidationError` with specific field information


## Testing Strategy

### Test-Driven Development (TDD) Approach

The SDK follows strict TDD methodology:

1. **Write tests first** before implementing any functionality
2. **Run tests** to confirm they fail (red phase)
3. **Implement minimal code** to make tests pass (green phase)
4. **Refactor** while keeping tests green
5. **Repeat** for each feature

### Unit Tests

Test individual components in isolation using pytest:

- **Validation Module**: 
  - Test `validate_api_key()` with None, empty string, invalid format, valid formats
  - Test `validate_email_address()` with invalid and valid email formats
  - Test `validate_email_params()` with missing, empty, and valid parameters
  
- **Exception Classes**: 
  - Test exception creation and inheritance hierarchy
  - Test exception message formatting
  - Test that all exceptions inherit from MailnowError
  
- **Client Initialization**: 
  - Test MailnowClient with None API key (should raise MailnowAuthError)
  - Test with empty API key (should raise MailnowAuthError)
  - Test with invalid format API key (should raise MailnowAuthError)
  - Test with valid API key (should succeed)
  
- **HTTP Client**: 
  - Test request building with proper headers and payload
  - Test response parsing for successful responses
  - Test error mapping for each HTTP status code (400, 401, 429, 5xx)
  - Test connection error handling
  - Use `httpx` mock or `respx` library for HTTP mocking

### Integration Tests

Test the SDK against the actual Mailnow API (or a test environment):

- **Successful Email Send**: Test complete flow with valid credentials and parameters
- **Authentication Errors**: Test with invalid API key
- **Validation Errors**: Test with invalid email parameters
- **Error Handling**: Test various error scenarios returned by the API

### Type Checking

- Run `mypy` in strict mode to verify all type annotations
- Ensure no `Any` types are used without justification
- Verify all function signatures have complete type hints

### Test Environment

- Use `mn_test_*` API keys for integration testing when available
- Mock HTTP responses for unit tests using `respx` library (httpx-compatible)
- Achieve minimum 90% code coverage
- Run tests in CI/CD pipeline on every commit

## Dependencies

### Required Dependencies

- **httpx**: HTTP client library for making API requests
  - Modern, well-maintained library with excellent async support
  - Better performance than `requests`
  - Built-in timeout and connection pooling

### Development Dependencies

- **pytest**: Testing framework for TDD
- **pytest-cov**: Code coverage reporting (target: 90%+)
- **respx**: HTTP mocking library for httpx
- **mypy**: Static type checker (run in strict mode)
- **black**: Code formatting
- **ruff**: Fast Python linter

## Package Structure

```
mailnow/
├── __init__.py          # Package initialization, expose MailnowClient
├── client.py            # Main MailnowClient class
├── http_client.py       # HTTP communication layer
├── validation.py        # Input validation functions
├── exceptions.py        # Custom exception classes
└── constants.py         # Constants (API base URL, timeouts, etc.)

tests/
├── __init__.py
├── test_client.py       # Tests for MailnowClient
├── test_validation.py   # Tests for validation functions
├── test_http_client.py  # Tests for HTTP client
└── test_exceptions.py   # Tests for exceptions

README.md                # Documentation and examples
pyproject.toml          # Package configuration
LICENSE                 # License file
```

## Configuration

### Constants

**Location:** `mailnow/constants.py`

```python
API_BASE_URL = "https://api.mailnow.xyz"
API_VERSION = "v1"
EMAIL_SEND_ENDPOINT = "/v1/email/send"
REQUEST_TIMEOUT = 30  # seconds
API_KEY_PREFIX_LIVE = "mn_live_"
API_KEY_PREFIX_TEST = "mn_test_"
```

### Timeout Configuration

- Default request timeout: 30 seconds
- Configurable via client initialization (future enhancement)


## Usage Example

```python
from mailnow import MailnowClient

# Initialize client
client = MailnowClient(api_key="mn_live_7e59df7ce4a14545b443837804ec9722")

# Send email
try:
    response = client.send_email(
        from_email="sender@example.com",
        to_email="recipient@example.com",
        subject="Test Email",
        html="<h1>Hello World</h1><p>This is a test email.</p>"
    )
    print(f"Email sent successfully: {response}")
except MailnowValidationError as e:
    print(f"Validation error: {e}")
except MailnowAuthError as e:
    print(f"Authentication error: {e}")
except MailnowError as e:
    print(f"Error sending email: {e}")
```

## Design Decisions

### 1. HTTP Client Library Choice

**Decision:** Use `httpx` as the primary HTTP client library.

**Rationale:**
- Modern, well-maintained library with excellent async support
- Better performance than `requests`
- Similar API to `requests` for easy adoption
- Built-in timeout and connection pooling

### 2. Synchronous vs Asynchronous

**Decision:** Start with synchronous API, add async support in future version.

**Rationale:**
- Simpler implementation for MVP
- Covers majority of use cases
- Async can be added later without breaking changes

### 3. Parameter Naming

**Decision:** Use `from_email` and `to_email` instead of `from` and `to`.

**Rationale:**
- `from` is a Python keyword and cannot be used as parameter name
- More explicit and Pythonic
- Map to API's `from` and `to` fields internally

### 4. Response Format

**Decision:** Return dictionary with parsed JSON response.

**Rationale:**
- Simple and flexible
- Easy to work with in Python
- Can be enhanced to response object in future without breaking changes

### 5. Validation Strategy

**Decision:** Perform client-side validation before API requests.

**Rationale:**
- Fail fast and provide immediate feedback
- Reduce unnecessary API calls
- Better user experience with clear error messages
- Reduces API costs for customers

### 6. Exception Hierarchy

**Decision:** Use a base `MailnowError` exception with specific subclasses.

**Rationale:**
- Allows customers to catch all SDK errors with a single except clause
- Enables fine-grained error handling when needed
- Follows Python exception best practices
- Makes error types discoverable and self-documenting

### 7. Strong Typing Throughout

**Decision:** Use comprehensive type hints for all functions, methods, and class attributes.

**Rationale:**
- Enables static type checking with mypy to catch errors before runtime
- Improves IDE auto-completion and inline documentation
- Makes code more maintainable and self-documenting
- Aligns with modern Python best practices (PEP 484, 585, 604)
- Facilitates TDD by making interfaces explicit

**Implementation:**
- Use `typing` module for complex types (Dict, Any, Optional, etc.)
- Type all function parameters and return values
- Use `-> None` for functions that don't return values
- Run mypy in strict mode during development and CI/CD

### 8. Test-Driven Development

**Decision:** Follow strict TDD methodology for all SDK development.

**Rationale:**
- Ensures high code quality and test coverage from the start
- Reduces bugs by catching issues early
- Makes refactoring safer with comprehensive test suite
- Documents expected behavior through tests
- Aligns with professional software development practices

**Implementation:**
- Write tests before implementation for every feature
- Use pytest as the testing framework
- Maintain minimum 90% code coverage
- Run tests automatically in CI/CD pipeline


## Security Considerations

1. **API Key Storage**: API keys are stored in memory only, never logged or persisted by the SDK
2. **HTTPS Only**: All API communication uses HTTPS to ensure encrypted transmission
3. **Input Validation**: All parameters are validated before sending to prevent injection attacks
4. **Error Messages**: Error messages avoid exposing sensitive information like full API keys
5. **No Credential Logging**: The SDK never logs API keys or sensitive request data

## Python Version Support

**Decision:** Support Python 3.12 and above.

**Rationale:**
- Python 3.12 includes performance improvements and modern type hinting features
- Allows use of latest language features for cleaner code
- Aligns with current Python support lifecycle
- Customers on older versions can use older SDK versions if needed

**Implementation:**
- Declare `requires-python = ">=3.12"` in pyproject.toml
- Use modern Python features where beneficial (e.g., PEP 585 type hints, match statements)
- Leverage Python 3.12's improved type system for better static analysis
- Test against Python 3.12+ in CI/CD pipeline

## Documentation Strategy

The SDK provides multiple layers of documentation to support different user needs:

### 1. README.md

Primary documentation file including:
- Quick installation instructions via pip
- Getting started guide with basic example
- API key format and authentication information
- Complete code examples for common use cases
- Error handling patterns
- Links to API documentation

### 2. Inline Docstrings

All public classes and methods include comprehensive docstrings:
- Class-level docstrings explaining purpose and usage
- Method docstrings with parameter descriptions
- Return value documentation
- Exception documentation (all possible exceptions listed)
- Usage examples where helpful

### 3. Exception Documentation

Clear documentation of all exception types:
- When each exception is raised
- How to handle each exception type
- Example error handling code

**Rationale:**
- Addresses Requirement 7 (documentation and examples)
- Enables quick onboarding for new users
- Provides reference for experienced users
- Supports IDE auto-completion and inline help


## Package Distribution

### Package Metadata

**Location:** `pyproject.toml`

The package configuration includes:
- Package name: `mailnow` (or `py-mailnow` if name is taken)
- Version: Semantic versioning (start with 0.1.0)
- Description: Clear one-line description of SDK purpose
- Python version requirement: >=3.12
- Dependencies: httpx with appropriate version constraints
- Author and maintainer information
- License: Specify open source license if applicable
- Project URLs: Repository, documentation, issue tracker

### Installation

The SDK is installable via pip:
```bash
pip install mailnow
```

**Rationale:**
- Addresses Requirement 6 (pip installation and packaging)
- Standard Python packaging approach
- Easy integration into existing projects
- Dependency management handled automatically

## HTTP Connection Management

### Connection Reuse Strategy

**Decision:** Use httpx client instance for connection pooling.

**Implementation:**
- HTTPClient class maintains a single httpx.Client instance
- Client instance is created during HTTPClient initialization
- Same client instance is reused for all requests
- Connection pooling is handled automatically by httpx

**Rationale:**
- Addresses Requirement 8.4 (connection reuse for multiple emails)
- Improves performance by avoiding connection overhead
- Reduces latency for subsequent requests
- httpx handles connection pooling transparently

### Timeout Configuration

**Decision:** Set 30-second default timeout for all requests.

**Rationale:**
- Addresses Requirement 8.2 (appropriate timeout values)
- Prevents indefinite hanging on network issues
- 30 seconds is reasonable for email API operations
- Can be made configurable in future versions if needed

### Resource Cleanup

**Decision:** Rely on Python garbage collection and context managers.

**Implementation:**
- httpx.Client automatically closes connections when garbage collected
- Future enhancement: Add context manager support to MailnowClient
- Future enhancement: Add explicit close() method

**Rationale:**
- Addresses Requirement 8.3 (proper connection closing)
- Simplifies initial implementation
- httpx handles cleanup automatically in most cases
- Can be enhanced with explicit cleanup methods later
