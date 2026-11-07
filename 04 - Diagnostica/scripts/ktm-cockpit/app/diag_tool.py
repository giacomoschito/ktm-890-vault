"""Strumento diagnostico da riga di comando — KTM 890 Duke via ELM327.

Comandi (tutti READ-ONLY tranne clear-dtc):
  ecu         trova quali centraline rispondono sul bus (TesterPresent)
  info        identificazione ECU completa (VIN, CalID, SW/HW, DTC, verdetto A2)
  dtc         legge i codici errore: OBD Mode 03 + Mode 07 + UDS 0x19
  clear-dtc   cancella i codici errore (OBD Mode 04 + UDS 0x14) — chiede conferma
  scan-dids   enumera tutti i DID leggibili in un intervallo (UDS 0x22)
  raw         invia una singola richiesta, solo servizi di lettura

Esempi (PowerShell, dalla cartella ktm-cockpit):
  python -m app.diag_tool --target COM7 info
  python -m app.diag_tool --target COM7 dtc
  python -m app.diag_tool --target COM7 clear-dtc
  python -m app.diag_tool --target COM7 scan-dids --range F100-F1FF
  python -m app.diag_tool --target COM7 raw 22F190

Senza --target usa KTM_ELM_HOST oppure il simulator su 127.0.0.1:35000.
Ogni esecuzione salva un report JSON + Markdown in "04 - Diagnostica/Letture ECU/".
Non usare insieme al server web: la porta COM può essere aperta da un solo programma.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from app import ecu_info, uds
from app.elm_client import ElmClient

READINGS_DIR = Path(__file__).resolve().parents[3] / "Letture ECU"

# Servizi ammessi dal comando `raw`: solo lettura/diagnostica passiva.
# Esclusi di proposito: 0x04/0x14 (cancellazione), 0x10 (sessioni), 0x11 (reset ECU),
# 0x27 (security access), 0x2E/0x2F/0x31 (scritture/routine), 0x34-0x37 (flash).
RAW_READ_ONLY_SIDS = {0x01, 0x02, 0x03, 0x06, 0x07, 0x09, 0x0A, 0x19, 0x22, 0x3E}


def save_report(kind: str, data: dict, md_lines: list[str]) -> Path:
    READINGS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    base = READINGS_DIR / f"{stamp}_{kind}"
    base.with_suffix(".json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    header = [
        f"# Lettura ECU — {kind} — {stamp}",
        "",
        "tags: #diagnostica #lettura-ecu",
        "",
        f"File dati completo: `{base.name}.json`",
        "",
    ]
    base.with_suffix(".md").write_text("\n".join(header + md_lines) + "\n", encoding="utf-8")
    return base.with_suffix(".md")


async def connect(args) -> ElmClient:
    client = await ElmClient.open(args.target, args.port, args.baud)
    await uds.setup_uds(client, header=args.header)
    return client


async def read_all_dtcs(client: ElmClient) -> dict:
    stored = await uds.read_dtcs(client)
    pending = await uds.read_pending_dtcs(client)
    uds_dtcs, uds_raw = await uds.read_dtcs_uds(client)
    return {
        "obd_stored": stored,
        "obd_pending": pending,
        "uds": [asdict(d) | {"label": d.label} for d in uds_dtcs],
        "uds_error": uds_raw.nrc_name,
    }


def dtc_md(d: dict) -> list[str]:
    lines = ["## Codici errore", ""]
    lines.append(f"- OBD memorizzati (Mode 03): {', '.join(d['obd_stored']) or 'nessuno'}")
    lines.append(f"- OBD in attesa (Mode 07): {', '.join(d['obd_pending']) or 'nessuno'}")
    if d["uds_error"]:
        lines.append(f"- UDS 0x19: rifiutato dalla ECU ({d['uds_error']})")
    elif not d["uds"]:
        lines.append("- UDS 0x19: nessun codice")
    else:
        lines += ["", "| Codice | Stato |", "|--------|-------|"]
        lines += [f"| {x['label']} | {', '.join(x['flags']) or hex(x['status'])} |" for x in d["uds"]]
    return lines


def print_dtcs(d: dict) -> None:
    print(f"OBD memorizzati : {', '.join(d['obd_stored']) or 'nessuno'}")
    print(f"OBD in attesa   : {', '.join(d['obd_pending']) or 'nessuno'}")
    if d["uds_error"]:
        print(f"UDS 0x19        : rifiutato ({d['uds_error']})")
    else:
        print(f"UDS 0x19        : {', '.join(x['label'] for x in d['uds']) or 'nessuno'}")


async def cmd_ecu(args) -> None:
    client = await ElmClient.open(args.target, args.port, args.baud)
    try:
        await uds.setup_uds(client)
        found = await uds.probe_ecus(client)
    finally:
        await client.close()
    for h, state in found.items():
        print(f"  {h} → {state}")
    if not found:
        print("Nessuna centralina ha risposto. Quadro su ON? Adattatore Euro5 inserito bene?")
    path = save_report("centraline", {"ecus": found},
                       ["## Centraline trovate", ""] + [f"- `{h}`: {s}" for h, s in found.items()])
    print(f"\nReport: {path}")


async def cmd_info(args) -> None:
    report = await ecu_info.collect(host=args.target, port=args.port, baud=args.baud)
    data = ecu_info.to_dict(report)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    md = ["## Identificazione", "", "| Campo | Valore |", "|-------|--------|"]
    for key in ("vin", "calibration_id", "software_version", "sw_number", "hw_number", "supplier", "serial", "ecu_name"):
        md.append(f"| {key} | {data.get(key) or '—'} |")
    md += ["", "## DID letti", ""] + [f"- **{k}**: `{v}`" for k, v in data["dids"].items()]
    md += ["", "## Verdetto A2 (euristico)", "", f"- probabile A2: {data['a2']['is_likely_a2']} "
           f"(confidenza {data['a2']['confidence']})"] + [f"- {r}" for r in data["a2"]["reasons"]]
    md += ["", "## Note", ""] + [f"- {n}" for n in data["notes"]]
    print(f"\nReport: {save_report('info', data, md)}")


async def cmd_dtc(args) -> None:
    client = await connect(args)
    try:
        d = await read_all_dtcs(client)
    finally:
        await client.close()
    print_dtcs(d)
    print(f"\nReport: {save_report('dtc', d, dtc_md(d))}")


async def cmd_clear_dtc(args) -> None:
    client = await connect(args)
    try:
        before = await read_all_dtcs(client)
        print("Codici PRIMA della cancellazione:")
        print_dtcs(before)
        print(
            "\nATTENZIONE: cancellare i codici non ripara il guasto. Se il problema c'è ancora,"
            "\nla spia si riaccende. Vengono azzerati anche i readiness monitor Euro5."
            "\nQuadro su ON, motore SPENTO."
        )
        if not args.yes and input("\nScrivi CANCELLA per procedere: ").strip() != "CANCELLA":
            print("Annullato, nessuna modifica.")
            return
        obd = await uds.clear_dtcs_obd(client)
        udsr = await uds.clear_dtcs_uds(client)
        await asyncio.sleep(1.0)
        after = await read_all_dtcs(client)
    finally:
        await client.close()

    result = {
        "before": before,
        "clear_obd_mode04": "ok" if obd.positive is not None else (obd.nrc_name or "nessuna risposta"),
        "clear_uds_0x14": "ok" if udsr.positive is not None else (udsr.nrc_name or "nessuna risposta"),
        "after": after,
    }
    print(f"\nOBD Mode 04 : {result['clear_obd_mode04']}")
    print(f"UDS 0x14    : {result['clear_uds_0x14']}")
    print("\nCodici DOPO:")
    print_dtcs(after)
    md = ["## Prima", ""] + dtc_md(before)[2:] + [
        "", "## Cancellazione", "",
        f"- OBD Mode 04: {result['clear_obd_mode04']}",
        f"- UDS 0x14 FFFFFF: {result['clear_uds_0x14']}",
        "", "## Dopo", "",
    ] + dtc_md(after)[2:]
    print(f"\nReport: {save_report('clear-dtc', result, md)}")


def parse_range(text: str) -> tuple[int, int]:
    a, _, b = text.partition("-")
    start, end = int(a, 16), int(b or a, 16)
    if not (0 <= start <= end <= 0xFFFF):
        raise argparse.ArgumentTypeError(f"intervallo non valido: {text}")
    return start, end


async def cmd_scan_dids(args) -> None:
    ranges = args.range or [(0xF180, 0xF1FF)]
    total = sum(e - s + 1 for s, e in ranges)
    print(f"Scansione di {total} DID su {args.header} (solo lettura). Stima: ~{total // 10}-{total // 5} s")
    client = await connect(args)

    def progress(did, start, end):
        if (did - start) % 64 == 0 or did == end:
            print(f"  … 0x{did:04X}", flush=True)

    hits: list[uds.DidScanHit] = []
    try:
        for start, end in ranges:
            hits += await uds.scan_dids(client, start, end, on_progress=progress)
    finally:
        await client.close()

    for h in hits:
        print(f"  0x{h.did:04X}  {h.status:<28} {h.ascii_value}")
    data = {
        "header": args.header,
        "ranges": [f"{s:04X}-{e:04X}" for s, e in ranges],
        "hits": [asdict(h) | {"did_hex": f"0x{h.did:04X}"} for h in hits],
    }
    md = [f"Centralina: `{args.header}` · intervalli: {', '.join(data['ranges'])}", "",
          "| DID | Stato | ASCII | HEX |", "|-----|-------|-------|-----|"]
    md += [f"| 0x{h.did:04X} | {h.status} | `{h.ascii_value}` | `{h.hex_value}` |" for h in hits]
    print(f"\n{len(hits)} DID trovati. Report: {save_report('scan-dids', data, md)}")


async def cmd_raw(args) -> None:
    req = args.request.replace(" ", "").upper()
    if len(req) < 2 or int(req[:2], 16) not in RAW_READ_ONLY_SIDS:
        sys.exit(f"Servizio 0x{req[:2]} non ammesso: `raw` accetta solo servizi di lettura "
                 f"({', '.join(f'0x{s:02X}' for s in sorted(RAW_READ_ONLY_SIDS))}).")
    client = await connect(args)
    try:
        r = await uds.raw_request(client, req, timeout=3.0)
    finally:
        await client.close()
    if r.positive is not None:
        res = uds.UdsResult.from_bytes(r.positive)
        print(f"OK   hex: {res.hex_value}\n     ascii: {res.ascii_value}")
    elif r.nrc is not None:
        print(f"NRC  {r.nrc_name}")
    else:
        print(f"Nessuna risposta valida. Grezzo: {r.raw!r}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="diag_tool", description="Diagnostica KTM 890 Duke via ELM327")
    p.add_argument("--target", default=os.environ.get("KTM_ELM_HOST", "127.0.0.1"),
                   help="COMx / /dev/ttyUSB0 per il cavo, oppure host del simulator")
    p.add_argument("--port", type=int, default=int(os.environ.get("KTM_ELM_PORT", "35000")),
                   help="porta TCP (solo simulator)")
    p.add_argument("--baud", type=int, default=int(os.environ["KTM_ELM_BAUD"]) if os.environ.get("KTM_ELM_BAUD") else None,
                   help="baud seriale (default 38400; molti ELM BT usano 38400, alcuni USB 115200)")
    p.add_argument("--header", default="7E0", help="indirizzo CAN della centralina (default 7E0 = motore)")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ecu", help="trova le centraline che rispondono")
    sub.add_parser("info", help="identificazione ECU completa")
    sub.add_parser("dtc", help="legge tutti i codici errore")
    c = sub.add_parser("clear-dtc", help="cancella i codici errore (chiede conferma)")
    c.add_argument("--yes", action="store_true", help="salta la conferma interattiva")
    s = sub.add_parser("scan-dids", help="enumera i DID leggibili")
    s.add_argument("--range", type=parse_range, action="append",
                   help="intervallo hex, es. F100-F1FF (ripetibile). Default F180-F1FF")
    r = sub.add_parser("raw", help="singola richiesta di sola lettura, es. 22F190")
    r.add_argument("request")
    return p


COMMANDS = {
    "ecu": cmd_ecu,
    "info": cmd_info,
    "dtc": cmd_dtc,
    "clear-dtc": cmd_clear_dtc,
    "scan-dids": cmd_scan_dids,
    "raw": cmd_raw,
}


def main() -> None:
    args = build_parser().parse_args()
    try:
        asyncio.run(COMMANDS[args.cmd](args))
    except ModuleNotFoundError as e:
        sys.exit(f"Libreria mancante ({e.name}). Installa: pip install -r requirements.txt")
    except OSError as e:
        sys.exit(f"Impossibile collegarsi a {args.target}: {e}")


if __name__ == "__main__":
    main()
