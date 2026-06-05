"""Decoder CAN bus per KTM 790/890 Duke.

ID e formule decodificate dalla community 790dukeforum (vedi vault
04 - Diagnostica/CAN Bus Telemetry.md). Da validare con dati reali quando
arriva la CANable.

Frame in input: dict {"arbitration_id": int, "data": bytes}
Output: dict con chiavi normalizzate (throttle_pct, gear, brake_front_pct, ecc.)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

# ID noti dalla community (790/890 Duke, Euro5, CAN @ 500 kbps)
CAN_ID_THROTTLE = 0x120  # gas (TPS)
CAN_ID_GEAR_CLUTCH = 0x129  # marcia inserita + stato frizione
CAN_ID_BRAKE_FRONT = 0x290  # pressione freno anteriore
CAN_ID_BRAKE_REAR = 0x12B  # pressione freno posteriore


@dataclass
class DecodedSignal:
    name: str
    value: float | int | str
    unit: str = ""


Decoder = Callable[[bytes], list[DecodedSignal]]


def _decode_throttle(data: bytes) -> list[DecodedSignal]:
    if len(data) < 2:
        return []
    raw = data[1]
    return [DecodedSignal("throttle_pct", round(raw * 100 / 255, 1), "%")]


def _decode_gear_clutch(data: bytes) -> list[DecodedSignal]:
    if len(data) < 3:
        return []
    gear_byte = data[0] & 0x0F
    clutch_pulled = bool(data[2] & 0x01)
    gear_map = {0: "N", 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}
    return [
        DecodedSignal("gear", gear_map.get(gear_byte, "?")),
        DecodedSignal("clutch_pulled", int(clutch_pulled)),
    ]


def _decode_brake_front(data: bytes) -> list[DecodedSignal]:
    if len(data) < 2:
        return []
    raw = (data[0] << 8) | data[1]
    return [DecodedSignal("brake_front_pct", round(raw * 100 / 0xFFFF, 1), "%")]


def _decode_brake_rear(data: bytes) -> list[DecodedSignal]:
    if len(data) < 2:
        return []
    raw = (data[0] << 8) | data[1]
    return [DecodedSignal("brake_rear_pct", round(raw * 100 / 0xFFFF, 1), "%")]


DECODERS: dict[int, Decoder] = {
    CAN_ID_THROTTLE: _decode_throttle,
    CAN_ID_GEAR_CLUTCH: _decode_gear_clutch,
    CAN_ID_BRAKE_FRONT: _decode_brake_front,
    CAN_ID_BRAKE_REAR: _decode_brake_rear,
}


def decode(arbitration_id: int, data: bytes) -> list[DecodedSignal]:
    decoder = DECODERS.get(arbitration_id)
    if decoder is None:
        return []
    return decoder(data)


# Test rapido con frame sintetici — da rivedere con i dati reali della moto
if __name__ == "__main__":
    samples = [
        (CAN_ID_THROTTLE, bytes([0x00, 0x80])),  # 50% gas
        (CAN_ID_GEAR_CLUTCH, bytes([0x03, 0x00, 0x00])),  # 3a marcia, frizione rilasciata
        (CAN_ID_BRAKE_FRONT, bytes([0x40, 0x00])),  # ~25% freno ant
        (CAN_ID_BRAKE_REAR, bytes([0x00, 0x00])),  # freno post libero
    ]
    for arb_id, data in samples:
        signals = decode(arb_id, data)
        print(f"ID 0x{arb_id:03X}: {[s.__dict__ for s in signals]}")
