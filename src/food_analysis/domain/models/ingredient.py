from typing import List, Optional
from pydantic import BaseModel, Field


class IngredientItem(BaseModel):
    """Normalized refrigerator ingredient item."""
    name: str = Field(..., description="식재료명 (예: 신김치, 대파, 스팸)")
    category: str = Field(default="기타", description="카테고리 (채소, 육류, 가공식품, 양념 등)")
    quantity_estimate: Optional[str] = Field(default="적당량", description="추정 수량 또는 분량")
    freshness: Optional[str] = Field(default="신선함", description="신선도 상태")


class VisionExtractRequest(BaseModel):
    """Manual text-input or direct ingredient parse request."""
    text_input: Optional[str] = Field(None, description="자유형 텍스트 (예: 냉장고에 김치 반포기랑 스팸 한캔, 대파 있어)")


class VisionExtractResponse(BaseModel):
    """Response DTO for Agent 1 ingredient extraction."""
    ingredients: List[IngredientItem]
    detected_count: int
    source: str = Field(default="gemini_vision", description="분석 소스 ('gemini_vision', 'text_parser', 'mock')")
    raw_summary: Optional[str] = None
