<div align="center">

# KTM 890 Duke — Digital Garage

**Il gemello digitale di una KTM 890 Duke 2021.**
Storico, manutenzione, diagnostica e telemetria in un unico sistema — basato su Obsidian, Git e Python.

![Obsidian](https://img.shields.io/badge/Obsidian-18181B?style=flat&logo=obsidian&logoColor=A78BFA)
![Python](https://img.shields.io/badge/Python_3.14-18181B?style=flat&logo=python&logoColor=4B8BBE)
![Git](https://img.shields.io/badge/Auto--sync-Git-18181B?style=flat&logo=git&logoColor=F05032)
![CAN bus](https://img.shields.io/badge/CAN_bus-Reverse_Engineering-18181B?style=flat)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

</div>

---

## Cos'è

Un sistema completo per conoscere, mantenere e analizzare una moto in ogni dettaglio.
Nato per una **KTM 890 Duke 2021**, è progettato per essere **scalabile e replicabile** su qualsiasi motocicletta.

Tre principi:

- **Tutto documentato** — ogni tagliando, gomma, uscita e spesa, per sempre e versionato.
- **Diagnostica fai-da-te** — leggere i dati direttamente dalla moto via OBD2 e CAN bus.
- **Open & replicabile** — il vault è il prototipo di un sistema riutilizzabile da chiunque.

---

## Caratteristiche

| Livello | Cosa fa | Stato |
|--------|---------|-------|
| **Storico** | Manutenzione, gomme, accessori, uscite — tracciati e versionati | Attivo |
| **Diagnostica** | Lettura/cancellazione codici errore via OBD2 (ELM327) | In allestimento |
| **Telemetria CAN** | RPM, marcia, angolo di piega, freni — letti dal bus CAN | In allestimento |
| **Dashboard** | Visualizzazione live e storica dei dati (Dataview / Python) | In sviluppo |
| **Manutenzione predittiva** | Avvisi su gomme e tagliandi in base ai km reali | In sviluppo |
| **Sync remoto** | Backup automatico su Git + cattura note da remoto | Attivo |

---

## Struttura del vault

```
.
├── 00 - Dashboard.md            Panoramica con query Dataview
├── 00 - Vision e Roadmap.md     La direzione del progetto
├── 01 - Moto/                   Scheda tecnica, mappature e riding modes
├── 02 - Manutenzione/           Gomme, tagliandi, storico interventi
├── 03 - Uscite/                 Log delle uscite (con template)
├── 04 - Diagnostica/            OBD2, CAN bus, script Python
├── 05 - Accessori/              Accessori montati e wishlist
├── 06 - App & Integrazioni/     GPS, app, automazioni, sync remoto
├── 07 - Tools & Repos/          Strumenti software e librerie
└── Templates/                   Template per uscite e manutenzioni
```

---

## Stack tecnologico

- **Obsidian** + **Dataview** — knowledge base in markdown, query sui dati
- **Git / GitHub** — versionamento e backup automatico (plugin Obsidian Git)
- **Python 3.14** — `python-can`, `python-obd`, `pyserial`, `pandas`, `rich`
- **Hardware** — adattatore Euro5 ISO 19689, ELM327, interfaccia CAN (CANable)

---

## Diagnostica & Telemetria CAN

La 890 Duke usa un connettore **Euro5 ISO 19689** e un bus **CAN a 500 kbps**.
Il progetto sfrutta il reverse engineering della community per decodificare i messaggi:

| CAN ID | Dati |
|--------|------|
| `0x120` | RPM motore, posizione gas |
| `0x129` | Marcia inserita, frizione |
| `0x12B` | Velocità ruote, angolo di piega |
| `0x290` | Pressione freno anteriore |

> Decoder di riferimento: [blalor/ktm-can](https://github.com/blalor/ktm-can) ·
> Analisi: [SavvyCAN](https://github.com/collin80/SavvyCAN)

---

## Roadmap

- [x] Struttura vault e documentazione completa
- [x] Backup automatico e versionamento su Git
- [x] Cattura note da remoto
- [ ] Lettura OBD2 base (codici errore, dati live)
- [ ] Decodifica telemetria CAN della moto
- [ ] Dashboard dati live
- [ ] Manutenzione predittiva con alert
- [ ] Generalizzazione multi-moto

---

## Replicabile

Vuoi farne uno per la tua moto? La struttura è pensata per essere clonata:
adatta la scheda tecnica, i parametri CAN e l'hardware al tuo modello.
Il sistema è agnostico — cambia la moto, non l'impianto.

---

## Disclaimer

Progetto personale e non commerciale, **non affiliato a KTM AG**.
Le operazioni di diagnostica e sul bus CAN sono a proprio rischio: lavorare sempre
in sicurezza e in sola lettura finché non si conosce a fondo il sistema.

---

## Licenza

Distribuito con licenza **MIT**. Vedi [LICENSE](LICENSE).
