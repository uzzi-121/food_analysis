from typing import List, Optional
from ..core.logger import setup_logger
from ..domain.models.ingredient import VisionExtractResponse
from ..domain.models.recipe import RecipeCandidate, SynthesizedRecipe, CookingStep
from ..domain.models.audio import TTSGenerationResponse
from ..agents.vision_agent import IngredientVisionAgent
from ..agents.harvester_agent import RecipeHarvesterAgent
from ..agents.synthesizer_agent import GoldenRecipeSynthesizerAgent
from ..agents.script_agent import VoiceScriptAgent
from ..agents.tts_agent import TTSAudioAgent

logger = setup_logger("Orchestrator")


class CookCastOrchestrator:
    """Master Orchestrator for the 5-Agent Chain Pipeline."""

    def __init__(
        self,
        vision_agent: Optional[IngredientVisionAgent] = None,
        harvester_agent: Optional[RecipeHarvesterAgent] = None,
        synthesizer_agent: Optional[GoldenRecipeSynthesizerAgent] = None,
        script_agent: Optional[VoiceScriptAgent] = None,
        tts_agent: Optional[TTSAudioAgent] = None
    ):
        self.vision_agent = vision_agent or IngredientVisionAgent()
        self.harvester_agent = harvester_agent or RecipeHarvesterAgent()
        self.synthesizer_agent = synthesizer_agent or GoldenRecipeSynthesizerAgent()
        self.script_agent = script_agent or VoiceScriptAgent()
        self.tts_agent = tts_agent or TTSAudioAgent(script_agent=self.script_agent)

    async def step1_extract_ingredients(
        self,
        text_input: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ) -> VisionExtractResponse:
        """Execute Agent 1: Ingredient Vision Extractor."""
        return await self.vision_agent.analyze(
            text_input=text_input,
            image_bytes=image_bytes,
            mime_type=mime_type
        )

    async def step2_recommend_recipes(self, ingredients: List[str]) -> List[RecipeCandidate]:
        """Execute Agent 2: Recipe Harvester (traditional ingredient match)."""
        return await self.harvester_agent.recommend_recipes(ingredients)

    async def step2_discover_by_intent(self, query: str, context_ingredients: List[str] = []) -> List[RecipeCandidate]:
        """Execute Agent 2: Recipe Harvester (Natural language intent discovery)."""
        return await self.harvester_agent.recommend_by_intent(query, context_ingredients)

    async def step3_synthesize_recipe(self, recipe_id: str, available_ingredients: List[str]) -> SynthesizedRecipe:
        """Execute Agent 3: Golden Recipe Synthesizer."""
        return await self.synthesizer_agent.synthesize(recipe_id, available_ingredients)

    async def step4_and_5_render_audio(self, recipe_id: str, dish_title: str, steps: List[CookingStep]) -> TTSGenerationResponse:
        """Execute Agent 4 & 5: Script Crafter and TTS Audio Engine."""
        return await self.tts_agent.render_recipe_audio(recipe_id, dish_title, steps)


orchestrator = CookCastOrchestrator()
