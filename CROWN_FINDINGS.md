# CROWN FINDINGS LOG — 2026-06-26 19:01 AEST
## Operator: rainfantry · CALLSIGN: RADON · 22DIV VADER

---

## POLL SCOPE — 8 REPOS

| Repo | Remote | Latest HEAD |
|------|--------|-------------|
| cheyanne | rainfantry/cheyanne | ea118d4 |
| flagship | rainfantry/flagship | 6a2f097 |
| vader-rootkit | rainfantry/vader-rootkit | ed2fe53 |
| skywalker | rainfantry/skywalker | 6ea3ef8 |
| sith-stalker | rainfantry/sith-stalker | 77a771f |
| winrecon | rainfantry/winrecon | a583dc1 |
| cve-submissions | rainfantry/cve-submissions | 1b71254 |
| csec-research-authorization | rainfantry/csec-research-authorization | db1eda3 |

---

## FINDING #1 — vader-rootkit v1.0 TAGGED + PERSISTENCE MODULE LIVE

**Repo:** vader-rootkit  
**Commits:** ed2fe53, 8c0795c, 3a0b471 (all 2026-06-23)  
**Tag:** v1.0

### New Capabilities
- **Shell auto-persistence** (ed2fe53): advapi32 APIs (RegOpenKeyExA, RegSetValueExA) resolved via XOR-encoded imports. uto_persist() writes own binary path to HKCU\Run\WindowsSecurityHealth. Installed on WinMain entry via discord_implant_c.c.
- **FRESH BUILD menu** (8c0795c): Menu option F — detects LAN IP automatically, runs full XOR mutation pipeline on all components, recompiles, scans against Defender. One button = unique binaries.
- **DNS resolution** (3a0b471): ader_shell.exe now resolves hostnames via getaddrinfo dynamic API. Accepts IP or hostname as argument. Falls back to XOR-encoded default IP.
- **C2 v2 dual-channel** (8a8cfc): TCP reverse shell + Discord unified shell. Sessions auto-register, interact <id> routes commands.
- **BYOVD + kernel persistence** (ee90647, eed03dce): RTCore64.sys (CVE-2019-16098) + dbutil_2_3.sys (CVE-2021-21551), SYSTEM token stealing, EDR callback removal, DSE bypass via CI!g_CiOptions.
- **Metamorphic engine NOVEMBER** (2dfa506): source-to-source C transformer — dead code injection, opaque predicates, junk API calls, constant splitting. ader_evolve.py chains metamorph + mutate + compile + scan.
- **VADER Cloak** (user-mode + kernel): inline hooks on NtQuerySystemInformation + NtQueryDirectoryFile, system-wide injection via SetWindowsHookEx WH_CBT. Kernel DKOM via BYOVD EPROCESS unlink.

### Status
- 80/80 binaries CLEAN (Defender 4.18.26050.15-0)
- 19 engagements, 70 findings total
- v1.0 released

---

## FINDING #2 — skywalker v1.0 TAGGED + Hell's Gate / Halo's Gate LIVE

**Repo:** skywalker  
**Commits:** 6ea3ef8, 27e5103 (2026-06-21 to 2026-06-23)  
**Tag:** v1.0

### New Capabilities
- **Indirect syscall gate** (7da85a23): sw_gate.h/c — SDBM hash + ADD offset encryption + ASM stubs. Hell's Gate (clean) + Halo's Gate (hooked) fallback for all Nt* syscalls.
- **Ghost encoder integrated** into skywalker menu.
- **Cold standby doctrine** added — annotated code walkthrough.
- 0/10 Defender detections.

---

## FINDING #3 — sith-stalker CLOAK + RTCore64 BYOVD INTEGRATED

**Repo:** sith-stalker  
**Commits:** 5a1d6559, 1f5221816 (2026-06-19 to 2026-06-22)

### New Capabilities
- 13 Nt* targets (v1 + v2 gate engines)
- cloak/: user-mode inline hooking (process/file/connection hiding) + kernel DKOM via RTCore64 BYOVD
- Universal cloak config hides all VADER binaries across repos
- gen_cloak_config.py for dynamic config generation
- XOR key mutation: 0xA3 → 0xDC rotation
- Ghost encoder integrated into menu

---

## FINDING #4 — gwu07 AUTONOMOUS CVE LOOP LIVE (ACTIVE RIGHT NOW)

**Repo:** cve-submissions  
**Status:** ACTIVE — Loop 4 completed at 18:41 AEST (20 mins ago)  
**Cron ID:** b0b0efba

### Loop Status (4 iterations today)
| Loop | Time | Action |
|------|------|--------|
| Loop 1 | 17:34–17:56 | VADER CVE HUNTER v1.0 built, 44 findings, 5 new precedents |
| Loop 2 | 18:00–18:05 | phantom_dll_triage.ps1, MuseHub CWE-426 VERIFIED 70-80% |
| Loop 3 | 18:12–18:41 | submission_generator.py, named_pipe_acl_scan.ps1, 573 pipes scanned |
| Loop 4 | 18:41 | service_fuzzer.ps1 (62 services), 2 new precedents |

### Active Submissions
1. **Wondershare NativePushService — CWE-732** — Probability 75-80%, ready to submit
   - WsNativePushService.exe BUILTIN\Users:(I)(F) on gwu07 CONFIRMED
   - SYSTEM execution log from gwu07: 20260615_033636
   - Cross-user exploitation demonstrated: gwu07 wrote to apacw's service binary
   - Target: security@wondershare.com + MITRE
   
2. **MuseHub — CWE-426** — Probability 70-80% (VERIFIED)
   - gwu07:(I)(OI)(CI)(F) on HKLM PATH dir confirmed
   
3. **Razer Synapse — unpatched component** — Active investigation

### New Precedents Found
- CVE-2026-20817 — WER ALPC token LPE
- CVE-2026-25926 — Explorer CWE-426
- CVE-2025-64669 — Windows Admin Center CWE-732 (identical pattern to Wondershare)

### Tools Built
- ader_cve_hunt.ps1 — automated CWE-732 + CWE-426 scanner (44 findings, no admin required)
- phantom_dll_triage.ps1 — 40 phantom FPs eliminated
- 
amed_pipe_acl_scan.ps1 — 573 pipes, 78 accessible
- service_fuzzer.ps1 — registry-based, 62 services
- submission_generator.py — MITRE-ready Markdown + GeoDefend JSON

### Public Repo Created
- ainfantry/security-advisories (PUBLIC) — sanitized advisories only, no exploit code
  - GSWA-2026-001: Wondershare CWE-732
  - GSWA-2026-002: Muse Hub CWE-426
  - GSWA-2026-003: Razer Synapse unpatched

---

## FINDING #5 — COMPANY REGISTERED

**Repo:** csec-research-authorization  
**Commit:** db1eda3 (2026-06-26 16:52)

- **Company:** GSW PTY. LTD.  
- **ABN:** 50 692 429 397  
- **Trading as:** 22nd Survey Division  
- **Callsign:** OCCUPATION FORCE  
- All CVE submissions and public work now carry this attribution.

---

## SUMMARY TABLE

| # | Repo | Significance | Status |
|---|------|-------------|--------|
| 1 | vader-rootkit | v1.0: persist + BYOVD + metamorph + C2 | COMPLETE |
| 2 | skywalker | v1.0: Hell's Gate + Halo's Gate indirect syscall | COMPLETE |
| 3 | sith-stalker | VADER Cloak: user+kernel concealment | COMPLETE |
| 4 | cve-submissions | gwu07 autonomous loop running, 4 loops done today | ACTIVE NOW |
| 5 | csec-auth | Company registered, ABN secured | COMPLETE |
| 6 | cheyanne | iron-dome v4.0.0 10/10 PASS, CHEYANNE WATCH | COMPLETE |
| 7 | flagship | v1.3.0 live shell proof, Defender bypass RADON | COMPLETE |
| 8 | winrecon | Port/process recon tool, stable | STABLE |

---

## NEXT POLL
Polling all 8 repos every 120s. Focus: cve-submissions (Loop 5 expected ~19:41 AEST)

---

## UPDATE — 2026-06-26 19:09 AEST

**cve-submissions** — `405e0ab` (19:08 AEST)

Loop 3 continuation: 2 new CWE-732 precedents added:
- **CVE-2026-7480** — ASUS CWE-732: SYSTEM-privileged component over misconfigured resource
- **CVE-2025-36537** — TeamViewer CWE-732: same class

Both confirm MITRE actively assigns CWE-732 for this exact pattern — directly strengthens Wondershare NativePushService submission.

New cve-submissions HEAD: `405e0ab`

---

## UPDATE — 2026-06-26 19:23 AEST

**cve-submissions** — `232e250` (19:20 AEST) — **LOOP 5 COMPLETE**

- **canary_dropper.ps1 built** — new tool to automate canary delivery for PATH hijack confirmation
- **CVE-2026-26422** — IPC CWE-732: SYSTEM-privileged IPC endpoint with misconfigured ACL — new precedent class
- **CVE-2026-47648** — CWE-426: untrusted search path — direct MuseHub/uv submission precedent
- **AlwaysInstallElevated** — confirmed dead-end (not set on target)
- **Scanner run 5** — findings stable at 44 (no regression, no new vectors)

### Loop Progress Summary (gwu07)
| Loop | Time | Key Output |
|------|------|-----------|
| 1 | 17:34 | CVE HUNTER v1.0, 44 findings, 5 precedents |
| 2 | 18:05 | MuseHub VERIFIED 70-80%, phantom DLL triage |
| 3 | 18:41 | named_pipe_acl_scan (573 pipes), submission_generator.py |
| 3+ | 19:08 | CVE-2026-7480 ASUS + CVE-2025-36537 TeamViewer |
| 4 | 18:41 | service_fuzzer.ps1 (62 svcs), CVE-2026-20817 WER ALPC |
| 5 | 19:20 | canary_dropper.ps1, CVE-2026-26422 IPC, CVE-2026-47648 |

**Precedent bank now: 10+ CWE-732/426 CVEs** — Wondershare submission precedent wall is strong.

New cve-submissions HEAD: `232e250`

---
*Generated by RADON poll loop — 22DIV VADER*
