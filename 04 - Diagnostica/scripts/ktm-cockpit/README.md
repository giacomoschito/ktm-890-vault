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

Sostituisci il simulator con l'ELM327 fisico. Due opzioni:

**A) ELM327 USB:** rilevato come `COMx`. Sostituisci in `app/elm_client.py`
la classmethod `tcp` con una `serial` (pyserial).

**B) ELM327 Bluetooth:** abbinalo in Windows come porta seriale BT virtuale
(es. COM7) → stessa cosa del caso A.

In entrambi i casi, prima di partire avvia `start_server.ps1` impostando le
variabili d'ambiente:
```powershell
$env:KTM_ELM_HOST = "COM7"  # o COMx
```
(serve patch minima per supporto serial — la facciamo quando arriva l'hardware)

## Struttura

```
app/
  simulator.py    — emulatore ELM327 TCP (porta 35000)
  elm_client.py   — client ELM327 unificato + decoder PID OBD-II
  can_decoder.py  — decoder frame CAN (per CANable, fase 2)
  maintenance.py  — legge YAML dal vault e calcola alert
  db.py           — SQLite (telemetria persistita)
  main.py         — FastAPI + WebSocket + dashboard
  templates/
    index.html    — dashboard web (Geist + Chart.js, dark theme KTM)
data/
  cockpit.db      — telemetria storica (auto-creato)
```
