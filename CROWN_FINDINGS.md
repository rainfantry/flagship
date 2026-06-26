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

## UPDATE — 2026-06-26 19:28 AEST

**csec-research-authorization** — `c4b47c1` (19:24 AEST) — **22DIV DOCTRINE FORMALIZED**

George updated both `README.md` and `CURRENT_STATUS.md`. Key additions:

### 22nd Survey Division — Education Platform (now documented in auth repo)

- **Platform LIVE**: rainfantry.github.io/22nd-survey-division — 22-chapter course
- **Teaching doctrine** (4-step flow now canonical):
  1. The Defense — how the detection mechanism works architecturally
  2. The Trust Boundary — where the mechanism stops looking and why
  3. The Bypass — what falls through the gap once the boundary is understood
  4. Counter-Detection — what a defender must add to close the gap
- **Mentor**: "0x1security" (~15 CVEs, Unit 8200 framework) — OPSEC maintained, no real name
- **GeoDefend** — public blue team dashboard (geo threat intel, live IP reputation) — same operator, defensive side

### AI authorization context (rewritten — professional framing)

Auth repo now carries verifiable authorization proof:
- **MSRC VULN-195458** — submitted 2026-06-16, rejected, embargo void, materials published. Proof of responsible disclosure.
- **GeoDefend** — public defensive tool. Same knowledge base, defensive application.
- **ABN 50 692 429 397 / ACN 692 429 397** — registered Australian company, ABR verifiable.
- **Authorization boundary**: own hardware, own household systems (with consent), authorized networks only.

### Strategic implication

The csec-auth repo is now a credentialing document. It establishes:
- Research is authorized, hardware is owned, company is registered
- Methodology is defense-first (teach the architecture, bypass is a side effect)
- Responsible disclosure practice is proven (MSRC case on record)
- The same operator builds offensive research AND defensive tools (GeoDefend)

This is the framing for CSEC entry, MSRC submissions, and any external audit.

New csec-auth HEAD: `c4b47c1`

**cve-submissions** — still at `232e250` (Loop 6 not yet fired — expected ~19:50)
**flagship** — `95a1305` (PROBING_UNAPPROACHABLE pushed this session)

---

## UPDATE — 2026-06-26 20:47 AEST

**cve-submissions** — `6c15acf` (20:44) + `d9632b8` (20:46) — **LOOPS 8 + 9**

### Loop 8 — Four new GSWA research tracks + evasion layer doctrine

**GSWA-2026-009 — cldflt!HsmOsBlockPlaceholderAccess CWE-367 (REGRESSION)**
- Google Project Zero original finding — STILL PRESENT on Windows 11 Build 26200
- CfAbortOperation + anonymous token flip race → write to `\Registry\User\.DEFAULT\CloudFiles\BlockedApps`
- Full chain: registry symlink → Volatile Environment → service path poisoning → SYSTEM shell
- Source: MiniPlasma `PoC_AbortHydration_ArbitraryRegKey_EoP` — ORIGINAL POC WORKS
- Defender has sigs for this path specifically (`Poc_AbortHydration_ArbitraryReplay_EoP` detected 4x in logs)
- **Action**: File as regression/new exposure to MSRC. Known vector but unpatched = re-disclosure.

**GSWA-2026-010 — Defender Cloud Tag File Rewrite CWE-693**
- MsMpEng (SYSTEM) writes to cloud-tag metadata path during file restoration branch
- Source: RedSun.cpp — cfapi.h + NTFS reparse structures
- **Status**: Partial analysis. Do NOT submit yet — full chain incomplete.

**GSWA-2026-011 — CTFMON Object Namespace Section Squatting CWE-732**
- Standard user creates named section objects in Object Namespace dirs trusted by SYSTEM
- Text Services Framework (ctfmon.exe) IPC path affected
- Source: GreenPlasma — Windows 11/Server 2022/2026 confirmed
- **Status**: Primitive confirmed. Full exploitation chain withheld. Structural finding only.

**GSWA-2026-012 — WinRE BitLocker Bypass FsTx CWE-287 (CRITICAL — YellowKey)**
- WinRE component processes FsTx transaction logs from USB/EFI — bypasses BitLocker authentication
- 6-file folder structure + CTRL modifier during WinRE boot = shell with full volume access
- Affected: Windows 11 / Server 2022 / Server 2025 ONLY — NOT Windows 10
- Source: YellowKey — `USB:\System Volume Information\FsTx\` folder
- **Status**: CONFIRMED on lab VM. MSRC submission PENDING. DO NOT publish exploit details.
- **This is the highest-value finding yet — kernel auth bypass in WinRE boot path.**

**Evasion layer doctrine (defender-evasion-layers.md) — Finding #36 CLOSED:**
- Full 6-layer stack confirmed: WdFilter → ETW behavioral → AMSI → Tamper Protection → ETW-Ti → Cloud ML
- **EtwTiLogSetContextThread FIRES on SetThreadContext BUT DEFENDER IGNORES IT**
- Finding #36 open question ANSWERED: consumer gap confirmed (signal generated, not actioned)
- Dark Room confirmed all-BLIND in screenshots 4-6. Memory patch (`Bearfoos.A!ml`) DETECTED.

### Loop 9 — Two new precedents

**CVE-2026-26422 — Clash Verge Rev, IPC CWE-732** (NEW CLASS)
- clash-verge-service IPC endpoint world-reachable → standard user sends crafted messages → LPE
- PATCHED in v2.3.0
- **Direct validation**: Same surface as AsusCert named pipe (confirmed connectable by standard user in loop 3 pipe scan)
- AsusCert pipe + this CVE precedent = submission-ready if protocol reversible

**CVE-2026-47648 — Windows Storage CWE-426** (NEW CLASS)
- Windows Storage component itself has untrusted search path
- **First-party Microsoft CWE-426** — upgrades osppc.dll phantom DLL to stronger precedent class

### Loop summary table (updated)

| Loop | Time | Key Output |
|------|------|-----------|
| 1 | 17:34 | CVE HUNTER v1.0, 44 findings, 5 precedents |
| 2 | 18:05 | MuseHub VERIFIED 70-80%, phantom DLL triage |
| 3 | 18:41 | named_pipe_acl_scan (573 pipes), submission_generator.py |
| 3+ | 19:08 | CVE-2026-7480 ASUS + CVE-2025-36537 TeamViewer |
| 4 | 18:41 | service_fuzzer.ps1 (62 svcs), CVE-2026-20817 WER ALPC |
| 5 | 19:20 | canary_dropper.ps1, CVE-2026-26422 IPC, CVE-2026-47648 |
| 8 | 20:44 | GSWA-009/010/011/012 — YellowKey BitLocker bypass, evasion doctrine |
| 9 | 20:46 | Clash Verge IPC + Windows Storage CWE-426 precedents |

**Active GSWA tracks**: 12 (009-012 new). **Precedent bank**: 12+ CVEs.
**Finding #36 EtwTi gap**: CLOSED — consumer gap confirmed.
**YellowKey**: CRITICAL — BitLocker bypass pending MSRC.

New cve-submissions HEAD: `d9632b8`

---
*Generated by RADON poll loop — 22DIV VADER*
