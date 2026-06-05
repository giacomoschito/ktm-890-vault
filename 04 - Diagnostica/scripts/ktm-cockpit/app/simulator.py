"""ELM327 simulator — TCP server che emula un ELM327 reale via socket.

Permette di sviluppare l'intera pipeline (backend, decoder, dashboard) senza
toccare la moto. Quando arriverà l'ELM327 BT/USB reale, basterà puntare il
client a quello invece che al simulatore.

Protocollo: subset ELM327 AT + risposte PID OBD-II Mode 01 in hex.
Avvio:  python -m app.simulator
Client: socket TCP su 127.0.0.1:35000  →  scrivi b"010C\r" per RPM, ecc.
"""

from __future__ import annotations

import asyncio
import math
import random
import time
from dataclasses import dataclass

HOST = "127.0.0.1"
PORT = 35000


@dataclass
class RideState:
    """Stato dinamico di una uscita simulata (giro su statale + curve)."""

    t0: float

    def now(self) -> float:
        return time.time() - self.t0

    def rpm(self) -> int:
        t = self.now()
        base = 3500 + 2000 * math.sin(t / 8)
        base += random.gauss(0, 150)
        return int(max(900, min(10500, base)))

    def speed_kmh(self) -> int:
        t = self.now()
        v = 70 + 40 * math.sin(t / 12) + random.gauss(0, 3)
        return int(max(0, min(220, v)))

    def coolant_c(self) -> int:
        t = self.now()
        return int(min(98, 50 + t / 12))

    def oil_c(self) -> int:
        return self.coolant_c() + random.randint(-3, 5)

    def throttle_pct(self) -> int:
        rpm = self.rpm()
        return max(0, min(100, int((rpm - 1500) / 90 + random.gauss(0, 4))))

    def voltage(self) -> float:
        return round(14.1 + random.gauss(0, 0.1), 2)

    def gear(self) -> int:
        v = self.speed_kmh()
        if v < 15:
            return 1
        if v < 40:
            return 2
        if v < 70:
            return 3
        if v < 100:
            return 4
        if v < 140:
            return 5
        return 6


def hex2(n: int) -> str:
    return f"{n & 0xFF:02X}"


def encode_pid(pid: str, state: RideState) -> str:
    """Codifica risposta OBD-II Mode 01 secondo SAE J1979."""
    if pid == "0C":  # RPM = (A*256 + B) / 4
        raw = state.rpm() * 4
        return f"41 0C {hex2(raw >> 8)} {hex2(raw)}"
    if pid == "0D":  # Speed = A
        return f"41 0D {hex2(state.speed_kmh())}"
    if pid == "05":  # Coolant temp = A - 40
        return f"41 05 {hex2(state.coolant_c() + 40)}"
    if pid == "5C":  # Oil temp = A - 40
        return f"41 5C {hex2(state.oil_c() + 40)}"
    if pid == "11":  # Throttle = A * 100/255
        return f"41 11 {hex2(int(state.throttle_pct() * 255 / 100))}"
    if pid == "42":  # Control module voltage = (A*256 + B) / 1000
        mv = int(state.voltage() * 1000)
        return f"41 42 {hex2(mv >> 8)} {hex2(mv)}"
    if pid == "A4":  # Transmission actual gear (non standard, KTM)
        return f"41 A4 {hex2(state.gear())}"
    return "NO DATA"


AT_RESPONSES = {
    "ATZ": "ELM327 v1.5",
    "ATE0": "OK",
    "ATL0": "OK",
    "ATH0": "OK",
    "ATS0": "OK",
    "ATSP0": "OK",
    "ATSP6": "OK",
    "ATCAF1": "OK",
    "ATCAF0": "OK",
    "ATDP": "AUTO, ISO 15765-4 (CAN 11/500)",
    "ATRV": None,  # gestito sotto
    "ATI": "ELM327 v1.5",
}

# --- ECU simulata "KTM 890 Duke 2021 full power" per testare il rilevamento A2 ---
# Cambia FAKE_A2=True per simulare invece una variante depotenziata
FAKE_A2 = False

SIM_VIN = "VBKEXJ408MM123456"  # KTM WMI = VBK
SIM_CALIBRATION_ID = "KTM89021A2-35KW-V107" if FAKE_A2 else "KTM89021FP-105KW-V112"
SIM_SW_VERSION = "1.07.A2" if FAKE_A2 else "1.12.FP"
SIM_HW_NUMBER = "0261S20189"  # Bosch ME17 fittizio
SIM_ECU_NAME = "ECM-EDC17C84"

# DIDs standard ISO 14229 supportati
UDS_DIDS = {
    0xF186: b"\x03",  # active diagnostic session = default
    0xF187: SIM_HW_NUMBER.encode(),
    0xF188: SIM_SW_VERSION.encode(),
    0xF189: SIM_SW_VERSION.encode(),
    0xF18A: b"BOSCH",
    0xF18C: b"BOSCH-SN-7723004A",
    0xF190: SIM_VIN.encode(),
    0xF194: SIM_SW_VERSION.encode(),
    0xF195: SIM_CALIBRATION_ID.encode(),
    0xF197: SIM_ECU_NAME.encode(),
    0xF1A2: SIM_HW_NUMBER.encode(),
}


def encode_mode09(pid: str) -> str:
    """Mode 09 OBD-II — vehicle information."""
    if pid == "02":  # VIN
        vin = SIM_VIN.encode().hex().upper()
        # response: 49 02 01 <17 bytes>
        return "49 02 01 " + " ".join(vin[i:i+2] for i in range(0, len(vin), 2))
    if pid == "04":  # CalibrationID
        cal = SIM_CALIBRATION_ID.encode().hex().upper()
        return "49 04 01 " + " ".join(cal[i:i+2] for i in range(0, len(cal), 2))
    if pid == "06":  # CVN
        return "49 06 01 12 34 56 78"
    if pid == "0A":  # ECU name
        name = SIM_ECU_NAME.encode().hex().upper()
        return "49 0A 01 " + " ".join(name[i:i+2] for i in range(0, len(name), 2))
    return "NO DATA"


def encode_mode22(did_hex: str) -> str:
    """Mode 22 UDS ReadDataByIdentifier."""
    try:
        did = int(did_hex, 16)
    except ValueError:
        return "NO DATA"
    payload = UDS_DIDS.get(did)
    if payload is None:
        return "7F 22 31"  # NRC: requestOutOfRange
    high = (did >> 8) & 0xFF
    low = did & 0xFF
    body = " ".join(f"{b:02X}" for b in payload)
    return f"62 {high:02X} {low:02X} {body}"


def encode_mode03() -> str:
    """Mode 03 — read DTCs (simuliamo zero codici attivi)."""
    return "43 00"


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    state = RideState(t0=time.time())
    peer = writer.get_extra_info("peername")
    print(f"[sim] client connesso: {peer}")
    try:
        while True:
            data = await reader.readuntil(b"\r")
            cmd = data.decode("ascii", errors="ignore").strip().upper().replace(" ", "")
            if not cmd:
                continue
            if cmd in AT_RESPONSES:
                resp = AT_RESPONSES[cmd]
                if cmd == "ATRV":
                    resp = f"{state.voltage():.1f}V"
                writer.write(f"{resp}\r\r>".encode())
            elif cmd.startswith("01") and len(cmd) >= 4:
                pid = cmd[2:4]
                writer.write(f"{encode_pid(pid, state)}\r\r>".encode())
            elif cmd.startswith("09") and len(cmd) >= 4:
                writer.write(f"{encode_mode09(cmd[2:4])}\r\r>".encode())
            elif cmd.startswith("22") and len(cmd) >= 6:
                writer.write(f"{encode_mode22(cmd[2:6])}\r\r>".encode())
            elif cmd.startswith("03"):
                writer.write(f"{encode_mode03()}\r\r>".encode())
            elif cmd.startswith("ATSH"):
                writer.write(b"OK\r\r>")
            else:
                writer.write(b"?\r\r>")
            await writer.drain()
    except (asyncio.IncompleteReadError, ConnectionResetError):
        print(f"[sim] client disconnesso: {peer}")
    finally:
        writer.close()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[sim] ELM327 simulator in ascolto su {HOST}:{PORT}")
    print(f"[sim] test rapido:  python -c \"import socket;s=socket.socket();s.connect(('{HOST}',{PORT}));s.sendall(b'010C\\r');print(s.recv(64))\"")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[sim] arresto")
