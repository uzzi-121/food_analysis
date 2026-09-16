from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from ...core.config import settings
from ...core.logger import setup_logger
from ...domain.models.audio import TTSGenerationRequest, TTSGenerationResponse
from ...workflows.orchestrator import CookCastOrchestrator
from ..dependencies import get_orchestrator

logger = setup_logger("AudioAPI")
router = APIRouter(prefix="/audio", tags=["Audio"])


@router.post("/generate", response_model=TTSGenerationResponse)
async def generate_audio(
    payload: TTSGenerationRequest,
    orchestrator: CookCastOrchestrator = Depends(get_orchestrator)
):
    """Agent 4 & 5: Generate friendly radio chef script and step-by-step TTS audio."""
    response = await orchestrator.step4_and_5_render_audio(
        recipe_id=payload.recipe_id,
        dish_title=payload.dish_title,
        steps=payload.steps
    )
    return response


@router.get("/stream/{filename}")
async def stream_audio(filename: str):
    """Stream generated MP3 audio chunk."""
    safe_name = Path(filename).name
    file_path = settings.AUDIO_DIR / safe_name

    if not file_path.exists():
        logger.warning(f"Audio file not found: {file_path}")
        raise HTTPException(status_code=404, detail="오디오 파일을 찾을 수 없습니다.")

    return FileResponse(
        path=str(file_path),
        media_type="audio/mpeg",
        filename=safe_name
    )
