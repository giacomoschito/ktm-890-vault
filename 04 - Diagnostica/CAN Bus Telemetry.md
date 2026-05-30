# CAN Bus Telemetry — KTM 890 Duke (Reverse Engineering)

tags: #diagnostica #can-bus #telemetria #avanzato

> La strada avanzata: leggere direttamente il bus CAN per avere TUTTI i dati,
> non solo quelli esposti dall'OBD2 standard. Questa è la base per la dashboard custom.

---

## Perché Questa Strada

L'OBD2 standard (via ELM327) dà solo i parametri "obbligatori" Euro5: RPM, gas, temperatura, velocità, tensione. KTM **non** espone il resto via PID standard.

Ma quei dati **viaggiano comunque** sul bus CAN della moto. Sniffando il bus si leggono direttamente — la community li ha già parzialmente decodificati.

---

## Messaggi CAN Decodificati dalla Community (790/890)

> ⚠️ Questi ID provengono da reverse engineering di utenti sul forum 790dukeforum.
> Vanno **verificati sulla tua moto specifica** — possono variare per anno/firmware.
> Li usiamo come punto di partenza, non come verità assoluta.

| Dato | ID (hex) | ID (dec) | Byte | Note |
|------|----------|----------|------|------|
| Posizione gas (TPS) | 0x120 | 288 | byte 3 | Throttle position |
| Marcia + frizione | 0x129 | 297 | byte 1 | Gear & clutch position |
| Forza freno anteriore | 0x290 | 656 | byte 1-2 | Front brake force |
| Forza freno posteriore | 0x12B | 299 | byte 3-4 | Rear brake force |
| Velocità | da identificare | — | D0, D1 | Formula: `((D0*256)+D1)/16` |

> Ci sono altri ID ancora da mappare (RPM, temperatura, angolo di piega se presente,
> stato TC/ABS). Parte del divertimento è scoprirli noi loggando il bus.

---

## 🎁 Decoder Pronto: libreria `ktm-can` (clonata nel vault)

Esiste già una **libreria Python che decodifica i messaggi CAN KTM**: [blalor/ktm-can](https://github.com/blalor/ktm-can).
Clonata in `07 - Tools & Repos/ktm-can/`. Decoder originale di Dan Plastina (reverse engineering su SuperDuke 1290 / 690 Enduro R).

### Messaggi decodificati dalla libreria

| CAN ID | Frequenza | Dati forniti |
|--------|-----------|--------------|
| `0x120` | 20 ms | **RPM motore**, posizione gas, kill switch, mappa gas |
| `0x129` | 20 ms | **Marcia inserita**, interruttore frizione |
| `0x12A` | 50 ms | Mappa gas richiesta, stato gas |
| `0x12B` | 10 ms | **Velocità ruota ant/post, angolo di piega (lean), inclinazione** |
| `0x290` | 10 ms | **Pressione freno anteriore** |
| `0x450` | 50 ms | Pulsante traction control |

> ⚠️ Questi valori sono confermati su **690 Enduro R / SuperDuke 1290**.
> La 890 condivide molto dell'architettura ma gli ID **vanno verificati** sulla tua moto.
> La libreria è la nostra base: la testiamo, e dove i dati non tornano li ricalibriamo.

### Come la useremo
```python
# La libreria fa il lavoro pesante di parsing
from ktm_can import decoder
# Leggiamo i frame con python-can e li passiamo al decoder
# → otteniamo RPM, marcia, lean angle, ecc. in valori leggibili
```

> Il codice del decoder è in `07 - Tools & Repos/ktm-can/src/ktm_can/decoder.py`.
> I test in `tests/` documentano la struttura esatta dei messaggi.

---

## Hardware Necessario per il CAN Sniffing

Un ELM327 economico **non basta** per sniffare tutto il bus: i cloni lenti perdono frame.
Servono interfacce CAN vere e proprie:

### Opzione A — OBDLink MX+ (consigliata, plug & play)
- Interfaccia OBD2 Bluetooth **veloce**, gestisce il monitor CAN completo
- Provata dalla community 790/890 con RaceChrono per telemetria pista
- Costo: ~€60-80
- Pro: affidabile, fa anche OBD2 standard, app pronte (RaceChrono)
- Contro: più costosa, meno "hacking puro"

### Opzione B — CANable / Arduino + MCP2515 (DIY, massimo apprendimento)
- Interfaccia CAN USB economica (CANable ~€20-30) o Arduino + modulo MCP2515 (~€15)
- Si usa con Python (`python-can` + driver SLCAN)
- Costo: ~€15-30
- Pro: economico, controllo totale, impari davvero come funziona il CAN
- Contro: più fiddly, devi configurare driver e cablaggio

### In entrambi i casi serve sempre
- L'adattatore **KTM 6-pin → OBD2** (quello da €3.44) per l'aggancio fisico

---

## ⚠️ Verifica Compatibilità Adattatore 790/890

L'adattatore economico spesso elenca "KTM 125/200/690/990/1190" ma **non** sempre 790/890.
La 790/890 è Euro5 e il pinout potrebbe differire.

**Prima di comprare:** cerca un adattatore che elenchi **esplicitamente "790 / 890" o "Euro5"**.
Cerca su AliExpress/Amazon: `"KTM 790 890 OBD2 adapter Euro5"`.

La community conferma che sulla 890R il connettore 6-pin → OBD2 funziona e supporta K-Line + CAN-Bus.

---

## Stack Software per il CAN Custom

```python
import can          # pip install python-can

# Configurazione bus (esempio per interfaccia SLCAN/CANable)
bus = can.interface.Bus(
    bustype='slcan',
    channel='COM4',      # la porta del tuo adattatore CAN
    bitrate=500000       # KTM CAN gira a 500 kbps
)

# Sniffing: leggi tutti i frame e stampali
for msg in bus:
    print(f"ID: {hex(msg.arbitration_id)}  Data: {msg.data.hex()}")
```

Da qui costruiamo il decoder che mappa ogni ID al dato leggibile.

---

## Roadmap CAN Sniffing

1. **Fase 1** — Hardware: adattatore 6-pin (verificato 790/890) + interfaccia CAN
2. **Fase 2** — Logging grezzo: cattura tutti i frame mentre guidi (a moto ferma, su cavalletto, vari regimi)
3. **Fase 3** — Decode: confronta i dati grezzi con gli ID noti della community, identifica i tuoi
4. **Fase 4** — Decoder Python: trasforma i frame in dati leggibili (RPM, marcia, temp...)
5. **Fase 5** — Dashboard live + log su Obsidian / CSV
6. **Fase 6** — Grafana / dashboard web scalabile

---

## Sicurezza CAN Bus

- **Solo lettura (sniffing):** zero rischi, ascolti soltanto il traffico
- **NON inviare frame** sul bus finché non sai esattamente cosa fai (un frame sbagliato può confondere le centraline)
- Lavora a moto ferma su cavalletto per le prime sessioni di logging
- Tieni un caricabatterie a portata (sessioni lunghe a contatto ON scaricano la batteria)

---

## Fonti Community

- [ODB2/CANbus data for the 890R | 790 Duke Forum](https://www.790dukeforum.com/threads/odb2-canbus-data-for-the-890r-gear-front-brake-force-etc.4303/)
- [790 Duke CAN BUS Mapping | 790 Duke Forum](https://www.790dukeforum.com/threads/790-duke-can-bus-mapping.4995/)
- [KTM 890 Duke R - OBD2 Data Pull for Track | 790 Duke Forum](https://www.790dukeforum.com/threads/ktm-890-duke-r-obd2-data-pull-for-track.3604/)
