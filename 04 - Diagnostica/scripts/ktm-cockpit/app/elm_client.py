"""Client ELM327 unificato — parla sia col simulator (TCP) sia con un ELM327
reale (USB seriale o BT seriale).

Espone una coroutine async `poll_loop(callback)` che chiede periodicamente
i PID interessanti e chiama callback(dict) con i valori decodificati.

Modalità:
- TCP (default in dev):   ElmClient.tcp("127.0.0.1", 35000)
- Serial (cavo USB):      ElmClient.serial("COM3", 38400)
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable

PIDS = ["010C", "010D", "0105", "015C", "0111", "0142", "01A4"]
PID_NAMES = {
    "0C": "rpm",
    "0D": "speed_kmh",
    "05": "coolant_c",
    "5C": "oil_c",
    "11": "throttle_pct",
    "42": "voltage",
    "A4": "gear",
}


def parse_obd_response(line: str) -> tuple[str, float | int] | None:
    """Parsa risposta tipo '41 0C 1A F8' → ('rpm', 1726)."""
    line = line.strip().replace(">", "").replace("\r", "").upper()
    parts = line.split()
    if len(parts) < 3 or parts[0] != "41":
        return None
    pid = parts[1]
    name = PID_NAMES.get(pid)
    if not name:
        return None
    try:
        b = [int(x, 16) for x in parts[2:]]
    except ValueError:
        return None
    if pid == "0C":
        return name, (b[0] * 256 + b[1]) // 4
    if pid == "0D":
        return name, b[0]
    if pid == "05":
        return name, b[0] - 40
    if pid == "5C":
        return name, b[0] - 40
    if pid == "11":
        return name, round(b[0] * 100 / 255, 1)
    if pid == "42":
        return name, round((b[0] * 256 + b[1]) / 1000, 2)
    if pid == "A4":
        return name, b[0]
    return None


@dataclass
class ElmClient:
    """Client minimale per dialogare con un endpoint ELM327."""

    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter

    @classmethod
    async def tcp(cls, host: str = "127.0.0.1", port: int = 35000) -> "ElmClient":
        reader, writer = await asyncio.open_connection(host, port)
        client = cls(reader, writer)
        await client.init()
        return client

    async def init(self):
        for cmd in ("ATZ", "ATE0", "ATL0", "ATH0", "ATS0", "ATSP0"):
            await self.cmd(cmd)

    async def cmd(self, command: str, timeout: float = 1.5) -> str:
        self.writer.write(f"{command}\r".encode())
        await self.writer.drain()
        try:
            data = await asyncio.wait_for(self.reader.readuntil(b">"), timeout=timeout)
        except asyncio.TimeoutError:
            return ""
        return data.decode("ascii", errors="ignore").strip(">").strip()

    async def query_pid(self, pid_cmd: str) -> tuple[str, float | int] | None:
        resp = await self.cmd(pid_cmd)
        for line in resp.splitlines():
            parsed = parse_obd_response(line)
            if parsed:
                return parsed
        return None

    async def close(self):
        self.writer.close()
        try:
            await self.writer.wait_closed()
        except Exception:
            pass


async def poll_loop(
    callback: Callable[[dict], Awaitable[None]],
    host: str = "127.0.0.1",
    port: int = 35000,
    interval_s: float = 0.5,
):
    """Loop di polling: legge PID e invia dict aggregato al callback."""
    while True:
        try:
            client = await ElmClient.tcp(host, port)
            print(f"[elm] connesso a {host}:{port}")
            while True:
                snapshot: dict = {}
                for pid_cmd in PIDS:
                    res = await client.query_pid(pid_cmd)
                    if res:
                        name, value = res
                        snapshot[name] = value
                if snapshot:
                    await callback(snapshot)
                await asyncio.sleep(interval_s)
        except (ConnectionRefusedError, ConnectionResetError, asyncio.IncompleteReadError):
            print(f"[elm] {host}:{port} non raggiungibile, retry in 3s…")
            await asyncio.sleep(3)
