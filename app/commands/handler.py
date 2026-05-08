"""
NOVA AI - Command Handler
Uses flexible keyword matching so "open the chrome" == "open chrome"
"""

import os
import datetime
import webbrowser
import subprocess
import platform
from typing import Callable
from app.services.task_tools import TaskTools

CommandResult = tuple[bool, str | None]


def _has(text: str, *keywords) -> bool:
    """Return True if ALL keywords appear anywhere in text."""
    return all(k in text for k in keywords)


def _any_phrase(text: str, *phrases) -> bool:
    """Return True if ANY phrase is contained in text."""
    return any(p in text for p in phrases)


class CommandHandler:

    def __init__(self, on_reset_memory: Callable) -> None:
        self._reset_memory = on_reset_memory
        self._os = platform.system().lower()

    def process(self, text: str) -> CommandResult:
        t = text.lower().strip()

        # Strip wake word prefix
        for prefix in ("hey nova ", "ok nova ", "nova "):
            if t.startswith(prefix):
                t = t[len(prefix):]
                break

        # ── PC Shutdown/Restart (check BEFORE generic exit) ──────────────────
        if _has(t, "shutdown") and _any_phrase(t, "pc", "computer", "laptop", "system"):
            return True, "I won't shut down your computer automatically for safety. Please do it manually."

        if _has(t, "restart") and _any_phrase(t, "pc", "computer", "laptop", "system"):
            return True, "I won't restart your computer automatically for safety. Please do it manually."

        # ── Exit NOVA ────────────────────────────────────────────────────────
        if _any_phrase(t, "exit", "quit", "goodbye", "bye bye", "shut down nova", "stop nova"):
            return True, "__EXIT__"
        if t in ("bye", "shutdown", "stop"):
            return True, "__EXIT__"

        # ── Time ─────────────────────────────────────────────────────────────
        if _any_phrase(t, "what time", "current time", "what's the time", "tell me the time"):
            now = datetime.datetime.now().strftime("%I:%M %p")
            return True, f"The current time is {now}."

        # ── Date ─────────────────────────────────────────────────────────────
        if _any_phrase(t, "what date", "today's date", "what day", "what's today", "current date"):
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return True, f"Today is {today}."

        # ── Open Chrome ──────────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "chrome", "google chrome"):
            return self._open_app(
                windows=["chrome",
                         r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                         r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"],
                mac="open -a 'Google Chrome'", linux="google-chrome",
                success_msg="Opening Google Chrome for you.",
                fail_msg="I couldn't find Chrome. Is it installed?",
            )

        # ── Open Firefox ─────────────────────────────────────────────────────
        if _has(t, "open") and "firefox" in t:
            return self._open_app(
                windows=["firefox", r"C:\Program Files\Mozilla Firefox\firefox.exe"],
                mac="open -a Firefox", linux="firefox",
                success_msg="Opening Firefox.",
                fail_msg="I couldn't find Firefox.",
            )

        # ── Open Notepad ─────────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "notepad", "text editor", "note pad"):
            return self._open_app(
                windows=["notepad"],
                mac="open -a TextEdit", linux="gedit",
                success_msg="Opening Notepad.",
                fail_msg="Couldn't open Notepad.",
            )

        # ── Open VS Code ─────────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "vs code", "vscode", "visual studio code"):
            return self._open_app(
                windows=["code"],
                mac="open -a 'Visual Studio Code'", linux="code",
                success_msg="Opening VS Code.",
                fail_msg="VS Code doesn't seem to be installed.",
            )

        # ── Open Calculator ──────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "calculator", "calc"):
            return self._open_app(
                windows=["calc"],
                mac="open -a Calculator", linux="gnome-calculator",
                success_msg="Opening the calculator.",
                fail_msg="Couldn't open the calculator.",
            )

        # ── Open File Explorer ───────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "file explorer", "explorer", "my files", "my folder"):
            return self._open_app(
                windows=["explorer"],
                mac="open .", linux="nautilus",
                success_msg="Opening File Explorer.",
                fail_msg="Couldn't open File Explorer.",
            )

        # ── Open Task Manager ────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "task manager", "taskmanager"):
            return self._open_app(
                windows=["taskmgr"],
                mac="open -a 'Activity Monitor'", linux="gnome-system-monitor",
                success_msg="Opening Task Manager.",
                fail_msg="Couldn't open Task Manager.",
            )

        # ── Open Spotify ─────────────────────────────────────────────────────
        if _has(t, "open") and "spotify" in t:
            appdata = os.environ.get("APPDATA", "")
            return self._open_app(
                windows=["spotify", os.path.join(appdata, r"Spotify\Spotify.exe")],
                mac="open -a Spotify", linux="spotify",
                success_msg="Opening Spotify for you.",
                fail_msg="Couldn't find Spotify. Is it installed?",
            )

        # ── Open WhatsApp ─────────────────────────────────────────────────────
        if _has(t, "open") and "whatsapp" in t:
            launched = self._try_open_windows_app("whatsapp")
            if not launched:
                webbrowser.open("https://web.whatsapp.com")
                return True, "Opening WhatsApp Web in your browser."
            return True, "Opening WhatsApp."

        # ── Open Telegram ─────────────────────────────────────────────────────
        if _has(t, "open") and "telegram" in t:
            launched = self._try_open_windows_app("telegram")
            if not launched:
                webbrowser.open("https://web.telegram.org")
                return True, "Opening Telegram Web in your browser."
            return True, "Opening Telegram."

        # ── Open YouTube ─────────────────────────────────────────────────────
        if _has(t, "open") and "youtube" in t:
            webbrowser.open("https://youtube.com")
            return True, "Opening YouTube for you."

        # ── Open Google ──────────────────────────────────────────────────────
        if _has(t, "open") and "google" in t and "chrome" not in t:
            webbrowser.open("https://google.com")
            return True, "Opening Google."

        # ── Open Gmail ───────────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "gmail", "my email", "my mail"):
            webbrowser.open("https://mail.google.com")
            return True, "Opening Gmail."

        # ── Open GitHub ──────────────────────────────────────────────────────
        if _has(t, "open") and "github" in t:
            webbrowser.open("https://github.com")
            return True, "Opening GitHub."

        # ── Open Instagram ────────────────────────────────────────────────────
        if _has(t, "open") and "instagram" in t:
            webbrowser.open("https://instagram.com")
            return True, "Opening Instagram."

        # ── Open Twitter / X ──────────────────────────────────────────────────
        if _has(t, "open") and _any_phrase(t, "twitter", " x "):
            webbrowser.open("https://x.com")
            return True, "Opening X (Twitter)."

        # ── Web Search ───────────────────────────────────────────────────────
        if _any_phrase(t, "search for", "search google for", "look up", "google search", "search the web"):
            query = t
            for rm in ("search google for", "search the web for", "search for", "look up", "google search for"):
                query = query.replace(rm, "")
            query = query.strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
                return True, f"Searching Google for: {query}"

        # ── Play music ───────────────────────────────────────────────────────
        if _any_phrase(t, "play music", "play some music", "play a song"):
            webbrowser.open("https://music.youtube.com")
            return True, "Opening YouTube Music for you."

        # ── Screenshot ───────────────────────────────────────────────────────
        if _any_phrase(t, "take a screenshot", "take screenshot", "capture screen", "screenshot"):
            try:
                import pyautogui
                # Save to Documents (works even on OneDrive setups)
                save_dir = os.path.join(os.path.expanduser("~"), "Documents")
                os.makedirs(save_dir, exist_ok=True)
                path = os.path.join(save_dir, "nova_screenshot.png")
                pyautogui.screenshot(path)
                return True, f"Screenshot saved to your Documents folder."
            except ImportError:
                return True, "Install pyautogui to enable screenshots: pip install pyautogui"
            except Exception as e:
                return True, f"Screenshot failed: {e}"

        # ── System info ──────────────────────────────────────────────────────
        if _any_phrase(t, "system info", "system information", "my system", "what os am i"):
            info = (
                f"You're running {platform.system()} {platform.release()}, "
                f"on a {platform.machine()} machine."
            )
            return True, info

        # ── Clear memory ─────────────────────────────────────────────────────
        if _any_phrase(t, "clear memory", "reset memory", "forget everything", "clear chat", "start over"):
            self._reset_memory()
            return True, "Memory cleared. Fresh start! What would you like to talk about?"

        # ── Help ─────────────────────────────────────────────────────────────
        if t in ("help", "what can you do", "commands", "features", "your features"):
            return True, (
                "I can open apps like Chrome, Firefox, WhatsApp, Spotify, Notepad, VS Code, "
                "Calculator, and Task Manager. I can also open websites like YouTube, Gmail, "
                "GitHub, and Instagram, search Google, tell you the time and date, take "
                "screenshots, and have full AI conversations. Just say nova followed by your request!"
            )
        # ── Headlines ───────────────────────────────────────────────────────
        if _any_phrase(t, "today headlines", "today's headlines", "news headlines", "latest headlines"):
            headlines = TaskTools.get_headlines(limit=5)
            if not headlines:
                return True, "I couldn't fetch headlines right now. Please try again shortly."
            formatted = "Here are today's top headlines: " + " | ".join(headlines)
            return True, formatted

        # ── Create presentation ─────────────────────────────────────────────
        if _any_phrase(t, "make ppt", "create ppt", "create presentation", "make presentation"):
            topic = t
            for rm in ("make ppt on", "create ppt on", "create presentation on", "make presentation on", "make ppt", "create ppt", "create presentation", "make presentation"):
                topic = topic.replace(rm, "")
            topic = topic.strip() or "AI Strategy"
            path = TaskTools.create_ppt(topic)
            return True, f"Done. I created your presentation on {topic}. File saved at {path}"

        # ── Research helper ─────────────────────────────────────────────────
        if _any_phrase(t, "do research on", "research on", "research this"):
            topic = t.replace("do research on", "").replace("research on", "").replace("research this", "").strip()
            brief = TaskTools.quick_research_brief(topic)
            return True, brief

        # ── Send to AI ───────────────────────────────────────────────────────
        return False, None

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _open_app(self, windows: list, mac: str, linux: str,
                  success_msg: str, fail_msg: str) -> CommandResult:
        try:
            if self._os == "windows":
                for path in windows:
                    try:
                        subprocess.Popen(path, shell=True,
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
                        return True, success_msg
                    except Exception:
                        continue
                return True, fail_msg
            elif self._os == "darwin":
                subprocess.Popen(mac, shell=True)
                return True, success_msg
            else:
                subprocess.Popen(linux, shell=True)
                return True, success_msg
        except Exception as e:
            return True, f"{fail_msg} (Error: {e})"

    def _try_open_windows_app(self, app_name: str) -> bool:
        try:
            subprocess.Popen(f"start {app_name}", shell=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False