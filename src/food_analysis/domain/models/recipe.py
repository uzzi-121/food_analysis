from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RecipeCandidate(BaseModel):
    id: str = Field(..., description="레시피 고유 식별자")
    title: str = Field(..., description="요리 명칭 (예: 스팸 김치볶음밥)")
    description: str = Field(..., description="한 줄 소개 및 특징")
    match_rate: int = Field(..., description="보유 재료 매칭률 (0~100%)")
    matched_ingredients: List[str] = Field(default_factory=list, description="매칭된 보유 재료")
    missing_ingredients: List[str] = Field(default_factory=list, description="부족한 재료")
    estimated_time_minutes: int = Field(..., description="예상 총 소요시간(분)")
    difficulty: str = Field("쉬움", description="난이도 (쉬움, 보통, 고급)")
    tags: List[str] = Field(default_factory=list, description="키워드 태그 (#초간단, #밥도둑 등)")
    thumbnail_emoji: str = Field("🍳", description="대표 이모지")
    source_reference: Optional[str] = Field("유튜브 & 인기 블로그 종합", description="참조 출처")
    # Natural Language Intent Extension
    ai_reasoning: Optional[str] = Field(None, description="사용자 의도에 맞춘 AI 추천 이유")
    intent_score: int = Field(85, description="사용자 의도 부합 점수 (0~100)")


class NaturalRecipeQueryRequest(BaseModel):
    """Request payload for natural language cooking intent discovery with optional context ingredients."""
    query: str = Field(default="", description="원하는 요리 스타일 또는 자연어 요리 요청 (예: '비 오는 날 얼큰한 국물 요리')")
    context_ingredients: List[str] = Field(default_factory=list, description="냉장고 보유 식재료 리스트 (예: ['계란', '돼지고기'])")


class CookingStep(BaseModel):
    step_number: int = Field(..., description="단계 번호 (1부터 시작)")
    title: str = Field(..., description="단계 요약 제목 (예: 재료 썰기, 파기름 내기)")
    guide_text: str = Field(..., description="텍스트 화면용 설명")
    audio_script: str = Field(..., description="오디오 TTS 전용 친절한 구어체 대본")
    pause_seconds: int = Field(3, description="대본 발화 후 행동 대기 시간(초)")
    timer_seconds: Optional[int] = Field(None, description="타이머가 필요한 경우 소요시간(초)")
    heat_level: str = Field("없음", description="불 세기 (강불, 중불, 약불, 불끄기, 없음)")
    tips: Optional[str] = Field(None, description="셰프 꿀팁")


class RecipeSynthesizerRequest(BaseModel):
    recipe_id: str = Field(..., description="선택된 레시피 ID")
    recipe_title: str = Field(..., description="요리명")
    available_ingredients: List[str] = Field(default_factory=list, description="사용자 냉장고 보유 식재료 리스트")


class RequiredIngredient(BaseModel):
    name: str
    amount: str = "적당량"
    is_available: bool = True
    substitute_hint: Optional[str] = None


class SeasoningRatio(BaseModel):
    name: str
    ratio: str
    tip: Optional[str] = None


class SynthesizedRecipe(BaseModel):
    id: str
    title: str
    subtitle: str
    match_percentage: int
    prep_time_min: int
    cook_time_min: int
    servings: str = "1~2인분"
    required_ingredients: List[RequiredIngredient] = Field(default_factory=list)
    seasoning_ratios: List[SeasoningRatio] = Field(default_factory=list)
    substitutions: List[Dict[str, str]] = Field(default_factory=list)
    steps: List[CookingStep] = Field(default_factory=list)
    chef_secrets: List[str] = Field(default_factory=list)
    sources: List[Dict[str, str]] = Field(default_factory=list)
