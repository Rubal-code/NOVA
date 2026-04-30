"""
NOVA AI - Display Utilities
Colorful, styled terminal output
"""

import sys
import time


# ── ANSI colour palette ──────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    CYAN    = "\033[96m"
    BLUE    = "\033[94m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"


def banner() -> None:
    print(f"""
{C.CYAN}{C.BOLD}
 ███╗   ██╗ ██████╗ ██╗   ██╗ █████╗
 ████╗  ██║██╔═══██╗██║   ██║██╔══██╗
 ██╔██╗ ██║██║   ██║██║   ██║███████║
 ██║╚██╗██║██║   ██║╚██╗ ██╔╝██╔══██║
 ██║ ╚████║╚██████╔╝ ╚████╔╝ ██║  ██║
 ╚═╝  ╚═══╝ ╚═════╝   ╚═══╝  ╚═╝  ╚═╝
{C.RESET}
{C.GREY} Neural Optimized Voice Assistant  v2.0{C.RESET}
{C.GREY} ─────────────────────────────────────{C.RESET}
""")


def info(msg: str) -> None:
    print(f"{C.GREY}[{C.CYAN}NOVA{C.GREY}]{C.RESET} {msg}")


def nova_says(msg: str) -> None:
    print(f"\n{C.CYAN}{C.BOLD}🤖 NOVA:{C.RESET} {C.WHITE}{msg}{C.RESET}\n")


def user_says(msg: str) -> None:
    print(f"{C.GREEN}{C.BOLD}🎤 You:{C.RESET}  {C.WHITE}{msg}{C.RESET}")


def warn(msg: str) -> None:
    print(f"{C.YELLOW}⚠  {msg}{C.RESET}")


def error(msg: str) -> None:
    print(f"{C.RED}✖  {msg}{C.RESET}")


def success(msg: str) -> None:
    print(f"{C.GREEN}✔  {msg}{C.RESET}")


def thinking() -> None:
    print(f"{C.GREY}   Thinking...{C.RESET}", end="", flush=True)


def clear_thinking() -> None:
    # Overwrite the "Thinking..." line
    print(f"\r{' ' * 20}\r", end="", flush=True)


def listening_indicator() -> None:
    print(f"\n{C.MAGENTA}🎙  Listening...{C.RESET}")


def divider() -> None:
    print(f"{C.GREY}{'─' * 45}{C.RESET}")
