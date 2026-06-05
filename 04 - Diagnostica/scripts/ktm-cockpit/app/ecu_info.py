"""ECU info reader + euristica rilevamento depotenziamento A2.

Sequenza one-shot:
  1. setup_uds()
  2. legge VIN (mode 09 02 + UDS F190)
  3. legge calibration ID (mode 09 04 + UDS F195)
  4. legge software version (UDS F189, F188)
  5. prova DIDs proprietari KTM noti
  6. legge fault codes (mode 03)
  7. valuta indicatori A2

Output: dict serializzabile da esporre via /api/ecu.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from app.elm_client import ElmClient
from app.uds import (
    DID_KTM_CANDIDATES,
    DID_NAMES,
    mode09,
    read_did,
    read_dtcs,
    setup_uds,
)

# KTM WMI (World Manufacturer Identifier) — prime 3 cifre VIN
KTM_WMI = ("VBK", "ZK1", "MD2")


@dataclass
class A2Assessment:
    """Verdetto sull'eventuale depotenziamento A2 (35 kW)."""

    is_likely_a2: bool = False
    confidence: str = "unknown"  # low | medium | high
    reasons: list[str] = field(default_factory=list)
    evidence_against: list[str] = field(default_factory=list)


@dataclass
class EcuReport:
    vin: str | None = None
    vin_valid_ktm: bool = False
    calibration_id: str | None = None
    software_version: str | None = None
    sw_number: str | None = None
    hw_number: str | None = None
    supplier: str | None = None
    serial: str | None = None
    ecu_name: str | None = None
    dids: dict[str, str] = field(default_factory=dict)
    dtcs: list[str] = field(default_factory=list)
    a2: A2Assessment = field(default_factory=A2Assessment)
    notes: list[str] = field(default_factory=list)


# Pattern testuali nella calibration ID / software version che suggeriscono A2
A2_PATTERNS = [
    re.compile(r"A2", re.IGNORECASE),
    re.compile(r"35\s?KW", re.IGNORECASE),
    re.compile(r"LIM", re.IGNORECASE),
    re.compile(r"RESTR", re.IGNORECASE),
]
FULL_POWER_PATTERNS = [
    re.compile(r"FP", re.IGNORECASE),
    re.compile(r"FULL", re.IGNORECASE),
    re.compile(r"105\s?KW", re.IGNORECASE),
    re.compile(r"77\s?KW", re.IGNORECASE),  # 890 STD = 77 kW = 105 CV
]


def assess_a2(calibration_id: str | None, sw_version: str | None) -> A2Assessment:
    """Euristica testuale. Non è prova certa: serve cross-check con DB community."""
    a = A2Assessment()
    texts = [t for t in (calibration_id, sw_version) if t]
    blob = " | ".join(texts)
    if not texts:
        a.confidence = "low"
        a.reasons.append("Nessun CalID/SW letto — impossibile valutare.")
        return a

    for pat in A2_PATTERNS:
        if pat.search(blob):
            a.is_likely_a2 = True
            a.reasons.append(f"Match pattern A2: '{pat.pattern}' in '{blob}'")
    for pat in FULL_POWER_PATTERNS:
        if pat.search(blob):
            a.evidence_against.append(f"Match pattern full power: '{pat.pattern}' in '{blob}'")

    if a.evidence_against and not a.is_likely_a2:
        a.confidence = "high"
        a.reasons.append("Calibration ID/SW suggeriscono variante FULL POWER (non A2).")
    elif a.is_likely_a2 and not a.evidence_against:
        a.confidence = "medium"
    elif a.is_likely_a2 and a.evidence_against:
        a.confidence = "low"
        a.reasons.append("Pattern contraddittori — necessario cross-check community DB.")
    else:
        a.confidence = "low"
        a.reasons.append("Nessun pattern noto trovato. Va cercato il CalID nei DB tuning KTM.")
    return a


async def collect(host: str = "127.0.0.1", port: int = 35000) -> EcuReport:
    """Esegue tutta la scansione one-shot dell'ECU."""
    report = EcuReport()
    try:
        client = await ElmClient.tcp(host, port)
    except (ConnectionRefusedError, OSError) as e:
        report.notes.append(f"ELM non raggiungibile su {host}:{port} → {e}")
        return report

    try:
        await setup_uds(client)

        # Mode 09
        if (r := await mode09(client, 0x02)):
            report.vin = r.ascii_value.strip()
        if (r := await mode09(client, 0x04)):
            report.calibration_id = r.ascii_value.strip()
        if (r := await mode09(client, 0x0A)):
            report.ecu_name = r.ascii_value.strip()

        # UDS Mode 22 — DIDs standard
        for did, name in DID_NAMES.items():
            res = await read_did(client, did)
            if res is None:
                continue
            value = res.ascii_value.strip()
            report.dids[name] = value
            if name == "VIN" and not report.vin:
                report.vin = value
            elif name == "SystemSupplierECUSoftwareVersionNumber" and not report.calibration_id:
                report.calibration_id = value
            elif name == "VehicleManufacturerECUSoftwareVersionNumber":
                report.software_version = value
            elif name == "VehicleManufacturerECUSoftwareNumber":
                report.sw_number = value
            elif name == "VehicleManufacturerECUHardwareNumber":
                report.hw_number = value
            elif name == "SystemSupplierIdentifier":
                report.supplier = value
            elif name == "ECUSerialNumber":
                report.serial = value

        # DIDs proprietari KTM candidati (solo quelli che rispondono)
        for did in DID_KTM_CANDIDATES:
            res = await read_did(client, did)
            if res is not None:
                report.dids[f"DID_0x{did:04X}"] = f"{res.ascii_value} ({res.hex_value})"

        # DTCs
        report.dtcs = await read_dtcs(client)

        # Validazione e verdetto
        if report.vin:
            report.vin_valid_ktm = report.vin[:3] in KTM_WMI
            if not report.vin_valid_ktm:
                report.notes.append(f"VIN prefix '{report.vin[:3]}' non corrisponde a KTM WMI noti.")
        report.a2 = assess_a2(report.calibration_id, report.software_version)

        if report.calibration_id:
            report.notes.append(
                f"📌 Cerca questo CalID nei forum tuning KTM 890 per confermare variante: '{report.calibration_id}'"
            )
    finally:
        await client.close()
    return report


def to_dict(r: EcuReport) -> dict:
    return asdict(r)
