# Pre-Installazione PC — Prima che Arrivi l'Hardware

tags: #diagnostica #setup #pc

> Fai tutto questo ora. Quando arriva il cavo, salti direttamente al primo collegamento.

---

## Step 1 — ⚠️ TuneECU (NON per la 890 Duke)

> TuneECU **non supporta** la KTM 890 Duke che ha una ECU Bosch di nuova generazione.
> TuneECU funziona solo su KTM 690/990/1190 con ECU vecchia.
> **Salta questo step.** Il nostro stack è direttamente Python + ELM327.

---

## Step 2 — Driver FTDI (per il cavo ELM327)

I driver FTDI servono a Windows per riconoscere il chip dentro il tuo ELM327 USB.
Installarli ora evita sorprese quando colleghi il cavo.

### Scarica i Driver

1. Vai su **ftdichip.com**
2. Sezione **Drivers** → **VCP Drivers** (Virtual COM Port)
3. Scarica il pacchetto per **Windows** → `CDM v2.12.xx WHQL Certified.exe`
4. Installa come amministratore

### Verifica Post-Installazione

Dopo l'installazione:
- Apri **Gestione Dispositivi** (tasto destro su Start → Gestione dispositivi)
- Espandi **Porte (COM e LPT)**
- Per ora non vedi nulla di nuovo — è normale (il cavo non è collegato)
- Quando collegherai il cavo ELM327, comparirà qui come `USB Serial Port (COMx)`

---

## Step 3 — Python

### Installa Python 3.12+

1. Vai su **python.org/downloads**
2. Scarica **Python 3.12.x** (o versione più recente)
3. Durante l'installazione: ⚠️ **spunta "Add Python to PATH"** — fondamentale
4. Clicca "Install Now"

### Verifica

Apri **Prompt dei Comandi** (cmd) e scrivi:
```
python --version
```
Deve rispondere con: `Python 3.12.x`

Se non funziona, riavvia il PC e riprova.

---

## Step 4 — Librerie Python

Apri il **Prompt dei Comandi** e installa le librerie una per una:

```cmd
pip install pyserial
pip install python-obd
pip install rich
pip install pandas
```

### A cosa servono

| Libreria | Funzione |
|----------|----------|
| `pyserial` | Comunicazione con la porta COM (il cavo USB) |
| `python-obd` | Legge i dati OBD/ELM327 in modo semplice |
| `rich` | Dashboard colorata nel terminale — bella da vedere |
| `pandas` | Salva i dati in CSV/Excel per analisi future |

---

## Step 5 — VS Code (Editor di Codice)

### Installa VS Code

1. Vai su **code.visualstudio.com**
2. Scarica per Windows → installa
3. Apri VS Code

### Estensioni da Installare

Dentro VS Code, vai sull'icona Extensions (Ctrl+Shift+X) e installa:

| Estensione | Funzione |
|------------|---------|
| **Python** (Microsoft) | Supporto Python completo |
| **Pylance** | Autocompletamento intelligente |

### Apri la Cartella del Progetto

1. File → Open Folder
2. Crea una nuova cartella: `C:\KTM DUKE 890\04 - Diagnostica\scripts\`
3. Aprila in VS Code
4. Sarà la nostra base di lavoro per tutti gli script

---

## Step 6 — Script di Test (da eseguire subito)

Crea il file `C:\KTM DUKE 890\04 - Diagnostica\scripts\test_setup.py` e incolla questo:

```python
# Test installazione librerie — esegui prima del collegamento hardware

import sys

def check_library(name):
    try:
        __import__(name)
        print(f"  OK  {name}")
    except ImportError:
        print(f"  MANCANTE  {name}  → pip install {name}")

print("=== Test Setup Diagnostica KTM ===\n")
print(f"Python: {sys.version}\n")

print("Librerie:")
check_library("serial")      # pyserial
check_library("obd")         # python-obd
check_library("rich")
check_library("pandas")

print("\nSetup completo. Pronto per il collegamento hardware.")
```

Eseguilo con: **tasto destro sul file → Run Python File in Terminal**

Output atteso:
```
=== Test Setup Diagnostica KTM ===

Python: 3.12.x

Librerie:
  OK  serial
  OK  obd
  OK  rich
  OK  pandas

Setup completo. Pronto per il collegamento hardware.
```

Se qualcosa è MANCANTE, riesegui il `pip install` di quella libreria.

---

## Checklist Pre-Installazione

- [x] ~~TuneECU~~ — non supporta 890 Duke, saltato
- [ ] Driver FTDI installati (fare quando arriva il cavo)
- [x] Python 3.14.3 installato ✓
- [x] Librerie installate: pyserial, python-obd, rich, pandas ✓
- [x] VS Code 1.122.1 installato ✓
- [x] Cartella `scripts/` creata ✓
- [x] `test_setup.py` eseguito → 4/4 OK ✓

---

## Quando Arriva il Cavo

Solo a quel punto:
1. Collega ELM327 USB al PC
2. Metti il cavo KTM→OBD2 in mezzo
3. Guarda Gestione Dispositivi → comparirà la porta COM (es. COM3)
4. Configura quella porta in TuneECU (Settings → Communication)
5. Accendi il contatto della moto (motore spento)
6. TuneECU → Connect → benvenuto nella diagnostica

---

## Tempo Stimato per Tutto

| Step | Tempo |
|------|-------|
| TuneECU | 5 min |
| Driver FTDI | 3 min |
| Python | 5 min |
| Librerie pip | 2 min |
| VS Code | 5 min |
| Test script | 2 min |
| **Totale** | **~20 minuti** |
