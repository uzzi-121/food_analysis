from food_analysis.domain.protocols import (
    IVisionAgent,
    IHarvesterAgent,
    ISynthesizerAgent,
    IScriptAgent,
    ITTSAgent,
)
from food_analysis.agents import (
    IngredientVisionAgent,
    RecipeHarvesterAgent,
    GoldenRecipeSynthesizerAgent,
    VoiceScriptAgent,
    TTSAudioAgent,
)


def test_agent_protocols_compliance():
    """Verify that all 5 domain agents adhere to their respective runtime Protocols."""
    vision = IngredientVisionAgent()
    harvester = RecipeHarvesterAgent()
    synthesizer = GoldenRecipeSynthesizerAgent()
    script = VoiceScriptAgent()
    tts = TTSAudioAgent()

    assert isinstance(vision, IVisionAgent)
    assert isinstance(harvester, IHarvesterAgent)
    assert isinstance(synthesizer, ISynthesizerAgent)
    assert isinstance(script, IScriptAgent)
    assert isinstance(tts, ITTSAgent)
