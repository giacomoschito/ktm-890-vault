# Inbox Google Drive — Cattura Note da Remoto

tags: #remoto #inbox #google-drive #workflow

> Soluzione per scrivere info da fuori casa e farle archiviare nel vault da Claude.
> Adottata perché il connettore GitHub non è disponibile nell'account Claude.

---

## Il Documento Inbox

- **Nome:** `KTM 890 - Inbox` (Google Doc)
- **Link:** https://docs.google.com/document/d/15px-6dxX5aO-BCr2zbItsLyx3qIZpQPjugUbo017keI/edit
- **File ID:** `15px-6dxX5aO-BCr2zbItsLyx3qIZpQPjugUbo017keI`

> Aggiungilo ai preferiti / home screen del telefono per accesso rapido.

---

## Come Funziona

```
[Telefono, fuori casa]                      [PC, con Claude Code]
 Apri "KTM 890 - Inbox" su Google Docs   →   "leggi l'inbox e archivia"
 Scrivi la nota al volo (una per riga)   →   Claude legge da Google Drive
 Salva (automatico)                      →   estrae, archivia nel file giusto
                                         →   committa su GitHub + svuota inbox
```

### Da fuori casa (telefono)
1. Apri l'app **Google Docs** → documento **KTM 890 - Inbox**
2. Scrivi sotto "NOTE DA ARCHIVIARE", una nota per riga
3. Formato libero, esempi:
   - `rifornito 13L a 1.89 euro, km 5750`
   - `giro al passo del Sempione, 120km, mappatura Street, stupendo`
   - `cambiato olio a 6000km da Wile, 85 euro`

### Al PC (con Claude Code)
Scrivi semplicemente: **"leggi l'inbox e archivia"**

Claude:
1. Legge il Google Doc inbox via connettore Drive
2. Capisce a quale file del vault appartiene ogni nota
3. Aggiorna i file giusti (uscite, manutenzione, km, ecc.)
4. Fa commit + push su GitHub
5. Svuota l'inbox (così non si riarchivia due volte)

---

## Perché Questa Soluzione

| Aspetto | Valutazione |
|---------|-------------|
| Connettori speciali richiesti | ❌ Nessuno — usa Google Docs che hai già |
| Funziona dal telefono | ✅ Sì, da qualsiasi device |
| Costo | ✅ Gratis |
| Dipende dal PC acceso | ❌ No (la nota resta su Drive finché non la processi) |
| Verificato | ✅ Loop scrittura+lettura testato il 2026-05-30 |

---

## Limite da Conoscere

Non è "tempo reale": le note restano nell'inbox finché non sei al PC e chiedi a
Claude di archiviarle. È un sistema di **cattura + archiviazione differita**, perfetto
per non perdere informazioni quando sei in giro.

---

## Alternativa Futura

Se un giorno il connettore GitHub diventasse disponibile nel tuo piano Claude,
si potrà avere la scrittura diretta in tempo reale. Per ora l'inbox Drive è la
soluzione più solida e gratuita. Vedi [[Accesso Remoto Vault]].
