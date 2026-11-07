---
tipo: piano-tecnico
stato: SOFTWARE PRONTO (in attesa cavo)
ecu: Bosch ME17.9.21 (Infineon TriCore TC1724)
aggiornato: 2026-11-07
---

# Reverse Engineering ECU — KTM 890 Duke 2021

tags: #diagnostica #reverse-engineering #uds #rea #mappatura

> Tre obiettivi: **leggere tutto** quello che la centralina espone, **togliere gli errori**
> (e la spia ASSISTENZA dopo i tagliandi fatti in casa), e in prospettiva **mapparla**.
> Questa nota dice cosa è fattibile, con quali strumenti, e cosa è già pronto nel software.

---

## In breve

| Obiettivo | Fattibile con il cavo da ~€45? | Stato |
|-----------|-------------------------------|-------|
| Leggere identificazione ECU, codici errore, dati live | ✅ Sì | Software pronto: `diag_tool` |
| Scoprire tutti gli identificativi (DID) che la ECU espone | ✅ Sì | Software pronto: `diag_tool scan-dids` |
| Cancellare i codici errore | ✅ Sì (servizi standard OBD/UDS) | Software pronto: `diag_tool clear-dtc` |
| Reset spia **ASSISTENZA** | ➖ Probabilmente non serve | Si fa dal menu nascosto del cruscotto ([[Reset Spia Assistenza KTM 890]], Opzione 0); il cavo è il piano B |
| Mappatura (leggere/scrivere la mappa) | ❌ No | Serve uno strumento professionale; prima va chiarita la questione A2 |

**Su REA:** è utile per analizzare un *programma* di diagnosi (Windows o Android), non la
centralina. Il firmware della ECU è per processore TriCore, che REA 6.8.0 non sa decompilare
(vedi [[#Dove serve davvero REA]]).

---

## Fatti verificati (novembre 2026)

| Fatto | Fonte |
|-------|-------|
| La ECU della 890 Duke è una **Bosch ME17.9.21** | Scheda tuning iTunesystem (890 Duke GP) |
| Il processore è un **Infineon TriCore TC1724** | Note di rilascio Alientech K-Suite 4.02: "BOSCH ME17.9.21 TC1724 supported in OBD" |
| Lettura/scrittura via OBD possibile solo con strumenti professionali (Alientech KESS3, Autotuner) | Alientech, Autotuner |
| Tester con **service reset** che dichiara la 890 Duke: **Duonix Bike-Scan 2 Pro** (~€449) | Touratech |
| **Healtech FI Cleaner**: cancella errori iniezione, dichiara 890 Duke 2020-2022 (non fa service reset) | 2wheelhq / Healtech |
| Supporto **TuneECU** per la 890: **non confermato** da nessuna fonte | Ricerca senza riscontri |
| Intervalli ufficiali KTM: primo tagliando a 1.000 km, poi ogni **15.000 km / 12 mesi** | PDF "Service Times KTM Street" (verifica la riga della tua moto) |

> Nota: un intervallo di 12 mesi spiega perché la spia può accendersi anche a pochi km:
> la moto aveva ~5.500 km ma poteva essere scaduto il tempo dall'ultimo tagliando registrato.

### Correzioni alle note precedenti
- [[OBD2 Setup KTM]] dice prima che TuneECU **non** supporta la 890 e poi che la **supporta**: nessuna delle due è verificata. Trattalo come non supportato finché non lo provi.
- [[Reset Spia Assistenza KTM 890]]: MotoScan è nato per BMW e il supporto KTM 890 non è verificato; idem KTMFlash/TunerPro. Un indizio (riferito a BMW) dice che gli ELM327 non riescono a inviare i messaggi lunghi che servono per il service reset.
- [[Roadmap Zero-Cost]]: "reset spia via comando custom replicando MotoScan" presuppone di conoscere il comando, che **non** conosciamo: va scoperto (Obiettivo 2).

---

## Obiettivo 1 — Leggere tutti i dettagli

Hardware: adattatore Euro5 6-pin → OBD2 + ELM327 (vedi [[Lista Acquisti Diagnostica]]).

### Il giorno che arriva il cavo

```powershell
cd "C:\KTM DUKE 890\04 - Diagnostica\scripts\ktm-cockpit"
.\.venv\Scripts\pip install -r requirements.txt     # aggiunge pyserial-asyncio

# quadro ON, motore SPENTO, ELM327 abbinato (es. COM7)
python -m app.diag_tool --target COM7 ecu          # 1. quali centraline rispondono
python -m app.diag_tool --target COM7 info         # 2. VIN, CalID, SW/HW, verdetto A2
python -m app.diag_tool --target COM7 dtc          # 3. tutti i codici errore
python -m app.diag_tool --target COM7 scan-dids --range F100-F1FF   # 4. identificazione completa
```

Ogni comando salva un report `.md` + `.json` in `04 - Diagnostica/Letture ECU/`, consultabile da Obsidian.
Se l'ELM327 non risponde prova `--baud 115200` (alcuni USB) o `--baud 9600`.

### Scansione progressiva dei DID (il vero "reverse engineering" della ECU)
La ECU risponde solo agli identificativi che conosce: la scansione li trova da sola.
Velocità stimata ~5-10 DID al secondo.

| Passo | Intervallo | Durata | Cosa cerchiamo |
|-------|-----------|--------|----------------|
| 1 | `F100-F1FF` | ~30-60 s | Identificazione standard ISO 14229 |
| 2 | `F000-F0FF` | ~30-60 s | Dati di sistema |
| 3 | `0100-0FFF` | ~10 min | DID costruttore (KTM/Bosch) |
| 4 | `1000-EFFF` | ore | Solo se i passi 1-3 rendono — lasciala girare con caricabatterie collegato |

Usa `--header` per le altre centraline trovate con `ecu` (es. ABS, cruscotto). I DID che rispondono
`securityAccessDenied` esistono ma sono protetti: li annotiamo e basta.

---

## Obiettivo 2 — Togliere gli errori e la spia ASSISTENZA

### Codici errore — pronto
```powershell
python -m app.diag_tool --target COM7 clear-dtc
```
Legge i codici, mostra cosa sta per cancellare, chiede di scrivere `CANCELLA`, invia
OBD Mode 04 + UDS 0x14, rilegge e salva il report prima/dopo.
- Cancellare non ripara: se il guasto c'è ancora la spia torna.
- Vengono azzerati anche i readiness monitor Euro5 (si ripristinano guidando).

### Spia ASSISTENZA — da scoprire
Non è un codice errore: è un contatore che KTM azzera con una procedura proprietaria,
probabilmente sul cruscotto TFT o sulla ECU, spesso protetta da *security access* (0x27).
**Non invio comandi di scrittura "a tentativi"**: un DID sbagliato può alterare la configurazione.

La strada di reverse engineering pulita, sulla tua moto:
1. **Dal cruscotto, prima di tutto**: più proprietari 790/890 riportano un menu service nascosto nel TFT (Settings evidenziato + ▲▼ per 5 s, salvataggio tenendo premuto SET). Procedura completa nell'Opzione 0 di [[Reset Spia Assistenza KTM 890]]. I passi seguenti servono solo se non funziona.
2. **`diag_tool ecu`**: trova l'indirizzo del cruscotto e delle altre centraline.
3. **Osserva chi lo sa fare**: con la CANable collegata ([[Lista Acquisti Diagnostica]] fase 2) registra il bus mentre un tester o l'officina esegue il reset:
   ```powershell
   python -m app.can_logger --interface slcan --channel COM8 --only-diag
   ```
   Il log mostra la sequenza esatta (sessione, eventuale security access, scrittura o routine).
4. **Se c'è security access** con chiave che cambia ogni volta (seed/key), il log da solo non basta:
   serve l'algoritmo della chiave, ed è qui che REA può aiutare (sezione sotto).
5. **Alternativa pragmatica**: reset in officina (€20-50) la prima volta, registrando il traffico se te lo lasciano fare.

---

## Obiettivo 3 — Mappatura

### Prima di tutto: la questione A2
In [[Fase A - UDS Read-Only]] è annotato che il libretto riporta "depotenziata" ma la moto supera i 200 km/h.
Va chiarito **prima** di qualsiasi mappatura: con libretto A2 la moto deve restare a 35 kW, e una
moto più potente di quanto riportato sul libretto è un problema con assicurazione e controlli.
Il comando `info` legge il Calibration ID per aiutarti a capirlo.

### Aspetti legali
- Una ECU modificata su una moto omologata Euro5 non è conforme per la strada (modifica delle caratteristiche costruttive, art. 78 CdS) e l'assicurazione può rivalersi in caso di sinistro. In pista è un altro discorso.
- Lo scarico **Arrow omologato** con DB killer è legale anche senza rimappatura; una mappa dedicata è un'ottimizzazione, non un obbligo.

### Percorso tecnico realistico
1. **Backup completo**: un centro tuning con KESS3 o Autotuner legge la ME17.9.21 via OBD. Fatti consegnare il file `.bin` originale e conservalo nel vault (fuori da git se pesante).
2. **Analisi**: posso aiutarti sul dump con **Ghidra** (gratuito, ha il processore TriCore) per il codice e con script Python per individuare le tabelle (mappe 2D/3D). Gli strumenti dedicati alle mappe (es. WinOLS) sono a pagamento.
3. **Scrittura**: solo con lo strumento professionale, che ricalcola i checksum. Mai con l'ELM327: rischio di bloccare la centralina.
4. Spesso costa meno una mappa già pronta da un preparatore (flash per posta) che attrezzarsi da soli.

---

## Dove serve davvero REA

REA (installato nel repo, vedi `.claude/skills/reverse-engineer-anything`) analizza **programmi**:
eseguibili Windows, .NET, app Android, app Electron.

| Uso | Serve? |
|-----|--------|
| Analizzare un software di diagnosi KTM che possiedi legalmente, per capire la sequenza del reset service o l'algoritmo della chiave | ✅ È il caso d'uso giusto. In UE è consentito solo per l'interoperabilità (Direttiva 2009/24/CE, art. 6) e limitato a quello |
| Analizzare il dump della ECU (TriCore) | ❌ REA 6.8.0 decompila firmware "nudi" solo per x86, x86-64, ARM, ARM64, 6502 e 68k. Si usa Ghidra direttamente |
| Analizzare il traffico CAN o le risposte UDS | ❌ Non sono programmi: li analizziamo con Python |

Per usarlo sul tuo PC: `npx rea-agents setup`, e per i programmi nativi Ghidra 12.1.x con
`GHIDRA_INSTALL_DIR` impostato. Per le app Android serve anche il JAR di jadx-headless-mcp.

---

## Cosa è stato provato e cosa no

- ✅ Provato sul simulator: `ecu`, `info`, `dtc`, `clear-dtc` (con e senza conferma), `scan-dids`, blocco delle scritture in `raw`, `can_logger` su bus virtuale, server web.
- ❓ Da verificare sulla moto: che la ECU risponda su `7E0` a 500 kbit/s via ELM327, quali DID proprietari esistono, se la cancellazione UDS richiede una sessione estesa.

---

## Fonti

- [iTunesystem — KTM 890 Duke GP, ECU Bosch ME17.9.21](https://itunesystem.file-service.com/tuning-specs/ktm/890/2023/890-duke-gp-115hp)
- [Alientech K-Suite 4.02 — ME17.9.21 TC1724 in OBD](https://tuning-shop.com/de/ueber-uns/nachrichten/alientech-news-update-k-suite-release-402/)
- [Autotuner — Bosch ME17.9.21](https://www.autotuner.com/pt/blogs/novidades/bosch-me17-9-21-me17-9-21-1)
- [Touratech — Duonix Bike-Scan 2 Pro per KTM Euro5](https://www.touratech.com/nl/duonix-bike-scan-2-pro-diagnostic-device-for-ktm-with-obd-euro5-iso19689-diagnostic-cable.html)
- [Healtech FI Cleaner per KTM](https://2wheelhq.com/collections/healtech/products/healtech-fi-cleaner-tool-for-ktm-models)
- [KTM — Service Times KTM Street (PDF)](https://ktm.com/language-masters/en/service/maintenance/Service%20Times%20KTM%20Street.pdf)
- [REA — guida raw binary (architetture supportate)](https://github.com/morluto/rea/blob/main/docs/raw-binary.md)

---

## Cross-link

- [[Fase A - UDS Read-Only]] · [[Reset Spia Assistenza KTM 890]] · [[Lista Acquisti Diagnostica]]
- [[CAN Bus Telemetry]] · [[Roadmap Zero-Cost]] · [[01 - Moto/Mappature e Riding Modes]]
- Codice: `04 - Diagnostica/scripts/ktm-cockpit/` (`app/diag_tool.py`, `app/can_logger.py`)
