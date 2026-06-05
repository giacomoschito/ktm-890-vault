---
tipo: roadmap
budget_totale_target: 12-30 EUR
stato: FASE 0 OPERATIVA
---

# Roadmap Zero-Cost — Cockpit KTM 890 Duke

tags: #roadmap #cockpit #diy

> Strategia: massimizzare il software a costo zero ORA con il PC che hai già, ridurre l'hardware al minimo indispensabile. Pavimento invalicabile per dialogare con la moto: ~€12-15 (adattatore + ELM327).

---

## Stato Attuale (2026-06-05)

| Fase | Stato |
|------|-------|
| **0. Software platform** (no hardware) | ✅ **OPERATIVA** |
| **1. Hardware minimo OBD-II** (€12-15) | ⏳ Da ordinare |
| **2. CAN bus sniffing** (€15-20) | ⏳ Futura |
| **3. Smartphone telemetria** (free) | 📋 Pianificata |

---

## FASE 0 — Software Platform Locale ✅ FATTO

**Progetto:** `04 - Diagnostica/scripts/ktm-cockpit/`

Stack costruito stasera, **funziona senza moto**:

```
┌──────────────┐   TCP:35000    ┌─────────────────┐  WebSocket  ┌──────────┐
│  simulator   │ ───────────►   │  FastAPI + SQLite│ ──────────► │ browser  │
│  ELM327 fake │                │  (cockpit.db)    │             │ dashboard│
└──────────────┘                └─────────────────┘             └──────────┘
                                       │
                                       └── legge ── vault YAML ──► alert manutenzione
```

### Componenti
- **`app/simulator.py`** — emulatore ELM327 TCP che genera RPM/vel/temp realistici
- **`app/elm_client.py`** — client unificato (TCP per dev, seriale per hardware reale)
- **`app/can_decoder.py`** — decoder frame CAN con ID già noti dalla community 790/890
- **`app/maintenance.py`** — legge frontmatter YAML di `00 - Dashboard.md` e `Storico Tagliandi.md`, calcola alert km/giorni
- **`app/db.py`** — SQLite per telemetria storica
- **`app/main.py`** — FastAPI + WebSocket live + endpoint REST
- **`app/templates/index.html`** — dashboard dark Geist + Chart.js (tema KTM arancio)

### Verifica fatta
- `GET /api/status` → legge correttamente km_attuale 5407 dal vault
- WebSocket `/ws/live` → snapshot ogni 0.5s con dati live
- Test snapshot ricevuto: `{rpm:5041, speed:95, gear:4, oil:53, voltage:14.19}`

### Avvio
Due terminali PowerShell:
```powershell
cd "C:\KTM DUKE 890\04 - Diagnostica\scripts\ktm-cockpit"
.\start_sim.ps1     # terminale 1
.\start_server.ps1  # terminale 2
```
Browser: http://127.0.0.1:8000

---

## FASE 1 — Hardware Minimo (€12-25) ⏳

Vedi [[Lista Acquisti Diagnostica]] aggiornata con link precisi.

**Da comprare (versione minimum spend):**
1. Adattatore Euro5 ISO 19689 → OBD2 (~€7-12)
2. ELM327 Bluetooth (vgate iCar Pro BT 4.0 raccomandato, ~€20)

**Patch software al ricevimento:**
- Abbinare ELM327 BT a Windows → diventa `COM7` (o simile)
- Estendere `elm_client.py` con `ElmClient.serial(port, baud)` (pyserial già installato)
- Avviare: `$env:KTM_ELM_HOST="COM7"; .\start_server.ps1`
- Il simulator si spegne, parla direttamente con la moto

**Cosa otteniamo subito:**
- RPM, velocità, temp liquido/olio, voltaggio, gas, marcia (PID standard)
- **Lettura/cancellazione codici errore** (DTC)
- **Reset spia ASSISTENZA** via comando custom (replicando MotoScan)

---

## FASE 2 — CAN Bus Sniffing (€15-30) ⏳

Una volta che la fase 1 funziona:
- CANable clone (€15) + breakout OBD2 (€6)
- Decoder già scritto in `can_decoder.py` con ID 790dukeforum
- Sblocca: forza freni, posizione frizione, dati ABS/TC granulari

---

## FASE 3 — Smartphone come Sensore (FREE) 📋

**Senza toccare la moto**, dati real time durante le uscite:

- **App Sensor Logger** (free, Android+iOS) → CSV con GPS+IMU
- Import endpoint nel backend FastAPI: `POST /api/ride/import`
- Stima angolo piega, accelerazioni laterali, frenate
- Correlazione con telemetria moto (quando hai entrambe)

**Bonus integrazioni a costo zero:**
- **KTM My Ride** export tracce
- **OCR cruscotto** via foto (Tesseract gratis, già pacchettizzabile)

---

## Cosa NON Compriamo

| Tool | Costo | Perché no |
|------|-------|-----------|
| Healtech SP1 | €60-80 | Fa SOLO il service reset. Il nostro software lo fa con €12 di cavi. |
| MotoScan Pro | €15 app | Lo scriviamo noi in Python. |
| KTMFlash + cavo dedicato | €30-40 | Solo se in futuro vorrai rimappare la ECU. Non ora. |
| OBDLink MX+ | €100 | Premium di lusso. Il vgate iCar Pro a €20 fa quello che ci serve. |

---

## Cross-link

- Progetto codice: `04 - Diagnostica/scripts/ktm-cockpit/README.md`
- [[Lista Acquisti Diagnostica]] — link precisi non sbagliare
- [[OBD2 Setup KTM]] — guida storica
- [[CAN Bus Telemetry]] — decode ID
- [[Reset Spia Assistenza KTM 890]] — opzioni reset
