---
tipo: piano-tecnico
fase: A
stato: SOFTWARE PRONTO (in attesa hardware)
budget: ~45 EUR
---

# Fase A — UDS Read-Only + Rilevamento A2

tags: #diagnostica #uds #a2 #cockpit

> **Obiettivo:** capire se la moto è davvero depotenziata a 35 kW (A2) o full power 105 CV (77 kW), **senza spendere più di €45** e senza toccare la ECU in scrittura.

---

## Logica

Il libretto dice "depotenziata" ma test in strada privata >200 km/h → la 890 A2 reale non ci arriva (si pianta a ~160-170). Tre scenari possibili:
1. Libretto A2 ma moto già repotenziata da qualcuno (NON conforme = problema legale/assicurativo)
2. Lettura errata del libretto
3. "Depotenziata" è solo annotazione amministrativa, non un cap fisico

L'unico modo per saperlo con certezza è **leggere la calibration ID** dell'ECU e confrontarla con il database community KTM 890.

---

## Cosa fa il software (FATTO)

Progetto: `04 - Diagnostica/scripts/ktm-cockpit/`

### Modulo `app/uds.py`
Client UDS (ISO 14229) + OBD-II Mode 09 sopra ELM327. Read-only puro.

**Cosa legge:**
| Mode | PID/DID | Significato |
|------|---------|-------------|
| 09 | 02 | VIN |
| 09 | 04 | Calibration ID |
| 09 | 0A | ECU name |
| 22 | F186 | Sessione diagnostica attiva |
| 22 | F187 | Spare part number costruttore |
| 22 | F188/F189 | Software number + version (costruttore) |
| 22 | F18A | Identificativo supplier (BOSCH) |
| 22 | F18C | Serial number ECU |
| 22 | F190 | VIN (UDS) |
| 22 | F194/F195 | SW number + version (supplier) |
| 22 | F197 | Tipo motore / nome ECU |
| 22 | F1A2 | Hardware number costruttore |
| 22 | 0x2000-0xF0xx | DIDs proprietari KTM da esplorare |
| 03 | — | DTC memorizzati |

### Modulo `app/ecu_info.py`
Sequenza one-shot + euristica A2 detection.

**Logica A2:**
- Pattern testuali nella calibration ID / software version:
  - **Sospetto A2:** `A2`, `35KW`, `LIM`, `RESTR`
  - **Pro full power:** `FP`, `FULL`, `105KW`, `77KW`
- Verdetto a 3 livelli: `high` / `medium` / `low` confidence
- **Non è prova certa.** Il CalID va sempre cross-checkato manualmente sui forum tuning KTM.

### Endpoint `/api/ecu`
JSON con tutto il report. Pulsante "Esegui scansione ECU" nel dashboard web.

---

## Verifica software (FATTA stasera)

Test con simulator integrato. Configurazione `FAKE_A2=False` (simula full power):

```json
{
  "vin": "VBKEXJ408MM123456",
  "vin_valid_ktm": true,
  "calibration_id": "KTM89021FP-105KW-V112",
  "a2": {
    "is_likely_a2": false,
    "confidence": "high",
    "evidence_against": [
      "Match pattern full power: 'FP'",
      "Match pattern full power: '105KW'"
    ]
  }
}
```

✅ Pipeline funziona. Switch a `FAKE_A2=True` nel simulator → verdetto si inverte.

---

## Cosa serve per usarlo sulla moto

### Hardware (€45 totale, vedi [[Lista Acquisti Diagnostica]])

1. **Adattatore Euro5 6-pin → OBD2** (~€20)
   - KDS-online.de: https://kds-online.de/en/obd-adapter-euro5-for-motorcycle-6-pin-to-obd2-k-line-can-bus.html

2. **ELM327 Bluetooth 4.0** (~€25)
   - Vgate iCar Pro BT 4.0: https://www.amazon.it/s?k=vgate+iCar+Pro+BT+4.0

### Patch software (10 righe quando arriva)

Estensione di `app/elm_client.py` per supportare seriale BT:
```python
@classmethod
async def serial_port(cls, port: str = "COM7", baud: int = 115200):
    # apre porta seriale via pyserial-asyncio
    ...
```

Avvio: `$env:KTM_ELM_HOST="COM7"; .\start_server.ps1`

---

## Procedura il giorno X (quando arriva l'hardware)

1. Abbinare ELM327 Bluetooth in Windows (Bluetooth → Add device → PIN 1234 o 0000) → si crea COM7 (o simile)
2. Quadro KTM su **ON** (motore SPENTO — sicurezza)
3. Collegare adattatore Euro5 alla presa diagnostica (sotto sella, lato sx batteria)
4. Innestare ELM327 sulla OBD2 dell'adattatore
5. PC: `$env:KTM_ELM_HOST="COM7"; .\start_server.ps1`
6. Browser http://127.0.0.1:8000 → click "Esegui scansione ECU"
7. Salvare il JSON di output nel vault
8. **Cross-check del CalID sui forum:**
   - 790dukeforum.com → search calibration ID
   - ktm-forum.it → topic tuning 890
   - Reddit r/KTMDuke
   - Telegram gruppi tuning Bosch ME17
9. Verdetto finale: A2 sì/no/inconclusivo

---

## Limiti onesti

- Il pattern matching testuale **non sostituisce** un dump completo della mappa ECU
- Alcuni dealer riprogrammano lasciando il CalID originale → falso negativo possibile
- Senza accesso ai DB community (privati) il cross-check resta manuale
- Per certezza al 100% serve **Fase B** (Tactrix OpenPort 2.0 €220 + dump completo) o **centro tuning** (€50-80 lettura ECU)

---

## File toccati in questa fase

```
ktm-cockpit/
├── app/
│   ├── uds.py          ← NUOVO
│   ├── ecu_info.py     ← NUOVO
│   ├── simulator.py    ← esteso (Mode 09/22/03)
│   ├── main.py         ← +endpoint /api/ecu
│   └── templates/
│       └── index.html  ← +card "Identificazione ECU"
```

---

## Cross-link

- [[Roadmap Zero-Cost]] — piano fasi completo
- [[Lista Acquisti Diagnostica]] — hardware preciso
- [[OBD2 Setup KTM]] — basics
- [[CAN Bus Telemetry]] — fase 2 (futuro)
- README progetto: `04 - Diagnostica/scripts/ktm-cockpit/README.md`
