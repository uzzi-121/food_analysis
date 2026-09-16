import asyncio
from typing import List, Optional
from .base import BaseAgent
from ..domain.models.recipe import CookingStep
from ..domain.models.audio import TTSGenerationResponse, StepAudioInfo
from ..infrastructure.adapters.tts_engine import TTSEngine
from .script_agent import VoiceScriptAgent


class TTSAudioAgent(BaseAgent):
    """Agent 5: TTS Audio Rendering & Chunking Engine.
    Converts scripts and SSML into streamable MP3 files, supporting individual step-level audio navigation.
    """

    def __init__(
        self,
        tts_engine: Optional[TTSEngine] = None,
        script_agent: Optional[VoiceScriptAgent] = None
    ):
        super().__init__(name="Agent-5:TTSAudioEngine")
        self.tts_engine = tts_engine or TTSEngine()
        self.script_agent = script_agent or VoiceScriptAgent()

    async def render_recipe_audio(
        self,
        recipe_id: str,
        dish_title: str,
        steps: List[CookingStep]
    ) -> TTSGenerationResponse:
        """Render audio for each individual cooking step and assemble audio response."""
        self.log_step(f"Rendering step-by-step audio for recipe {recipe_id} ({dish_title})")

        # 1. Build SSML script
        ssml_full = self.script_agent.craft_ssml_script(dish_title, steps)

        # 2. Render each step's audio concurrently
        async def process_step(step: CookingStep) -> StepAudioInfo:
            filename = f"{recipe_id}_step_{step.step_number}.mp3"
            script_text = self.script_agent.prepare_step_script(step)

            # Generate file via TTSEngine
            audio_url = await self.tts_engine.synthesize_to_file(script_text, filename)
            if not audio_url:
                audio_url = f"/api/v1/audio/stream/{filename}"

            duration = self.tts_engine.estimate_duration_seconds(script_text)

            return StepAudioInfo(
                step_number=step.step_number,
                step_title=step.title,
                audio_filename=filename,
                audio_url=audio_url,
                duration_seconds=duration,
                timer_seconds=step.timer_seconds,
                pause_seconds=step.pause_seconds,
                script_text=step.audio_script
            )

        # Run synthesis tasks concurrently
        tasks = [process_step(step) for step in steps]
        step_audios = await asyncio.gather(*tasks)
        step_audios = list(step_audios)
        step_audios.sort(key=lambda s: s.step_number)

        # 3. Render full audio
        full_filename = f"{recipe_id}_full.mp3"
        full_audio_url = await self.tts_engine.synthesize_to_file(ssml_full, full_filename)

        return TTSGenerationResponse(
            recipe_id=recipe_id,
            full_audio_url=full_audio_url or f"/api/v1/audio/stream/{full_filename}",
            step_audios=step_audios,
            ssml_script=ssml_full,
            engine_used="edge"
        )
