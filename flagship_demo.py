#!/usr/bin/env python3
import os, sys, time, platform, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GOLD  = "\033[38;5;220m"
CYAN  = "\033[96m"
GREEN = "\033[92m"
RED   = "\033[91m"
DIM   = "\033[2m"
BOLD  = "\033[1m"
RST   = "\033[0m"

ROOT = os.path.dirname(os.path.abspath(__file__))

print(GOLD + """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ███████╗██╗      █████╗  ██████╗ ███████╗██╗  ██╗██╗██████╗              ║
║    ██╔════╝██║     ██╔══██╗██╔════╝ ██╔════╝██║  ██║██║██╔══██╗             ║
║    █████╗  ██║     ███████║██║  ███╗███████╗███████║██║██████╔╝             ║
║    ██╔══╝  ██║     ██╔══██║██║   ██║╚════██║██╔══██║██║██╔═══╝              ║
║    ██║     ███████╗██║  ██║╚██████╔╝███████║██║  ██║██║██║                  ║
║    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝                  ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║       ADF RISING SUN           IRON-DOME           IDF MAGEN DAVID          ║
║       ─────────────            ─────────           ──────────────           ║
║            ╿                  /‾‾‾‾‾‾\\              ✦   ✦   ✦              ║
║       \\ \\  ╿  / /            /  ≋≋≋≋≋ \\           ✦    ✡    ✦             ║
║        \\   ╿   /            /  MISSILE  \\        ✦  22DIV  ✦              ║
║    ─────\\──☀──/─────       /  INTERCEPTED\\         ✦    ✡    ✦             ║
║        /   ╿   \\           ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾          ✦   ✦   ✦             ║
║       / /  ╿  \\ \\          DOME ACTIVE ✓                                   ║
║            ╿                                                                 ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OPERATOR: rainfantry  ✦  CALLSIGN: RADON  ✦  22DIV VADER UNIT             ║
║  CHEYANNE C2  ✦  IRON-SUN SHELL  ✦  VADER EVASION  ✦  IRON-DOME BUILDER   ║
║  OWN HARDWARE ONLY  ✦  AUTHORIZED RESEARCH  ✦  OPSEC ACTIVE                ║
╚══════════════════════════════════════════════════════════════════════════════╝
""" + RST)

print(CYAN + BOLD + """  ╔══════════════════════════════════════════╗
  ║          FLAGSHIP COMMAND MENU           ║
  ╠══════════════════════════════════════════╣
  ║  """ + GREEN + "B" + CYAN + """  — BUILD    iron-dome payload            ║
  ║  """ + GREEN + "T" + CYAN + """  — TEST     full suite (iron_sun_suite)  ║
  ║  """ + GREEN + "L" + CYAN + """  — LIVE     loopback shell test          ║
  ║  """ + GREEN + "C" + CYAN + """  — CHEYANNE launch C2 menu               ║
  ║  """ + GREEN + "D" + CYAN + """  — DESIGNATE generate callsign           ║
  ║  """ + GREEN + "W" + CYAN + """  — WATCH    screenshot monitor (3-shot)  ║
  ║  """ + GREEN + "S" + CYAN + """  — SITREP   repo status                  ║
  ║  """ + GREEN + "X" + CYAN + """  — EXIT                                  ║
  ╚══════════════════════════════════════════╝""" + RST)

print()
print(GOLD + "  ════ SITREP ════════════════════════════════════════" + RST)
print(f"  {CYAN}Machine:{RST}  {platform.node()} / {platform.system()} {platform.release()}")
print(f"  {CYAN}Python:{RST}   {sys.version.split()[0]}")
gcc = shutil.which("gcc")
print(f"  {CYAN}gcc:{RST}      {gcc or 'NOT FOUND'}")
print()

files = [
    ("iron_sun.c",          "shell source        "),
    ("iron_dome_builder.py","unified builder     "),
    ("iron_sun_suite.py",   "test suite          "),
    ("live_test.py",        "loopback test       "),
    ("vader_menu.py",       "cheyanne C2         "),
    ("designate.py",        "callsign generator  "),
]
for fname, desc in files:
    path = os.path.join(ROOT, fname)
    status = f"{GREEN}[PRESENT]{RST}" if os.path.exists(path) else f"{RED}[MISSING]{RST}"
    print(f"  {status}  {fname:<28} {DIM}{desc}{RST}")

print()
print(GREEN + "  EVASION SCOREBOARD:" + RST)
print(f"  {GREEN}v1{RST} XOR=0xFC  EVADED  PID 37008  18s  avpui+avp ACTIVE")
print(f"  {GREEN}v2{RST} XOR=0xAB  EVADED  PID 21972  18s  avpui+avp ACTIVE")
print(f"  {GREEN}v3{RST} XOR=0xDE  EVADED  PID 27576  18s  avpui+avp ACTIVE")
print()
print(f"  {GREEN}KILL CHAIN: 8/8 PASS{RST}  {DIM}(gwu07 / LAPTOP-R32M8MLI){RST}")
print()
print(GOLD + "  FLAGSHIP v1.0.0 — RADON — 2026-06-26" + RST)
print(DIM + "  Screenshot taken — standing by..." + RST)
print()
time.sleep(20)
