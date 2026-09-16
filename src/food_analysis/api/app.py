from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from ..core.config import settings
from ..core.logger import setup_logger
from .v1.router import api_v1_router

logger = setup_logger("FastAPIApp")


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="냉장고 식재료 기반 실시간 레시피 종합 및 핸즈프리 오디오 가이드 AI 에이전트",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount Static Files & Templates
    settings.STATIC_DIR.mkdir(parents=True, exist_ok=True)
    settings.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
    templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

    # Include API v1 router
    app.include_router(api_v1_router)

    @app.get("/", tags=["UI"])
    async def read_root(request: Request):
        """Serve the CookCast AI Single Page Web Application."""
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": settings.APP_NAME,
                "version": settings.APP_VERSION
            }
        )

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "tts_engine": settings.TTS_ENGINE
        }

    return app


app = create_app()
