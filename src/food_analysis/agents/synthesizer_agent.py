from typing import List, Optional
from .base import BaseAgent
from ..domain.models.recipe import (
    SynthesizedRecipe,
    RequiredIngredient,
    SeasoningRatio,
    CookingStep,
)
from ..infrastructure.adapters.search_client import SearchClient
from ..infrastructure.adapters.youtube_client import YouTubeClient


class GoldenRecipeSynthesizerAgent(BaseAgent):
    """Agent 3: Golden Recipe Synthesizer.
    Reconciles multiple recipe sources into a unified golden ratio recipe,
    suggests missing ingredient substitutes, and standardizes steps.
    """

    def __init__(
        self,
        search_client: Optional[SearchClient] = None,
        youtube_client: Optional[YouTubeClient] = None
    ):
        super().__init__(name="Agent-3:GoldenRecipeSynthesizer")
        self.search_client = search_client or SearchClient()
        self.youtube_client = youtube_client or YouTubeClient()

        # Step templates for key recipes
        self.steps_database = {
            "spam-kimchi-fried-rice": [
                CookingStep(
                    step_number=1,
                    title="재료 손질하기",
                    guide_text="대파는 얇게 송송 썰고, 스팸은 옥수수알 크기로 작게 깍둑썰기해주세요. 신김치는 가위로 잘게 잘라줍니다.",
                    audio_script="첫 번째 단계, 재료 썰기입니다. 대파는 얇게 송송 썰어주시고, 스팸은 옥수수알 크기로 잘게 깍둑썰기 해주세요. 신김치는 밥그릇 안에서 가위로 잘게 잘라두면 설거지거리가 줄어든답니다.",
                    pause_seconds=4,
                    timer_seconds=None,
                    heat_level="없음",
                    tips="스팸 크기를 작게 썰수록 밥알과 고르게 씹혀 맛이 살아납니다."
                ),
                CookingStep(
                    step_number=2,
                    title="파기름과 스팸 볶기",
                    guide_text="팬에 식용유 2스푼을 두르고 중불을 켠 후, 대파와 스팸을 노릇해질 때까지 1분 30초간 볶아줍니다.",
                    audio_script="두 번째 단계, 파기름과 스팸 볶기입니다. 팬에 식용유 두 스푼을 두르고 중불을 켜주세요. 썰어둔 대파와 스팸을 넣고 달달 볶아줍니다. 스팸 겉면이 노릇해지면서 맛있는 기름 냄새가 올라올 때까지 1분 30초 정도 볶아주세요.",
                    pause_seconds=3,
                    timer_seconds=90,
                    heat_level="중불",
                    tips="스팸의 자체 기름이 충분히 빠져나올 때까지 노릇하게 구워주세요."
                ),
                CookingStep(
                    step_number=3,
                    title="간장 불맛 입히기 & 김치 볶기",
                    guide_text="재료를 팬 한쪽으로 밀고, 빈 곳에 진간장 1큰술을 둘러 살짝 눌린 뒤 김치와 설탕 반 스푼을 넣고 2분간 볶습니다.",
                    audio_script="세 번째 단계, 양념과 김치 투하입니다! 볶던 재료를 팬 한쪽으로 밀어두고, 빈 공간에 진간장 한 스푼을 둘러 지글지글 끓여 불맛을 내주세요. 그 다음 썰어둔 김치를 넣고 설탕 반 스푼을 톡톡 뿌려 2분간 달달 볶아줍니다.",
                    pause_seconds=3,
                    timer_seconds=120,
                    heat_level="중강불",
                    tips="간장을 살짝 태우듯 끓여 섞어주면 식당에서 먹는 불맛이 납니다."
                ),
                CookingStep(
                    step_number=4,
                    title="밥 넣고 비비기 & 마무리 눋히기",
                    guide_text="불을 약불로 줄이고 밥 1공기를 넣어 골고루 섞어준 뒤, 센 불에서 1분간 팬에 눌러붙게 눋혀 참기름을 둘러 완성합니다.",
                    audio_script="마지막 단계입니다. 이제 불을 약불로 줄이고 따뜻한 밥 한 공기를 넣어주세요. 주걱을 세워 밥알을 가르듯이 골고루 비벼줍니다. 밥이 잘 섞였다면 팬에 넓게 펴고 센 불로 1분간 바삭하게 눋혀준 뒤, 불을 끄고 참기름 반 스푼을 둘러주면 완성입니다!",
                    pause_seconds=2,
                    timer_seconds=60,
                    heat_level="약불 ➡️ 센불",
                    tips="마지막에 계란후라이를 얹어 노른자를 터뜨려 비벼 드시면 환상적입니다."
                )
            ],
            "pork-kimchi-jjigae": [
                CookingStep(
                    step_number=1,
                    title="고기 볶아 기름 내기",
                    guide_text="냄비에 식용유 1스푼을 두르고 돼지고기(또는 스팸)를 넣어 겉면이 바삭해질 때까지 2분간 볶아줍니다.",
                    audio_script="첫 번째 단계, 고기 볶기입니다. 냄비에 불을 중불로 켜고 고기를 넣어주세요. 고기 겉면이 노릇노릇해지고 기름이 배어 나올 때까지 2분간 달달 볶아줍니다.",
                    pause_seconds=3,
                    timer_seconds=120,
                    heat_level="중불",
                    tips="고기를 먼저 바짝 볶아야 찌개 국물에 깊은 풍미가 우러납니다."
                ),
                CookingStep(
                    step_number=2,
                    title="김치와 고춧가루 볶기",
                    guide_text="김치와 고춧가루 1스푼, 다진 마늘 1스푼을 넣고 고기 기름에 2분간 함께 볶아줍니다.",
                    audio_script="두 번째 단계, 김치 볶기입니다. 썰어둔 신김치와 고춧가루 한 스푼, 다진 마늘을 넣고 고기 기름과 함께 2분간 볶아주세요.",
                    pause_seconds=3,
                    timer_seconds=120,
                    heat_level="중불",
                    tips="김치가 투명해질 때까지 충분히 볶아주어야 시원한 국물이 됩니다."
                ),
                CookingStep(
                    step_number=3,
                    title="물 붓고 된장 풀어 푹 끓이기",
                    guide_text="물 500ml(약 2컵 반)를 붓고 된장 반 작은술, 국간장 1큰술을 넣은 뒤 강불에서 7분간 푹 끓입니다.",
                    audio_script="세 번째 단계, 찌개 끓이기입니다. 물 500밀리리터를 붓고, 된장 반 작은술과 국간장 한 큰술을 풀어줍니다. 뚜껑을 덮고 강불에서 7분 동안 보글보글 끓여주세요. 타이머 7분 시작할게요!",
                    pause_seconds=4,
                    timer_seconds=420,
                    heat_level="강불",
                    tips="된장 반 스푼이 군내를 잡고 진한 감칠맛을 폭발시키는 비법입니다."
                ),
                CookingStep(
                    step_number=4,
                    title="두부, 대파 넣고 마무리",
                    guide_text="도톰하게 썬 두부와 어슷 썬 대파를 넣고 2분간만 한소끔 더 끓여 완성합니다.",
                    audio_script="마지막 단계입니다. 도톰하게 썰어둔 두부와 송송 썬 대파를 국물 위에 얹어주세요. 2분간만 더 끓여 대파 숨이 죽으면, 얼큰하고 든든한 김치찌개 완성입니다! 맛있게 드세요.",
                    pause_seconds=2,
                    timer_seconds=120,
                    heat_level="중불",
                    tips="마지막에 후춧가루를 톡톡 뿌려주면 칼칼한 향이 배가됩니다."
                )
            ],
            "rolled-omelet": [
                CookingStep(
                    step_number=1,
                    title="계란물 풀기 및 간 맞추기",
                    guide_text="볼에 계란 4개를 깨 넣고 소금 3꼬집, 우유(또는 물) 2스푼을 넣어 알끈이 풀리도록 잘 저어줍니다.",
                    audio_script="첫 번째 단계, 계란물 만들기입니다. 볼에 계란 4개를 깨 넣고, 소금 세 꼬집과 부드러움을 더해줄 우유 두 스푼을 넣어주세요. 포크나 젓가락으로 알끈이 부드럽게 풀리도록 충분히 저어줍니다.",
                    pause_seconds=3,
                    timer_seconds=None,
                    heat_level="없음",
                    tips="체에 한 번 걸러주면 카스테라처럼 결이 매끄러워집니다."
                ),
                CookingStep(
                    step_number=2,
                    title="팬 코팅 & 1차 계란물 붓기",
                    guide_text="팬에 식용유를 두르고 키친타월로 살짝 닦아낸 뒤 약불에서 계란물의 1/3을 얇게 부어줍니다.",
                    audio_script="두 번째 단계, 굽기 시작입니다. 프라이팬에 기름을 살짝 두르고, 반드시 '약불'로 켜주세요. 계란물의 3분의 1을 얇게 부어 팬 전체에 고르게 펴줍니다.",
                    pause_seconds=3,
                    timer_seconds=60,
                    heat_level="약불",
                    tips="불이 세면 계란이 부풀어 찢어지니 꼭 약불을 유지하세요."
                ),
                CookingStep(
                    step_number=3,
                    title="돌돌 말아가며 계란물 잇기",
                    guide_text="계란이 70% 익었을 때 끝에서부터 돌돌 말고, 빈 공간에 남은 계란물을 부어가며 도톰하게 말아줍니다.",
                    audio_script="세 번째 단계, 말아주기입니다. 계란 윗면이 촉촉할 때 주걱이나 젓가락으로 끝에서부터 조심스럽게 접어 말아주세요. 말아둔 계란을 한쪽으로 당기고, 빈자리에 남은 계란물을 이어 부어주며 두껍게 말아줍니다.",
                    pause_seconds=3,
                    timer_seconds=120,
                    heat_level="약불",
                    tips="완전히 다 익기 전에 말아야 층과 층 사이가 풀리지 않고 잘 붙습니다."
                ),
                CookingStep(
                    step_number=4,
                    title="한 김 식혀 썰기 및 완성",
                    guide_text="도마 위에 올려 2분간 한 김 식힌 뒤 먹기 좋은 크기로 썰어 완성합니다.",
                    audio_script="마지막 완성 단계입니다! 완성된 계란말이를 도마 위에 꺼내두고, 바로 썰지 마시고 2분 정도 한 김 식혀주세요. 온기가 살짝 식어야 부서지지 않고 예쁘게 썰립니다. 케첩을 곁들여 맛있게 드세요!",
                    pause_seconds=2,
                    timer_seconds=120,
                    heat_level="불끄기",
                    tips="뜨거울 때 바로 썰면 모양이 찌그러지므로 꼭 식힌 후 썰어주세요."
                )
            ],
            "spam-tofu-kimchi": [
                CookingStep(
                    step_number=1,
                    title="두부 데치기 및 스팸 썰기",
                    guide_text="두부는 끓는 물에 1분간 데쳐 따뜻하게 건져두고, 스팸은 0.7cm 두께로 널찍하게 썰어줍니다.",
                    audio_script="첫 번째 단계, 두부 데치기와 스팸 썰기입니다. 냄비에 물을 끓이고 두부를 통째로 넣어 1분간 따뜻하게 데쳐 건져내주세요. 그 사이 스팸은 먹음직스럽게 도톰한 크기로 썰어둡니다.",
                    pause_seconds=3,
                    timer_seconds=60,
                    heat_level="강불",
                    tips="두부를 따뜻하게 데쳐내야 스팸, 볶음김치와 어우러질 때 부드러운 식감이 극대화됩니다."
                ),
                CookingStep(
                    step_number=2,
                    title="스팸 노릇하게 굽기",
                    guide_text="팬을 달군 뒤 기름 없이 스팸을 올려 앞뒤로 노릇노릇하게 2분간 구워 접시에 덜어냅니다.",
                    audio_script="두 번째 단계, 스팸 굽기입니다. 달궈진 팬에 기름 없이 썰어둔 스팸을 올려주세요. 스팸 자체의 기름이 배어 나오며 겉면이 바삭하고 노릇해질 때까지 앞뒤로 2분간 구워 접시에 덜어둡니다.",
                    pause_seconds=3,
                    timer_seconds=120,
                    heat_level="중불",
                    tips="스팸을 굽고 남은 고소한 기름에 그대로 김치를 볶을 거예요!"
                ),
                CookingStep(
                    step_number=3,
                    title="스팸 기름에 신김치 달달 볶기",
                    guide_text="스팸 기름이 남은 팬에 신김치, 설탕 반 스푼, 고춧가루 반 스푼, 참기름 1스푼을 넣고 3분간 달달 볶아줍니다.",
                    audio_script="세 번째 단계, 마성의 김치 볶기입니다! 스팸 기름이 남은 팬에 쫑쫑 썬 신김치를 넣고, 설탕 반 스푼과 참기름 한 스푼을 둘러주세요. 중불에서 3분간 달달 볶아 김치가 투명해지고 윤기가 흐르면 불을 끕니다.",
                    pause_seconds=3,
                    timer_seconds=180,
                    heat_level="중불",
                    tips="설탕이 신김치의 톡 쏘는 신맛을 잡아주고 감칠맛을 폭발시킵니다."
                ),
                CookingStep(
                    step_number=4,
                    title="플레이팅 및 완성",
                    guide_text="데친 두부를 한 입 크기로 썰어 접시 한쪽에 돌려 담고, 구운 스팸과 볶은 김치를 올려 통깨를 뿌려 완성합니다.",
                    audio_script="마지막 단계, 플레이팅입니다. 따뜻한 두부를 먹기 좋게 썰어 접시 가장자리에 빙 둘러 담고, 가운데에 볶음김치와 노릇한 스팸을 담아주세요. 통깨를 솔솔 뿌려주면 완벽한 10분 완성 맥주 안주 두부김치 완성입니다!",
                    pause_seconds=2,
                    heat_level="불끄기",
                    tips="두부 한 조각에 스팸, 김치를 삼합으로 얹어 드시면 기가 막힙니다."
                )
            ],
            "kimchi-pancake": [
                CookingStep(
                    step_number=1,
                    title="김치와 스팸 잘게 썰기",
                    guide_text="신김치와 스팸을 가위나 칼로 잘게 깍둑썰기해 볼에 담습니다.",
                    audio_script="첫 번째 단계, 재료 썰기입니다. 신김치와 스팸을 씹는 맛이 살아있도록 잘게 썰어 큰 볼에 담아주세요.",
                    pause_seconds=3,
                    heat_level="없음"
                ),
                CookingStep(
                    step_number=2,
                    title="바삭한 반죽 만들기",
                    guide_text="부침가루 1컵, 차가운 물 1컵, 고춧가루 1스푼, 설탕 0.3스푼을 넣고 날가루가 보이지 않을 정도로만 살살 섞습니다.",
                    audio_script="두 번째 단계, 바삭한 반죽 만들기입니다. 부침가루 한 컵과 차가운 물 한 컵, 고춧가루 한 스푼을 넣고 가볍게 섞어주세요. 너무 많이 저으면 바삭함이 줄어드니 날가루만 없애주세요.",
                    pause_seconds=3,
                    heat_level="없음",
                    tips="차가운 얼음물이나 탄산수를 쓰면 훨씬 바삭해집니다."
                ),
                CookingStep(
                    step_number=3,
                    title="센 불에서 바삭하게 부치기",
                    guide_text="팬에 식용유를 넉넉히 두르고 반죽을 얇게 편 뒤 센 불에서 앞뒤로 바삭하게 3분씩 부쳐 완성합니다.",
                    audio_script="마지막 단계, 부치기입니다! 팬에 기름을 넉넉히 두르고 센 불에서 반죽을 얇게 펴주세요. 가장자리가 바삭하게 튀겨지듯 익으면 뒤집어 3분간 노릇하게 부쳐내면 완성입니다!",
                    pause_seconds=2,
                    timer_seconds=180,
                    heat_level="중강불"
                )
            ]
        }

    async def synthesize(self, recipe_id: str, available_ingredients: List[str]) -> SynthesizedRecipe:
        """Synthesize recipe ratios, substitute recommendations, and standardized steps."""
        self.log_step(f"Synthesizing golden recipe for {recipe_id} with available ingredients: {available_ingredients}")
        recipe_data = self.search_client.get_recipe_by_id(recipe_id)
        if not recipe_data:
            recipe_data = self.search_client.recipe_database[0]
            recipe_id = recipe_data["id"]

        yt_data = self.youtube_client.fetch_chef_insights(recipe_id)

        # Normalize available list
        avail_lower = [a.strip().lower() for a in available_ingredients]

        # Build required ingredients with availability check
        required_ings: List[RequiredIngredient] = []
        for ing_name in recipe_data["primary_ingredients"]:
            is_avail = any(ing_name.lower() in a or a in ing_name.lower() for a in avail_lower)
            # Find substitution hint if not available
            sub_hint = None
            if not is_avail:
                for sub in recipe_data.get("substitutions", []):
                    if sub["target"] == ing_name:
                        sub_hint = f"{sub['substitute']}으로 대체 가능"
                        break
            required_ings.append(RequiredIngredient(
                name=ing_name,
                amount="적당량",
                is_available=is_avail,
                substitute_hint=sub_hint
            ))

        # Build seasoning ratios
        seasoning_ratios = [
            SeasoningRatio(name=s["name"], ratio=s["ratio"], tip=s.get("tip"))
            for s in recipe_data.get("default_seasoning", [])
        ]

        # Get cooking steps
        steps = self.steps_database.get(recipe_id)
        if not steps:
            steps = [
                CookingStep(
                    step_number=1,
                    title="식재료 손질",
                    guide_text="준비된 재료들을 먹기 좋은 크기로 다듬어주세요.",
                    audio_script="첫 번째 단계, 재료 준비와 손질입니다. 식재료를 깨끗이 씻고 먹기 좋은 크기로 썰어주세요.",
                    pause_seconds=3,
                    heat_level="없음"
                ),
                CookingStep(
                    step_number=2,
                    title="볶기 및 조리",
                    guide_text="팬에 기름을 두르고 재료를 넣고 볶아줍니다.",
                    audio_script="두 번째 단계, 조리 시작입니다. 중불에서 재료를 달달 볶아주세요.",
                    pause_seconds=3,
                    timer_seconds=180,
                    heat_level="중불"
                ),
                CookingStep(
                    step_number=3,
                    title="완성 및 플레이팅",
                    guide_text="간을 맞추고 그릇에 담아 완성합니다.",
                    audio_script="마지막 단계입니다. 접시에 예쁘게 담아 따뜻할 때 맛있게 드세요!",
                    pause_seconds=2,
                    heat_level="불끄기"
                )
            ]

        # Substitutions dictionary
        substitutions = [
            {"target": s["target"], "substitute": s["substitute"]}
            for s in recipe_data.get("substitutions", [])
        ]

        # Combine chef secrets
        chef_secrets = recipe_data.get("chef_secrets", []) + yt_data.get("key_tips", [])

        # Calculate matching percentage
        matched_count = sum(1 for r in required_ings if r.is_available)
        match_percentage = int((matched_count / max(len(required_ings), 1)) * 100)

        # Prioritize top-viewed YouTube chef sources and verified high-ranking platforms
        synthesized_sources = []
        if yt_data and yt_data.get("channel"):
            synthesized_sources.append({
                "title": f"👑 {yt_data.get('channel')} - {yt_data.get('video_title')} (조회수 {yt_data.get('views', '100만회 이상')})",
                "url": "https://youtube.com"
            })
        for s in recipe_data.get("sources", []):
            synthesized_sources.append({
                "title": f"⭐ {s.get('title')}",
                "url": s.get("url", "#")
            })

        return SynthesizedRecipe(
            id=recipe_id,
            title=recipe_data["title"],
            subtitle=recipe_data["subtitle"],
            match_percentage=match_percentage,
            prep_time_min=recipe_data["prep_time_min"],
            cook_time_min=recipe_data["cook_time_min"],
            servings="1~2인분",
            required_ingredients=required_ings,
            seasoning_ratios=seasoning_ratios,
            substitutions=substitutions,
            steps=steps,
            chef_secrets=chef_secrets[:4],
            sources=synthesized_sources
        )
