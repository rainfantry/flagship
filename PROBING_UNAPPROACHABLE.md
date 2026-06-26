# PROBING UNAPPROACHABLE PROGRAMS
## VADER Research | 22nd Survey Division | 2026-06-26
## Classes: Kernel drivers · PPL processes · SYSTEM services · AV internals

---

## THE PROBLEM

Some programs actively resist investigation:

| Class | Why They're Hard | Standard Tools Fail Because |
|-------|-----------------|---------------------------|
| Kernel drivers (.sys) | Ring 0 — no user-mode debugger attach | x64dbg/WinDbg user-mode can't reach |
| PPL processes (MsMpEng.exe) | Protected Process Light — OpenProcess denied | Even SYSTEM can't get a handle |
| SYSTEM services | Elevated privilege, no console | `taskkill /f` denied from standard user |
| AV/EDR binaries | Self-protection hooks, anti-debug | Frida/x64dbg injection blocked by own hooks |
| mpengine.dll | No exports, 100MB packed ML engine | No IAT, no symbols, obfuscated internally |

The VADER program has encountered every class. This doc maps the toolchain to crack each one.

---

## CLASS 1 — KERNEL DRIVERS

### Targets in VADER scope
- `bindflt.sys` — primary CVE target (ZERO CVEs, AppXSvc chain)
- `wcifs.sys` — secondary (ZERO LPE CVEs)
- `WdFilter.sys` — Defender's kernel filter (understand to blind it)
- `cldflt.sys` — fully mapped (5+ CVEs, reference target)

### Tool stack: Static (offline, no execution)

**Ghidra (free, recommended for drivers)**
```
1. File → Import → bindflt.sys
2. Analysis → Auto Analyze (accept defaults, takes ~60s)
3. Symbol resolution:
   Symbol Server: https://msdl.microsoft.com/download/symbols
   Project → Add Externs from File → load bindflt.pdb (auto-download)
   Result: All exported function names, many internal names resolved
4. Navigate to: Exports → FltGetRoutineAddress (if present)
5. Navigate to: Function calls → FltCreateCommunicationPort
   → Trace to the pre-callback that handles messages
   → This is the entry point for BfSetupFilterEx kernel handler
```

**IDA Pro (faster decompilation, Hex-Rays C pseudo-code)**
```
1. Load bindflt.sys as PE (default)
2. Options → Symbol Path: srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
3. Edit → Plugins → Hex-Rays Decompiler → decompile any function to C
4. Key shortcut: F5 = decompile current function
5. Target first: Functions window → filter "Bf" → BfSetupFilterEx handler
```

**Key things to look for in bindflt.sys:**
```
namesup.c code  → path validation (where does it normalise/validate paths?)
mapping.c code  → bind mount creation (where does it USE the validated path?)
create.c code   → IRP_MJ_CREATE handler (where does it follow the binding?)

TOCTOU gap = time between namesup validation and mapping creation
If a junction can be swapped in that window → race condition → SYSTEM execution
```

**Finding BfSetupFilterEx's kernel handler:**
```
1. In Ghidra/IDA: search for string "BindFlt" or "bindflt"
2. Find FltCreateCommunicationPort call → callback parameter = message handler
3. Message handler is the kernel-side BfSetupFilterEx
4. From there: trace parameter extraction → path handling → mapping.c calls
```

### Tool stack: Dynamic (requires kernel debugging)

**Option A: VM + WinDbg kernel debug (best)**
```
Setup:
  VM: Windows 11 in VMware/Hyper-V with Test Signing OFF
  Host: WinDbg Preview (from Microsoft Store, free)
  Connection: vmnet (VMware) or KDNet over IP

On VM:
  bcdedit /debug on
  bcdedit /dbgsettings net hostip:<HOST_IP> port:50000

On Host WinDbg:
  File → Kernel Debug → Net → port 50000 → wait for VM boot
  Once connected:
  
  # Break in at bindflt load
  bp bindflt!BfSetupFilterEx

  # When hit: display call stack + parameters
  k        (call stack)
  r        (registers — RCX = first param in x64 calling convention)
  dt bindflt!_BINDFLT_MESSAGE_PARAMETERS @rcx  (display structure)
  
  # Step through validation → use gap
  p        (step over)
  t        (step into)
```

**Option B: ETW tracing (no kernel debugger needed)**
```powershell
# bindflt has its own ETW provider
$session = "bindflt-trace"
logman create trace $session -p "Microsoft-Windows-Containers-BindFlt" 0xff 0xff -o bindflt.etl
logman start $session

# Trigger: Add-AppxPackage (causes BfSetupFilterEx calls)
Add-AppxPackage -Path ".\test.msix" -ErrorAction SilentlyContinue

logman stop $session
# Open bindflt.etl in WPA (Windows Performance Analyzer) or ETWExplorer
# See: paths passed to BfSetupFilterEx, timing of events

# wcifs provider:
-p "Microsoft-Windows-Containers-Wcifs" 0xff 0xff
```

**Option C: ProcMon (userland view, no kernel debugger)**
```
ProcMon filter:
  Process Name = AppXSvc (or svchost.exe)
  Path contains = <msix_package_name>
  Operation = CreateFile, ReadFile, QueryNameInformationFile

Result: Shows exactly which paths AppXSvc opens during BfSetupFilterEx
        Shows junction following behaviour
        Shows the order of operations (validation window)
```

---

## CLASS 2 — PPL PROCESSES (Protected Process Light)

### What PPL is
Process Protection Level (PPL) prevents PROCESS_ALL_ACCESS even from admin.
`MsMpEng.exe` (Defender engine) runs as PP/PPL-AntiMalware — highest protection.

```
Standard user:  OpenProcess → ACCESS_DENIED
Admin/SYSTEM:   OpenProcess → ACCESS_DENIED (even NT AUTHORITY\SYSTEM denied handle)
PPL:            Only another PPL process with same or higher signer can open it
```

### VADER's PPL bypass: RTCore64 (already owned)

You already have RTCore64.sys with arbitrary kernel R/W via IOCTL.
That bypass works at ring 0 — PPL is a user-mode construct enforced by the kernel.
When you own the kernel, PPL is meaningless.

```c
// RTCore64 gives you: read/write any kernel address

// To read PPL process memory:
// 1. Find EPROCESS for MsMpEng.exe (walk ActiveProcessLinks from PsInitialSystemProcess)
// 2. Read EPROCESS.Protection byte (offset 0x87a on Win11 26200)
//    Protection byte format: bits[7:4] = Signer, bits[3:0] = Level
//    MsMpEng: 0x62 = WinTcb-Light (level 2, signer AntiMalware)
// 3. Temporarily clear Protection byte (set to 0x00)
// 4. From a SYSTEM process: OpenProcess(PROCESS_ALL_ACCESS, ..., pid)
//    Now succeeds — PPL disabled
// 5. ReadProcessMemory / VirtualQueryEx / etc.
// 6. Restore Protection byte to 0x62

// Alternatively: read MsMpEng virtual memory directly via kernel R/W
// EPROCESS.VadRoot → walk VAD tree → find module base → read bytes
```

**Simpler approach: dump mpengine.dll off disk**
```powershell
# mpengine.dll is on disk — not PPL protected when NOT loaded
$defPath = "C:\ProgramData\Microsoft\Windows Defender\Definition Updates"
$guid = (Get-ChildItem $defPath -Directory | Sort-Object LastWriteTime -Desc | Select -First 1).FullName
$mpe = Join-Path $guid "mpengine.dll"
Copy-Item $mpe "C:\Users\Ghaleb Jomma\vader-rootkit\analysis\mpengine.dll"
```

### Investigating MsMpEng.exe behavior without a handle

```powershell
# What MsMpEng sees (ETW):
# Provider: Microsoft-Antimalware-Engine
wevtutil qe "Microsoft-Windows-Windows Defender/Operational" /c:50 /f:text

# Scan triggers (which files get scanned):
logman create trace mpeng -p "Microsoft-Antimalware-Engine" 0xff 0xff -o mpeng.etl
logman start mpeng
# ... trigger scan ...
logman stop mpeng

# API calls from MsMpEng (using Procmon with elevated rights):
# Filter: Process Name = MsMpEng.exe
# Shows: File I/O, Registry, Network — even without OpenProcess access
```

---

## CLASS 3 — mpengine.dll ($150K MSRC TARGET)

### Why it's the holy grail
- MSRC highest bounty tier: memory corruption → code execution
- mpengine.dll processes EVERY file Defender scans
- It contains a complete file format parser for 70+ formats (ZIP, CAB, OOXML, etc.)
- Memory corruptions here = SYSTEM code execution without any user interaction
- Tavis Ormandy (Project Zero) found multiple: CVE-2017-0290, CVE-2022-21969

### Static analysis approach (Ghidra)

```
1. Copy mpengine.dll from Definition Updates GUID folder (see above)
2. Load in Ghidra — it's a standard DLL despite size (~100MB)
3. DO NOT use symbol server — mpengine has NO public symbols
4. Auto-analyze: ~10-30 minutes

Key things to hunt:
- String refs: "zip", "rar", "cab", "docx", "pdf" → parser entry points
- Function pattern: reads input buffer → parses structure → branch on magic bytes
- Dangerous patterns: malloc(user_controlled_size), memcpy without bounds check
- Integer overflow before malloc: size_t len = hdr.count * sizeof(ENTRY) — if count is huge, wraps to 0

Tools to help:
- Capa (FireEye) — auto-identifies capabilities in binary without symbols
- BinDiff — compare mpengine.dll across signature updates → find where parsers changed
- findcrypt2 (IDA plugin) — identifies crypto constants (useful for finding specific parsers)
```

### Dynamic fuzzing approach

```python
# Defender's scan function is exposed via IOCTL through MsMpEng
# Or: just drop files and watch Defender scan them (logs event)

# Minimal harness (Python + subprocess):
import subprocess, os, struct, random

def write_fuzz_file(data, path):
    with open(path, 'wb') as f:
        f.write(data)

# Start with valid ZIP: mutate length fields, entry counts, offsets
# ZIP local file header: PK\x03\x04 + 26 bytes metadata
zip_header = b'PK\x03\x04' + b'\x00' * 26
for i in range(1000):
    data = bytearray(zip_header)
    # Flip: entry count, compressed size, uncompressed size (overflow candidates)
    pos = random.randint(0, len(data)-4)
    data[pos:pos+4] = struct.pack('<I', random.randint(0, 0xFFFFFFFF))
    
    path = f"C:\\Temp\\fuzz_{i:04d}.zip"
    write_fuzz_file(bytes(data), path)
    # Defender auto-scans on write — watch for WER crash report in %LOCALAPPDATA%\CrashDumps
    # or: Event ID 1000 in Windows Application log = MsMpEng crash
```

**Monitoring for mpengine crashes:**
```powershell
# Watch for Defender crashes in real-time
while ($true) {
    $crash = Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000} -MaxEvents 1 -EA SilentlyContinue |
             Where-Object { $_.Message -match "MsMpEng" }
    if ($crash) {
        Write-Host "[CRASH] $($crash.TimeCreated) — $($crash.Message)" -ForegroundColor Red
        # Grab crash dump from: C:\ProgramData\Microsoft\Windows Defender\Quarantine
        #                    or: C:\ProgramData\Microsoft\Windows\WER\ReportQueue
        break
    }
    Start-Sleep 2
}
```

---

## CLASS 4 — SYSTEM SERVICES (no console, no debugger)

### Probing services that resist standard investigation

**Service: AppXSvc (the bindflt trigger)**
```powershell
# AppXSvc is svchost.exe — can't attach debugger to svchost without killing other services
# Approach 1: ProcMon — filter by PID of the specific svchost running AppXSvc
$pid = (Get-WmiObject Win32_Service -Filter "Name='AppXSvc'").ProcessId
# ProcMon filter: PID = $pid

# Approach 2: ETW — AppXSvc has its own provider
logman create trace appx -p "Microsoft-Windows-AppXDeploymentServer" 0xff 0xff -o appx.etl
logman start appx
Add-AppxPackage -Path ".\test.msix" -EA SilentlyContinue  # trigger
logman stop appx
# Open in WPA → see every file/registry operation AppXSvc makes
```

**Service: WsNativePushService (Wondershare — already OWNED)**
```powershell
# This one we already replaced the binary for — we own it
# To understand what it does before replacement:

# Read strings from binary
$path = (Get-WmiObject Win32_Service -Filter "Name='WsNativePushService'").PathName -replace '"',''
strings64.exe $path  # Sysinternals strings tool

# Or PowerShell equivalent:
$bytes = [System.IO.File]::ReadAllBytes($path)
$text = [System.Text.Encoding]::Unicode.GetString($bytes)
$text -split "`0" | Where-Object { $_.Length -gt 5 } | Select-Object -First 50
```

**General: Any SYSTEM service with no console**
```powershell
# Attach WinDbg to running service (requires admin, not for PPL):
# 1. Find PID
$svcPid = (Get-Process -Name svchost | Where-Object {
    (Get-WmiObject Win32_Service | Where-Object { $_.ProcessId -eq $_.Id }).Name -match "target"
}).Id

# 2. WinDbg.exe -p $svcPid  (works for non-PPL services)

# 3. Or: inject DLL via RTCore64 kernel patch
# Write to service process memory directly using kernel R/W
# Plant shellcode at known address, patch vtable or function pointer to redirect there
```

---

## CLASS 5 — AV/EDR BINARIES (self-protecting)

### The self-hook problem

AV products hook themselves. When you inject into MsMpEng, your injection code is scanned.
When you try to hook ntdll in an AV process, the AV's own hooks fire on your hook calls.

**VADER solution: don't fight inside — observe from outside**

```
Option A: Kernel observation (RTCore64)
  - Read AV process memory directly from ring 0
  - No injection, no detection
  - See: hooks in ntdll (look for JMP bytes at function entries)
  - See: in-memory configuration, detection rules, ML model buffers

Option B: VMI (Virtual Machine Introspection)
  - Run AV in a VM
  - From host: read VM memory (VMware GuestMemRead, libvmi, DRAKVUF)
  - AV can't detect observation from outside the VM
  - Can pause VM, snapshot, inspect, resume — no timing pressure

Option C: Network observation (passive)
  - AV makes network calls to cloud (query + classification)
  - Wireshark / Fiddler (with SSL bump) intercepts the requests
  - See: what hashes/features are sent, what cloud responds
  - Identifies: what triggers cloud query vs local verdict

Option D: Differential analysis
  - Scan file A → verdict X
  - Mutate one byte → verdict Y
  - Map which bytes/positions affect the verdict
  - Reverse-engineer feature extraction without seeing source code
  - Automates: mutation coverage of the detection surface
```

---

## CLASS 6 — EtwTi KERNEL TELEMETRY (Finding #36 open question)

### Probing the kernel's own telemetry system

The unresolved question: does `EtwTiLogSetContextThread` fire when we set DR0-DR3?

**Direct probe:**
```c
// Build this as a test binary (C + MASM):

#include <windows.h>
#include <evntrace.h>

// Step 1: Start an ETW trace session capturing EtwTi events
// ETW-Ti provider GUID: {22fb2cd6-0e7b-422b-a0c7-2fad1fd0e716}
// (Microsoft-Windows-Threat-Intelligence)

// Step 2: SetThreadContext on self with DR0 set to AmsiScanBuffer addr
CONTEXT ctx = {0};
ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;
ctx.Dr0 = (DWORD64)GetProcAddress(GetModuleHandle(L"amsi.dll"), "AmsiScanBuffer");
ctx.Dr7 = 0x1;  // enable DR0
SetThreadContext(GetCurrentThread(), &ctx);

// Step 3: Read ETW session events
// If EtwTiLogSetContextThread fired → event appears in trace
// If no event → provider-level gap (kernel doesn't generate telemetry for this)

// Step 4: Even if event fires — does Defender consume and act on it?
// Plant a HWBP payload that does something distinctive but harmless
// Check Defender telemetry in Event Viewer: Windows Defender Operational log
// If Defender generates a detection event → consumer receives telemetry
// If no detection → consumer gap (Defender ignores EtwTi for SetThreadContext)
```

**XPerf/WPR method:**
```powershell
# Capture kernel-level telemetry including EtwTi
wpr -start GeneralProfile -start VirtualAllocTracing
# ... trigger SetThreadContext with debug registers ...
wpr -stop etw_capture.etl

# Open in WPA → Trace → System Activity → Threat Intelligence
# Look for EtwTiLogSetContextThread events
# If present: Defender receives them → check why it doesn't act
# If absent: provider gap confirmed → MSRC submission angle
```

---

## DECISION TREE — WHICH TOOL FOR WHICH TARGET

```
Is the target a kernel driver (.sys)?
  → YES: Start with Ghidra + symbol server (static)
          Then ETW trace (dynamic, no kernel debugger needed)
          Then VM + WinDbg kernel debug (dynamic, full power)

Is the target a PPL process (MsMpEng.exe)?
  → YES: Option A — read memory via RTCore64 kernel R/W (already owned)
          Option B — copy DLL from disk (not PPL protected)
          Option C — ETW observation (works regardless of PPL)

Is the target a SYSTEM service with no console?
  → YES: ProcMon (filter by PID) for file/reg/net activity
          ETW trace (provider specific to service)
          WinDbg attach (if service process is not PPL)

Is the target an AV/EDR?
  → YES: VMI (run in VM, observe from host)
          Differential fuzzing (observe outputs, infer internals)
          Kernel R/W via RTCore64 (read memory from ring 0)
          Network interception (cloud query analysis)

Do you need to understand the DETECTION ENGINE (mpengine.dll)?
  → YES: Copy from disk → Ghidra (static, no PPL concern)
          Harness fuzzing (drop malformed files, watch for crashes)
          Differential scanning (map which mutations change verdict)
```

---

## PRIORITY FOR VADER PROGRAM

| Target | Why | First Move |
|--------|-----|-----------|
| `bindflt.sys` | Primary CVE target — ZERO CVEs | Ghidra + symbol server → message.c handler |
| `AppXSvc` (bindflt trigger) | Maps paths into BfSetupFilterEx | ProcMon filter + ETW BindFlt provider |
| EtwTi gap (Finding #36) | MSRC submission angle if confirmed | XPerf WPR capture during SetThreadContext |
| `mpengine.dll` | $150K bounty class | Copy from disk → Ghidra → file format parsers |
| `WdFilter.sys` | Maps Defender's kernel visibility | Ghidra → FltRegisterFilter callbacks |

---

*RADON · 22DIV VADER · 2026-06-26*
*Own hardware only. Authorized research. ABN 50 692 429 397 — 22nd Survey Division.*
