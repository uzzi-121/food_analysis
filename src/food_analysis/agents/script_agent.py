from typing import List, Optional
from .base import BaseAgent
from ..domain.models.recipe import CookingStep
from ..infrastructure.adapters.gemini_client import GeminiClient


class VoiceScriptAgent(BaseAgent):
    """Agent 4: Voice Script & SSML Crafter.
    Transforms recipe steps into radio chef podcast style script with SSML tags and timing pauses.
    """

    def __init__(self, gemini_client: Optional[GeminiClient] = None):
        super().__init__(name="Agent-4:ScriptCrafter")
        self.gemini_client = gemini_client or GeminiClient()

    def craft_ssml_script(self, dish_title: str, steps: List[CookingStep]) -> str:
        """Create a complete SSML document for the recipe."""
        self.log_step(f"Crafting SSML script for {dish_title} ({len(steps)} steps)")
        ssml_parts = [
            '<speak>',
            '  <p>',
            f'    안녕하세요! 쿡캐스트 오디오 셰프입니다. 오늘 냉장고 재료로 함께 만들어볼 요리는 <emphasis level="moderate">{dish_title}</emphasis>입니다.',
            '    손에 물이나 양념이 묻어도 괜찮으니 편안하게 제 목소리를 들으며 따라와 주세요.',
            '  </p>',
            '  <break time="2s"/>'
        ]

        for step in steps:
            ssml_parts.append(f'  <s>{step.step_number}단계, {step.title}입니다.</s>')
            ssml_parts.append('  <p>')
            ssml_parts.append(f'    {step.audio_script}')
            ssml_parts.append('  </p>')
            pause = step.pause_seconds if step.pause_seconds else 3
            ssml_parts.append(f'  <break time="{pause}s"/>')

        ssml_parts.append('  <p>요리가 맛있게 완성되었습니다! 오늘도 맛있는 집밥 드시고 행복한 하루 보내세요.</p>')
        ssml_parts.append('</speak>')

        return "\n".join(ssml_parts)

    def prepare_step_script(self, step: CookingStep) -> str:
        """Generate speech-ready plain text for individual step playback."""
        timer_text = f" 타이머 {step.timer_seconds // 60}분 맞춰드릴게요!" if step.timer_seconds and step.timer_seconds >= 60 else ""
        return f"{step.step_number}단계, {step.title}. {step.audio_script}{timer_text}"
