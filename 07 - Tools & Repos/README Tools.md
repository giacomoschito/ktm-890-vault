# Tools & Repos — Magazzino Strumenti del Progetto

tags: #tools #repository #software

> Strumenti software, librerie e repository utili al progetto, raccolti qui.

---

## Repository Clonati (in questa cartella)

### ktm-can ⭐ il più importante
- **Cosa è:** Libreria Python che decodifica i messaggi CAN bus delle KTM
- **Percorso:** `07 - Tools & Repos/ktm-can/`
- **Fonte:** [github.com/blalor/ktm-can](https://github.com/blalor/ktm-can)
- **A cosa ci serve:** È il cuore della Fase 2 (CAN sniffing). Decodifica RPM, marcia, angolo di piega, velocità ruote, freni. Vedi [[04 - Diagnostica/CAN Bus Telemetry]]
- **Licenza:** Open source

### awesome-automotive-can-id
- **Cosa è:** Raccolta di CAN ID e payload per varie marche/modelli di veicoli
- **Percorso:** `07 - Tools & Repos/awesome-automotive-can-id/`
- **Fonte:** [github.com/iDoka/awesome-automotive-can-id](https://github.com/iDoka/awesome-automotive-can-id)
- **A cosa ci serve:** Riferimento per il reverse engineering, metodologia e confronto

---

## Software da Installare (non clonabili — vanno scaricati)

### SavvyCAN ⭐ essenziale per il CAN
- **Cosa è:** Tool GUI open source per catturare, analizzare e fare reverse engineering del CAN bus
- **Fonte:** [github.com/collin80/SavvyCAN](https://github.com/collin80/SavvyCAN) · [savvycan.com](https://www.savvycan.com/)
- **A cosa ci serve:** Quando colleghiamo la CANable, SavvyCAN ci mostra graficamente tutti i frame, ci aiuta a identificare quale ID cambia quando muovi il gas/freno/cambio. Lo strumento principe per scoprire gli ID della 890.
- **Come installarlo:** Scarica il binario Windows dalle Release GitHub (NON serve compilare)
- **Licenza:** GPL v3

---

## Librerie Python (già installate sul PC ✓)

| Libreria | Uso | Stato |
|----------|-----|-------|
| `python-can` | Lettura frame CAN grezzi | ✅ Installata |
| `python-obd` | Lettura PID OBD2 standard | ✅ Installata |
| `pyserial` | Comunicazione porta COM | ✅ Installata |
| `rich` | Dashboard nel terminale | ✅ Installata |
| `pandas` | Log e analisi dati | ✅ Installata |

---

## MCP Server per Obsidian (per accesso remoto — da valutare)

> Per rendere il vault raggiungibile da Claude (anche da remoto). Vedi [[06 - App & Integrazioni/Accesso Remoto Vault]]

| MCP Server | Note | Fonte |
|------------|------|-------|
| **Obsidian Local REST API** | Plugin Obsidian con MCP server integrato | [github](https://github.com/coddingtonbear/obsidian-local-rest-api) |
| **MarkusPfundstein/mcp-obsidian** | MCP popolare via REST API | [github](https://github.com/MarkusPfundstein/mcp-obsidian) |
| **obsidian-mcp-server-enhanced** | Pensato per accesso REMOTO da claude.ai via Tailscale | [github](https://github.com/BoweyLou/obsidian-mcp-server-enhanced) |
| **jacksteamdev/obsidian-mcp-tools** | Ricerca semantica + Templater | [github](https://github.com/jacksteamdev/obsidian-mcp-tools) |

---

## Aggiornamento Repo

Per aggiornare i repo clonati all'ultima versione:
```bash
cd "07 - Tools & Repos/ktm-can" && git pull
```
