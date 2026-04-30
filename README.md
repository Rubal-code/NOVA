# 🤖 NOVA AI — Neural Optimized Voice Assistant

> A fast, intelligent, voice-powered AI assistant built with **Groq** (Llama 3), **SpeechRecognition**, and **gTTS**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🧠 AI Brain | Groq API (Llama 3 70B — ultra fast inference) |
| 🎙 Voice Input | Google Speech Recognition |
| 🔊 Voice Output | gTTS (online) or pyttsx3 (offline fallback) |
| 💬 Memory | Full conversation history (configurable depth) |
| ⌨️ Text Mode | Auto-fallback if microphone is unavailable |
| 🌐 Web Commands | Open YouTube, Google, search the web |
| 🕐 System Commands | Time, date, system info, screenshot |
| 🎨 Styled CLI | Colorful, readable terminal output |
| 🔒 Secure Config | API keys in `.env`, never in source |

---

## 🚀 Quick Start

### 1. Clone & enter the project
```bash
git clone https://github.com/Rubal-code/NOVA-AI.git
cd NOVA-AI
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note for Linux/macOS:** PyAudio needs PortAudio:
> ```bash
> # Ubuntu/Debian
> sudo apt-get install portaudio19-dev python3-pyaudio
>
> # macOS (Homebrew)
> brew install portaudio
> ```

### 4. Configure your API key
```bash
cp .env.example .env
# Open .env and set your GROQ_API_KEY
# Get a free key at https://console.groq.com
```

### 5. Run NOVA
```bash
python run.py
```

---

## ⚙️ Configuration

All settings live in your `.env` file:

```env
GROQ_API_KEY=your_key_here       # Required
GROQ_MODEL=llama3-70b-8192       # AI model
ASSISTANT_NAME=Nova              # Her name
USER_NAME=Boss                   # Your name
WAKE_WORD=nova                   # Trigger word
TTS_ENGINE=gtts                  # gtts or pyttsx3
SR_LANGUAGE=en-US                # Recognition language
MAX_HISTORY=20                   # Conversation memory depth
```

---

## 🗣️ Voice Commands

| Say... | Action |
|---|---|
| "What time is it?" | Current time |
| "What's today's date?" | Current date |
| "Open YouTube" | Opens YouTube |
| "Search Google for Python tutorials" | Google search |
| "Clear memory" | Resets conversation history |
| "System info" | OS and machine info |
| "Take a screenshot" | Saves screenshot (needs pyautogui) |
| "Play music" | Opens YouTube Music |
| "Goodbye" / "Exit" | Shuts down NOVA |

---

## 📁 Project Structure

```
NOVA-AI/
├── run.py                  # Entry point
├── requirements.txt        # Dependencies
├── .env.example            # Config template
├── .gitignore
└── app/
    ├── main.py             # Main orchestrator
    ├── config.py           # Configuration manager
    ├── voice/
    │   ├── listener.py     # Speech recognition
    │   └── speaker.py      # Text-to-speech
    ├── brain/
    │   └── groq_brain.py   # AI (Groq / Llama 3)
    ├── commands/
    │   └── handler.py      # Built-in commands
    └── utils/
        └── display.py      # Styled CLI output
```

---

## 🤝 Contributing

PRs and issues are welcome! Please open an issue before making large changes.

---

## 📄 License

MIT — free to use, modify, and distribute.
