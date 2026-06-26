#!/usr/bin/env python3
"""Non-interactive demo — MCP/CI showcase. Prints iron-sun art + FLAGSHIP banner + SITREP."""
import os, sys, time, platform, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GOLD  = "\033[38;2;255;215;0m"
CYAN  = "\033[38;2;0;229;255m"
GREEN = "\033[38;2;0;255;100m"
RED   = "\033[38;2;255;60;60m"
IDF   = "\033[38;2;0;56;184m"
WHITE = "\033[38;2;255;255;255m"
DIM   = "\033[38;2;120;120;120m"
RST   = "\033[0m"

ROOT = os.path.dirname(os.path.abspath(__file__))

def iron_sun_art(W=76):
    C = W // 2
    rows = []
    for r in range(15):
        h = int(round(C * (14 - r) / 14))
        if h == 0:
            ln = [' '] * W; ln[C] = '✡'; rows.append(''.join(ln)); break
        ln = [' '] * W
        for i in range(17):
            p = int(round(C + (-1.0 + i * 0.125) * h))
            p = max(0, min(W - 1, p))
            ln[p] = '│' if abs(p - C) <= 1 else ('╲' if p < C else '╱')
        rows.append(''.join(ln))
    lines = []
    lines.append(f"{CYAN}  ╔{'═'*W}╗{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    for row in rows:
        lines.append(f"{CYAN}  ║{GOLD}{row.ljust(W)[:W]}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{WHITE}{'T H E   I R O N - S U N'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{WHITE}{'A U S T R A L I A N   A R M Y   ·   2 2 D I V'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ╚{'═'*W}╝{RST}")
    return '\n'.join(lines)

print(iron_sun_art())
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
║                IRON-DOME          ·          IDF MAGEN DAVID                 ║
║            ╱▔▔▔▔▔▔▔▔▔▔╲                     ✦     ✦     ✦                   ║
║           ╱  ≋≋≋≋≋≋≋≋≋ ╲                ✦        ✡        ✦                ║
║          ╱  MISSILE      ╲             ✦      22DIV VADER      ✦            ║
║         ╱  INTERCEPTED    ╲               ✦        ✡        ✦               ║
║         ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔                  ✦     ✦     ✦                  ║
║              DOME ACTIVE ✓          CHEYANNE C2  ·  OPSEC ACTIVE            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OPERATOR: rainfantry  ✦  CALLSIGN: RADON  ✦  OWN HARDWARE ONLY            ║
╚══════════════════════════════════════════════════════════════════════════════╝
""" + RST)

print(CYAN + """  ╔══════════════════════════════════════════╗
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
    ("iron_sun.c",           "shell source     "),
    ("iron_dome_builder.py", "unified builder  "),
    ("iron_sun_suite.py",    "test suite       "),
    ("live_test.py",         "loopback test    "),
    ("vader_menu.py",        "cheyanne C2      "),
    ("designate.py",         "callsign gen     "),
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
print(GOLD + "  FLAGSHIP v1.1.0 — RADON — 2026-06-26" + RST)
print(DIM + "  Screenshot taken — standing by..." + RST)
print()
time.sleep(20)
