# Vision & Roadmap — Cosa ci permette di fare questo sistema

tags: #vision #roadmap

> La stella polare del progetto. Dove stiamo andando e perché ne vale la pena.

---

## In una frase

Trasformare la KTM 890 Duke da "moto che guido" a **moto che conosco in ogni
dettaglio** — con storico completo, diagnostica fai-da-te, telemetria reale e
una dashboard che mostra tutto. E costruirlo in modo che diventi un'app per
qualsiasi motociclista.

---

## I 6 Livelli del Sistema

### Livello 1 — Memoria storica della moto ✅ GIÀ ATTIVO
Il vault registra **tutto, per sempre**: tagliandi, gomme, accessori, uscite, spese.
- Mai più "quando ho cambiato l'olio?"
- Quando rivendi: storico documentato = **la moto vale di più e si vende prima**
- Sai esattamente quanto ti costa la moto al km

### Livello 2 — Diagnostica fai-da-te 🔜 (ELM327)
Colleghi il cavo e **leggi/cancelli i codici errore da solo**.
- Spia motore accesa? In 2 minuti sai se è grave o un sensore da niente
- Risparmi €50-100 ogni volta che eviti il meccanico solo per "leggere l'errore"
- Controlli salute moto: temperatura, tensione batteria, parametri motore

### Livello 3 — Telemetria completa 🔜 (CAN sniffing)
Leggi dati che **nemmeno il cruscotto ti mostra**.
- Angolo gas preciso, forza frenata ant/post, marcia, stato frizione
- Logging reale di ogni uscita: cosa ha fatto davvero la moto
- Analisi guida: dove e come freni, come acceleri, il tuo stile

### Livello 4 — Dashboard 🎯 (l'obiettivo visibile)
Tutti i dati in **una bella dashboard**, live e storica.
- Grafici di consumo, temperature, usura gomme nel tempo
- Mappe delle uscite con dati moto sovrapposti
- Sfrutta la potenza del PC per visualizzazioni e diagnostica

### Livello 5 — Manutenzione predittiva 🎯
Il sistema **ti avvisa prima** che serva.
- "Gomme posteriori al 70% — cambio previsto tra ~3.000 km"
- "Tagliando olio tra 800 km — prenota officina"
- Promemoria basati sui km reali, non su stime generiche

### Livello 6 — App scalabile 🚀 (il sogno grande)
Tutto questo è già la **base di un'app per altri motociclisti**.
- Il vault = database · gli script Python = backend · manca solo il frontend
- Se funziona per la tua Duke, funziona per migliaia di altre moto
- Da progetto personale a prodotto

---

## Esempi Concreti di "Cosa potrò fare"

| Situazione | Cosa fai con il sistema |
|------------|-------------------------|
| Spia accesa la mattina | Colleghi PC, leggi codice, capisci se puoi partire — invece di panico |
| Sali un passo di montagna | Vedi la temperatura olio salire in tempo reale, sai quando la moto soffre |
| Torni da una gita | Scarichi il log: km, marce usate, gas, temperature, tutto su grafico |
| Controlli le gomme | Il sistema stima usura e ti dice quanti km mancano al cambio |
| Vendi la moto tra 3 anni | Mostri storico completo e documentato = +valore, +fiducia compratore |
| Un amico ha una Duke | Gli dai accesso al sistema → diventa multi-moto → diventa app |

---

## Onestà: cosa è sicuro e cosa è da conquistare

| Livello | Affidabilità |
|---------|--------------|
| 1 — Storico vault | ✅ Certo, già funziona |
| 2 — Diagnostica codici | ✅ Molto affidabile (Euro5 espone i fault codes) |
| 3 — Telemetria CAN | 🟡 Fattibile — community ha già decodificato parte dei dati, il resto lo scopriamo noi |
| 4 — Dashboard | ✅ Certo una volta che i dati arrivano |
| 5 — Predittiva | ✅ Logica semplice sui dati raccolti |
| 6 — App | 🟡 Ambizioso ma realistico, step dopo step |

> La parte "da conquistare" (CAN decoding) è anche la più divertente: è vero
> reverse engineering, si impara tantissimo, e la community ci ha già aperto la strada.

---

## Perché ne vale la pena

1. **Impari** a fare i lavori sulla tua moto (risparmio + soddisfazione)
2. **Conosci** la tua moto meglio di qualsiasi meccanico
3. **Risparmi** su diagnosi, e prevedi i problemi prima che diventino costosi
4. **Documenti** tutto → valore alla rivendita
5. **Costruisci** qualcosa di tuo che può diventare un prodotto

---

Collegato a: [[00 - Dashboard]] · [[04 - Diagnostica/Lista Acquisti Diagnostica]] · [[04 - Diagnostica/CAN Bus Telemetry]] · [[06 - App & Integrazioni/Claude & Automazioni]]
