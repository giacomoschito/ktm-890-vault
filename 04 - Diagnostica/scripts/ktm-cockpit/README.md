# KTM 890 Duke Cockpit

Sistema di telemetria + manutenzione, **fase 0 zero-cost**. Funziona già adesso
con il simulator ELM327 incluso, senza hardware sulla moto.

## Avvio in 2 terminali

**Terminale 1 — simulator (emula la moto):**
```powershell
cd "C:\KTM DUKE 890\04 - Diagnostica\scripts\ktm-cockpit"
.\start_sim.ps1
```

**Terminale 2 — backend + dashboard:**
```powershell
cd "C:\KTM DUKE 890\04 - Diagnostica\scripts\ktm-cockpit"
.\start_server.ps1
```

Apri http://127.0.0.1:8000 nel browser.

## Quando arriva l'ELM327 reale

Il supporto seriale è pronto: USB (`COMx`) o Bluetooth abbinato in Windows
(porta seriale virtuale, es. `COM7`). Installa prima le dipendenze aggiornate:
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

**Dashboard web** con la moto al posto del simulator:
```powershell
$env:KTM_ELM_HOST = "COM7"     # o COMx
$env:KTM_ELM_BAUD = "38400"    # opzionale, default 38400
.\start_server.ps1
```

**Strumento diagnostico** da riga di comando (non insieme al server: la porta
COM la può aprire un solo programma):
```powershell
python -m app.diag_tool --target COM7 ecu         # centraline che rispondono
python -m app.diag_tool --target COM7 info        # identificazione ECU + verdetto A2
python -m app.diag_tool --target COM7 dtc         # codici errore (OBD + UDS)
python -m app.diag_tool --target COM7 clear-dtc   # cancella codici (chiede conferma)
python -m app.diag_tool --target COM7 scan-dids --range F100-F1FF
python -m app.diag_tool --target COM7 raw 22F190  # singola lettura (solo servizi read-only)
```
I report finiscono in `04 - Diagnostica/Letture ECU/`. Senza `--target` i
comandi parlano col simulator, utile per provarli prima.

**Registratore CAN** (fase 2, con CANable):
```powershell
python -m app.can_logger --interface slcan --channel COM8 --only-diag
```
Log in `04 - Diagnostica/Log CAN/`. Piano completo: `04 - Diagnostica/Reverse Engineering ECU.md`.

## Struttura

```
app/
  simulator.py    — emulatore ELM327 TCP (porta 35000)
  elm_client.py   — client ELM327 unificato + decoder PID OBD-II
  uds.py          — client UDS/OBD (lettura, DTC, cancellazione, scansione DID)
  ecu_info.py     — identificazione ECU + euristica A2
  diag_tool.py    — strumento diagnostico da riga di comando
  can_logger.py   — registratore CAN passivo (fase 2)
  can_decoder.py  — decoder frame CAN (per CANable, fase 2)
  maintenance.py  — legge YAML dal vault e calcola alert
  db.py           — SQLite (telemetria persistita)
  main.py         — FastAPI + WebSocket + dashboard
  templates/
    index.html    — dashboard web (Geist + Chart.js, dark theme KTM)
data/
  cockpit.db      — telemetria storica (auto-creato)
```
