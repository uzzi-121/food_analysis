import pytest
import sys
from pathlib import Path

# Ensure src is in sys.path during test runs
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from fastapi.testclient import TestClient
from food_analysis.api.app import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Session-scoped FastAPI test client."""
    return TestClient(app)
