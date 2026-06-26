# MUTATION NOTE — AsusCertService Named Pipe LPE Track
## 2026-06-26 20:52 AEST | RADON | Synthesised from cve-submissions loops 3-9

---

## THE LEAD

**AsusCertService** exposes a named pipe (`\\.\pipe\asuscert`) that is:
- Connectable by standard users (confirmed: loop 3 named_pipe_acl_scan, 573 pipes enumerated)
- Owned by a service running as **LocalSystem** (SYSTEM)
- Protocol **unknown** — no public reversal found

This is the exact attack surface that produced CVE-2026-20817 (WER SvcElevatedLaunch ALPC)
and CVE-2026-26422 (Clash Verge IPC endpoint). Both: privileged service + world-accessible
endpoint + no caller validation = LPE.

---

## PRECEDENT CHAIN (three loop build)

| CVE | Service | Mechanism | Outcome |
|-----|---------|-----------|---------|
| CVE-2026-20817 | WER SvcElevatedLaunch | ALPC, no privilege check | SeDebugPrivilege token |
| CVE-2026-26422 | Clash Verge Rev IPC | Named pipe, world-reachable | LPE (patched v2.3.0) |
| CVE-2026-7480 | ASUS SysControl Interface | RPC, client-side auth only | SYSTEM + arb exec |
| GSWA-2026-011 | CTFMON Text Services | Object namespace squatting | Primitive confirmed |

AsusCertService hits four of these patterns simultaneously:
- Named pipe (not ALPC, Win32 accessible) ✓
- World-connectable (standard user) ✓
- LocalSystem service ✓
- ASUS vendor (CVE-2026-7480 shows MITRE assigns CWE for ASUS IPC issues) ✓

**Assessment: MEDIUM probability. Gated on protocol reversal.**

---

## WHAT BLOCKS IT

Protocol unknown. The pipe accepts connections from standard users but the message
format has not been reversed. Without knowing what the service accepts, a crafted
privilege-escalation request cannot be constructed.

**What the service likely does** (inference from "AsusCert" name):
- Certificate management for ASUS hardware signing (secure boot, firmware updates)
- Possible operations: certificate query, certificate install, signature verification
- If any operation causes the service to write a file to a SYSTEM-only path,
  or launch a process, or impersonate the caller — that's the LPE trigger

---

## REVERSAL APPROACH (no Sysinternals required on RADON)

### Step 1 — Observe pipe traffic during normal ASUS operation

```powershell
# Start ETW trace on named pipe I/O
$session = "asuscert-pipe-trace"
logman create trace $session -p "Microsoft-Windows-Kernel-File" 0x80 0x4 -o asuscert.etl
logman start $session

# Trigger ASUS certificate activity:
# - Open ASUS Armoury Crate (forces cert check on launch)
# - Or: install an ASUS driver update (triggers firmware signing)

Start-Sleep 30
logman stop $session
# Open asuscert.etl in WPA → filter pipe name "asuscert" → ReadFile/WriteFile events
# Payload bytes visible in ETW file I/O trace
```

### Step 2 — Replicate pipe client in PowerShell

```powershell
# Connect to the pipe as standard user
$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", "asuscert",
    [System.IO.Pipes.PipeDirection]::InOut)
$pipe.Connect(3000)  # 3 second timeout

# Read server hello (if service sends first)
$reader = New-Object System.IO.StreamReader($pipe)
$serverHello = $reader.ReadLine()
Write-Host "Server: $serverHello"

# Send null/empty message — observe response/error
$writer = New-Object System.IO.StreamWriter($pipe)
$writer.WriteLine("")
$writer.Flush()
$response = $reader.ReadLine()
Write-Host "Response: $response"
$pipe.Dispose()
```

### Step 3 — Fuzz message structure

```powershell
# Send structured messages — observe service behaviour in Event Viewer
# Pattern from CVE-2026-26422: Clash Verge accepted JSON over IPC
# Pattern from CVE-2026-20817: WER used RPC-style struct (length-prefixed)

$pipe = New-Object System.IO.Pipes.NamedPipeClientStream(".", "asuscert",
    [System.IO.Pipes.PipeDirection]::InOut)
$pipe.Connect(1000)

# Try common IPC framing patterns:
$tests = @(
    [byte[]](0x00, 0x00, 0x00, 0x00),            # null header
    [byte[]](0x01, 0x00, 0x00, 0x00),            # op code 1
    [byte[]]([System.Text.Encoding]::UTF8.GetBytes('{"op":"status"}')),   # JSON
    [byte[]]([System.Text.Encoding]::UTF8.GetBytes("GETCERT`r`n")),       # text command
    [byte[]](0xFF, 0xFF, 0xFF, 0xFF)              # invalid marker
)

foreach ($msg in $tests) {
    try {
        $pipe.Write($msg, 0, $msg.Length)
        $buf = New-Object byte[] 4096
        $n = $pipe.Read($buf, 0, $buf.Length)
        $hex = ($buf[0..($n-1)] | ForEach-Object { "{0:X2}" -f $_ }) -join " "
        Write-Host "Sent $($msg.Length)b → Got $n b: $hex"
    } catch { Write-Host "Error: $_" }
}
$pipe.Dispose()
```

### Step 4 — If service crashes (access violation in Event Viewer ID 1000)

```powershell
# Crash = memory corruption in message parsing = potential CVE
# Capture crash dump from:
Get-ChildItem "C:\ProgramData\Microsoft\Windows\WER\ReportQueue" |
    Where-Object { $_.Name -match "[Aa]sus" } |
    Sort-Object LastWriteTime -Desc | Select-Object -First 3
```

---

## PROBABILITY LADDER

| State | Probability | Next Action |
|-------|-------------|------------|
| Pipe connectable (confirmed) | N/A — fact | — |
| Service crashes on malformed input | → 40-60% CVE (memory corruption) | Fuzz step 3 |
| Service executes caller-controlled command | → 60-75% CVE (SYSTEM exec) | Protocol reversal |
| Service validates caller properly | → ~0% LPE | Dead vector — document |
| Protocol reversed, no unsafe operation found | → 0% LPE (information only) | Dead vector |

---

## SUBMISSION PATH IF FOUND

**Vendor**: ASUSTeK Computer Inc.  
**Contact**: security@asus.com  
**CWE**: CWE-732 (pipe ACL) OR CWE-306 (missing auth) OR CWE-787 (memory corruption)  
**Precedent**: CVE-2026-7480 (same vendor, same IPC pattern, same outcome — MITRE assigned)  
**CVSS estimate**: 7.0-8.5 (local, no auth, SYSTEM impact)

---

*RADON · 22DIV VADER · 2026-06-26*
