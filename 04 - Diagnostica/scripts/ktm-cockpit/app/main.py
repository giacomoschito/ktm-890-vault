"""Backend FastAPI — server cockpit KTM 890 Duke.

Endpoint:
- GET  /              dashboard HTML
- GET  /api/status    stato manutenzione (legge vault)
- GET  /api/history   ultimi N campioni telemetria (SQLite)
- WS   /ws/live       stream live (snapshot JSON ogni 0.5s)

Avvio (sviluppo):
    uvicorn app.main:app --reload --port 8000

Per il live streaming: avvia anche il simulator in un altro terminale,
oppure imposta KTM_ELM_HOST/KTM_ELM_PORT verso un ELM327 reale (BT serial).
"""

from __future__ import annotations

import asyncio
import json
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, desc, select

from app import elm_client, maintenance
from app.db import Sample, engine, init_db, save_sample

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

ELM_HOST = os.environ.get("KTM_ELM_HOST", "127.0.0.1")
ELM_PORT = int(os.environ.get("KTM_ELM_PORT", "35000"))

clients: set[WebSocket] = set()
latest_snapshot: dict = {}


async def broadcast(snapshot: dict):
    global latest_snapshot
    latest_snapshot = snapshot
    save_sample(snapshot)
    dead: list[WebSocket] = []
    payload = json.dumps(snapshot)
    for ws in clients:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        clients.discard(ws)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(
        elm_client.poll_loop(broadcast, host=ELM_HOST, port=ELM_PORT, interval_s=0.5)
    )
    print(f"[main] polling ELM su {ELM_HOST}:{ELM_PORT}")
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(title="KTM 890 Duke Cockpit", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return (TEMPLATES_DIR / "index.html").read_text(encoding="utf-8")


@app.get("/api/status")
async def api_status():
    s = maintenance.status()
    return {
        "km_attuale": s.km_attuale,
        "ultimo_km": s.ultimo_km,
        "ultimo_data": s.ultimo_data.isoformat() if s.ultimo_data else None,
        "tipo_prossimo": s.tipo_prossimo,
        "km_prossimo": s.km_prossimo_intervento,
        "km_mancanti": s.km_mancanti,
        "giorni_mancanti": s.giorni_mancanti,
        "alerts": s.alerts,
        "latest": latest_snapshot,
    }


@app.get("/api/history")
async def api_history(limit: int = 500):
    with Session(engine) as session:
        rows = session.exec(select(Sample).order_by(desc(Sample.ts)).limit(limit)).all()
    return [
        {
            "ts": r.ts.isoformat(),
            "rpm": r.rpm,
            "speed_kmh": r.speed_kmh,
            "coolant_c": r.coolant_c,
            "oil_c": r.oil_c,
            "throttle_pct": r.throttle_pct,
            "voltage": r.voltage,
            "gear": r.gear,
        }
        for r in reversed(rows)
    ]


@app.websocket("/ws/live")
async def ws_live(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    if latest_snapshot:
        await ws.send_text(json.dumps(latest_snapshot))
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        clients.discard(ws)
