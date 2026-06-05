# Lista Acquisti — Setup Diagnostica (ELM327 + CAN DIY)

tags: #diagnostica #acquisti

> Percorso scelto: **ELM327 (PID standard + fault codes) + CAN DIY sniffing** con Python.
> Budget totale: ~€20-45 in due fasi. Software PC già pronto al 100% (vedi [[Roadmap Zero-Cost]]).

---

## ⭐ ACQUISTI MINIMI — NON SBAGLIARE

Due pezzi soli, totale **~€20-30**. Funzionano insieme. Compra **entrambi** dallo stesso store se possibile per ridurre spedizione.

### 1. Adattatore Euro5 ISO 19689 6-pin → OBD2

**Cosa cercare nel titolo:** "Euro5" + "6 pin" + "OBD2" + ("KTM" o "790/890" o "ISO 19689").
**Cosa NON comprare:** adattatori che dicono "690/990/1190" senza menzionare Euro5 — è il connettore vecchio, NON entra nella tua 890 2021.

**⭐ Scelta 1 — KDS-online.de** (Germania, negozio specializzato moto, niente dogana UE)
- Link diretto: https://kds-online.de/en/obd-adapter-euro5-for-motorcycle-6-pin-to-obd2-k-line-can-bus.html
- Prezzo: ~€20 + ~€6 spedizione
- Vantaggio: descrizione tecnica chiara, supporta sia K-Line sia CAN, garanzia commerciale UE

**Scelta 2 — Amazon Italia**
- Cerca: https://www.amazon.it/s?k=adattatore+Euro5+OBD2+moto+6+pin
- Verifica nel titolo "Euro5" o "ISO 19689"
- ASIN di riferimento internazionale: **B09GX4PVQ1** (SuperOBD)
- Prezzo: ~€15-22

**Scelta 3 — AliExpress (economica, attesa lunga)**
- Ricerca: https://it.aliexpress.com/w/wholesale-Euro5-motorcycle-OBD2-6-pin-adapter-KTM.html
- Prezzo: ~€7-12
- ATTENZIONE: leggi le recensioni, scegli venditore con >95% feedback e foto reali

---

### 2. ELM327 Bluetooth (per smartphone + PC)

**Cosa cercare:** ELM327 v1.5 con chip **PIC18F25K80** (originale) o marca affidabile.
**Cosa NON comprare:** generici "ELM327 v2.1 mini" da €3 (chip clone, falsi positivi, perdono pacchetti).

**⭐ Scelta consigliata — Vgate iCar Pro BT 4.0**
- Compatibile Android + iOS (BLE), funziona anche su Windows BT
- Chip affidabile, supporta tutti i PID OBD-II + protocolli moto
- Link Amazon.it: https://www.amazon.it/s?k=vgate+iCar+Pro+BT+4.0
- Prezzo: ~€20-28

**Alternativa USB — Vgate vLinker FS USB**
- Per chi vuole solo PC, niente BT
- Link Amazon.it: https://www.amazon.it/s?k=vLinker+FS+USB
- Prezzo: ~€25

**Premium (se vuoi spendere di più) — OBDLink SX USB**
- Gold standard, zero problemi driver, chip vero
- Link: https://www.amazon.it/s?k=OBDLink+SX+USB
- Prezzo: ~€30-35

**Economica — ELM327 USB FTDI** (rischio compatibilità)
- Solo se cerchi sotto i €10 e accetti possibili problemi
- Link AliExpress: https://it.aliexpress.com/w/wholesale-ELM327-USB-FTDI.html
- Prezzo: ~€8-12

---

## 💰 Ricapitolando — Le 3 strade

| Strada | Pezzo 1 | Pezzo 2 | Totale |
|--------|---------|---------|--------|
| **🍗 Economica** | Adattatore AliExpress €10 | ELM327 BT generico €8 | **~€18** |
| **⭐ Consigliata** | Adattatore KDS-online €20 + sped €6 | Vgate iCar Pro BT 4.0 €25 | **~€51** |
| **💥 Sicura** | Adattatore Amazon Euro5 €20 | OBDLink SX USB €35 | **~€55** |

**Decisione personale:** vai sulla **Consigliata**. €30 in più sull'economica ti tolgono ore di frustrazione con cavi che perdono pacchetti.

Vedi anche [[Roadmap Zero-Cost]] per il piano fasi completo.

---

## ⚠️ SCOPERTA CRITICA — La 890 2021 è Euro5

La tua KTM 890 Duke 2021 monta il connettore diagnostico **Euro5 ISO 19689**,
**diverso** dal vecchio 6-pin KTM (690/990/1190).

| Tipo | Per quali moto | Va bene per te? |
|------|----------------|------------------|
| Vecchio 6-pin KTM | 125/200/690/990/1190 (pre-Euro5) | ❌ NO — non entra |
| **Euro5 ISO 19689** | 790/890, Super Duke 2020+, Husqvarna, GasGas | ✅ SÌ — questo |

> L'adattatore da €3.44 trovato all'inizio elencava "690/990/1190" → era quello
> SBAGLIATO. Compra solo adattatori che dicono esplicitamente **"Euro5"** o **"ISO 19689"**.

### Dove si trova il connettore sulla moto
**Lato sinistro della batteria, sotto la sella.** Connettore a 6 pin con tappo in gomma.

### Pinout connettore Euro5 (lato moto)
- CAN High (ISO 15765-4)
- CAN Low (ISO 15765-4)
- K-Line (ISO 9141-2 / 14230-4)
- Ground
- VBAT +12V

---

## FASE 1 — Lettura OBD2 + fault codes (~€20-30)

### Pezzo 1 — Adattatore Euro5 6-pin → OBD2 ⭐ IL PEZZO CHIAVE

| | |
|-|-|
| **A cosa serve** | Converte il connettore Euro5 della moto in una presa OBD2 standard 16 pin. È la base di TUTTO: serve sia per l'ELM327 (Fase 1) sia per il CAN (Fase 2). Supporta CAN-Bus + K-Line. |
| **Prezzo** | €12-25 |

**Dove comprarlo (in ordine di consiglio per l'Italia):**
- 🇪🇺 **KDS-online.de** (Germania, spedizione UE, niente dogana, negozio specializzato moto): [OBD Adapter Euro5 6 Pin to OBD2](https://kds-online.de/en/obd-adapter-euro5-for-motorcycle-6-pin-to-obd2-k-line-can-bus.html)
- 🛒 **Amazon** — SuperOBD Euro5 ISO 19689 (ASIN B09GX4PVQ1): [link Amazon.com](https://www.amazon.com/dp/B09GX4PVQ1) · cerca lo stesso su [Amazon.it "adattatore Euro5 OBD2 moto KTM"](https://www.amazon.it/s?k=adattatore+Euro5+OBD2+moto+KTM)
- 🛒 **AliExpress**: cerca [`Euro5 motorcycle OBD2 6 pin adapter KTM`](https://it.aliexpress.com/w/wholesale-Euro5-motorcycle-OBD2-6-pin-adapter-KTM.html) — verifica "Euro5/ISO 19689" nel titolo

### Pezzo 2 — ELM327 USB (lettura affidabile)

| | |
|-|-|
| **A cosa serve** | Si innesta sulla presa OBD2 e collega al PC via USB. Legge RPM, gas, temperatura, velocità, tensione e soprattutto **legge/cancella i codici errore** (utilissimo per la manutenzione). Lavora con python-obd. |
| **Prezzo** | €10-25 |

**Dove comprarlo:**
- ✅ **Più affidabile in assoluto — OBDLink SX USB** (chip vero, zero problemi driver): cerca [`OBDLink SX USB`](https://www.amazon.it/s?k=OBDLink+SX+USB) (~€25)
- 💰 **Economico — ELM327 USB con chip FTDI** (NON CH340): cerca [`ELM327 USB FTDI`](https://www.amazon.it/s?k=ELM327+USB+FTDI) o su [AliExpress](https://it.aliexpress.com/w/wholesale-ELM327-USB-FTDI.html) (~€10)

> Per il PC l'OBDLink SX è la scelta sicura: molti ELM327 USB cinesi danno timeout.
> €15 in più ti tolgono ore di frustrazione con i driver.

---

## FASE 2 — CAN bus sniffing DIY (~€25-35)

### Pezzo 3 — Interfaccia CAN USB (CANable)

| | |
|-|-|
| **A cosa serve** | Legge **direttamente il bus CAN** della moto = TUTTI i dati che viaggiano (marcia, frizione, forza freni, gas, e altro da scoprire), non solo i PID OBD2 standard. È il cuore della dashboard custom. Lavora con python-can (già installato). |
| **Prezzo** | €15-30 |

**Dove comprarlo:**
- ✅ **Amazon — DSD TECH SH-C30A** (basato su CANable, con supporto + garanzia 1 anno, firmware candlelight/SLCAN): [link Amazon.com (ASIN B0BQ5G3KLR)](https://www.amazon.com/dp/B0BQ5G3KLR) · cerca su [Amazon.it "DSD TECH USB CAN"](https://www.amazon.it/s?k=DSD+TECH+USB+CAN)
- 💰 **AliExpress — CANable 2.0 Type-C** (STM32G431, CAN-FD/SLCAN): [item link](https://www.aliexpress.com/item/1005006842262016.html) (~€15-20)

### Pezzo 4 — Breakout OBD2 (per agganciare il CAN)

| | |
|-|-|
| **A cosa serve** | Spinotto OBD2 maschio con fili liberi: si infila nella presa OBD2 (dopo l'adattatore Euro5) e ti dà accesso ai fili CAN-H, CAN-L e GND da collegare ai morsetti della CANable. Tutto reversibile, niente tagli sulla moto. |
| **Prezzo** | €6-10 |

**Dove comprarlo:**
- 🛒 cerca [`connettore OBD2 maschio cavo pigtail`](https://www.amazon.it/s?k=connettore+OBD2+maschio+cavo+pigtail) su Amazon.it
- 🛒 o [`OBD2 male plug pigtail 16 pin`](https://it.aliexpress.com/w/wholesale-OBD2-male-plug-pigtail-16-pin.html) su AliExpress

---

## Schema Cablaggio CAN (Fase 2)

```
Moto (Euro5 6pin) → [Adattatore Euro5] → presa OBD2 → [Breakout OBD2] → fili
                                                                         │
   OBD2 pin 6  (CAN High) ──────────────────────────────────────────────► CANable CAN-H
   OBD2 pin 14 (CAN Low)  ──────────────────────────────────────────────► CANable CAN-L
   OBD2 pin 4  (Ground)   ──────────────────────────────────────────────► CANable GND
                                                                         │
                                                                  [CANable] ─USB─► PC
                                                                                   python-can
```

| Pin OBD2 | Segnale | Al CANable |
|----------|---------|------------|
| 6 | CAN High | CAN-H |
| 14 | CAN Low | CAN-L |
| 4 | Ground | GND |

- **Bitrate KTM:** 500 kbps (500000)
- **Terminazione:** il bus moto è già terminato → jumper 120Ω della CANable **OFF**
- **Solo lettura:** non inviare frame finché non sai cosa fai

---

## Riepilogo Budget

| Fase | Pezzo | Prezzo |
|------|-------|--------|
| 1 | Adattatore Euro5 6pin→OBD2 | €12-25 |
| 1 | ELM327 USB (o OBDLink SX) | €10-25 |
| 2 | CANable (DSD TECH SH-C30A) | €15-30 |
| 2 | Breakout OBD2 | €6-10 |
| | **TOTALE** | **~€45-90** |

> Versione economica (FTDI + CANable AliExpress): ~€45
> Versione affidabile (OBDLink SX + DSD TECH Amazon): ~€75-90

---

## Software PC (già fatto ✓)

- [x] Python 3.14.3 · pyserial · python-obd · python-can 4.6.1 · rich · pandas · VS Code 1.122.1

---

## Checklist

### Prima di comprare
- [ ] Guardare il connettore sotto la sella (lato sx batteria) e fotografarlo
- [ ] Confermare che è il 6-pin Euro5

### Fase 1
- [ ] Adattatore Euro5 (verificato "Euro5/ISO 19689")
- [ ] ELM327 USB / OBDLink SX
- [ ] Driver installati + primo collegamento + lettura fault codes

### Fase 2
- [ ] CANable + breakout OBD2
- [ ] Cablaggio CAN-H / CAN-L / GND
- [ ] Primo logging frame → decode → [[CAN Bus Telemetry]]
