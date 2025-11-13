"""Constants for the Mailnow SDK."""

# API Configuration
API_BASE_URL: str = "https://api.mailnow.xyz"
EMAIL_SEND_ENDPOINT: str = "/v1/email/send"

# Request Configuration
REQUEST_TIMEOUT: int = 30  # seconds

# API Key Prefixes
API_KEY_PREFIX_LIVE: str = "mn_live_"
API_KEY_PREFIX_TEST: str = "mn_test_"
