"""Shared types for the Mailnow SDK."""

from typing import TypedDict


class Attachment(TypedDict):
    filename: str
    content: str
    content_type: str
