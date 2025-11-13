# Technology Stack

## Language & Version

- Python 3.12+ (minimum required version)
- Fully type-annotated codebase

## Core Dependencies

- `httpx>=0.27.0` - HTTP client for API requests

## Development Dependencies

- `pytest>=8.0.0` - Testing framework
- `pytest-cov>=4.1.0` - Code coverage
- `respx>=0.21.0` - HTTP mocking for tests
- `mypy>=1.8.0` - Static type checking
- `black>=24.0.0` - Code formatting
- `ruff>=0.2.0` - Linting

## Build System

- Build backend: `hatchling`
- Package name: `py-mailnow`
- Distribution: Wheel packages via `hatch.build`

## Type Checking Configuration

- mypy strict mode enabled
- All functions must have type annotations
- No implicit optionals allowed
- Strict equality checks enforced

## Code Quality Tools

- Black (line length: 88)
- Ruff (pycodestyle, pyflakes, isort, flake8-bugbear, comprehensions, pyupgrade)
- pytest with coverage reporting

## Common Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=mailnow --cov-report=term-missing

# Type checking
mypy mailnow

# Code formatting
black mailnow tests

# Linting
ruff check mailnow tests

# Build package
python -m build
```
