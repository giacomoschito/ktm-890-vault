---
tipo: procedura
hardware_richiesto: ELM327 o cavo dedicato KTM
software_richiesto: vedi opzioni sotto
livello: intermedio
---

# Reset Spia ASSISTENZA — KTM 890 Duke 2021

tags: #diagnostica #service-reset #tuneecu #ktm890

> **Contesto:** Dopo il cambio olio + filtro DIY del 2026-06-05 (~5.300 km), la spia/messaggio **ASSISTENZA** sul cruscotto rimane attiva.
> L'ECU/Cluster Bosch non sa che la manutenzione è stata fatta e va resettata via diagnosi.

---

## Come Funziona il Reminder Service KTM

Il reminder è un contatore software memorizzato nell'**ECU Bosch** (e/o nel cluster TFT) della 890 Duke 2021. Si attiva al raggiungimento di:
- intervalli km predefiniti (5.000 / 10.000 km a seconda configurazione),
- o intervalli di tempo (ogni 12 mesi).

**Non si resetta da menù utente** sulla 890 Duke (a differenza di altri modelli). Serve un tool diagnostico esterno.

---

## Opzioni per il Reset (dalla più economica alla più completa)

### Opzione A — MotoScan (Android + ELM327 Bluetooth) ⭐ CONSIGLIATA

**Hardware:** ELM327 Bluetooth + adattatore KTM 6-pin → OBD2 (già pianificati in [[Lista Acquisti Diagnostica]])
**Software:** MotoScan (app Android) — versione PRO **€10-15** una tantum
**Funziona sulla 890 Duke:** Sì, supporta service reset KTM serie 790/890/1290

**Procedura:**
1. Installa MotoScan Pro dal Play Store
2. Collega ELM327 BT all'adattatore → presa diagnostica moto
3. Quadro su ON (motore spento)
4. Apri MotoScan → seleziona **KTM** → modello **890 Duke**
5. Menu **Service** → **Reset Service Reminder**
6. Conferma → spegni quadro → riaccendi: spia sparita

**Pro:** Economico, mobile, anche lettura DTC e dati live
**Contro:** Solo Android (no iOS), funzionalità avanzate ECU limitate

---

### Opzione B — KTMFlash / Tunerpro + cavo USB KTM dedicato

**Hardware:** Cavo USB-KTM dedicato (€20-40, AliExpress/eBay "KTM diagnostic cable USB")
**Software:** **KTMFlash** o **Tunerpro RT** (Windows, gratuiti)
**Funziona sulla 890 Duke:** Parzialmente — supporto Bosch ME17.x variabile

**Procedura standard:**
1. Driver FTDI/CH340 → installa
2. Connetti cavo → moto su quadro ON
3. KTMFlash → Connect → riconosce ECU
4. Menu **Service** → **Reset Service Counter**

**Pro:** Apre la strada a backup mappa ECU e funzionalità avanzate
**Contro:** Setup più complesso, supporto 890 Duke non garantito al 100%

---

### Opzione C — Healtech SP1 Service Reset Tool (hardware dedicato)

**Hardware:** Tool standalone Healtech **SP1** (€60-80, sito healtech-electronics.com)
**Software:** Nessuno — è un dispositivo dedicato con bottoni
**Funziona sulla 890 Duke:** Sì, ufficialmente supportato

**Procedura:**
1. Collega SP1 alla presa diagnostica KTM (con adattatore incluso)
2. Quadro ON
3. Premi tasto su SP1 → conferma reset
4. Fatto

**Pro:** Plug & play, zero configurazione PC, sempre funziona
**Contro:** Più caro, fa SOLO service reset (niente DTC, niente dati live)

---

### Opzione D — Officina KTM con KTM Dealer Tool (SDS)

**Hardware/Software:** KTM Dealer (SDS) — proprietario, solo concessionari
**Costo:** €20-50 di manodopera per il solo reset
**Quando ha senso:** Se hai problemi con A/B/C o vuoi anche aggiornamento firmware ECU.

---

## Setup Raccomandato per Te

Dato che in [[Lista Acquisti Diagnostica]] hai già pianificato:
- Adattatore KTM 6-pin → OBD2 (€3.44)
- ELM327 (USB e/o Bluetooth, €5-12)

→ **Vai di Opzione A (MotoScan)** se hai un telefono Android.
→ Se solo iPhone: vai di **Opzione B** (cavo USB + Windows + KTMFlash) o, se non vuoi rischi, **Opzione C** (Healtech SP1).

---

## File da Scaricare sul PC (per Opzione B)

| File | Dove | Note |
|------|------|------|
| Driver FTDI | ftdichip.com → "VCP Drivers" | Per cavi con chip FT232 |
| Driver CH340 | sparkfun.com / wch.cn | Per cavi con chip CH340 |
| KTMFlash | forum xda / ktm-forum.it (community) | Verifica versione compatibile 890 |
| Tunerpro RT | tunerpro.net | Alternativa più stabile |
| MotoScan APK | Solo Google Play (no APK pirata!) | Pagamento in-app |

> ⚠️ Scarica solo da fonti ufficiali. Evita .exe da forum sconosciuti — rischio malware.

---

## Cosa NON Fare

- ❌ Non scollegare batteria sperando di resettare la spia: non funziona sulla 890 Duke moderna
- ❌ Non usare la procedura di altri modelli KTM (es. 690 Duke vecchio menu nascosto) — non si applica
- ❌ Non flashare la ECU senza backup completo della mappa originale
- ❌ Non lasciare il quadro ON per ore: scarica la batteria

---

## Cross-link

- [[OBD2 Setup KTM]] — guida completa sistema diagnostica
- [[Lista Acquisti Diagnostica]] — cavo + ELM327 da ordinare
- [[02 - Manutenzione/Storico Tagliandi]] — tagliando 2026-06-05 che ha generato la spia
- [[00 - Dashboard]] — open issue tracker
