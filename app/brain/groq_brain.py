"""
NOVA AI - AI Brain (Groq)
Manages conversation history and generates responses via Groq.
"""

from groq import Groq
from app.config import config
from app.utils import display


class NovaBrain:
    """Maintains conversation state and communicates with the Groq LLM."""

    def __init__(self) -> None:
        self._client = Groq(api_key=config.GROQ_API_KEY)
        self._history: list[dict] = []
        self._system_message = {
            "role": "system",
            "content": config.system_prompt(),
        }

   

    def chat(self, user_input: str) -> str:
        """Send a user message and return NOVA's response."""
        self._history.append({"role": "user", "content": user_input})
        self._trim_history()

        display.thinking()

        try:
            response = self._client.chat.completions.create(
                model=config.GROQ_MODEL,
                messages=[self._system_message] + self._history,
                temperature=0.75,
                max_tokens=700,
            )
            reply = response.choices[0].message.content.strip()

        except Exception as e:
            display.clear_thinking()
            display.error(f"Groq API error: {e}")
            reply = "I'm sorry, I hit a temporary connection issue. Please try again in a moment."

        display.clear_thinking()
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def reset_memory(self) -> None:
        self._history.clear()

    def history(self) -> list[dict]:
        return list(self._history)

    @property
    def history_length(self) -> int:
        return len(self._history)

    

    def _trim_history(self) -> None:
        max_messages = config.MAX_HISTORY * 2  
        if len(self._history) > max_messages:
            self._history = self._history[-max_messages:]
