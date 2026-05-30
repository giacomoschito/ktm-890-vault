# Diagnostica KTM 890 Duke — Guida Completa da Zero

tags: #diagnostica #tuneecu #can-bus #diy

> **Livello:** Principiante · **PC:** Portatile Windows · **Obiettivo:** Leggere dati moto, codici errore, costruire un sistema di monitoraggio

---

## Perché la KTM Non Ha l'OBD2 Standard

Le auto hanno un connettore OBD2 (standard dal 1996) sotto il cruscotto.
Le moto usano protocolli proprietari dei costruttori.

La KTM 890 Duke 2021 usa:
- **Connettore:** 6 pin **Euro5 ISO 19689** (lato sinistro batteria, sotto la sella)
- **Protocollo:** CAN bus (ISO 15765-4) @ 500 kbps + K-Line
- **ECU:** Bosch (gestisce motore, TC, ABS, mappature)

Per parlarci dall'esterno serve un adattatore hardware specifico.

> 📋 Per la lista d'acquisto definitiva con link e prezzi vedi [[Lista Acquisti Diagnostica]].
> Per il CAN sniffing avanzato vedi [[CAN Bus Telemetry]].

---

## Schema Generale del Sistema

```
┌─────────────────┐     ┌───────────────────┐     ┌──────────────┐
│  KTM 890 Duke   │     │  Cavo adattatore  │     │  PC Windows  │
│                 │     │                   │     │              │
│  6-pin KTM  ───►│────►│  KTM → USB/FTDI  │────►│  TuneECU    │
│  diagnostico    │     │  ~€10 AliExpress  │     │  (software   │
│                 │     │                   │     │   gratuito)  │
└─────────────────┘     └───────────────────┘     └──────────────┘
```

---

## Percorso Scelto: PC + ELM327 + Python Custom

> ⚠️ TuneECU NON supporta la 890 Duke (ECU Bosch nuova generazione).
> TuneECU funziona solo su KTM 690/990/1190 con ECU vecchia.
>
> Obiettivo: leggere dati live, codici errore e costruire un sistema di monitoraggio proprietario.
> Stack: Hardware (€12) → python-obd + pyserial → Dashboard custom integrata col vault.

---

## Fase 1 — Hardware: Il Cavo Giusto

### Setup Identificato (Economico e Completo)

**Pezzo 1 — Adattatore KTM 6-pin → OBD2** · già trovato su AliExpress
- Converte il connettore proprietario KTM verde (6 pin) nello standard OBD2 (16 pin)
- Prezzo: **€3.44**
- Da solo non fa nulla — serve il pezzo 2

**Pezzo 2A — ELM327 USB** (per uso con PC + TuneECU)
- Si innesta sulla presa OBD2 del cavo sopra
- Collega il tutto al PC via USB
- Cerca: `"ELM327 USB OBD2 scanner CH340"`
- Prezzo: **€5-10**
- Software: TuneECU (gratuito) — lettura dati, codici errore, backup ECU

**Pezzo 2B — ELM327 Bluetooth** (per uso con telefono + MotoScan)
- Stessa cosa ma wireless
- Cerca: `"ELM327 Bluetooth OBD2 v2.1"`
- Prezzo: **€8-12**
- App: MotoScan (iOS/Android, €10-15)

```
Setup PC completo:
KTM 6-pin → [Adattatore €3.44] → OBD2 → [ELM327 USB €7] → PC → TuneECU
Totale: ~€10-12

Setup mobile:
KTM 6-pin → [Adattatore €3.44] → OBD2 → [ELM327 BT €10] → Telefono → MotoScan
Totale: ~€14-16
```

> **Nota:** ELM327 + questo adattatore è ottimo per lettura dati e codici errore.
> Per operazioni avanzate ECU (backup mappa completo, rimappatura) potrebbe servire
> in futuro il cavo USB dedicato KTM (€15-20). Si valuta dopo aver esplorato il base.

---

## Fase 2 — Software: TuneECU

### Cos'è TuneECU

TuneECU è un software gratuito Windows sviluppato dalla community per:
- Leggere e cancellare codici errore (Fault Codes / DTC)
- Monitorare dati live in tempo reale (RPM, temperatura, velocità, TC, ABS...)
- Leggere e scrivere mappe ECU (rimappatura)
- Fare backup della mappa originale

**Sito ufficiale:** tunecu.eu
**Compatibilità:** Windows 7/8/10/11 — 32 e 64 bit
**Costo:** Gratuito

### Compatibilità 890 Duke 2021

TuneECU supporta la serie 890 Duke. La versione ECU installata sulla tua moto determina le funzionalità disponibili. Lo scopriamo al primo collegamento.

---

## Fase 3 — Installazione e Setup

### 3.1 — Download TuneECU

1. Vai su **tunecu.eu** → Download
2. Scarica la versione più recente (es. TuneECU 2.x.x)
3. Installa normalmente su Windows

### 3.2 — Driver del Cavo

Quando colleghi il cavo USB-KTM al PC per la prima volta:
- Windows potrebbe installare i driver automaticamente
- Se non funziona, scarica il driver manualmente in base al chip:
  - **FTDI:** cerca "FTDI driver Windows" → ftdichip.com
  - **CH340:** cerca "CH340 driver Windows" → link comune su Arduino community

**Come capire quale chip ha il tuo cavo:**
Collegalo al PC → Gestione Dispositivi (Device Manager) → Porte COM → guarda il nome del dispositivo.

### 3.3 — Primo Avvio TuneECU

1. Apri TuneECU
2. Vai su **Settings → Communication**
3. Seleziona la porta COM assegnata al tuo cavo
4. Baud rate: lascia automatico o prova 38400

---

## Fase 4 — Primo Collegamento alla Moto

### Procedura Sicura

1. **Moto spenta** — non avviare il motore
2. Localizza il connettore diagnostico (vedi sotto)
3. Collega il cavo KTM al connettore della moto
4. Collega l'altra estremità al PC
5. **Accendi solo il contatto** (chiave su ON, motore spento)
6. Apri TuneECU → Connect
7. Aspetta che riconosca l'ECU

### Dove Si Trova il Connettore

```
Vista laterale destra della moto:
- Smonta la coda (2-4 viti) oppure
- Alza la sella e guarda sotto
- Connettore a 6 pin con tappo di protezione in gomma
- Spesso vicino alla batteria
```

> Se non riesci a trovarlo, dimmi e cerchiamo la posizione esatta sul manuale della 890 Duke 2021.

### Cosa Fare Prima di Modificare Qualcosa

**REGOLA D'ORO:** Solo lettura finché non hai capito bene il sistema.

1. Connetti e leggi i dati (solo visualizzazione)
2. Salva la mappa ECU originale (backup!)
3. Leggi i codici errore
4. Solo dopo: valuta modifiche

---

## Fase 5 — Cosa Puoi Leggere

### Dati Live (Real-Time)

| Dato | Descrizione |
|------|-------------|
| RPM | Giri motore istantanei |
| TPS | Apertura farfalla (%) |
| MAP | Pressione collettore aspirazione |
| ECT | Temperatura liquido raffreddamento |
| EOT | Temperatura olio motore |
| Battery | Tensione batteria |
| Gear | Marcia inserita |
| Speed | Velocità ruota |
| TC status | Traction Control — livello e interventi |
| ABS status | Stato ABS |

### Fault Codes (Codici Errore)

TuneECU legge tutti i DTC (Diagnostic Trouble Codes) memorizzati dall'ECU.
- Ogni codice ha un numero e una descrizione
- Puoi vedere se il codice è **attivo** (problema presente) o **memorizzato** (problema passato)
- Puoi cancellare i codici memorizzati

### ECU Info

- Versione firmware ECU
- Numero seriale ECU
- Mappa attualmente caricata

---

## Fase 6 — Costruire un Sistema di Monitoraggio Custom

Questa è la parte dove usiamo Python + Claude per costruire qualcosa di nostro.

### Architettura del Sistema

```
KTM CAN Bus
    │
    ▼
Cavo USB-KTM
    │
    ▼
Python (pyserial / python-can)
    │
    ├──► Dashboard live (terminale o web)
    ├──► Log CSV / JSON
    ├──► Obsidian vault (aggiornamento automatico note)
    └──► Grafana (visualizzazione storica)
```

### Librerie Python Utili

```python
# Comunicazione seriale con il cavo FTDI
import serial          # pip install pyserial

# Parsing dati CAN bus
import can             # pip install python-can

# Dashboard terminale
import rich            # pip install rich

# Dashboard web
import streamlit       # pip install streamlit

# Database locale
import sqlite3         # built-in Python

# Grafici
import plotly          # pip install plotly
```

### Esempio Minimo — Lettura Dati (da sviluppare insieme)

```python
import serial
import time

# Connessione al cavo KTM
ser = serial.Serial('COM3', 38400, timeout=1)

def read_ktm_data():
    """Legge un frame di dati dall'ECU KTM"""
    # Il protocollo specifico lo definiamo dopo
    # aver identificato la COM port e testato la connessione
    pass

# Loop principale
while True:
    data = read_ktm_data()
    if data:
        print(f"RPM: {data['rpm']} | Temp: {data['temp']}°C")
    time.sleep(0.1)
```

> Nota: il protocollo esatto e i comandi specifici li calibriamo una volta che hai il cavo e fai il primo collegamento con TuneECU. TuneECU è il riferimento per capire come l'ECU risponde.

---

## Checklist Progressiva

### Step 1 — Hardware (da fare ora)
- [ ] Trovare e ordinare cavo TuneECU USB-KTM (AliExpress/eBay)
- [ ] Verificare dove si trova il connettore diagnostico sulla moto

### Step 2 — Software base
- [ ] Scaricare e installare TuneECU
- [ ] Installare driver cavo (FTDI o CH340)
- [ ] Primo collegamento moto → PC
- [ ] Leggere versione ECU e codici errore
- [ ] Salvare backup mappa ECU originale

### Step 3 — Monitoraggio live
- [ ] Esplorare i dati live su TuneECU
- [ ] Capire i parametri più utili per il tuo uso
- [ ] Screenshot del pannello dati live

### Step 4 — Sistema custom con Python
- [ ] Installare Python sul portatile
- [ ] Installare librerie: pyserial, rich
- [ ] Script base di lettura dati
- [ ] Logging su file CSV
- [ ] Integrazione con vault Obsidian

### Step 5 — Dashboard avanzata (futuro)
- [ ] Dashboard web con Streamlit o Grafana
- [ ] Alert automatici (es. temperatura alta)
- [ ] Sincronizzazione con log uscite Obsidian

---

## Sicurezza — Regole d'Oro

1. **Backup prima di tutto:** prima di qualsiasi modifica ECU, salva la mappa originale
2. **Solo lettura all'inizio:** non toccare nulla finché non capisci cosa fa
3. **Contatto ON, motore OFF:** per diagnostica base non serve avviare il motore
4. **Non interrompere il collegamento** durante una scrittura ECU (rischio brick)
5. **Usa cavi di qualità:** un cavo scadente può dare letture errate o bloccare la comunicazione
6. **Attenzione alla batteria:** sessioni lunghe con contatto ON scaricano la batteria — tieni un caricabatterie disponibile

---

## Risorse

- **TuneECU:** tunecu.eu (download + forum)
- **Forum KTM Italia:** ktm-forum.it
- **Reddit:** r/KTM (inglese, molto attivo)
- **YouTube:** cerca "TuneECU KTM 890" per tutorial video
- **GitHub:** cerca "KTM CAN bus" per progetti open source
