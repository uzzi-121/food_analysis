"""Base Agent abstract class for the CookCast AI multi-agent architecture."""

from abc import ABC
import logging
from ..core.logger import setup_logger


class BaseAgent(ABC):
    """Abstract base class for all domain agents."""

    def __init__(self, name: str):
        self.name = name
        self.logger = setup_logger(name)

    def log_step(self, message: str) -> None:
        """Helper to log agent-specific execution steps."""
        self.logger.info(f"[{self.name}] {message}")
