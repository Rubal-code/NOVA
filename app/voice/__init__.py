# app/voice/__init__.py
try:
    from .listener import listen, listen_for_wake_word
    from .speaker import speak
except ImportError as e:
    print(f"[NOVA] Voice module warning: {e}")