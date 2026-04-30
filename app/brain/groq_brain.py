"""
NOVA AI - AI Brain (Groq)
Manages conversation history and generates responses via Groq.
"""

from groq import Groq
from app.config import config
from app.utils import display


class NovaBrain:
    """
    Maintains conversation state and communicates with the Groq LLM.
    """

    def __init__(self) -> None:
        self._client = Groq(api_key=config.GROQ_API_KEY)
        self._history: list[dict] = []
        self._system_message = {
            "role": "system",
            "content": config.system_prompt(),
        }

    # ── Public API ───────────────────────────────────────────────────────────

    def chat(self, user_input: str) -> str:
        """
        Send a user message and return NOVA's response.
        Conversation history is kept automatically.
        """
        self._history.append({"role": "user", "content": user_input})
        self._trim_history()

        display.thinking()

        try:
            response = self._client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[self._system_message] + self._history,
                temperature=0.7,
                max_tokens=512,
            )
            reply = response.choices[0].message.content.strip()

        except Exception as e:
            display.clear_thinking()
            display.error(f"Groq API error: {e}")
            reply = "I'm sorry, I ran into an issue connecting to my brain. Please try again."

        display.clear_thinking()
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def reset_memory(self) -> None:
        """Clear conversation history."""
        self._history.clear()

    @property
    def history_length(self) -> int:
        return len(self._history)

    # ── Private helpers ──────────────────────────────────────────────────────

    def _trim_history(self) -> None:
        """Keep conversation history within MAX_HISTORY pairs."""
        max_messages = config.MAX_HISTORY * 2  # pairs → messages
        if len(self._history) > max_messages:
            self._history = self._history[-max_messages:]
