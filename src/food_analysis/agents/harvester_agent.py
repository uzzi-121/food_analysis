from typing import List, Optional
from .base import BaseAgent
from ..domain.models.recipe import RecipeCandidate
from ..infrastructure.adapters.search_client import SearchClient
from ..infrastructure.adapters.youtube_client import YouTubeClient


class RecipeHarvesterAgent(BaseAgent):
    """Agent 2: Recipe Harvester.
    Harvests verified chef recipes from web search & YouTube knowledge base
    based on available user ingredients.
    """

    def __init__(
        self,
        search_client: Optional[SearchClient] = None,
        youtube_client: Optional[YouTubeClient] = None
    ):
        super().__init__(name="Agent-2:RecipeHarvester")
        self.search_client = search_client or SearchClient()
        self.youtube_client = youtube_client or YouTubeClient()

    async def recommend_recipes(self, ingredients: List[str]) -> List[RecipeCandidate]:
        """Harvest and rank top 3 recipe candidates matching available ingredients."""
        self.log_step(f"Harvesting recipes for ingredients: {ingredients}")
        raw_matches = self.search_client.find_matching_recipes(ingredients)

        candidates: List[RecipeCandidate] = []
        for item in raw_matches[:3]:  # Top 3 curated recipes as per plan
            recipe = item["recipe"]
            yt_data = self.youtube_client.fetch_chef_insights(recipe["id"])
            source_ref = f"{yt_data.get('channel', '요리 연구소')} & 상위 블로그 종합"

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
                source_reference=source_ref
            ))

        return candidates
