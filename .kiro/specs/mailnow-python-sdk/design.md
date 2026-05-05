# Design Document

## Overview

The Mailnow Python SDK is a lightweight, user-friendly client library that wraps the Mailnow email API. The design follows Python best practices with strong typing throughout and Test-Driven Development (TDD) methodology. The SDK provides a simple, intuitive interface for sending emails using a class-based architecture with clear separation between the client interface, HTTP communication, validation, and error handling.

## Architecture

The SDK follows a layered architecture:

```
+----------------------------------+
|   Customer Application Code     |
+----------------+-----------------+
                 |
+----------------v-----------------+
|     MailnowClient (Public)       |
|  - send_email()                  |
+----------------+-----------------+
                 |
+----------------v-----------------+
|   Validation & Serialization     |
|  - validate_email_params()       |
|  - validate_attachments()        |
|  - validate_api_key()            |
+----------------+-----------------+
                 |
+----------------v-----------------+
|      HTTP Client Layer           |
|  - send_email_request()          |
+----------------+-----------------+
                 |
+----------------v-----------------+
|      Mailnow API Service         |
|  https://api.mailnow.xyz         |
+----------------------------------+
```

## Components and Interfaces

### 1. MailnowClient Class

The main entry point for customers. This class handles initialization and provides the public API.

**Location:** `mailnow/client.py`

**Interface:**
```python
from typing import Dict, Any, List, Optional

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
        html: str,
        attachments: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Send an email via the Mailnow API.

        Args:
            from_email: Sender email address
            to_email: Recipient email address
            subject: Email subject line
            html: HTML content of the email
            attachments: Optional list of attachment dicts, each with keys:
                - filename (str): Name of the file
                - content (str): Base64-encoded file content
                - content_type (str): MIME type (e.g. "application/pdf")

        Returns:
            Dict[str, Any]: Response from the API

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
from typing import Optional, List, Dict

def validate_api_key(api_key: Optional[str]) -> None: ...

def validate_email_address(email: str) -> None: ...

def validate_email_params(
    from_email: str,
    to_email: str,
    subject: str,
    html: str,
    attachments: Optional[List[Dict[str, str]]] = None,
) -> None: ...

def validate_attachments(attachments: List[Dict[str, str]]) -> None:
    """
    Validate a list of attachment dicts.
    Each must have non-empty filename, content, and content_type.
    Raises MailnowValidationError on any violation.
    """
```

### 3. HTTP Client Module

**Location:** `mailnow/http_client.py`

The payload type for `send_email_request` is widened from `Dict[str, str]` to `Dict[str, Any]` to accommodate the attachments list.

### 4. Exception Classes

No changes. Existing hierarchy covers all attachment validation errors via `MailnowValidationError`.

## Data Models

### Email Request Payload (without attachments)

```json
{
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email subject",
    "html": "<h1>Email content</h1>"
}
```

### Email Request Payload (with attachments)

```json
{
    "from": "sender@example.com",
    "to": "recipient@example.com",
    "subject": "Email subject",
    "html": "<h1>Email content</h1>",
    "attachments": [
        {
            "filename": "report.pdf",
            "content": "<base64-encoded string>",
            "content_type": "application/pdf"
        }
    ]
}
```

### Attachment Dict (Python)

```python
{
    "filename": str,      # Name of the file, e.g. "report.pdf"
    "content": str,       # Base64-encoded file content
    "content_type": str,  # MIME type, e.g. "application/pdf"
}
```

### API Response (Success)

```json
{
    "success": true,
    "message_id": "msg_abc123",
    "status": "queued"
}
```

### API Response (Error)

```json
{
    "error": {
        "code": "validation_error",
        "message": "Invalid email address"
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system - essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

The following properties are derived from Requirement 9 and are designed for Property-Based Testing using [Hypothesis](https://hypothesis.readthedocs.io/). Each test must run a minimum of 100 iterations.

---

Property 1: Valid attachments appear in payload with all required fields

*For any* list of valid attachment dicts (each with non-empty `filename`, `content`, and `content_type`), calling `send_email` with those attachments should result in the HTTP request payload containing an `"attachments"` array where every element includes all three fields with their original values.

**Validates: Requirements 9.1, 9.3, 9.8**

---

Property 2: No attachments means no attachments key in payload

*For any* valid email (from, to, subject, html), calling `send_email` with `attachments=None` or `attachments=[]` should result in the HTTP request payload containing no `"attachments"` key.

**Validates: Requirements 9.2**

---

Property 3: Attachments with missing or empty required fields are rejected

*For any* attachment dict where at least one of `filename`, `content`, or `content_type` is absent, empty, or whitespace-only, calling `send_email` with that attachment should raise `MailnowValidationError` before any HTTP request is made.

**Validates: Requirements 9.4, 9.5, 9.6, 9.7**

## Error Handling

### Error Mapping Strategy

- **400 Bad Request** -> `MailnowValidationError`
- **401 Unauthorized** -> `MailnowAuthError`
- **429 Too Many Requests** -> `MailnowRateLimitError`
- **5xx Server Errors** -> `MailnowServerError`
- **Network/Connection Errors** -> `MailnowConnectionError`

### Validation Error Handling

Client-side validation order:
1. Validate required email fields (from, to, subject, html)
2. Validate email address formats
3. Validate each attachment for required fields and non-empty values
4. Raise `MailnowValidationError` with a specific message identifying the problem

## Testing Strategy

### Dual Testing Approach

Both unit tests and property-based tests are required and complementary:

- **Unit tests** verify specific examples, edge cases, and error conditions
- **Property-based tests** verify universal properties that hold across all inputs

### Unit Tests

- `validate_attachments()` with valid, missing-field, and empty-value inputs
- `send_email()` with `attachments=None`, `attachments=[]`, and a valid attachment list
- `send_email()` with an attachment missing each required field

### Property-Based Testing

**Library:** [Hypothesis](https://hypothesis.readthedocs.io/)

Each property-based test must:
- Run a minimum of 100 iterations (`@settings(max_examples=100)`)
- Include a comment in the format: `# Feature: mailnow-python-sdk, Property N: <property text>`
- Each correctness property must be implemented by a single property-based test

**Generators needed:**
- `valid_attachment()` - generates a dict with non-empty `filename`, `content`, `content_type`
- `invalid_attachment()` - generates a dict with at least one field absent, empty, or whitespace-only

### Type Checking

- Run `mypy` in strict mode on all source files
- All function signatures must have complete type hints

## Design Decisions

### Attachment Representation

**Decision:** Use `List[Dict[str, str]]` rather than a dedicated dataclass.

**Rationale:** Consistent with the existing pattern of plain dicts for API payloads. Minimal surface area with no new public types to maintain.

### Payload Serialization

**Decision:** Only include `"attachments"` key when attachments are provided and non-empty.

**Rationale:** Matches the Go reference implementation (`omitempty` behavior). Keeps backward compatibility for existing callers.

### HTTP Client Payload Type

**Decision:** Widen `send_email_request` payload from `Dict[str, str]` to `Dict[str, Any]`.

**Rationale:** Attachments are a `List[Dict[str, str]]`, not a `str`, so the narrower type is incorrect.

### Validation Strategy

**Decision:** Add `validate_attachments()` called from `validate_email_params()`.

**Rationale:** Keeps validation centralized and independently testable. Consistent with the existing fail-fast pattern.
