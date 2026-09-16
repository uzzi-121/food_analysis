import sys
from pathlib import Path

# Add src to sys.path for direct execution
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import uvicorn
from food_analysis.core.config import settings

if __name__ == "__main__":
    print("============================================================")
    print("🍳 CookCast AI - 최신 Clean Architecture 멀티 에이전트 가동")
    print(f"   ▶ 로컬 웹 URL : http://localhost:{settings.PORT}")
    print(f"   ▶ API 문서    : http://localhost:{settings.PORT}/docs")
    print("============================================================")
    uvicorn.run(
        "food_analysis.api.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
