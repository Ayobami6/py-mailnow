# Project Structure

## Directory Layout

```
mailnow/                    # Main package directory
├── __init__.py            # Package exports and version
├── client.py              # MailnowClient class (main API)
├── http_client.py         # HTTPClient for API communication
├── validation.py          # Input validation functions
├── exceptions.py          # Custom exception classes
└── constants.py           # Constants and configuration

tests/                      # Test suite
├── test_client.py         # Client tests
├── test_http_client.py    # HTTP client tests
├── test_validation.py     # Validation tests
└── test_exceptions.py     # Exception tests
```

## Architecture Patterns

### Separation of Concerns

- `client.py` - High-level API interface
- `http_client.py` - Low-level HTTP communication
- `validation.py` - Input validation logic
- `exceptions.py` - Error handling types

### Exception Hierarchy

All exceptions inherit from `MailnowError` base class:
- `MailnowValidationError` - Invalid input parameters
- `MailnowAuthError` - Authentication failures
- `MailnowRateLimitError` - Rate limit exceeded (429)
- `MailnowServerError` - Server errors (5xx)
- `MailnowConnectionError` - Network failures

### Validation Strategy

- Validate early: Check inputs before making API calls
- Fail fast: Raise exceptions immediately on invalid input
- Clear messages: Provide specific error messages

## Code Conventions

### Docstrings

- Use Google-style docstrings for all public APIs
- Include Args, Returns, Raises, and Example sections
- Provide detailed descriptions for complex behavior

### Type Hints

- All functions must have complete type annotations
- Use `Dict[str, Any]` for API response types
- Use `Optional[T]` for nullable parameters
- Import types from `typing` module

### Testing

- Test class names: `Test<ClassName><Feature>`
- Test method names: `test_<method>_<scenario>`
- Use descriptive docstrings for each test
- Mock external HTTP calls using `unittest.mock.Mock`

### Imports

- Standard library imports first
- Third-party imports second
- Local imports last
- Use absolute imports for package modules
