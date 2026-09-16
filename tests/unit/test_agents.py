import pytest
from food_analysis.agents.vision_agent import IngredientVisionAgent
from food_analysis.agents.harvester_agent import RecipeHarvesterAgent
from food_analysis.agents.synthesizer_agent import GoldenRecipeSynthesizerAgent
from food_analysis.agents.script_agent import VoiceScriptAgent
from food_analysis.agents.tts_agent import TTSAudioAgent
from food_analysis.domain.models.recipe import CookingStep


@pytest.mark.asyncio
async def test_agent1_vision_text_extraction():
    agent = IngredientVisionAgent()
    res = await agent.analyze(text_input="신김치 반포기, 스팸 1캔, 대파 1대, 계란 2개")
    assert len(res.ingredients) >= 4
    names = [i.name for i in res.ingredients]
    assert "신김치" in names
    assert "스팸" in names
    assert res.detected_count == len(res.ingredients)


@pytest.mark.asyncio
async def test_agent2_harvester_recommendation():
    agent = RecipeHarvesterAgent()
    candidates = await agent.recommend_recipes(["김치", "스팸", "대파", "계란"])
    assert len(candidates) >= 1
    assert candidates[0].id == "spam-kimchi-fried-rice"
    assert candidates[0].match_rate > 50


@pytest.mark.asyncio
async def test_agent2_intent_discovery():
    agent = RecipeHarvesterAgent()
    # Query: Rainy day & spicy hot soup
    candidates = await agent.recommend_by_intent("오늘 비 오는데 얼큰한 국물 요리 먹고 싶어")
    assert len(candidates) >= 1
    assert candidates[0].id == "pork-kimchi-jjigae"
    assert candidates[0].ai_reasoning is not None
    assert "국물" in candidates[0].ai_reasoning or "얼큰" in candidates[0].ai_reasoning

    # Query: Late-night beer snack
    snack_candidates = await agent.recommend_by_intent("맥주랑 먹을 10분 간단 안주")
    assert len(snack_candidates) >= 1
    assert snack_candidates[0].id == "rolled-omelet"
    assert snack_candidates[0].ai_reasoning is not None

    # Dual input: Ingredients ['계란', '돼지고기'] + Desired recipe '얼큰한 국물 요리'
    dual_candidates = await agent.recommend_by_intent(
        query="얼큰한 국물 요리",
        context_ingredients=["계란", "돼지고기"]
    )
    assert len(dual_candidates) >= 1
    assert dual_candidates[0].id == "pork-kimchi-jjigae"
    assert "돼지고기" in dual_candidates[0].ai_reasoning

    # User scenario: '매콤한 두부 조림 알려줘' with pantry ingredients ['두부', '대파', '양파']
    tofu_candidates = await agent.recommend_by_intent(
        query="매콤한 두부 조림 알려줘",
        context_ingredients=["두부", "대파", "양파"]
    )
    assert len(tofu_candidates) == 2  # Exactly 2 curated recipes
    assert tofu_candidates[0].id == "spicy-braised-tofu"
    assert "두부조림" in tofu_candidates[0].title
    assert tofu_candidates[0].intent_score >= 90
    assert tofu_candidates[0].match_rate >= 95  # >= 90% requirement (top is 95%+)
    assert tofu_candidates[1].match_rate >= 90  # 2nd candidate is also >= 90%
    assert all(c.match_rate >= 90 for c in tofu_candidates)


@pytest.mark.asyncio
async def test_agent3_synthesizer():
    agent = GoldenRecipeSynthesizerAgent()
    recipe = await agent.synthesize("spam-kimchi-fried-rice", ["김치", "스팸", "대파"])
    assert recipe.title == "스팸 김치볶음밥"
    assert len(recipe.steps) >= 3
    assert len(recipe.seasoning_ratios) > 0
    assert len(recipe.substitutions) > 0
    assert recipe.video_id is not None
    assert recipe.steps[0].image_url is not None

    tofu_recipe = await agent.synthesize("spicy-braised-tofu", ["두부", "대파", "양파"])
    assert "두부조림" in tofu_recipe.title
    assert tofu_recipe.video_id == "w2X3P78C7n4"
    assert len(tofu_recipe.steps) == 4
    assert tofu_recipe.steps[0].image_url == "/static/images/steps/spicy-braised-tofu_step1.svg"


def test_agent4_script_ssml_crafter():
    agent = VoiceScriptAgent()
    steps = [
        CookingStep(
            step_number=1,
            title="재료 썰기",
            guide_text="대파와 스팸을 썰어주세요.",
            audio_script="첫 번째 단계, 대파와 스팸을 썰어주세요.",
            pause_seconds=3,
            heat_level="없음"
        )
    ]
    ssml = agent.craft_ssml_script("스팸 김치볶음밥", steps)
    assert "<speak>" in ssml
    assert "</speak>" in ssml
    assert '<break time="3s"/>' in ssml


@pytest.mark.asyncio
async def test_agent5_tts_rendering():
    tts_agent = TTSAudioAgent()
    steps = [
        CookingStep(
            step_number=1,
            title="재료 썰기",
            guide_text="대파를 송송 썰어주세요.",
            audio_script="첫 번째 단계, 대파를 얇게 썰어주세요.",
            pause_seconds=3,
            heat_level="없음"
        )
    ]
    res = await tts_agent.render_recipe_audio("test-recipe", "테스트 요리", steps)
    assert len(res.step_audios) == 1
    assert "test-recipe_step_1.mp3" in res.step_audios[0].audio_url
