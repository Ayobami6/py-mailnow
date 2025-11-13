mplementation Plan

- [x] 1. Create custom exception classes (TDD)
- [x] 1.1 Write tests for exception classes
  - Write tests for base `MailnowError` exception
  - Write tests for each specific exception class: `MailnowValidationError`, `MailnowAuthError`, `MailnowRateLimitError`, `MailnowServerError`, `MailnowConnectionError`
  - Test exception inheritance hierarchy
  - Test exception message formatting
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 1.2 Implement exception classes
  - Implement base `MailnowError` exception class with type hints
  - Implement specific exception classes with proper inheritance
  - Add comprehensive docstrings explaining when each exception is raised
  - Verify all tests pass
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 2. Create constants module
  - Define API base URL constant with type annotation
  - Define email send endpoint constant
  - Define request timeout constant (30 seconds)
  - Define API key prefix constants
  - _Requirements: 2.2, 8.2_

- [x] 3. Implement validation module (TDD)
- [x] 3.1 Write tests for validation functions
  - Write tests for `validate_api_key()` with None, empty, invalid format, and valid formats
  - Write tests for `validate_email_address()` with invalid and valid email formats
  - Write tests for `validate_email_params()` with missing, empty, and valid parameters
  - Test that appropriate `MailnowValidationError` exceptions are raised with descriptive messages
  - _Requirements: 1.2, 1.4, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 3.2 Implement validation functions
  - Implement `validate_api_key()` function with type hints
  - Implement `validate_email_address()` function using regex pattern
  - Implement `validate_email_params()` function to validate all required fields
  - Ensure all validation functions raise `MailnowValidationError` with descriptive messages
  - Verify all tests pass
  - _Requirements: 1.2, 1.4, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 4. Implement HTTP client class (TDD)
- [x] 4.1 Write tests for HTTPClient initialization
  - Write tests for HTTPClient initialization with api_key and base_url
  - Test that httpx client is properly configured with timeout
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 4.2 Implement HTTPClient initialization
  - Create HTTPClient class with `__init__` method with full type hints
  - Accept api_key: str and optional base_url: str parameters
  - Store API key and base URL as typed instance variables
  - Initialize httpx.Client with timeout configuration
  - Verify tests pass
  - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 4.3 Write tests for send_email_request method
  - Write tests for successful POST request with proper headers and payload
  - Test successful response parsing (2xx status)
  - Test HTTP 400 maps to `MailnowValidationError`
  - Test HTTP 401 maps to `MailnowAuthError`
  - Test HTTP 429 maps to `MailnowRateLimitError`
  - Test HTTP 5xx maps to `MailnowServerError`
  - Test network errors map to `MailnowConnectionError`
  - Use respx library to mock httpx requests
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 4.4 Implement send_email_request method
  - Implement method with type hints: Dict[str, str] -> Dict[str, Any]
  - Build POST request to `/v1/email/send` endpoint
  - Set `Content-Type: application/json` and `X-API-Key` headers
  - Serialize payload as JSON in request body
  - Parse successful responses and return parsed JSON
  - Map HTTP status codes to appropriate exceptions
  - Handle httpx exceptions and convert to `MailnowConnectionError`
  - Extract error messages from API response and include in exceptions
  - Verify all tests pass
  - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 5. Implement MailnowClient class (TDD)
- [x] 5.1 Write tests for MailnowClient initialization
  - Write tests for initialization with None API key (should raise MailnowAuthError)
  - Write tests for initialization with empty API key (should raise MailnowAuthError)
  - Write tests for initialization with invalid format API key (should raise MailnowAuthError)
  - Write tests for initialization with valid API key (should succeed)
  - Test that HTTPClient instance is created
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 5.2 Implement MailnowClient initialization
  - Create MailnowClient class with `__init__` method with type hints
  - Accept api_key: str parameter
  - Validate API key using validation module
  - Initialize HTTPClient instance
  - Raise `MailnowAuthError` if API key is missing or invalid
  - Verify all tests pass
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 5.3 Write tests for send_email method
  - Write tests for successful email sending with valid parameters
  - Write tests for validation errors with missing/empty parameters
  - Write tests for validation errors with invalid email addresses
  - Write tests that proper payload is built and passed to HTTPClient
  - Write tests that response is returned correctly
  - _Requirements: 2.1, 2.5, 3.1, 3.2, 3.3, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5.4 Implement send_email method
  - Implement method with full type hints for all parameters and return value
  - Accept parameters: from_email: str, to_email: str, subject: str, html: str
  - Validate all email parameters using validation module
  - Build payload dictionary mapping parameters to API format
  - Call HTTPClient.send_email_request() with payload
  - Return parsed response dictionary
  - Verify all tests pass
  - _Requirements: 2.1, 2.5, 3.1, 3.2, 3.3, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 5.5 Add comprehensive docstrings with type information
  - Document MailnowClient class with usage examples
  - Document __init__ method with parameter descriptions and exceptions
  - Document send_email method with parameter descriptions, return value, and all possible exceptions
  - Include type information in docstrings
  - _Requirements: 7.3, 7.4_

- [x] 6. Configure package initialization
  - Update `mailnow/__init__.py` to expose MailnowClient class
  - Import and expose all exception classes for easy access
  - Add package-level docstring with brief description
  - Define `__version__` variable with type annotation
  - Define `__all__` list for explicit exports
  - _Requirements: 1.1, 7.4_

- [x] 7. Update pyproject.toml configuration
  - Fix package name from "py-maailnow" to "mailnow" or "py-mailnow"
  - Add httpx as a dependency with version constraint
  - Add respx as a development dependency for testing
  - Add mypy as a development dependency for type checking
  - Update description with clear SDK purpose
  - Ensure Python version requirement is set to >=3.12
  - Add project metadata (author, license, repository URL if applicable)
  - _Requirements: 6.1, 6.2, 6.3, 8.1_

- [x] 8. Create comprehensive README documentation
  - Write installation instructions using pip
  - Add quick start example showing client initialization and email sending
  - Document all exception types with descriptions
  - Add error handling examples
  - Include API key format information
  - Add usage examples for different scenarios
  - Mention type hints and mypy compatibility
  - _Requirements: 6.4, 7.1, 7.2, 7.4_

- [ ] 9. Run type checking and verify coverage
  - Run mypy in strict mode on all source files
  - Fix any type errors identified by mypy
  - Run pytest with coverage reporting
  - Verify minimum 90% code coverage is achieved
  - _Requirements: All requirements (verification step)_
