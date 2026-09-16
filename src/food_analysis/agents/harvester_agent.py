from typing import List, Optional
from .base import BaseAgent
from ..domain.models.recipe import RecipeCandidate
from ..infrastructure.adapters.search_client import SearchClient
from ..infrastructure.adapters.youtube_client import YouTubeClient
from ..infrastructure.adapters.gemini_client import GeminiClient


class RecipeHarvesterAgent(BaseAgent):
    """Agent 2: Recipe Harvester.
    Harvests verified chef recipes based on available ingredients and user natural language intent.
    """

    def __init__(
        self,
        search_client: Optional[SearchClient] = None,
        youtube_client: Optional[YouTubeClient] = None,
        gemini_client: Optional[GeminiClient] = None
    ):
        super().__init__(name="Agent-2:RecipeHarvester")
        self.search_client = search_client or SearchClient()
        self.youtube_client = youtube_client or YouTubeClient()
        self.gemini_client = gemini_client or GeminiClient()

    async def recommend_recipes(self, ingredients: List[str]) -> List[RecipeCandidate]:
        """Harvest and rank top 3 recipe candidates matching available ingredients."""
        self.log_step(f"Harvesting recipes for ingredients: {ingredients}")
        raw_matches = self.search_client.find_matching_recipes(ingredients)

        candidates: List[RecipeCandidate] = []
        for item in raw_matches[:3]:
            recipe = item["recipe"]
            yt_data = self.youtube_client.fetch_chef_insights(recipe["id"])
            views_str = f" (조회수 {yt_data.get('views')})" if yt_data.get('views') else ""
            source_ref = f"{yt_data.get('channel', '요리 연구소')}{views_str} & 상위 인기 레시피 종합"

            candidates.append(RecipeCandidate(
                id=recipe["id"],
                title=recipe["title"],
                description=recipe["subtitle"],
                match_rate=item["match_rate"],
                matched_ingredients=item["matched_ingredients"],
                missing_ingredients=item["missing_ingredients"],
                estimated_time_minutes=recipe["prep_time_min"] + recipe["cook_time_min"],
                difficulty=recipe["difficulty"],
                tags=recipe["tags"],
                thumbnail_emoji=recipe["thumbnail_emoji"],
                source_reference=source_ref,
                ai_reasoning=f"보유 중인 재료 {len(item['matched_ingredients'])}개와 가장 잘 어울리는 추천 요리입니다.",
                intent_score=item["match_rate"]
            ))

        return candidates

    async def recommend_by_intent(self, query: str, context_ingredients: List[str] = []) -> List[RecipeCandidate]:
        """Analyze natural language intent and recommend top recipes with AI reasoning."""
        self.log_step(f"Discovering recipes by natural query: '{query}', context ingredients: {context_ingredients}")

        # 1. Analyze intent via Gemini Adapter (taking both query and context ingredients)
        all_recipes = self.search_client.recipe_database
        intent_data = await self.gemini_client.analyze_cooking_intent(
            query=query,
            recipe_catalogue=all_recipes,
            context_ingredients=context_ingredients
        )

        # Merge ingredients from query and context
        merged_ingredients = list(set(context_ingredients + intent_data.get("extracted_ingredients", [])))

        # 2. Get base ingredient match rankings
        raw_matches = self.search_client.find_matching_recipes(merged_ingredients)

        best_id = intent_data.get("best_recipe_id")
        reasoning = intent_data.get("reasoning", "사용자의 취향과 상황에 딱 맞는 추천 요리입니다.")
        mood = intent_data.get("mood", "맞춤 요리")

        # 3. Re-rank based on intent: Best matched recipe comes first with high score
        candidates: List[RecipeCandidate] = []

        # Find best recipe first
        best_item = next((m for m in raw_matches if m["recipe"]["id"] == best_id), None)
        if not best_item:
            best_recipe_obj = self.search_client.get_recipe_by_id(best_id) or all_recipes[0]
            best_item = {
                "recipe": best_recipe_obj,
                "match_rate": 85,
                "matched_ingredients": merged_ingredients,
                "missing_ingredients": []
            }

        yt_data = self.youtube_client.fetch_chef_insights(best_item["recipe"]["id"])
        views_str = f" (조회수 {yt_data.get('views')})" if yt_data.get('views') else ""
        source_ref = f"{yt_data.get('channel', '요리 연구소')}{views_str} & 상위 인기 레시피 종합"

        # Add top intent match
        candidates.append(RecipeCandidate(
            id=best_item["recipe"]["id"],
            title=best_item["recipe"]["title"],
            description=best_item["recipe"]["subtitle"],
            match_rate=max(best_item["match_rate"], 88),
            matched_ingredients=best_item["matched_ingredients"],
            missing_ingredients=best_item["missing_ingredients"],
            estimated_time_minutes=best_item["recipe"]["prep_time_min"] + best_item["recipe"]["cook_time_min"],
            difficulty=best_item["recipe"]["difficulty"],
            tags=best_item["recipe"]["tags"] + [f"#{mood}"],
            thumbnail_emoji=best_item["recipe"]["thumbnail_emoji"],
            source_reference=source_ref,
            ai_reasoning=reasoning,
            intent_score=96
        ))

        # Add remaining matches (excluding the best one)
        for item in raw_matches:
            if item["recipe"]["id"] == best_id:
                continue
            if len(candidates) >= 3:
                break

            recipe = item["recipe"]
            yt_info = self.youtube_client.fetch_chef_insights(recipe["id"])
            views_info = f" (조회수 {yt_info.get('views')})" if yt_info.get('views') else ""
            source = f"{yt_info.get('channel', '요리 연구소')}{views_info} & 상위 인기 레시피 종합"

            candidates.append(RecipeCandidate(
                id=recipe["id"],
                title=recipe["title"],
                description=recipe["subtitle"],
                match_rate=item["match_rate"],
                matched_ingredients=item["matched_ingredients"],
                missing_ingredients=item["missing_ingredients"],
                estimated_time_minutes=recipe["prep_time_min"] + recipe["cook_time_min"],
                difficulty=recipe["difficulty"],
                tags=recipe["tags"],
                thumbnail_emoji=recipe["thumbnail_emoji"],
                source_reference=source,
                ai_reasoning=f"함께 고려해볼 수 있는 {recipe['title']}입니다.",
                intent_score=max(50, item["match_rate"])
            ))

        return candidates
