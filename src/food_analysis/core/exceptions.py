"""Domain-specific exceptions for CookCast AI."""


class CookCastException(Exception):
    """Base exception for all domain errors."""
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class VisionExtractionError(CookCastException):
    """Raised when Agent 1 fails to extract ingredients from image or text."""
    pass


class RecipeHarvestError(CookCastException):
    """Raised when Agent 2 fails to harvest matching recipes."""
    pass


class SynthesisError(CookCastException):
    """Raised when Agent 3 fails to reconcile recipes into a golden ratio."""
    pass


class AudioGenerationError(CookCastException):
    """Raised when Agent 4 or Agent 5 fails during script or TTS rendering."""
    pass
