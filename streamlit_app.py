import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import pygame
import os
import asyncio
import edge_tts

# ── Your Existing Backend Imports ─────────────────────────────
from app.brain.groq_brain import NovaBrain
from app.commands.handler import CommandHandler

# ── Streamlit Config ──────────────────────────────────────────
st.set_page_config(
    page_title="NOVA AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ── Initialize Audio Engine ───────────────────────────────────
pygame.mixer.init()

# ── Edge TTS Voice Function ───────────────────────────────────
async def edge_speak(text):

    filename = "nova_voice.mp3"

    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-GuyNeural",   # Deep Male Voice
        rate="+20%"                # Faster Speech
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()

    if os.path.exists(filename):
        os.remove(filename)


def speak(text):
    asyncio.run(edge_speak(text))

# ── Session State ─────────────────────────────────────────────
if "brain" not in st.session_state:
    st.session_state.brain = NovaBrain()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Reset Memory ──────────────────────────────────────────────
def reset_memory():
    st.session_state.messages = []

# ── Command Handler ───────────────────────────────────────────
if "handler" not in st.session_state:
    st.session_state.handler = CommandHandler(
        on_reset_memory=reset_memory
    )

# ── Header ────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; color:cyan;'>
        🤖 NOVA AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

# ── Animated AI Orb ───────────────────────────────────────────
st.markdown(
    """
    <div style="
        width:150px;
        height:150px;
        border-radius:50%;
        background:cyan;
        margin:auto;
        box-shadow:0 0 60px cyan;
        animation:pulse 2s infinite;
    ">
    </div>

    <style>
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow: 0 0 20px cyan;
        }

        50% {
            transform: scale(1.1);
            box-shadow: 0 0 80px cyan;
        }

        100% {
            transform: scale(1);
            box-shadow: 0 0 20px cyan;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ── Voice Recorder ────────────────────────────────────────────
st.markdown("## 🎤 Speak to NOVA")

audio_bytes = audio_recorder()

voice_text = None

# ── Speech Recognition ────────────────────────────────────────
if audio_bytes:

    try:
        audio_path = "temp_audio.wav"

        with open(audio_path, "wb") as f:
            f.write(audio_bytes)

        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)

        voice_text = recognizer.recognize_google(audio_data)

        st.success(f"🗣 You said: {voice_text}")

        os.remove(audio_path)

    except Exception as e:
        st.error(f"Speech recognition failed: {e}")



# Voice gets priority
user_prompt = voice_text 

# ── Display Previous Messages ─────────────────────────────────
for role, message in st.session_state.messages:

    with st.chat_message(role):
        st.markdown(message)

# ── Main Assistant Logic ──────────────────────────────────────
if user_prompt:

    # Save User Message
    st.session_state.messages.append(("user", user_prompt))

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Thinking Animation
    with st.spinner("🧠 NOVA is thinking..."):

        try:
            # Command Handler
            handled, command_response = (
                st.session_state.handler.process(user_prompt)
            )

            if handled:

                if command_response == "__EXIT__":
                    reply = "Goodbye! Shutting down NOVA."

                else:
                    reply = command_response

            else:
                # AI Brain Response
                reply = st.session_state.brain.chat(user_prompt)

        except Exception as e:
            reply = f"Error: {str(e)}"

    # Save Assistant Reply
    st.session_state.messages.append(("assistant", reply))

    # Display Assistant Reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    # Speak Assistant Reply
    speak(reply)

st.markdown("---")

st.caption("⚡ Powered by NOVA AI")