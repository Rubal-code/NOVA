"""
NOVA AI - Configuration Manager
Loads and validates all settings from .env
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ── Groq API ────────────────────────────────────────
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # ── Assistant identity ───────────────────────────────
    ASSISTANT_NAME: str = os.getenv("ASSISTANT_NAME", "Nova")
    USER_NAME: str = os.getenv("USER_NAME", "Boss")

    # ── Voice / TTS settings ────────────────────────────
    TTS_ENGINE: str = os.getenv("TTS_ENGINE", "gtts")      # "gtts" or "pyttsx3"
    TTS_LANGUAGE: str = os.getenv("TTS_LANGUAGE", "en")
    TTS_SLOW: bool = os.getenv("TTS_SLOW", "false").lower() == "true"

    # ── Speech recognition ──────────────────────────────
    SR_LANGUAGE: str = os.getenv("SR_LANGUAGE", "en-US")
    SR_TIMEOUT: int = int(os.getenv("SR_TIMEOUT", "7"))
    SR_PHRASE_LIMIT: int = int(os.getenv("SR_PHRASE_LIMIT", "15"))
    WAKE_WORD: str = os.getenv("WAKE_WORD", "nova").lower()

    # ── Conversation memory ─────────────────────────────
    MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "20"))
    MIC_INDEX: int = int(os.getenv("MIC_INDEX", "-1"))
    REQUIRE_WAKE_WORD: bool = os.getenv("REQUIRE_WAKE_WORD", "false").lower() == "true"

    # ── System prompt ───────────────────────────────────
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        (
            f"You are NOVA (Neural Optimized Voice Assistant), a highly intelligent, "
            f"witty, and helpful AI assistant. You speak naturally and concisely — "
            f"your responses are clear and conversational, suitable for voice output. "
            f"Avoid using markdown, bullet points, or special symbols in your responses. "
            f"Keep answers brief unless the user asks for detail. Speak like a friendly human teammate and proactively suggest practical next actions. "
            f"You are assisting a user named {{user_name}}."
        ),
    )

    @classmethod
    def validate(cls) -> None:
        """Raise an error if critical config is missing."""
        if not cls.GROQ_API_KEY:
            raise EnvironmentError(
                "❌  GROQ_API_KEY is not set.\n"
                "    Create a .env file and add: GROQ_API_KEY=your_key_here\n"
                "    Get a free key at: https://console.groq.com"
            )

    @classmethod
    def system_prompt(cls) -> str:
        return cls.SYSTEM_PROMPT.format(user_name=cls.USER_NAME)


config = Config()