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


# Curated High-Resolution Real Food Image Catalogue
INGREDIENT_IMAGE_CATALOGUE = {
    "두부": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&auto=format&fit=crop&q=80",
    "대파": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=400&auto=format&fit=crop&q=80",
    "파": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?w=400&auto=format&fit=crop&q=80",
    "양파": "https://images.unsplash.com/photo-1508747703725-719777637510?w=400&auto=format&fit=crop&q=80",
    "김치": "https://images.unsplash.com/photo-1583032015879-bf6b5bb8b438?w=400&auto=format&fit=crop&q=80",
    "신김치": "https://images.unsplash.com/photo-1583032015879-bf6b5bb8b438?w=400&auto=format&fit=crop&q=80",
    "묵은지": "https://images.unsplash.com/photo-1583032015879-bf6b5bb8b438?w=400&auto=format&fit=crop&q=80",
    "스팸": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&auto=format&fit=crop&q=80",
    "햄": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&auto=format&fit=crop&q=80",
    "계란": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&auto=format&fit=crop&q=80",
    "달걀": "https://images.unsplash.com/photo-1582722872445-44dc5f7e3c8f?w=400&auto=format&fit=crop&q=80",
    "돼지고기": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&auto=format&fit=crop&q=80",
    "삼겹살": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&auto=format&fit=crop&q=80",
    "목살": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=400&auto=format&fit=crop&q=80",
    "소고기": "https://images.unsplash.com/photo-1558030006-450675393462?w=400&auto=format&fit=crop&q=80",
    "차돌박이": "https://images.unsplash.com/photo-1558030006-450675393462?w=400&auto=format&fit=crop&q=80",
    "된장": "https://images.unsplash.com/photo-1584269600464-37b1b58a9fe7?w=400&auto=format&fit=crop&q=80",
    "마늘": "https://images.unsplash.com/photo-1615477039757-3f338d384073?w=400&auto=format&fit=crop&q=80",
    "고추": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400&auto=format&fit=crop&q=80",
    "청양고추": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=400&auto=format&fit=crop&q=80",
    "감자": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&auto=format&fit=crop&q=80",
    "당근": "https://images.unsplash.com/photo-1598170845058-32b9d6a5c317?w=400&auto=format&fit=crop&q=80",
    "참치": "https://images.unsplash.com/photo-1534482421-64566f976cfa?w=400&auto=format&fit=crop&q=80",
    "애호박": "https://images.unsplash.com/photo-1590779033100-9f60a05a013d?w=400&auto=format&fit=crop&q=80",
    "버섯": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&auto=format&fit=crop&q=80",
    "밥": "https://images.unsplash.com/photo-1516684732162-798a0062be99?w=400&auto=format&fit=crop&q=80",
}


@router.get("/image")
async def get_ingredient_image(name: str):
    """Retrieve verified high-resolution food image from external web/catalogue."""
    cleaned = name.strip()
    for key, url in INGREDIENT_IMAGE_CATALOGUE.items():
        if key in cleaned or cleaned in key:
            return {"name": name, "image_url": url}
    # Dynamic culinary fallback image
    return {
        "name": name,
        "image_url": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&auto=format&fit=crop&q=80"
    }

