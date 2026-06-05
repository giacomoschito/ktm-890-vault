"""Persistenza SQLite per telemetria + uscite."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from sqlmodel import Field, Session, SQLModel, create_engine

DB_PATH = Path(__file__).parent.parent / "data" / "cockpit.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)


class Sample(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime = Field(default_factory=datetime.utcnow, index=True)
    rpm: int | None = None
    speed_kmh: int | None = None
    coolant_c: int | None = None
    oil_c: int | None = None
    throttle_pct: float | None = None
    voltage: float | None = None
    gear: int | None = None
    source: str = "elm327"


def init_db():
    SQLModel.metadata.create_all(engine)


def save_sample(snapshot: dict, source: str = "elm327"):
    sample = Sample(
        rpm=snapshot.get("rpm"),
        speed_kmh=snapshot.get("speed_kmh"),
        coolant_c=snapshot.get("coolant_c"),
        oil_c=snapshot.get("oil_c"),
        throttle_pct=snapshot.get("throttle_pct"),
        voltage=snapshot.get("voltage"),
        gear=snapshot.get("gear"),
        source=source,
    )
    with Session(engine) as s:
        s.add(sample)
        s.commit()
