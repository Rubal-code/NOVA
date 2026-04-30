"""
NOVA AI - Text-to-Speech (Speaker)
Supports gTTS (online) and pyttsx3 (offline)
"""

import os
import sys
import tempfile
import threading
from app.config import config
from app.utils.display import warn


def _speak_gtts(text: str) -> None:
    """Online TTS via Google Text-to-Speech."""
    try:
        from gtts import gTTS

        # ── Suppress pygame's startup banner ────────────────────────────────
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
        import pygame

        tts = gTTS(text=text, lang=config.TTS_LANGUAGE, slow=config.TTS_SLOW)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tmp_path = fp.name

        tts.save(tmp_path)

        # Use pygame for playback (more reliable than playsound)
        pygame.mixer.init()
        pygame.mixer.music.load(tmp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        pygame.mixer.quit()

        os.remove(tmp_path)

    except ImportError:
        warn("pygame not found, falling back to pyttsx3.")
        _speak_pyttsx3(text)
    except Exception as e:
        warn(f"gTTS failed ({e}), falling back to pyttsx3.")
        _speak_pyttsx3(text)


def _speak_pyttsx3(text: str) -> None:
    """Offline TTS via pyttsx3."""
    try:
        import pyttsx3

        engine = pyttsx3.init()
        voices = engine.getProperty("voices")

        # Prefer a female voice if available
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                break

        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    except Exception as e:
        warn(f"pyttsx3 TTS error: {e}")
        # Last-resort fallback: print the text
        print(f"[TTS fallback]: {text}")


def speak(text: str) -> None:
    """
    Speak the given text using the configured TTS engine.
    Runs synchronously so the program waits for speech to finish.
    """
    if not text or not text.strip():
        return

    engine = config.TTS_ENGINE.lower()

    if engine == "gtts":
        _speak_gtts(text)
    else:
        _speak_pyttsx3(text)
