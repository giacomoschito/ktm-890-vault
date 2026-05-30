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

## 🛠️ RUNBOOK — Path A GitHub (scelto)

### ✅ Fatto da Claude Code (locale)
- [x] `git init -b main` nel vault
- [x] Identità git impostata (Giacomo Schito · giacomoschito99@gmail.com)
- [x] `.gitignore` (esclude workspace Obsidian, repo-tool, file sistema)
- [x] `.gitattributes` (normalizza fine-riga PC/mobile)
- [x] Primo commit (`c60a376`, 30 file)

### 🔐 Step che fai TU (autenticazione — una volta sola)
In un terminale (PowerShell o cmd), dopo che `gh` è installato:
```
gh auth login
```
Rispondi alle domande:
1. `GitHub.com`
2. `HTTPS`
3. Authenticate Git with your GitHub credentials → `Yes`
4. `Login with a web browser`
5. Copia il codice mostrato, apri il browser, incollalo, autorizza

### 🚀 Poi Claude crea il repo e pusha
```
gh repo create ktm-890-vault --private --source="C:\KTM DUKE 890" --remote=origin --push
```
→ Repo privato creato su GitHub + vault caricato.

### 🔄 Sync automatico col plugin Obsidian Git
1. Obsidian → Settings → Community plugins → Browse
2. Cerca **"Obsidian Git"** (autore: Vinzent) → Install → Enable
3. Impostazioni plugin:
   - Auto commit-and-sync ogni **10 minuti**
   - Pull on startup → ON
   - Push on commit → ON

### 📱 Accesso da remoto via Claude
1. Su Claude (Desktop o claude.ai), collega il **connettore GitHub**
2. Crea un **Project "KTM 890 Duke"** (istruzioni pronte: [[Istruzioni Progetto Claude]])
3. Da fuori casa: scrivi a Claude → committa la nota sul repo
4. Il PC (Obsidian Git) la scarica al prossimo avvio/sync

### Test finale
- [ ] Dal telefono: "Claude, aggiungi nota: rifornito 13L oggi"
- [ ] Verifica che compaia nel vault sul PC dopo il sync
