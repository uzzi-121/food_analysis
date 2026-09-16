from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Package root: src/food_analysis
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
# Project root: food_analysis (where .env, pyproject.toml live)
PROJECT_ROOT = PACKAGE_ROOT.parent.parent


class Settings(BaseSettings):
    """Application configuration managed by Pydantic-Settings v2."""

    APP_NAME: str = "CookCast AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # AI & API Keys
    GEMINI_API_KEY: str = ""
    GEMINI_VISION_MODEL: str = "gemini-2.0-flash"
    GEMINI_TEXT_MODEL: str = "gemini-3.8-flash"

    # TTS Settings
    TTS_ENGINE: str = "edge"  # 'edge' or 'google'
    EDGE_TTS_VOICE: str = "ko-KR-SunHiNeural"
    GCP_TTS_VOICE: str = "ko-KR-Neural2-A"

    # Firebase Settings for Google Authentication
    FIREBASE_API_KEY: str = ""
    FIREBASE_AUTH_DOMAIN: str = ""
    FIREBASE_PROJECT_ID: str = ""
    FIREBASE_STORAGE_BUCKET: str = ""
    FIREBASE_MESSAGING_SENDER_ID: str = ""
    FIREBASE_APP_ID: str = ""

    # Directory Paths
    STATIC_DIR: Path = PACKAGE_ROOT / "web" / "static"
    TEMPLATES_DIR: Path = PACKAGE_ROOT / "web" / "templates"
    STORAGE_DIR: Path = PACKAGE_ROOT / "storage"
    UPLOAD_DIR: Path = PACKAGE_ROOT / "storage" / "uploads"
    AUDIO_DIR: Path = PACKAGE_ROOT / "storage" / "audio"
    CACHE_DIR: Path = PACKAGE_ROOT / "storage" / "cache"
    COMMUNITY_DIR: Path = PACKAGE_ROOT / "storage" / "community"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    def init_storage(self) -> None:
        """Ensure all storage and asset directories exist."""
        self.STATIC_DIR.mkdir(parents=True, exist_ok=True)
        self.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        self.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self.COMMUNITY_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.init_storage()
