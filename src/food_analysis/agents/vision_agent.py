import re
from typing import List, Optional
from .base import BaseAgent
from ..domain.models.ingredient import IngredientItem, VisionExtractResponse
from ..infrastructure.adapters.gemini_client import GeminiClient


class IngredientVisionAgent(BaseAgent):
    """Agent 1: Ingredient Vision Extractor.
    Extracts and normalizes refrigerator ingredients from images or free-form text.
    """

    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        super().__init__(name="Agent-1:VisionExtractor")
        self.gemini_client = gemini_client or GeminiClient()

        # Korean culinary categories mapping
        self.category_keywords = {
            "채소": ["양파", "대파", "파", "마늘", "고추", "청양고추", "애호박", "호박", "감자", "당근", "배추", "김치", "신김치", "묵은지", "버섯", "깻잎", "상추", "시금치", "콩나물"],
            "육류": ["돼지고기", "소고기", "닭고기", "삼겹살", "목살", "앞다리살", "차돌박이", "다짐육", "베이컨"],
            "해산물": ["오징어", "새우", "바지락", "멸치", "고등어", "참치"],
            "유제품": ["계란", "달걀", "우유", "치즈", "버터"],
            "가공식품": ["스팸", "햄", "소시지", "두부", "순두부", "어묵", "참치캔", "만두", "라면"],
            "양념 및 소스": ["진간장", "국간장", "된장", "고추장", "고춧가루", "설탕", "소금", "참기름", "식용유", "굴소스", "맛술", "후추"]
        }

    def _categorize(self, name: str) -> str:
        for cat, keywords in self.category_keywords.items():
            for kw in keywords:
                if kw in name:
                    return cat
        return "기타"

    def _extract_from_text(self, text: str) -> List[IngredientItem]:
        """Parse natural Korean text (comma, space, line breaks) into structured ingredients."""
        cleaned = re.sub(r'(그리고|와|과|랑|하고)', ',', text)
        tokens = [t.strip() for t in re.split(r'[,/\n]+', cleaned) if t.strip()]

        ingredients = []
        quantity_pattern = r'(\d+\s*(?:개|마리|줄|봉|캔|대|모|팩|근|g|kg|ml|L|큰술|작은술|스푼|공기|쪽)?|반\s*(?:포기|개|모|캔|공기|마리)|약간|적당량)$'
        for token in tokens:
            match = re.search(r'^(.*?)\s*' + quantity_pattern, token)
            if match and match.group(1).strip():
                raw_name = match.group(1).strip()
                raw_qty = match.group(2).strip() if match.group(2) else "적당량"
            else:
                raw_name = token.strip()
                raw_qty = "적당량"

            if len(raw_name) >= 1:
                ingredients.append(IngredientItem(
                    name=raw_name,
                    category=self._categorize(raw_name),
                    quantity_estimate=raw_qty,
                    freshness="신선함"
                ))

        return ingredients

    async def analyze(
        self,
        text_input: Optional[str] = None,
        image_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg"
    ) -> VisionExtractResponse:
        """Run vision extraction or text parsing agent."""
        if image_bytes:
            self.log_step("Extracting ingredients from refrigerator photo via Vision Extractor...")
            result = await self.gemini_client.extract_ingredients_from_image(image_bytes, mime_type)
            items = [
                IngredientItem(
                    name=item["name"],
                    category=item.get("category", self._categorize(item["name"])),
                    quantity_estimate=item.get("quantity_estimate", "적당량"),
                    freshness=item.get("freshness", "신선함")
                )
                for item in result.get("ingredients", [])
            ]
            if text_input and text_input.strip():
                text_items = self._extract_from_text(text_input)
                existing_names = {i.name for i in items}
                for ti in text_items:
                    if ti.name not in existing_names:
                        items.append(ti)

            return VisionExtractResponse(
                ingredients=items,
                detected_count=len(items),
                source="gemini_vision",
                raw_summary=result.get("summary", "냉장고 사진 분석이 완료되었습니다.")
            )

        if text_input and text_input.strip():
            self.log_step(f"Parsing ingredients from text: {text_input}")
            items = self._extract_from_text(text_input)
            item_names = ", ".join([i.name for i in items])
            return VisionExtractResponse(
                ingredients=items,
                detected_count=len(items),
                source="text_parser",
                raw_summary=f"입력하신 식재료 [{item_names}] 목록을 인식했습니다."
            )

        # Fallback default items
        default_names = ["신김치", "스팸", "대파", "계란"]
        items = [
            IngredientItem(name=n, category=self._categorize(n), quantity_estimate="적당량", freshness="신선함")
            for n in default_names
        ]
        return VisionExtractResponse(
            ingredients=items,
            detected_count=len(items),
            source="mock",
            raw_summary="기본 냉장고 추천 식재료 세트입니다."
        )
