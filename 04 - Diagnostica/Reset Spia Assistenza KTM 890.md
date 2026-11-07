---
tipo: procedura
hardware_richiesto: ELM327 o cavo dedicato KTM
software_richiesto: vedi opzioni sotto
livello: intermedio
---

# Reset Spia ASSISTENZA — KTM 890 Duke 2021

tags: #diagnostica #service-reset #tuneecu #ktm890

> [!tip] Aggiornamento 2026-11-07 — si resetta DAL CRUSCOTTO, senza cavo
> Più proprietari di 790/890 riportano un menu service nascosto nel TFT. **Prova prima l'Opzione 0 qui sotto.**
> Il supporto 890 Duke di MotoScan, KTMFlash/TunerPro e Healtech SP1 **non è confermato**;
> l'unico tester trovato che dichiara il service reset sulla 890 è il Duonix Bike-Scan 2 Pro (~€449).
> Strada via cavo e reverse engineering: [[Reverse Engineering ECU]].

> **Contesto:** Dopo il cambio olio + filtro DIY del 2026-06-05 (~5.300 km), la spia/messaggio **ASSISTENZA** sul cruscotto rimane attiva.
> L'ECU/Cluster Bosch non sa che la manutenzione è stata fatta e va resettata via diagnosi.

---

## Come Funziona il Reminder Service KTM

Il reminder è un contatore software memorizzato nell'**ECU Bosch** (e/o nel cluster TFT) della 890 Duke 2021. Si attiva al raggiungimento di:
- intervalli km predefiniti (5.000 / 10.000 km a seconda configurazione),
- o intervalli di tempo (ogni 12 mesi).

~~Non si resetta da menù utente~~ → **corretto 2026-11-07:** non c'è una voce visibile, ma esiste un **menu
service nascosto** nel cruscotto TFT, raggiungibile con una combinazione di tasti (Opzione 0).

> Intervalli ufficiali KTM 890 Duke: primo tagliando a 1.000 km, poi ogni **15.000 km o 12 mesi**.
> La spia scatta per **km oppure per data**: a ~5.500 km è quasi certamente scattata per i 12 mesi.

---

## Opzioni per il Reset (dalla più economica alla più completa)

### Opzione 0 — Dal cruscotto, gratis, 2 minuti ⭐ PROVA PRIMA QUESTA

> Fonte: procedure riportate da più proprietari 790/890 (forum, tutorial ScegliAuto). Non è un testo
> ufficiale KTM: se il tuo display si comporta diversamente, vale il manuale d'uso (sez. "Service" del
> capitolo strumentazione, [PDF ufficiale 890 Duke 2021](https://mobil.ktmshop.se/bike-manuals/21_3214300_en_OM.pdf)).

**Prima di iniziare**
- Moto ferma, **chiave su ON, motore spento**.
- Controlla che **data e ora del cruscotto siano giuste** (menu Settings): la spia scatta anche per data, e con un orologio sbagliato si riaccende subito.
- La spia ASSISTENZA deve essere **accesa** (alcuni riportano che il menu non si apre se è spenta). Lo è.

**Procedura** (tasti a sinistra sul manubrio: ▲ ▼ SET BACK)
1. Dalla schermata principale premi **SET** per aprire il menu.
2. Scorri con ▲/▼ fino a evidenziare la voce **Settings**. In alcune versioni software è dentro **Trip/Data**.
   **Non premere SET**: Settings deve restare solo evidenziata, non aperta. Non evidenziare "Service".
3. Tieni premuti **insieme ▲ e ▼** per circa **5 secondi**.
4. Compare la schermata dell'**intervallo service**, con km e mesi al prossimo tagliando.
5. Imposta i valori con ▲/▼ e SET. Due scelte sensate:
   - **15.000 km / 12 mesi**: intervallo ufficiale KTM;
   - **5.000 km**: se vuoi che la spia ti ricordi il cambio olio anticipato che fai tu (prossimo previsto a ~10.400 km).
6. **Per salvare, TIENI PREMUTO SET** per qualche secondo, finché torna la schermata principale.
   ⚠️ **Non usare BACK**: secondo più utenti esce senza salvare.
7. Spegni il quadro, aspetta 10 secondi, riaccendi: la spia deve essere sparita.

**Se non funziona**
| Sintomo | Cosa provare |
|---------|--------------|
| Con ▲+▼ non succede niente | Ricontrolla di essere su **Settings** (non dentro, non su Service). Poi prova **▲ + ▼ + SET insieme** (variante riportata su una 790) |
| Il menu si apre ma la spia torna | Hai salvato con BACK invece che tenendo premuto SET; ripeti |
| La spia torna dopo poco | Data/ora del cruscotto sbagliate, oppure scatta per data: verifica i mesi impostati |
| Non riesci a modificare i mesi | Su alcune 890 i mesi restano fissi a 12: va bene così, cambia solo i km |
| Nessuna variante funziona | Passa all'Opzione A/B (cavo) o D (officina, €20-50) |

**Dopo il reset**: annota data, km e valori impostati in [[02 - Manutenzione/Storico Tagliandi]].

---

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
