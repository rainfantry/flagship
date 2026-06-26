#!/usr/bin/env python3
"""WATCH-3 showcase — prints full banner stack then fires 3 mss shots."""
import os, sys, time, datetime, platform, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

GOLD = "\033[38;2;255;215;0m"
CYAN = "\033[38;2;0;229;255m"
GREEN= "\033[38;2;0;255;100m"
RED  = "\033[38;2;255;60;60m"
IDF  = "\033[38;2;0;56;184m"
WH   = "\033[38;2;255;255;255m"
DIM  = "\033[38;2;120;120;120m"
RST  = "\033[0m"

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, "screenshots")
os.makedirs(SHOTS, exist_ok=True)

# ── IRON-SUN dynamic ray art ─────────────────────────────────────────────────
def iron_sun_art(W=76):
    C = W // 2
    rows = []
    for r in range(15):
        h = int(round(C * (14 - r) / 14))
        if h == 0:
            ln = [' ']*W; ln[C] = '✡'; rows.append(''.join(ln)); break
        ln = [' ']*W
        for i in range(17):
            p = int(round(C + (-1.0 + i*0.125)*h))
            p = max(0, min(W-1, p))
            ln[p] = '│' if abs(p-C)<=1 else ('╲' if p<C else '╱')
        rows.append(''.join(ln))
    lines = []
    lines.append(f"{CYAN}  ╔{'═'*W}╗{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    for row in rows:
        lines.append(f"{CYAN}  ║{GOLD}{row.ljust(W)[:W]}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{WH}{'T H E   I R O N - S U N'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{WH}{'A U S T R A L I A N   A R M Y   ·   2 2 D I V'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ╚{'═'*W}╝{RST}")
    return '\n'.join(lines)

# ── IDF CYBER SQUAD ray art (builder v4.0.0 style) ───────────────────────────
def cyber_squad_art(W=76):
    C = W // 2
    rows = []
    for r in range(15):
        h = int(round(C * (14 - r) / 14))
        if h == 0:
            ln = [' ']*W; ln[C] = '✡'; rows.append(''.join(ln)); break
        ln = [' ']*W
        for i in range(17):
            p = int(round(C + (-1.0 + i*0.125)*h))
            p = max(0, min(W-1, p))
            ln[p] = '│' if abs(p-C)<=1 else ('╲' if p<C else '╱')
        rows.append(''.join(ln))
    lines = []
    lines.append(f"{CYAN}  ╔{'═'*W}╗{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    for row in rows:
        lines.append(f"{CYAN}  ║{GOLD}{row.ljust(W)[:W]}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{WH}{'I R O N - D O M E   ·   F U L L   P L A T F O R M'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{DIM}{'iron-sun  ·  GHOST ENCODER  ·  VADER  ·  CHEYANNE WATCH'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{GOLD}{'✡  IDF CYBER SQUAD  ✡  22DIV  ✡  VADER  ✡  ORACLE  ✡'.center(W)}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ║{IDF}{'▓'*W}{CYAN}║{RST}")
    lines.append(f"{CYAN}  ╚{'═'*W}╝{RST}")
    return '\n'.join(lines)

# ── Print all banners ─────────────────────────────────────────────────────────
print(iron_sun_art())
print()
print(cyber_squad_art())
print()
print(GOLD + """╔══════════════════════════════════════════════════════════════════════════════╗
║    ███████╗██╗      █████╗  ██████╗ ███████╗██╗  ██╗██╗██████╗              ║
║    ██╔════╝██║     ██╔══██╗██╔════╝ ██╔════╝██║  ██║██║██╔══██╗             ║
║    █████╗  ██║     ███████║██║  ███╗███████╗███████║██║██████╔╝             ║
║    ██╔══╝  ██║     ██╔══██║██║   ██║╚════██║██╔══██║██║██╔═══╝              ║
║    ██║     ███████╗██║  ██║╚██████╔╝███████║██║  ██║██║██║                  ║
║    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OPERATOR: rainfantry  ✦  CALLSIGN: RADON  ✦  22DIV VADER UNIT              ║
║  OWN HARDWARE ONLY  ✦  AUTHORIZED RESEARCH  ✦  OPSEC ACTIVE                 ║
╚══════════════════════════════════════════════════════════════════════════════╝""" + RST)

print()
print(CYAN + f"  Machine:  {platform.node()} / {platform.system()} {platform.release()}" + RST)
print(CYAN + f"  Python:   {sys.version.split()[0]}  ·  gcc: {shutil.which('gcc') or 'NOT FOUND'}" + RST)
print()

# ── WATCH-3 ───────────────────────────────────────────────────────────────────
try:
    import mss, mss.tools
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "mss", "-q"])
    import mss, mss.tools

print(GOLD + "  ╔══════════════════════════════════════════════════╗" + RST)
print(GOLD + "  ║      W A T C H — 3 - S H O T   M O N I T O R   ║" + RST)
print(GOLD + "  ╚══════════════════════════════════════════════════╝" + RST)
print()

saved = []
with mss.MSS() as sct:
    for i in range(1, 4):
        ts = datetime.datetime.now().strftime('%H%M%S')
        fname = f"watch3_{i}_{ts}.png"
        fpath = os.path.join(SHOTS, fname)
        sct.shot(output=fpath)
        saved.append(fname)
        size = os.path.getsize(fpath)
        print(f"  {GREEN}[{i}/3]{RST}  {fname}  {DIM}({size:,} bytes){RST}")
        if i < 3:
            print(f"  {DIM}  ...5s...{RST}")
            time.sleep(5)

print()
print(GREEN + "  [+] WATCH-3 COMPLETE — 3 screenshots saved to screenshots/" + RST)
print()
for f in saved:
    print(f"  {DIM}  {f}{RST}")
print()
print(GOLD + f"  FLAGSHIP v1.2.0 — RADON — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + RST)
print()
print(DIM + "  Standing by 20s for MCP capture..." + RST)
time.sleep(20)
