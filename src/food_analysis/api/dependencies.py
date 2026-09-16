from functools import lru_cache
from ..workflows.orchestrator import CookCastOrchestrator, orchestrator


@lru_cache()
def get_orchestrator() -> CookCastOrchestrator:
    """Dependency injection provider for the multi-agent orchestrator."""
    return orchestrator
