# Accesso Remoto al Vault via Claude

tags: #claude #remoto #mcp #architettura

> Obiettivo: scrivere a Claude da fuori casa → lui aggiunge/estrae info dal vault.

---

## La Realtà dell'Architettura (onestà tecnica)

Ci sono **tre "Claude" diversi** in gioco:

| Claude | Dove gira | Accesso al vault |
|--------|-----------|------------------|
| **Claude Code** (CLI) | Sul tuo PC, terminale | Diretto ai file (quello che usiamo ora) |
| **Claude Desktop** (app) | Sul tuo PC, GUI | Via MCP server configurati |
| **Claude mobile / claude.ai** | Cloud (telefono/web) | Solo se il vault è raggiungibile da internet |

Il punto critico: **da fuori casa**, il vault (che è sul PC) deve essere raggiungibile.
Due strade realistiche.

---

## PATH A — GitHub (consigliato: robusto e sicuro)

```
Vault → repo privato GitHub
  ├── PC: Obsidian Git plugin sincronizza automaticamente
  └── Da fuori: scrivi a Claude (con connettore GitHub) → committa la nota
              → il PC la scarica quando è acceso
```

**Pro:**
- Funziona anche con **PC spento** (la nota resta su GitHub, il PC la prende dopo)
- **Cronologia versioni** completa (ogni modifica tracciata)
- **Gratuito**, sicuro (repo privato)
- Gran parte la posso configurare io adesso (git init, struttura)

**Contro:**
- Serve un account GitHub
- La cattura passa da GitHub (piccola indirezione)

**Sicurezza:** repo **privato**, nessuna esposizione del PC a internet.

---

## PATH B — Obsidian Local REST API + Tailscale (live, avanzato)

```
Obsidian (plugin Local REST API + MCP server)
  └── Tailscale (VPN sicura) → Claude raggiunge il vault in tempo reale
```

**Pro:**
- Accesso **live** diretto al vault (lettura/scrittura in tempo reale)
- Niente indirezione

**Contro:**
- Il **PC deve restare sempre acceso**
- Esposizione di rete (mitigata da Tailscale, ma richiede attenzione)
- Setup più complesso (plugin, certificato, VPN)

**Sicurezza:** Tailscale crea una rete privata cifrata — accettabile, ma più superficie d'attacco del Path A.

---

## Cowork vs Dispatch (la tua domanda)

- **Cowork** (Anthropic): è il modo per **collegare i tuoi tool/connettori e skill** dentro Claude così che lavori in modo integrato. È rilevante: è qui che si "aggancia" il connettore GitHub o Obsidian. Esiste una procedura guidata (`setup-cowork`).
- **Dispatch**: ⚠️ non sono certo a quale prodotto/funzione ti riferisci con questo nome — non risulta tra gli strumenti che vedo. Se hai in mente qualcosa di specifico (un'app, un'estensione), dimmelo e lo verifico, così non ti do informazioni inventate.

**In breve:** per il tuo obiettivo NON è obbligatorio né Cowork né Dispatch. Il cuore è
(1) dove vive il vault + (2) un connettore. Cowork è il "contenitore" comodo per il punto 2.

---

## Il "Progetto" su Claude Desktop / claude.ai

Un **Project** (sia su Desktop che su claude.ai, si sincronizzano) ti dà:
- **Istruzioni personalizzate** permanenti (Claude sa sempre il contesto della moto)
- **Contesto del vault** sempre disponibile
- Accessibile da **telefono** (claude.ai mobile) → da qui scrivi "fuori casa"

Le istruzioni del progetto le preparo io (testo pronto da incollare).

---

## Architettura Consigliata Completa

```
        [Telefono fuori casa]
                │  "Claude, aggiungi: oggi rifornito 13L a 1.89€/L"
                ▼
        [claude.ai Project "KTM 890"]  ──con connettore GitHub──┐
                                                                 ▼
                                                    [repo privato GitHub]
                                                                 │
                                                                 ▼
        [PC a casa: Obsidian + Git plugin] ←── pull automatico ──┘
                │
                ▼
        [Vault aggiornato + Claude Code per analisi pesanti]
```

---

## Checklist Setup (dopo la scelta del path)

### Path A — GitHub
- [ ] Creare account GitHub (se non c'è)
- [ ] `git init` nel vault + repo privato
- [ ] `.gitignore` per escludere file di sistema
- [ ] Installare Obsidian Git plugin (auto-sync)
- [ ] Collegare connettore GitHub a Claude
- [ ] Creare Project "KTM 890" su claude.ai
- [ ] Test: aggiungere una nota dal telefono

### Path B — Live
- [ ] Installare plugin Obsidian Local REST API
- [ ] Installare Tailscale su PC e telefono
- [ ] Configurare MCP server Obsidian
- [ ] Collegare a Claude Desktop
- [ ] Test accesso remoto
