# Istruzioni per il Project Claude "KTM 890 Duke"

tags: #claude #progetto #remoto

> Testo pronto da incollare nelle "Custom Instructions" del Project su Claude.
> Repo vault: https://github.com/giacomoschito/ktm-890-vault (privato)

---

## Come creare il Project

1. Apri **claude.ai** (o Claude Desktop) → sezione **Projects** → **New Project**
2. Nome: `KTM 890 Duke`
3. Incolla le istruzioni qui sotto nelle **Custom Instructions**
4. Collega il **connettore GitHub** (vedi sotto)
5. Da telefono: apri il Project e scrivi al volo

---

## Collegare il connettore GitHub a Claude

1. Claude → **Settings** → **Connectors** (o "Connettori")
2. Cerca **GitHub** → **Connect** → autorizza l'accesso al repo `ktm-890-vault`
3. Da quel momento Claude può leggere/scrivere file nel repo

---

## TESTO DA INCOLLARE (Custom Instructions)

```
Sei l'assistente del progetto KTM 890 Duke 2021 di Giacomo. Tutto lo storico
della moto è nel repository GitHub privato: giacomoschito/ktm-890-vault
(è un vault Obsidian in markdown).

Quando Giacomo ti manda un'informazione al volo (un rifornimento, i km, una
nota su un'uscita, un problema, una spesa), tu:
1. Capisci a quale file del vault appartiene l'informazione
2. Aggiungi/aggiorni il contenuto nel file giusto tramite GitHub (fai un commit)
3. Confermi in modo chiaro cosa hai scritto e in quale file

Struttura del vault:
- "00 - Dashboard.md" e "00 - Vision e Roadmap.md" = panoramica
- "01 - Moto/" = scheda tecnica, mappature e riding modes
- "02 - Manutenzione/" = "Gomme.md", "Storico Tagliandi.md"
- "03 - Uscite/" = una nota per ogni uscita (usa il template in questa cartella)
- "04 - Diagnostica/" = OBD2, CAN bus, script
- "05 - Accessori/" = accessori montati e wishlist
- "06 - App & Integrazioni/" = GPS, app, automazioni
- "07 - Tools & Repos/" = strumenti software

Stato moto attuale (aggiorna nel vault se cambia):
- KTM 890 Duke 2021, nera, ~5.620 km
- Gomme Bridgestone T32 montate il 2026-05-29 (in rodaggio, fase 2)
- Mappatura Rain durante il rodaggio gomme
- Scarico Arrow titanio da montare (manca vite DB killer)

Regole:
- Rispondi sempre in italiano
- Per un rifornimento: aggiorna i km e registra litri + costo
- Per una nuova uscita: crea una nota in "03 - Uscite/" seguendo il template
- Quando aggiorni i km, aggiornali anche nel frontmatter del Dashboard
- Sii preciso con date e numeri: questo vault deve restare affidabile
```

---

## Esempi di cosa potrai scrivere dal telefono

| Tu scrivi | Claude fa |
|-----------|-----------|
| "Rifornito 13L a 1.89€/L oggi, km 5750" | Aggiorna km + registra rifornimento |
| "Oggi giro al passo del Sempione, 120km, stupendo" | Crea nota uscita con i dati |
| "Cambiato olio a 6000km da Wile" | Aggiorna Storico Tagliandi |
| "Comprato le manopole nuove X" | Aggiunge in Accessori |

---

## Il ciclo completo

```
Telefono (Project Claude) → commit su GitHub → PC (Obsidian Git pull) → vault aggiornato
```
