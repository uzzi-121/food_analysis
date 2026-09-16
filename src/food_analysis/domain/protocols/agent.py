from typing import Protocol, runtime_checkable, List, Optional
from ..models.ingredient import VisionExtractResponse
from ..models.recipe import RecipeCandidate, SynthesizedRecipe, CookingStep
from ..models.audio import TTSGenerationResponse


@runtime_checkable
class IVisionAgent(Protocol):
    """Protocol for Agent 1: Refrigerator Ingredient Vision Extractor."""
    async def analyze(
        self,
        text_input: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ) -> VisionExtractResponse:
        ...


@runtime_checkable
class IHarvesterAgent(Protocol):
    """Protocol for Agent 2: Recipe Harvester."""
    async def recommend_recipes(self, ingredients: List[str]) -> List[RecipeCandidate]:
        ...


@runtime_checkable
class ISynthesizerAgent(Protocol):
    """Protocol for Agent 3: Golden Recipe Synthesizer."""
    async def synthesize(self, recipe_id: str, available_ingredients: List[str]) -> SynthesizedRecipe:
        ...


@runtime_checkable
class IScriptAgent(Protocol):
    """Protocol for Agent 4: Voice Script & SSML Crafter."""
    def craft_ssml_script(self, dish_title: str, steps: List[CookingStep]) -> str:
        ...
    def prepare_step_script(self, step: CookingStep) -> str:
        ...


@runtime_checkable
class ITTSAgent(Protocol):
    """Protocol for Agent 5: TTS Audio Engine."""
    async def render_recipe_audio(self, recipe_id: str, dish_title: str, steps: List[CookingStep]) -> TTSGenerationResponse:
        ...
