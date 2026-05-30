---
km_attuale: 5620
km_gomme_t32: 120
stato_rodaggio: in corso (fase 2)
mappatura_attiva: Rain
---

# KTM 890 Duke 2021 — Dashboard

> Ritirata: 2026-05-29 · Colorazione: Nera · Da: Amico (Biella)

---

## Stato Attuale

| Parametro | Valore |
|-----------|--------|
| Chilometraggio moto | **5.620 km** |
| Gomme montate | Bridgestone T32 (dal 29/05/2026) |
| Km sulle T32 | **120 km** — fase 2 rodaggio |
| Rodaggio T32 | Fase 2 — puoi aprire gli angoli progressivamente |
| Mappatura attiva | Rain |
| Prossimo tagliando | ~10.000 km (olio motore) |
| Pressione ant. | 2,5 bar (verificare!) |
| Pressione post. | 2,9 bar (verificare!) |

---

## Checklist Immediata

- [ ] Fotografare libretto di manutenzione dell'amico
- [ ] Verificare pressione gomme (fredde, mattina — ant 2,5 / post 2,9 bar)
- [ ] Acquistare vite DB killer per scarico Arrow
- [ ] Installare KTM MY RIDE sul telefono
- [ ] Montare scarico Arrow (quando arriva la vite) — [[05 - Accessori/Montaggio Scarico Arrow]]

---

## Rodaggio Bridgestone T32

```
[━━━━━━━━━━━━░░░░░░░░] 120/200 km (60%)
Obiettivo: 200 km · Sei in Fase 2 — puoi allargare gli angoli
```

| Soglia | Stato | Azione |
|--------|-------|--------|
| 0-100 km | ✅ Completato | — |
| 100-200 km | **In corso** | Street mode ok, aumenta progressivamente l'angolo |
| 200+ km | — | Gomme a regime, Sport mode libero |

---

## Uscite Recenti

```dataview
TABLE date as "Data", km as "Km", route as "Percorso", mappatura as "Mappatura", rating as "Voto"
FROM "03 - Uscite"
WHERE file.name != "Template Uscita"
SORT date DESC
LIMIT 10
```

---

## Prossima Manutenzione

```dataview
TABLE tipo as "Intervento", km_previsti as "Km previsti", data_prevista as "Data stimata"
FROM "02 - Manutenzione"
WHERE prossimo_intervento = true
SORT km_previsti ASC
```

---

## Statistiche Gomme Attuali (T32)

| Parametro | Valore |
|-----------|--------|
| Marca/Modello | Bridgestone Battlax T32 |
| Data montaggio | 29/05/2026 |
| Km al montaggio | ~5.500 |
| Km percorsi | DA AGGIORNARE |
| Usura stimata | ~0% |
| Durata stimata | 8.000-12.000 km |
| Sostituzione prevista | ~13.500-17.500 km |

---

## Link Rapidi

| Sezione | Link |
|---------|------|
| 🎯 Vision & Roadmap | [[00 - Vision e Roadmap]] |
| Scheda tecnica | [[01 - Moto/Scheda Tecnica]] |
| Mappature | [[01 - Moto/Mappature e Riding Modes]] |
| Gomme | [[02 - Manutenzione/Gomme]] |
| Tagliandi | [[02 - Manutenzione/Storico Tagliandi]] |
| Accessori | [[05 - Accessori/Accessori]] |
| OBD2 / Diagnostica | [[04 - Diagnostica/OBD2 Setup KTM]] |
| Tracking GPS | [[06 - App & Integrazioni/Tracking GPS]] |
| Nuova uscita | [[Templates/Uscita Template]] |
