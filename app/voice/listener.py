"""
NOVA AI - Speech Recognition (Listener)
"""

import speech_recognition as sr
from app.config import config
from app.utils import display

_recognizer = sr.Recognizer()
_recognizer.energy_threshold = 400          # Higher = less sensitive to background noise
_recognizer.dynamic_energy_threshold = True  # Auto-adjusts to ambient noise
_recognizer.dynamic_energy_adjustment_damping = 0.15
_recognizer.pause_threshold = 0.8           # Seconds of silence to mark end of phrase
_recognizer.non_speaking_duration = 0.5


def listen(prompt: bool = True) -> str | None:
    """
    Listen for speech and return transcribed text, or None if nothing heard.
    """
    if prompt:
        display.listening_indicator()

    try:
        with sr.Microphone() as source:
            # Calibrate for ambient noise every time (0.3s is quick but effective)
            _recognizer.adjust_for_ambient_noise(source, duration=0.3)

            try:
                audio = _recognizer.listen(
                    source,
                    timeout=config.SR_TIMEOUT,
                    phrase_time_limit=config.SR_PHRASE_LIMIT,
                )
            except sr.WaitTimeoutError:
                return None  # Silence — normal, just loop

    except OSError:
        # Microphone not available
        raise

    try:
        text = _recognizer.recognize_google(audio, language=config.SR_LANGUAGE)
        text = text.strip()
        # Filter out very short noise triggers (single chars, empty)
        if len(text) < 2:
            return None
        return text.lower()

    except sr.UnknownValueError:
        return None   # Heard noise but couldn't understand — silent ignore
    except sr.RequestError as e:
        display.error(f"Speech recognition unavailable: {e}")
        return None


def listen_for_wake_word() -> bool:
    text = listen(prompt=False)
    if text:
        words = text.split()
        return config.WAKE_WORD.lower() in words
    return False