from typing import List, Dict, Any, Optional
from ...core.logger import setup_logger

logger = setup_logger("SearchAdapter")


class SearchClient:
    """Grounding & Web Recipe Knowledge Search Adapter."""

    def __init__(self):
        # Curated repository of verified home-chef recipes (matching Plan specifications)
        self.recipe_database: List[Dict[str, Any]] = [
            {
                "id": "spam-kimchi-fried-rice",
                "title": "스팸 김치볶음밥",
                "subtitle": "파기름과 진간장 눌림으로 불맛을 낸 15분 완성 황금 레시피",
                "primary_ingredients": ["김치", "신김치", "스팸", "대파", "계란", "밥"],
                "optional_ingredients": ["양파", "참기름", "고춧가루", "김가루", "통깨", "설탕"],
                "prep_time_min": 5,
                "cook_time_min": 10,
                "difficulty": "쉬움",
                "tags": ["#15분컷", "#초간단", "#자취요리", "#밥도둑"],
                "thumbnail_emoji": "🍳",
                "chef_secrets": [
                    "스팸을 옥수수알 크기로 작게 깍둑썰기해야 밥알과 완벽하게 어우러집니다.",
                    "팬 가장자리에 진간장 1큰술을 둘러 살짝 눌어붙게 태워 불맛을 입히는 것이 핵심!",
                    "신김치의 톡 쏘는 신맛은 설탕 반 스푼으로 감칠맛 나게 잡아줍니다."
                ],
                "sources": [
                    {"title": "백종원의 요리비책 - 초간단 김치볶음밥의 정석", "url": "https://youtube.com/watch?v=sample_kimchi1"},
                    {"title": "만개의 레시피 - 실패 없는 스팸 김치볶음밥 황금비율", "url": "https://10000recipe.com/recipe/sample1"}
                ],
                "default_seasoning": [
                    {"name": "진간장", "ratio": "1 큰술", "tip": "팬 가장자리에 둘러 불맛 내기"},
                    {"name": "설탕", "ratio": "0.5 큰술", "tip": "김치의 신맛 중화"},
                    {"name": "고춧가루", "ratio": "1 작은술", "tip": "먹음직스러운 붉은 색감"},
                    {"name": "참기름", "ratio": "1 작은술", "tip": "마지막 불 끄고 둘러주기"}
                ],
                "substitutions": [
                    {"target": "스팸", "substitute": "베이컨, 돼지고기 다짐육, 참치캔, 비엔나 소시지"},
                    {"target": "대파", "substitute": "쪽파 또는 양파 잘게 다진 것"}
                ]
            },
            {
                "id": "pork-kimchi-jjigae",
                "title": "돼지고기 김치찌개",
                "subtitle": "돼지기름에 달달 볶아 깊은 맛을 낸 진국 김치찌개",
                "primary_ingredients": ["김치", "신김치", "돼지고기", "두부", "대파"],
                "optional_ingredients": ["양파", "스팸", "다진마늘", "고춧가루", "된장", "국간장"],
                "prep_time_min": 10,
                "cook_time_min": 20,
                "difficulty": "보통",
                "tags": ["#국물요리", "#얼큰한국물", "#백종원레시피"],
                "thumbnail_emoji": "🍲",
                "chef_secrets": [
                    "고기를 먼저 볶아 돼지기름이 충분히 배어 나오게 한 뒤 김치를 볶아주세요.",
                    "된장 반 작은술을 국물에 풀어 넣으면 군내를 잡고 묵직한 감칠맛이 폭발합니다."
                ],
                "sources": [
                    {"title": "백종원 PAIK JONG WON - 전문점 맛 김치찌개 끓이는 법", "url": "https://youtube.com/watch?v=sample_pork1"},
                    {"title": "수미네 반찬 - 묵은지 돼지고기 찌개", "url": "https://tv.naver.com/sample2"}
                ],
                "default_seasoning": [
                    {"name": "다진 마늘", "ratio": "1 큰술", "tip": "국물의 알싸한 풍미"},
                    {"name": "고춧가루", "ratio": "1.5 큰술", "tip": "얼큰한 칼칼함"},
                    {"name": "국간장", "ratio": "1 큰술", "tip": "깊은 간 맞추기"},
                    {"name": "된장", "ratio": "0.5 작은술", "tip": "돼지고기 잡내 제거 비법"}
                ],
                "substitutions": [
                    {"target": "돼지고기", "substitute": "참치캔 1캔 또는 스팸 1캔"},
                    {"target": "두부", "substitute": "어묵, 버섯류 또는 떡국떡"}
                ]
            },
            {
                "id": "rolled-omelet",
                "title": "폭신폭신 호텔식 계란말이",
                "subtitle": "대파와 당근을 넣어 부드럽고 도톰하게 말아내는 영양 반찬",
                "primary_ingredients": ["계란", "달걀", "대파"],
                "optional_ingredients": ["양파", "당근", "스팸", "치즈", "우유", "맛술"],
                "prep_time_min": 5,
                "cook_time_min": 10,
                "difficulty": "쉬움",
                "tags": ["#단백질폭탄", "#아이반찬", "#초스피드"],
                "thumbnail_emoji": "🥚",
                "chef_secrets": [
                    "계란물에 우유나 물 2스푼을 섞고 체에 한번 걸러주면 카스텔라처럼 부드러워집니다.",
                    "약불에서 인내심을 갖고 2~3번에 나누어 부어가며 말아주는 것이 핵심입니다."
                ],
                "sources": [
                    {"title": "류수영 어남선생 계란말이 꿀팁", "url": "https://youtube.com/watch?v=sample_egg1"}
                ],
                "default_seasoning": [
                    {"name": "소금", "ratio": "0.3 작은술", "tip": "간 맞추기"},
                    {"name": "맛술(또는 설탕)", "ratio": "0.5 작은술", "tip": "달걀 비린내 제거 및 윤기"},
                    {"name": "우유(선택)", "ratio": "2 큰술", "tip": "부드러운 식감"}
                ],
                "substitutions": [
                    {"target": "우유", "substitute": "물 2큰술 또는 마요네즈 반 큰술"},
                    {"target": "맛술", "substitute": "설탕 한 꼬집이나 미림"}
                ]
            },
            {
                "id": "soybean-paste-stew",
                "title": "차돌 된장찌개",
                "subtitle": "구수한 된장과 애호박, 두부가 어우러진 정통 뚝배기 찌개",
                "primary_ingredients": ["된장", "두부", "대파", "양파"],
                "optional_ingredients": ["돼지고기", "소고기", "애호박", "감자", "청양고추", "다진마늘"],
                "prep_time_min": 10,
                "cook_time_min": 15,
                "difficulty": "보통",
                "tags": ["#구수한맛", "#든든한한끼", "#집밥정석"],
                "thumbnail_emoji": "🥘",
                "chef_secrets": [
                    "멸치 육수 또는 쌀뜨물을 사용하면 국물 맛이 훨씬 깊고 부드러워집니다.",
                    "고춧가루 반 스푼을 더해 칼칼한 끝맛을 살려주세요."
                ],
                "sources": [
                    {"title": "백종원 집밥 백선생 - 된장찌개 만능 베이스", "url": "https://youtube.com/watch?v=sample_doenjang1"}
                ],
                "default_seasoning": [
                    {"name": "재래식 된장", "ratio": "2 큰술", "tip": "채에 걸러 맑게 풀기"},
                    {"name": "고춧가루", "ratio": "0.5 큰술", "tip": "칼칼한 풍미"},
                    {"name": "다진 마늘", "ratio": "1 작은술", "tip": "감칠맛 업"}
                ],
                "substitutions": [
                    {"target": "두부", "substitute": "감자, 버섯류 또는 순두부"},
                    {"target": "애호박", "substitute": "양배추 또는 오이"}
                ]
            },
            {
                "id": "egg-fried-rice",
                "title": "황금 계란 볶음밥",
                "subtitle": "파기름과 굴소스 향이 솔솔 나는 10분 중국집 스타일 볶음밥",
                "primary_ingredients": ["계란", "달걀", "대파", "밥"],
                "optional_ingredients": ["스팸", "양파", "굴소스", "진간장", "참기름"],
                "prep_time_min": 3,
                "cook_time_min": 7,
                "difficulty": "쉬움",
                "tags": ["#10분완성", "#중국집볶음밥", "#초간단"],
                "thumbnail_emoji": "🍚",
                "chef_secrets": [
                    "밥을 넣기 전 스크램블 에그를 미리 고슬고슬하게 만들어 팬 한쪽에 밀어두세요.",
                    "센 불에서 수분을 날리며 볶아주어야 밥알이 뭉치지 않습니다."
                ],
                "sources": [
                    {"title": "백종원 초간단 계란볶음밥", "url": "https://youtube.com/watch?v=sample_egg_rice1"}
                ],
                "default_seasoning": [
                    {"name": "진간장", "ratio": "1 작은술", "tip": "간 맞추기"},
                    {"name": "굴소스", "ratio": "0.5 큰술", "tip": "중화풍 감칠맛"},
                    {"name": "참기름", "ratio": "0.5 작은술", "tip": "마무리 고소함"}
                ],
                "substitutions": [
                    {"target": "굴소스", "substitute": "진간장 1큰술 + 설탕 한 꼬집 또는 치킨스톡"},
                    {"target": "대파", "substitute": "쪽파"}
                ]
            },
            {
                "id": "spam-tofu-kimchi",
                "title": "백종원식 스팸 두부김치",
                "subtitle": "노릇하게 구운 스팸과 들기름에 달달 볶은 신김치를 따뜻한 두부에 곁들인 10분 완성 황금 안주",
                "primary_ingredients": ["김치", "신김치", "두부", "스팸"],
                "optional_ingredients": ["대파", "양파", "참기름", "들기름", "설탕", "고춧가루", "통깨"],
                "prep_time_min": 3,
                "cook_time_min": 7,
                "difficulty": "쉬움",
                "tags": ["#10분안주", "#맥주안주", "#야식", "#초간단", "#백종원레시피", "#두부요리"],
                "thumbnail_emoji": "🥓",
                "chef_secrets": [
                    "스팸을 도톰하게 썰어 노릇노릇하게 구워내면 자체 기름이 배어 나와 김치와 환상의 궁합을 이룹니다.",
                    "신김치는 들기름이나 참기름에 설탕 반 스푼을 넣고 센 불에서 수분을 날리며 볶아 감칠맛을 극대화하세요.",
                    "두부는 끓는 물에 1분 데치거나 전자레인지에 1분 30초 돌려 따끈따끈하게 곁들이면 훨씬 부드럽습니다."
                ],
                "sources": [
                    {"title": "백종원의 요리비책 - 술이 술술 들어가는 초간단 두부김치", "url": "https://youtube.com/watch?v=sample_tofu_kimchi1"}
                ],
                "default_seasoning": [
                    {"name": "설탕", "ratio": "0.5 큰술", "tip": "신김치의 신맛 중화 및 감칠맛 폭발"},
                    {"name": "참기름(또는 들기름)", "ratio": "1 큰술", "tip": "김치 볶을 때 고소한 풍미"},
                    {"name": "고춧가루", "ratio": "0.5 큰술", "tip": "먹음직스러운 색감"},
                    {"name": "통깨", "ratio": "약간", "tip": "플레이팅 마무리"}
                ],
                "substitutions": [
                    {"target": "스팸", "substitute": "돼지고기 삼겹살/앞다리살, 베이컨, 참치캔"},
                    {"target": "두부", "substitute": "계란말이 또는 어묵"}
                ]
            },
            {
                "id": "kimchi-pancake",
                "title": "바삭한 스팸 김치전",
                "subtitle": "신김치와 스팸을 쫑쫑 썰어 겉바속촉으로 부쳐내는 실패 없는 야식 안주",
                "primary_ingredients": ["김치", "신김치", "부침가루", "스팸"],
                "optional_ingredients": ["대파", "양파", "고춧가루", "설탕"],
                "prep_time_min": 5,
                "cook_time_min": 8,
                "difficulty": "쉬움",
                "tags": ["#야식", "#맥주안주", "#비오는날", "#초간단", "#10분완성"],
                "thumbnail_emoji": "🥞",
                "chef_secrets": [
                    "반죽에 차가운 탄산수나 얼음물을 섞어주면 글루텐 형성이 억제되어 바삭함이 오래 유지됩니다.",
                    "기름을 넉넉히 두르고 센 불에서 가장자리부터 튀기듯이 부쳐주는 것이 바삭한 식감의 비결입니다."
                ],
                "sources": [
                    {"title": "백종원의 요리비책 - 전집보다 바삭한 김치전 황금비법", "url": "https://youtube.com/watch?v=sample_kimchi_pancake"}
                ],
                "default_seasoning": [
                    {"name": "설탕", "ratio": "0.3 큰술", "tip": "김치 신맛 제거"},
                    {"name": "고춧가루", "ratio": "1 큰술", "tip": "먹음직스러운 붉은 색감"},
                    {"name": "부침가루", "ratio": "1 컵", "tip": "바삭한 반죽 베이스"}
                ],
                "substitutions": [
                    {"target": "스팸", "substitute": "참치캔, 오징어, 돼지고기 다짐육"}
                ]
            }
        ]

    def find_matching_recipes(self, user_ingredients: List[str]) -> List[Dict[str, Any]]:
        """Calculate match percentage for each recipe based on user ingredients."""
        normalized_user_ings = [ing.strip().lower() for ing in user_ingredients if ing.strip()]
        results = []

        for recipe in self.recipe_database:
            all_recipe_ings = recipe["primary_ingredients"] + recipe["optional_ingredients"]

            matched = []
            for user_ing in normalized_user_ings:
                for r_ing in all_recipe_ings:
                    if user_ing in r_ing.lower() or r_ing.lower() in user_ing:
                        if r_ing not in matched:
                            matched.append(r_ing)

            # Match score weighting: primary ingredients are essential
            primary_matched = [r for r in recipe["primary_ingredients"] if any(u in r.lower() or r.lower() in u for u in normalized_user_ings)]
            primary_rate = len(primary_matched) / max(len(recipe["primary_ingredients"]), 1)

            # Calculate base match rate
            if len(primary_matched) == 0:
                # If user lacks ALL primary ingredients, they CANNOT realistically cook this dish
                match_percentage = min(20, int((len(matched) / max(len(all_recipe_ings), 1)) * 30))
            else:
                match_percentage = min(100, int((primary_rate * 70) + (len(matched) / max(len(all_recipe_ings), 1) * 30)))
                # Boost if multiple primary ingredients match
                if len(primary_matched) >= 2:
                    match_percentage = max(match_percentage, 75)
                elif len(primary_matched) == 1:
                    match_percentage = max(match_percentage, 50)

            # Missing primary ingredients
            missing = [r for r in recipe["primary_ingredients"] if r not in matched]

            results.append({
                "recipe": recipe,
                "match_rate": match_percentage,
                "matched_ingredients": matched,
                "missing_ingredients": missing,
                "primary_matched_count": len(primary_matched)
            })

        # Sort by highest match rate, then by primary matched count and total matched ingredients
        results.sort(key=lambda x: (x["match_rate"], x["primary_matched_count"], len(x["matched_ingredients"])), reverse=True)
        return results

    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        for r in self.recipe_database:
            if r["id"] == recipe_id:
                return r
        return None
