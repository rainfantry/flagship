# HANDOFF INTEL — Key Corrections & New Context
## 2026-06-26 21:00 AEST | RADON | Source: cve-submissions/HANDOFF.md (2026-06-25)

---

## PROBABILITY CORRECTIONS (CONQUEST_SYNTHESIS had stale numbers)

| GSWA | Finding | Old Estimate | CORRECTED | Source |
|------|---------|-------------|-----------|--------|
| 001 | Wondershare NativePushService CWE-732 | 65-75% | **85-90%** | HANDOFF.md post-canary |
| 002 | MuseHub CWE-426 | 70-80% | **40-50%** | 22 canaries planted, ZERO fired as SYSTEM |
| 003 | Razer CVE-2025-27811 unpatched | - | **35-50%** | razer_elevation_service.exe v1.1.0.5 still shipping |
| HWBP | Defender HWBP (VULN-195458) | 20-35% | **REJECTED** | Wrong boundary — closed |

### Why MuseHub dropped from 70-80% to 40-50%

22 phantom DLL canaries deployed to `Muse Hub\lib` and `.local\bin` paths. ZERO fired as SYSTEM.
Canary list (all silent): osppc, osppcext, CCGLaunchPad + 11 others.

Root cause: SprintCSP.dll is patched on Win11 26200 — the primary SYSTEM DLL load trigger is dead.
**Three alternative triggers have NOT been tried on gwu07 yet:**
```powershell
# These may still fire a SYSTEM load via PATH:
Start-ScheduledTask "\Microsoft\Windows\DiskCleanup\SilentCleanup"
Start-ScheduledTask "\Microsoft\Windows\Application Experience\ProgramDataUpdater"
Start-ScheduledTask "\Microsoft\Windows\Diagnosis\Scheduled"
```
If any of these fires a SYSTEM-context canary → probability jumps back to 70-80%.

---

## uv (Astral) CWE-426 — COMPARISON INTEL

- **RADON**: uv writes to HKCU PATH (`C:\Users\Ghaleb Jomma\.local\bin`) — CORRECT behavior
- **gwu07**: uv writes to HKLM PATH (`C:\Users\gwu07\.local\bin`) — ANOMALOUS

This comparison is evidentially valuable:
- RADON proves the correct behavior EXISTS (HKCU is possible)
- gwu07 confirms the HKLM write is a defect (not intended by design)
- Likely cause: admin-context uv install on gwu07 wrote to HKLM instead of user-scoped HKCU
- This evidence belongs in `03_UV_ASTRAL_NEW.md` → strengthens the submission

---

## RAZER #04 — CVE-2025-27811 UNPATCHED (NEW, NOT IN CONQUEST_SYNTHESIS)

- Razer Synapse 4.0.503.7 ships `razer_elevation_service.exe v1.1.0.5`
- CVE-2025-27811: LPE via COM IPC in razer_elevation_service.exe v1.1.0.5 (Feb 2025)
- Patched in: v1.1.0.6 — but Razer's own distribution still ships v1.1.0.5 as of June 2026
- Strategy: "vendor notification + MITRE new CVE as unpatched prior disclosure"
- Same approach as Wondershare (#53 analogous to CVE-2024-26574 check)
- **Probability: 35-50%**
- Report already written: `FINAL_SUBMISSIONS/04_RAZER_UNPATCHED.md`
- Action: Notify security@razer.com. Wait 5 days. MITRE if no response.

---

## CRITICAL TECHNICAL GOTCHA — UAC SPLIT TOKEN ON gwu07

**gwu07 is in Administrators group with deny-only SID (standard UAC split token).**

Impact on service_fuzzer.ps1 results:
- `os.access(os.W_OK)` or `[System.IO.File]::WriteAllText()` tests may return TRUE for System32 files
- This generates false positives in automated scans
- **Always verify with `icacls` before treating a finding as real**
- The service_fuzzer.ps1 likely already uses icacls (needs confirmation)
- Applies to: ALL 62 services enumerated, ALL 44 findings — some may be false positives

**Confirmed by HANDOFF:** This was the root cause of false positives in Session 1 scanning.

---

## DEAD VECTORS — CONFIRMED (gwu07 deep scan complete)

From full scan of 50+ SYSTEM services on gwu07:

| Vector | Status |
|--------|--------|
| IKEEXT azureike.dll | HARDENED — LOAD_LIBRARY_SEARCH_SYSTEM32 flag 0x800 at offset 0x9A619 |
| WPN phantom DLLs (wpncore, wpnapps etc.) | CLEAN — all 6 scanned, no phantoms |
| CrossDevice COM CLSID E9F83CF2... | PATCHED (CVE-2025-24076). User-context only. |
| Steam Client Service | CLEAN — binary in TrustedInstaller-owned path |
| osppc/osppcext/CCG canaries | DORMANT — 22 deployed, zero SYSTEM fires |
| ALL Nightmare Eclipse exploits | PATCHED |
| RoguePlanet | PATCHED |
| COM HKCU hijack for SYSTEM LPE | ARCHITECTURE BLOCK — SYSTEM uses .DEFAULT not user HKCU |
| HKLM Run/RunOnce → user paths | 0 findings |
| COM LocalServer32/InprocServer32 → user paths | 0 findings |
| WMI providers, SSPs, auth packages | 0 findings |
| Scheduled tasks (144 elevated) | 0 findings |

**Do not reinvestigate any of these.**

---

## ACTIVE CANARIES ON gwu07 (deployed, monitoring)

| Path | Canary | Status |
|------|--------|--------|
| `C:\Users\gwu07\.local\bin\` | 14 phantom DLLs | DORMANT |
| `C:\Users\gwu07\AppData\Local\Muse Hub\lib\` | DLL set | DORMANT |
| `C:\Windows\Temp\ws_diag.log` | Wondershare binary canary | **SYSTEM HIT CONFIRMED** |
| `C:\Windows\Temp\vader_canary.log` | canary_dropper.ps1 target | New — per Loop 5 |
| `C:\Windows\Temp\vader_path_hijack.log` | PATH hijack canary | User-context only so far |

---

## OPEN ATTACK VECTORS (not yet explored, from HANDOFF)

These were listed as remaining attack surfaces as of 2026-06-25:

1. **ProcMon trace on ClickToRunSvc** — would prove/disprove osppc.dll loading. Needs admin ProcMon. This is Finding #47's gate.
2. **Windows Installer repair custom actions** — MSI packages with SYSTEM custom actions loading from writable paths. Not yet scanned.
3. **Application shimming (SDB)** — custom compatibility databases injecting DLLs. Not scanned.
4. **DLL sideloading in auto-elevated processes** — signed Microsoft EXEs that auto-elevate, load from CWD. Not scanned.
5. **Junction/symlink TOCTOU** — redirect SYSTEM file writes via directory junctions (post-Wondershare, this is the next write-anywhere vector).

---

## SUBMISSION QUEUE (priority order from HANDOFF)

1. **security@wondershare.com** → attach GSWA-001 report + SYSTEM canary evidence. **DO THIS FIRST.**
2. **security@musescore.com** (MuseHub) → after SilentCleanup/ProgramDataUpdater canary tried.
3. **security@razer.com** → Razer GSWA-003 / CVE-2025-27811 unpatched.
4. **github.com/astral-sh/uv/security** → uv CWE-426 with RADON vs gwu07 HKCU/HKLM comparison.
5. **MSRC** → YellowKey (GSWA-012), cldflt regression (GSWA-009) when evidence packages complete.

All: wait 5 business days → MITRE `cveform.mitre.org` regardless of vendor response.

---

*RADON · 22DIV VADER · 2026-06-26*
