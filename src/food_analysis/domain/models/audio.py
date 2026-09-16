from typing import List, Optional
from pydantic import BaseModel, Field
from .recipe import CookingStep


class TTSGenerationRequest(BaseModel):
    recipe_id: str
    dish_title: str
    steps: List[CookingStep]


class StepAudioInfo(BaseModel):
    """Audio metadata and timing for an individual cooking step."""
    step_number: int
    step_title: str
    audio_filename: str
    audio_url: str
    duration_seconds: float = 0.0
    timer_seconds: Optional[int] = None
    pause_seconds: int = 3
    script_text: str


class TTSGenerationResponse(BaseModel):
    """Response DTO for Agent 4 & 5 audio rendering."""
    recipe_id: str
    full_audio_url: Optional[str] = None
    step_audios: List[StepAudioInfo] = Field(default_factory=list)
    ssml_script: str = ""
    engine_used: str = Field(default="edge", description="'edge' or 'google'")
