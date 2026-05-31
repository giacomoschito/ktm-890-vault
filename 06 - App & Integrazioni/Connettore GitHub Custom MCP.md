# Connettore GitHub su Claude Pro (Custom MCP)

tags: #github #connettore #mcp #remoto #pro

> Piano Pro → custom connectors disponibili. GitHub si aggiunge come connettore
> personalizzato puntando al server MCP ufficiale di GitHub.

---

## Server MCP ufficiale GitHub

```
https://api.githubcopilot.com/mcp/
```

Repo da gestire: `giacomoschito/ktm-890-vault` (privato)

---

## Procedura (da claude.ai web o app)

1. Apri **claude.ai** → **Settings** (o **Customize**) → **Connectors**
2. Clicca **+** → **Add custom connector**
3. Compila:
   - **Name:** `GitHub`
   - **Remote MCP server URL:** `https://api.githubcopilot.com/mcp/`
4. Clicca **Add**
5. Parte il flusso **OAuth** → accedi a GitHub → **autorizza** l'accesso
   - Se ti fa scegliere i repo, concedi accesso almeno a **ktm-890-vault**
6. Tornato su Claude, il connettore **GitHub** deve risultare attivo

---

## Dopo il collegamento

1. Crea un **Project** "KTM 890 Duke" → incolla le istruzioni da [[Istruzioni Progetto Claude]]
2. Assicurati che il connettore GitHub sia abilitato nel Project
3. Dal telefono: scrivi a Claude → lui committa nel repo → il PC sincronizza

---

## ⚠️ Possibile intoppo (onestà)

Il server MCP di GitHub usa OAuth tramite GitHub App. In alcuni client Claude
questo flusso OAuth a volte **non si completa** (problema noto, in beta).

**Se succede:**
- Annota l'errore esatto che vedi
- Verifichiamo se serve passare da "Advanced settings" (OAuth Client ID/Secret di
  una GitHub OAuth App dedicata) oppure un approccio alternativo
- In ultima istanza resta sempre attivo il fallback **[[Inbox Google Drive]]** (già funzionante)

---

## Sicurezza

- Autorizza l'accesso **solo** al repo `ktm-890-vault` se l'opzione è disponibile
- Il connettore gira dal cloud di Anthropic verso il server GitHub (richiede HTTPS)
- Puoi revocare l'accesso in qualsiasi momento da GitHub → Settings → Applications

---

## Fonti
- [Get started with custom connectors (remote MCP) — Claude Help](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [GitHub official MCP Server](https://github.com/github/github-mcp-server)
