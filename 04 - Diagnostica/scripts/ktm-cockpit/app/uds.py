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
ISO_TP_LENGTH_LINE = re.compile(r"[0-9A-F]{3}")
ISO_TP_FRAME_PREFIX = re.compile(r"^[0-9A-F]:")
HEX_ONLY = re.compile(r"[0-9A-F]+")

# Negative Response Codes ISO 14229-1 (risposta "7F <SID> <NRC>")
NRC_NAMES: dict[int, str] = {
    0x10: "generalReject",
    0x11: "serviceNotSupported",
    0x12: "subFunctionNotSupported",
    0x13: "incorrectMessageLengthOrInvalidFormat",
    0x14: "responseTooLong",
    0x22: "conditionsNotCorrect",
    0x24: "requestSequenceError",
    0x31: "requestOutOfRange",
    0x33: "securityAccessDenied",
    0x35: "invalidKey",
    0x36: "exceededNumberOfAttempts",
    0x37: "requiredTimeDelayNotExpired",
    0x78: "responsePending",
    0x7E: "subFunctionNotSupportedInActiveSession",
    0x7F: "serviceNotSupportedInActiveSession",
}

# NRC che indicano "il DID esiste ma non è leggibile ora" (utile in scansione)
NRC_DID_EXISTS = {0x22, 0x33, 0x7F}


def _clean(resp: str) -> list[int]:
    """Estrae i byte da una risposta ELM327, riga per riga.

    Scarta le righe di stato (SEARCHING..., NO DATA, CAN ERROR, ?) e, nelle
    risposte multi-frame, la riga di lunghezza ISO-TP ("014") e i prefissi
    di frame ("0:", "1:", ...).
    """
    out: list[int] = []
    for raw_line in resp.upper().replace(">", "").splitlines():
        line = raw_line.strip()
        line = ISO_TP_FRAME_PREFIX.sub("", line).replace(" ", "")
        if not line or not HEX_ONLY.fullmatch(line):
            continue
        if ISO_TP_LENGTH_LINE.fullmatch(line):
            continue
        out.extend(int(line[i:i + 2], 16) for i in range(0, len(line) - 1, 2))
    return out


@dataclass
class RawResponse:
    """Esito di una richiesta UDS grezza."""

    request: str
    positive: list[int] | None  # byte dopo il SID positivo (SID + 0x40)
    nrc: int | None
    raw: str

    @property
    def nrc_name(self) -> str | None:
        return NRC_NAMES.get(self.nrc, f"0x{self.nrc:02X}") if self.nrc is not None else None


async def raw_request(client: ElmClient, request_hex: str, timeout: float = 2.0) -> RawResponse:
    """Invia una richiesta UDS/OBD in hex e separa risposta positiva da NRC."""
    req = request_hex.replace(" ", "").upper()
    sid = int(req[:2], 16)
    resp = await client.cmd(req, timeout=timeout)
    b = _clean(resp)
    nrc: int | None = None
    for i in range(len(b)):
        if b[i] == sid + 0x40:
            return RawResponse(req, b[i + 1:], None, resp)
        if b[i] == 0x7F and i + 2 < len(b) and b[i + 1] == sid and b[i + 2] != 0x78:
            nrc = b[i + 2]
    return RawResponse(req, None, nrc, resp)


def _format_dtc(hi: int, lo: int) -> str:
    """2 byte SAE J2012 → stringa tipo 'P0123'."""
    prefix = ["P", "C", "B", "U"][(hi >> 6) & 0x03]
    return f"{prefix}{(hi >> 4) & 0x03}{hi & 0x0F:X}{lo:02X}"


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
                code = _format_dtc(data[j], data[j + 1])
                if code != "P0000":
                    codes.append(code)
            break
    return codes


async def read_pending_dtcs(client: ElmClient) -> list[str]:
    """OBD-II Mode 07 — DTC in attesa di conferma (pending)."""
    r = await raw_request(client, "07")
    if not r.positive:
        return []
    count, data = r.positive[0], r.positive[1:]
    codes = [_format_dtc(data[j], data[j + 1]) for j in range(0, min(len(data) - 1, count * 2), 2)]
    return [c for c in codes if c != "P0000"]


# Bit dello status byte DTC (ISO 14229-1 D.2)
DTC_STATUS_BITS = {
    0: "testFailed",
    2: "pendingDTC",
    3: "confirmedDTC",
    7: "warningIndicatorRequested",
}


@dataclass
class UdsDtc:
    code: str           # es. "P0123"
    failure_type: int   # terzo byte DTC (Failure Type Byte)
    status: int
    flags: list[str]

    @property
    def label(self) -> str:
        return f"{self.code}-{self.failure_type:02X}"


async def read_dtcs_uds(client: ElmClient, status_mask: int = 0xFF) -> tuple[list[UdsDtc], RawResponse]:
    """UDS 0x19 02 ReadDTCInformation / reportDTCByStatusMask.

    A differenza del Mode 03 (solo DTC "emissioni") restituisce anche i codici
    proprietari del costruttore memorizzati nella centralina.
    """
    r = await raw_request(client, f"1902{status_mask:02X}", timeout=3.0)
    dtcs: list[UdsDtc] = []
    if r.positive and r.positive[0] == 0x02:
        records = r.positive[2:]  # salta subfunction + availabilityMask
        for j in range(0, len(records) - 3, 4):
            hi, mid, ftb, status = records[j:j + 4]
            flags = [name for bit, name in DTC_STATUS_BITS.items() if status & (1 << bit)]
            dtcs.append(UdsDtc(_format_dtc(hi, mid), ftb, status, flags))
    return dtcs, r


async def clear_dtcs_obd(client: ElmClient) -> RawResponse:
    """OBD-II Mode 04 — cancella DTC emissioni e azzera i readiness monitor."""
    return await raw_request(client, "04", timeout=5.0)


async def clear_dtcs_uds(client: ElmClient) -> RawResponse:
    """UDS 0x14 ClearDiagnosticInformation, gruppo FFFFFF = tutti i DTC."""
    return await raw_request(client, "14FFFFFF", timeout=5.0)


@dataclass
class DidScanHit:
    did: int
    status: str              # "ok" | NRC name
    hex_value: str = ""
    ascii_value: str = ""


async def scan_dids(
    client: ElmClient,
    start: int,
    end: int,
    on_progress=None,
) -> list[DidScanHit]:
    """Scansione READ-ONLY dei DID (0x22) nell'intervallo [start, end].

    Registra i DID che rispondono positivamente e quelli che esistono ma sono
    protetti (NRC 0x22/0x33/0x7F). Ignora requestOutOfRange (DID inesistente).
    Non invia mai scritture.
    """
    hits: list[DidScanHit] = []
    for did in range(start, end + 1):
        r = await raw_request(client, f"22{did:04X}")
        if r.positive and len(r.positive) >= 2 and r.positive[0] == did >> 8 and r.positive[1] == did & 0xFF:
            val = UdsResult.from_bytes(r.positive[2:])
            hits.append(DidScanHit(did, "ok", val.hex_value, val.ascii_value))
        elif r.nrc in NRC_DID_EXISTS:
            hits.append(DidScanHit(did, r.nrc_name or "?"))
        if on_progress:
            on_progress(did, start, end)
    return hits


# Indirizzi CAN 11-bit tipici dei moduli diagnosticabili (richiesta; risposta = +8)
CANDIDATE_ECU_HEADERS = ["7E0", "7E1", "7E2", "7E3", "7E4", "7E5", "7E6", "7E7"]


async def probe_ecus(client: ElmClient, headers: list[str] | None = None) -> dict[str, str]:
    """Trova quali centraline rispondono (TesterPresent 0x3E 00), read-only."""
    found: dict[str, str] = {}
    for h in headers or CANDIDATE_ECU_HEADERS:
        await client.cmd(f"ATSH{h}")
        r = await raw_request(client, "3E00", timeout=1.0)
        if r.positive is not None:
            found[h] = "risponde"
        elif r.nrc is not None:
            found[h] = f"risponde con NRC {r.nrc_name}"
    return found
