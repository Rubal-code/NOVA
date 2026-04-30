"""
NOVA AI - Main Orchestrator
Ties together: voice input → command handling → AI brain → voice output
"""

import sys
import datetime

from app.config import config
from app.utils import display
from app.voice.listener import listen
from app.voice.speaker import speak
from app.brain.groq_brain import NovaBrain
from app.commands.handler import CommandHandler


def _greet(brain: NovaBrain) -> None:
    hour = datetime.datetime.now().hour
    period = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
    greeting = (
        f"Good {period}, {config.USER_NAME}! "
        f"I'm {config.ASSISTANT_NAME}, your neural optimized voice assistant. "
        f"How can I help you today?"
    )
    display.nova_says(greeting)
    speak(greeting)


def _handle_text_mode(brain: NovaBrain, commands: CommandHandler) -> None:
    display.warn("Microphone not available — running in TEXT mode.")
    display.info("Type your message and press Enter. Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input(f"  {display.C.GREEN}You:{display.C.RESET} ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        display.user_says(user_input)
        handled, response = commands.process(user_input)

        if handled:
            if response == "__EXIT__":
                break
            display.nova_says(response)
            speak(response)
        else:
            reply = brain.chat(user_input)
            display.nova_says(reply)
            speak(reply)

        display.divider()


def _handle_voice_mode(brain: NovaBrain, commands: CommandHandler) -> None:
    wake = config.WAKE_WORD.lower()
    display.info(f"Say '{wake}' to wake me up | Say 'exit' or 'goodbye' to quit.\n")

    while True:
        try:
            user_input = listen()
        except KeyboardInterrupt:
            break

        if not user_input:
            continue

        # ── Wake word gate ────────────────────────────────────────────────────
        # Use whole-word matching so "innova" doesn't trigger "nova"
        words = user_input.lower().split()
        is_exit = any(w in words for w in ("exit", "quit", "goodbye", "bye", "shutdown"))
        has_wake = wake in words

        if not has_wake and not is_exit:
            # Quietly ignore — not addressed to NOVA
            continue

        display.user_says(user_input)

        # ── Built-in commands ─────────────────────────────────────────────────
        handled, response = commands.process(user_input)

        if handled:
            if response == "__EXIT__":
                break
            display.nova_says(response)
            speak(response)
        else:
            # ── AI brain ──────────────────────────────────────────────────────
            reply = brain.chat(user_input)
            display.nova_says(reply)
            speak(reply)

        display.divider()


def start_nova() -> None:
    display.banner()

    try:
        config.validate()
    except EnvironmentError as e:
        display.error(str(e))
        sys.exit(1)

    display.success(f"Groq model  : {config.GROQ_MODEL}")
    display.success(f"TTS engine  : {config.TTS_ENGINE}")
    display.success(f"Wake word   : {config.WAKE_WORD}")
    display.success(f"User        : {config.USER_NAME}")
    display.divider()

    brain = NovaBrain()
    commands = CommandHandler(on_reset_memory=brain.reset_memory)

    _greet(brain)
    display.divider()

    try:
        import speech_recognition as sr
        import pyaudio  # noqa: F401
        _handle_voice_mode(brain, commands)
    except ImportError:
        _handle_text_mode(brain, commands)
    except Exception as e:
        display.warn(f"Microphone init failed ({e}) — switching to text mode.")
        _handle_text_mode(brain, commands)

    farewell = f"Goodbye, {config.USER_NAME}! Have a wonderful day."
    display.nova_says(farewell)
    speak(farewell)
    display.divider()
    display.info("NOVA shut down. See you next time! 👋\n")