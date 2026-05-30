# Claude & Automazioni — Integrazione con il Vault

tags: #claude #automazioni #tools

---

## Come Usare Claude per Questo Vault

### Claude Desktop (quello che stai usando ora)

**Best practices:**
- Apri sempre questo vault come working directory
- Chiedi a Claude di aggiornare i file direttamente
- Usa frasi come: "aggiorna i km gomme a 1200" → Claude modifica Gomme.md
- Chiedi analisi: "quando devo cambiare le gomme basandoti sul mio utilizzo?"

### Comandi Utili da Darmi

```
"Registra uscita di oggi: 3 km commuting, mappatura Street, meteo sole"
"Aggiorna km moto a [X]"
"Aggiungi spesa manutenzione: [tipo] €[importo] il [data]"
"Analizza quando devo fare il prossimo tagliando"
"Mostrami tutte le uscite del mese scorso"
"Calcola l'usura attuale delle gomme"
```

---

## Plugin Obsidian Consigliati

### Essenziali

| Plugin | Funzione | Install |
|--------|----------|---------|
| **Dataview** | Query sui dati del vault (usa le tabelle nel Dashboard) | Community plugins |
| **Templater** | Template avanzati per uscite/manutenzioni | Community plugins |
| **Calendar** | Vista calendario delle uscite | Community plugins |
| **Charts** | Grafici consumo, km, usura | Community plugins |

### Nice to Have

| Plugin | Funzione |
|--------|----------|
| **Natural Language Dates** | Scrivi "ieri" invece di date ISO |
| **QuickAdd** | Aggiunta rapida di uscite da command palette |
| **Leaflet** | Visualizza mappe GPX dentro Obsidian |
| **Map View** | Mappa interattiva delle uscite |

### Come Installare Plugin Community
1. Settings → Community plugins → Browse
2. Cerca il nome del plugin
3. Install → Enable

---

## Automazioni Future

### Script Python — Aggiornamento Automatico Km
```python
# Idea: scrape o import da Strava/Rever API
# → aggiorna automaticamente km nel vault
import requests
import re

def update_km_in_vault(km_percorsi, vault_path):
    """Aggiorna i km nelle note Obsidian"""
    # ... da sviluppare
    pass
```

### Node-RED Flow — OBD2 → Obsidian
```
[OBD2 Bluetooth] → [Node-RED] → [File Obsidian] → [Dashboard]
```

### Python + Grafana
```python
# Legge tutti i log uscite dal vault
# Calcola statistiche aggregate
# Alimenta dashboard Grafana
```

---

## MCP Servers per Claude Desktop

I **Model Context Protocol (MCP)** servers espandono le capacità di Claude Desktop. Ecco quelli rilevanti per questo progetto:

### Già Configurati
- **File System MCP:** Legge/scrive file nel vault (quello che usiamo ora)
- **Google Drive MCP:** Accesso a file Google

### Da Considerare

| MCP Server | Funzione | Utilità per Moto |
|------------|----------|-----------------|
| **Strava MCP** | Accesso dati Strava | Import automatico percorsi |
| **Google Calendar MCP** | Gestione calendar | Promemoria tagliandi |
| **Weather MCP** | Dati meteo | Log automatico meteo uscite |
| **SQLite MCP** | Database locale | Storico strutturato |

### Come Installare MCP Servers
```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\KTM DUKE 890"]
    }
  }
}
```

---

## Progetto Scalabile — App KTM Tracker

### Vision
Una web app che qualsiasi motociclista può usare per:
- Tracciare la propria moto
- Monitorare manutenzioni
- Log percorsi con statistiche
- Diagnostica via OBD2
- Dashboard personalizzata

### Stack Tecnico Proposto
```
Frontend: Next.js + TailwindCSS (Vercel deploy)
Backend: Supabase (PostgreSQL + Auth)
Mobile: React Native o PWA
OBD2: WebBluetooth API
Mappe: Mapbox o Leaflet
```

### Roadmap Possibile
1. **Fase 1:** Web app semplice — log uscite e manutenzioni
2. **Fase 2:** Connessione OBD2 via browser/mobile
3. **Fase 3:** Community — condivisione percorsi
4. **Fase 4:** App mobile nativa

> Questo vault Obsidian è il prototipo/proof of concept dell'app!
