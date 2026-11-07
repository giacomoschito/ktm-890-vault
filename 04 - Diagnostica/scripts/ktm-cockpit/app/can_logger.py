"""Registratore passivo del bus CAN — base del reverse engineering.

Uso tipico (fase 2, con CANable/DSD TECH collegata al breakout OBD2):
  1. Avvia la registrazione
  2. Esegui l'operazione da osservare con uno strumento che la sa fare
     (es. reset service con un tester dedicato o in officina)
  3. Ferma con Ctrl+C e analizza il log: le richieste diagnostiche viaggiano
     sugli ID 0x7E0/0x7E8 (o simili), il resto è traffico normale della moto

Esempi:
  python -m app.can_logger --interface slcan --channel COM8
  python -m app.can_logger --interface gs_usb --channel 0
  python -m app.can_logger --interface slcan --channel COM8 --only-diag

Il bus è solo ascoltato: nessun frame viene trasmesso. Con slcan la modalità
listen-only viene richiesta all'adattatore quando supportata.
Log in formato candump (.log), leggibile da python-can, SavvyCAN e can-utils.
"""

from __future__ import annotations

import argparse
import time
from datetime import datetime
from pathlib import Path

import can

LOG_DIR = Path(__file__).resolve().parents[3] / "Log CAN"
DIAG_IDS = range(0x700, 0x800)  # richieste/risposte diagnostiche 11-bit


def main() -> None:
    p = argparse.ArgumentParser(description="Registratore CAN passivo KTM 890 Duke")
    p.add_argument("--interface", default="slcan", help="slcan | gs_usb | pcan | virtual …")
    p.add_argument("--channel", default="COM8", help="porta dell'adattatore CAN")
    p.add_argument("--bitrate", type=int, default=500000, help="KTM: 500 kbit/s")
    p.add_argument("--only-diag", action="store_true", help="salva solo gli ID 0x700-0x7FF")
    p.add_argument("--duration", type=float, default=0, help="secondi (0 = fino a Ctrl+C)")
    p.add_argument("--out", type=Path, help="file di output (default: Log CAN/<data>.log)")
    args = p.parse_args()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    out = args.out or LOG_DIR / f"{datetime.now():%Y-%m-%d_%H%M%S}{'_diag' if args.only_diag else ''}.log"

    kwargs: dict = {"interface": args.interface, "channel": args.channel}
    if args.interface != "virtual":
        kwargs["bitrate"] = args.bitrate
    if args.interface == "slcan":
        kwargs["listen_only"] = True

    filters = [{"can_id": 0x700, "can_mask": 0x700, "extended": False}] if args.only_diag else None
    seen: dict[int, int] = {}
    count = 0
    t_end = time.monotonic() + args.duration if args.duration else None

    with can.Bus(**kwargs, can_filters=filters) as bus, can.Logger(str(out)) as logger:
        print(f"[can] in ascolto su {args.interface}:{args.channel} → {out}  (Ctrl+C per fermare)")
        try:
            while t_end is None or time.monotonic() < t_end:
                msg = bus.recv(timeout=0.5)
                if msg is None:
                    continue
                if args.only_diag and msg.arbitration_id not in DIAG_IDS:
                    continue
                logger(msg)
                count += 1
                seen[msg.arbitration_id] = seen.get(msg.arbitration_id, 0) + 1
                if msg.arbitration_id in DIAG_IDS:
                    print(f"  DIAG 0x{msg.arbitration_id:03X}  {msg.data.hex(' ').upper()}")
        except KeyboardInterrupt:
            pass

    print(f"\n[can] {count} frame salvati in {out}")
    for arb_id, n in sorted(seen.items()):
        print(f"  0x{arb_id:03X}  {n} frame")


if __name__ == "__main__":
    main()
