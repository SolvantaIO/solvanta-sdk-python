"""Solvanta API errors."""

from __future__ import annotations


class SolvantaError(Exception):
    """Raised when the Solvanta API returns a non-success response."""

    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(f"[{status_code}] {code}: {message}")
