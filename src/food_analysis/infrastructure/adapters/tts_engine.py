import re
from typing import Optional
from ...core.config import settings
from ...core.logger import setup_logger

logger = setup_logger("TTSAdapter")


class TTSEngine:
    """High Quality Neural Korean TTS Engine Adapter (Edge-TTS & Google TTS ready)."""

    def __init__(self):
        self.voice = settings.EDGE_TTS_VOICE
        self.audio_dir = settings.AUDIO_DIR

    def _clean_ssml_for_speech(self, text: str) -> str:
        """Convert SSML tags into natural speech pauses and readable text."""
        # Replace break times with ellipses / periods for natural pause
        text = re.sub(r'<break\s+time=["\']?(\d+)s["\']?\s*\/?>', r'... ', text)
        text = re.sub(r'<break\s+time=["\']?(\d+)ms["\']?\s*\/?>', r'.. ', text)
        # Strip other XML/SSML tags like <speak>, <p>, <s>, <emphasis>
        text = re.sub(r'<[^>]+>', '', text)
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    async def synthesize_to_file(self, text: str, output_filename: str) -> Optional[str]:
        """Synthesize text to MP3 file in audio storage."""
        cleaned_text = self._clean_ssml_for_speech(text)
        if not cleaned_text:
            return None

        output_path = self.audio_dir / output_filename

        # Check cache: If file already exists and is non-empty, reuse it!
        if output_path.exists() and output_path.stat().st_size > 500:
            logger.info(f"Using cached audio file: {output_filename}")
            return f"/api/v1/audio/stream/{output_filename}"

        try:
            import edge_tts
            communicate = edge_tts.Communicate(text=cleaned_text, voice=self.voice)
            await communicate.save(str(output_path))
            logger.info(f"Successfully generated audio file: {output_path}")
            return f"/api/v1/audio/stream/{output_filename}"
        except Exception as e:
            logger.error(f"Error synthesizing audio with edge-tts: {e}")
            return None

    def estimate_duration_seconds(self, text: str) -> float:
        """Estimate speech duration based on Korean character count and pacing."""
        cleaned = self._clean_ssml_for_speech(text)
        # Average Korean TTS speech rate: ~5.5 characters per second
        char_count = len(cleaned.replace(" ", ""))
        pause_count = cleaned.count("...") + cleaned.count(". ")
        estimated = (char_count / 5.2) + (pause_count * 0.8)
        return round(max(3.0, estimated), 1)
