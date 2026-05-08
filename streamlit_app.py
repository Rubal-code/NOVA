"""Futuristic Streamlit frontend for NOVA."""

import streamlit as st

from app.brain.groq_brain import NovaBrain
from app.commands.handler import CommandHandler

st.set_page_config(page_title="NOVA • Futuristic Assistant", page_icon="🤖", layout="wide")

st.markdown(
    """
    <style>
    .stApp {background: radial-gradient(circle at 20% 20%, #1d2671 0%, #0f1020 35%, #090a13 100%); color: #EAEAF8;}
    .nova-title {font-size: 2.2rem; font-weight: 700; color: #7df9ff; text-shadow: 0 0 15px #7df9ff66;}
    .nova-sub {color: #bfc7ff; margin-bottom: 1rem;}
    .chat-box {border: 1px solid #2f3a7a; border-radius: 14px; padding: 0.75rem; background: #11142a88;}
    </style>
    """,
    unsafe_allow_html=True,
)

if "brain" not in st.session_state:
    st.session_state.brain = NovaBrain()
if "handler" not in st.session_state:
    st.session_state.handler = CommandHandler(on_reset_memory=st.session_state.brain.reset_memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='nova-title'>NOVA // FUTURE CONSOLE</div>", unsafe_allow_html=True)
st.markdown("<div class='nova-sub'>Human-like assistant for chat, research, headlines, and task execution.</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("Control Panel")
    if st.button("Clear Memory"):
        st.session_state.brain.reset_memory()
        st.session_state.messages = []
        st.success("Memory cleared.")

for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

user_prompt = st.chat_input("Ask NOVA anything (e.g., 'today headlines', 'create ppt on AI roadmap').")
if user_prompt:
    st.session_state.messages.append(("user", user_prompt))
    handled, command_response = st.session_state.handler.process(user_prompt)
    reply = command_response if handled and command_response != "__EXIT__" else st.session_state.brain.chat(user_prompt)
    st.session_state.messages.append(("assistant", reply))
    st.rerun()