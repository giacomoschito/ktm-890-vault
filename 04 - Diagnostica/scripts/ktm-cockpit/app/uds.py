"""UDS (ISO 14229) + OBD Mode 09 client su ELM327.

Read-only: leggiamo VIN, calibration ID, software version, DIDs vari.
Niente scritture, niente flash. Sicuro al 100%.

Strategia: usiamo `ElmClient.cmd()` per inviare raw commands.
ELM327 con ATCAF1 gestisce automaticamente l'ISO-TP framing.

Per UDS via OBD-II port serve impostare l'header tester ECU:
    ATSH 7E0     (engine ECU 11-bit, request)
    ATSP 6       (ISO 15765-4 CAN 11/500)
    ATCAF 1      (auto formatting)
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.elm_client import ElmClient

# DIDs ISO 14229 standard
DID_NAMES: dict[int, str] = {
    0xF186: "ActiveDiagnosticSession",
    0xF187: "VehicleManufacturerSparePartNumber",
    0xF188: "VehicleManufacturerECUSoftwareNumber",
    0xF189: "VehicleManufacturerECUSoftwareVersionNumber",
    0xF18A: "SystemSupplierIdentifier",
    0xF18C: "ECUSerialNumber",
    0xF190: "VIN",
    0xF194: "SystemSupplierECUSoftwareNumber",
    0xF195: "SystemSupplierECUSoftwareVersionNumber",
    0xF197: "SystemNameOrEngineType",
    0xF1A2: "VehicleManufacturerECUHardwareNumber",
}

# DIDs proprietari KTM/Bosch da indagare (range 0x2000-0xFEFF)
# Da arricchire dopo prime letture sulla moto reale
DID_KTM_CANDIDATES: list[int] = [
    0x2000, 0x2001, 0x2010,        # generici manufacturer
    0xF010, 0xF011, 0xF012,        # blocchi diagnostica estesa
    0xF1A0, 0xF1A1, 0xF1A3,        # variant identification
]

HEX_PAIR = re.compile(r"[0-9A-F]{2}")


def _clean(line: str) -> list[int]:
    return [int(m.group(0), 16) for m in HEX_PAIR.finditer(line.upper())]


@dataclass
class UdsResult:
    raw_bytes: list[int]
    ascii_value: str
    hex_value: str

    @classmethod
    def from_bytes(cls, b: list[int]) -> "UdsResult":
        ascii_chars = "".join(chr(x) if 32 <= x < 127 else "." for x in b)
        hex_str = " ".join(f"{x:02X}" for x in b)
        return cls(raw_bytes=b, ascii_value=ascii_chars, hex_value=hex_str)


async def setup_uds(client: ElmClient, header: str = "7E0"):
    """Configura l'ELM per sessioni UDS sull'ECU motore."""
    for cmd in ("ATZ", "ATE0", "ATL0", "ATH0", "ATS0", "ATSP6", "ATCAF1", f"ATSH{header}"):
        await client.cmd(cmd)


async def mode09(client: ElmClient, pid: int) -> UdsResult | None:
    """OBD-II Mode 09 — VIN (02), CalibrationID (04), CVN (06), ECU name (0A)."""
    resp = await client.cmd(f"09{pid:02X}")
    return _parse_mode09(resp, pid)


def _parse_mode09(resp: str, pid: int) -> UdsResult | None:
    bytes_ = _clean(resp)
    # cerca header 49 PP
    for i in range(len(bytes_) - 1):
        if bytes_[i] == 0x49 and bytes_[i + 1] == pid:
            # salta header 49 PP e il byte "Number Of Data Items" se presente
            payload = bytes_[i + 2:]
            if payload and payload[0] in (0x01, 0x02, 0x03, 0x04):
                payload = payload[1:]
            return UdsResult.from_bytes(payload)
    return None


async def read_did(client: ElmClient, did: int) -> UdsResult | None:
    """UDS Mode 22 ReadDataByIdentifier — legge un singolo DID."""
    high, low = (did >> 8) & 0xFF, did & 0xFF
    resp = await client.cmd(f"22{high:02X}{low:02X}")
    return _parse_mode22(resp, did)


def _parse_mode22(resp: str, did: int) -> UdsResult | None:
    bytes_ = _clean(resp)
    high, low = (did >> 8) & 0xFF, did & 0xFF
    for i in range(len(bytes_) - 2):
        if bytes_[i] == 0x62 and bytes_[i + 1] == high and bytes_[i + 2] == low:
            return UdsResult.from_bytes(bytes_[i + 3:])
        if bytes_[i] == 0x7F and bytes_[i + 1] == 0x22:
            return None  # negative response
    return None


async def read_dtcs(client: ElmClient) -> list[str]:
    """OBD-II Mode 03 — read stored DTCs."""
    resp = await client.cmd("03")
    bytes_ = _clean(resp)
    codes: list[str] = []
    for i in range(len(bytes_) - 1):
        if bytes_[i] == 0x43:
            count = bytes_[i + 1] if i + 1 < len(bytes_) else 0
            data = bytes_[i + 2:]
            for j in range(0, len(data) - 1, 2):
                if j // 2 >= count:
                    break
                hi, lo = data[j], data[j + 1]
                prefix = ["P", "C", "B", "U"][(hi >> 6) & 0x03]
                code = f"{prefix}{(hi >> 4) & 0x03}{hi & 0x0F:X}{lo:02X}"
                if code != "P0000":
                    codes.append(code)
            break
    return codes
