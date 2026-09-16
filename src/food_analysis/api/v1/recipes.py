from typing import List
from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends
from ...core.logger import setup_logger
from ...domain.models.recipe import RecipeCandidate, SynthesizedRecipe, RecipeSynthesizerRequest
from ...workflows.orchestrator import CookCastOrchestrator
from ..dependencies import get_orchestrator

logger = setup_logger("RecipesAPI")
router = APIRouter(prefix="/recipes", tags=["Recipes"])


class RecommendRequest(BaseModel):
    ingredients: List[str] = Field(..., description="보유 식재료 이름 리스트")


@router.post("/recommend", response_model=List[RecipeCandidate])
async def recommend_recipes(
    payload: RecommendRequest,
    orchestrator: CookCastOrchestrator = Depends(get_orchestrator)
):
    """Agent 2: Harvest top recipe recommendations based on available ingredients."""
    candidates = await orchestrator.step2_recommend_recipes(payload.ingredients)
    return candidates


@router.post("/synthesize", response_model=SynthesizedRecipe)
async def synthesize_recipe(
    payload: RecipeSynthesizerRequest,
    orchestrator: CookCastOrchestrator = Depends(get_orchestrator)
):
    """Agent 3: Synthesize golden ratio recipe with steps and substitute advice."""
    synthesized = await orchestrator.step3_synthesize_recipe(
        recipe_id=payload.recipe_id,
        available_ingredients=payload.available_ingredients
    )
    return synthesized
