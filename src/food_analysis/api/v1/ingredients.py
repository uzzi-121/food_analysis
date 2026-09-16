from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends
from ...core.logger import setup_logger
from ...domain.models.ingredient import VisionExtractResponse, VisionExtractRequest
from ...workflows.orchestrator import CookCastOrchestrator
from ..dependencies import get_orchestrator

logger = setup_logger("IngredientsAPI")
router = APIRouter(prefix="/ingredients", tags=["Ingredients"])


@router.post("/extract", response_model=VisionExtractResponse)
async def extract_ingredients(
    text_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    orchestrator: CookCastOrchestrator = Depends(get_orchestrator)
):
    """Agent 1: Extract refrigerator ingredients from uploaded photo or text description."""
    image_bytes = None
    mime_type = "image/jpeg"

    if file:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        logger.info(f"Received photo upload: {file.filename}, size: {len(image_bytes)} bytes")

    result = await orchestrator.step1_extract_ingredients(
        text_input=text_input,
        image_bytes=image_bytes,
        mime_type=mime_type
    )
    return result


@router.post("/extract-json", response_model=VisionExtractResponse)
async def extract_ingredients_json(
    payload: VisionExtractRequest,
    orchestrator: CookCastOrchestrator = Depends(get_orchestrator)
):
    """JSON version of ingredient extraction for direct API clients."""
    return await orchestrator.step1_extract_ingredients(
        text_input=payload.text_input
    )
