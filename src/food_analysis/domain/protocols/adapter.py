from typing import Protocol, runtime_checkable, List, Dict, Any, Optional


@runtime_checkable
class IGeminiAdapter(Protocol):
    """Protocol for Gemini Multi-modal & LLM client."""
    async def extract_ingredients_from_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> List[Dict[str, Any]]:
        ...
    async def generate_script(self, prompt: str) -> str:
        ...


@runtime_checkable
class ISearchAdapter(Protocol):
    """Protocol for Recipe Knowledge Base search."""
    def find_matching_recipes(self, user_ingredients: List[str]) -> List[Dict[str, Any]]:
        ...
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        ...


@runtime_checkable
class IYouTubeAdapter(Protocol):
    """Protocol for Chef YouTube Insights."""
    def fetch_chef_insights(self, dish_id: str) -> Dict[str, Any]:
        ...


@runtime_checkable
class ITTSEngineAdapter(Protocol):
    """Protocol for Neural TTS rendering."""
    async def synthesize_to_file(self, text_or_ssml: str, output_filename: str) -> Optional[str]:
        ...
    def estimate_duration_seconds(self, text: str) -> float:
        ...
