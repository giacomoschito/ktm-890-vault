# Tracking GPS & App Consigliati

tags: #gps #tracking #app

---

## Stack Consigliato per il Tuo Profilo

```
[Telefono sul moto] → Google Maps / Waze (navigazione)
[App ride tracker]  → Rever o Strava (log percorso)
[Diagnostica moto]  → KTM MY RIDE + MotoScan
[Storico & Note]    → Questo vault Obsidian
```

---

## App Navigazione

### Google Maps
- **Pro:** Tutti lo usano, aggiornato, traffico real-time
- **Contro:** Non ottimizzato per moto (sceglie autostrade)
- **Setup consigliato:**
  - Evita autostrade: Impostazioni → Percorsi → Evita pedaggi
  - Aggiungi tappe per creare percorsi più curvilinei
  - Mount telefono RAM su manubrio per visibilità

### Waze
- **Pro:** Migliore per traffico, avvisi autovelox
- **Contro:** Ancora meno moto-oriented di Google Maps
- **Uso ideale:** Commuting urbano quotidiano

---

## App Dedicate Moto (Consigliato Esplorare)

### Rever ⭐ Consigliato
- **Piattaforma:** iOS / Android
- **Costo:** Gratis (premium ~€3/mese)
- **Feature principali:**
  - Registrazione automatica percorsi
  - Mappe offline
  - Routing ottimizzato per strade curve
  - Community percorsi (scopri nuovi giri)
  - Export GPX
  - Statistiche velocità, distanza, tempo
- **Integrazione Obsidian:** Export GPX → embed in nota uscita

### Scenic
- Alternativa a Rever, routing simile
- Ottimo per pianificare passi alpini

### Strava (Opzione Alternativa)
- Non moto-specifico ma funziona
- Pro: già diffuso, community ampia
- Contro: pensato per ciclismo/running

---

## Integrazione con Obsidian

### Flusso di Lavoro Consigliato

1. **Prima dell'uscita:** Pianifica percorso su Rever/Maps
2. **Durante:** Telefono montato sul manubrio per navigazione
3. **Dopo l'uscita:** Compila Template Uscita in Obsidian con:
   - Km percorsi (da odometro moto)
   - Screenshot percorso da app
   - Note sensazioni, meteo, traffico
4. **Ogni settimana:** Aggiorna km gomme e stato moto

### Link Mappa nei File Uscita
```markdown
**Percorso:** [Giro Montagna 30/05](https://maps.app.goo.gl/XXXXX)
**GPX:** [[Uscite/GPX/2026-05-30.gpx]]
```

---

## Progetto Futuro — Dashboard Percorsi

### Stack Tecnico Possibile

```
Rever/Strava API
     ↓
Python script (scarica statistiche)
     ↓
JSON/CSV locale
     ↓
Obsidian Dataview (query e visualizzazione)
```

**O più ambizioso:**

```
OBD2 Bluetooth → Raspberry Pi
     ↓
MQTT / InfluxDB
     ↓
Grafana Dashboard (web app real-time)
```

---

## TPMS — Controllo Pressioni in Tempo Reale

### Prodotti Consigliati

| Prodotto | Compatibilità | Costo | Note |
|---------|--------------|-------|------|
| **Fobo Bike 2** | Universale | ~€80 | Bluetooth, app iOS/Android |
| **TPMS TubiX** | Universale | ~€50-70 | Economico, funziona bene |
| **Steelmate** | Universale | ~€40 | Budget option |

### Come Funziona
- Sensori si avvitano sui valvole gomme (ant + post)
- Trasmettono pressione via Bluetooth al telefono
- Alert se pressione cala durante la guida

---

## KTM MY RIDE App

**Cosa fa:**
- Connessione Bluetooth alla strumentazione TFT
- Personalizzazione schermate TFT
- Aggiornamenti modalità di guida
- Statistiche base

**Download:** App Store / Google Play → "KTM MY RIDE"

**Setup:**
1. Accendi moto (contact ON)
2. Apri app
3. Pairing Bluetooth automatico
4. Segui wizard iniziale

---

## Checklist Setup Iniziale

- [ ] Installare KTM MY RIDE sul telefono
- [ ] Acquistare RAM Mount per telefono sul manubrio
- [ ] Scaricare Rever (versione gratuita)
- [ ] Prima uscita weekend: testa registrazione percorso
- [ ] Esplorare acquisto TPMS per pressioni real-time
