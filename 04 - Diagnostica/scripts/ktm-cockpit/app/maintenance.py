"""Lettore manutenzione vault Obsidian.

Legge il frontmatter YAML di:
- 00 - Dashboard.md          (km_attuale, ultimo_cambio_olio_*)
- 02 - Manutenzione/Storico Tagliandi.md  (prossimo intervento, km_previsti)

Calcola km/giorni mancanti e produce alert.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

VAULT = Path(r"C:\KTM DUKE 890")
DASHBOARD = VAULT / "00 - Dashboard.md"
TAGLIANDI = VAULT / "02 - Manutenzione" / "Storico Tagliandi.md"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_frontmatter(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


@dataclass
class MaintenanceStatus:
    km_attuale: int | None = None
    km_prossimo_intervento: int | None = None
    data_prossimo_intervento: date | None = None
    tipo_prossimo: str | None = None
    ultimo_km: int | None = None
    ultimo_data: date | None = None
    alerts: list[str] = field(default_factory=list)

    @property
    def km_mancanti(self) -> int | None:
        if self.km_attuale is None or self.km_prossimo_intervento is None:
            return None
        return self.km_prossimo_intervento - self.km_attuale

    @property
    def giorni_mancanti(self) -> int | None:
        if self.data_prossimo_intervento is None:
            return None
        delta = self.data_prossimo_intervento - date.today()
        return delta.days


def _as_date(v: Any) -> date | None:
    if isinstance(v, date):
        return v
    if isinstance(v, str):
        try:
            return datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def status() -> MaintenanceStatus:
    dash = read_frontmatter(DASHBOARD)
    tag = read_frontmatter(TAGLIANDI)

    s = MaintenanceStatus(
        km_attuale=dash.get("km_attuale"),
        km_prossimo_intervento=tag.get("km_previsti"),
        data_prossimo_intervento=_as_date(tag.get("data_prevista")),
        tipo_prossimo=tag.get("tipo"),
        ultimo_km=tag.get("ultimo_intervento_km") or dash.get("ultimo_cambio_olio_km"),
        ultimo_data=_as_date(
            tag.get("ultimo_intervento_data") or dash.get("ultimo_cambio_olio_data")
        ),
    )

    km_left = s.km_mancanti
    if km_left is not None:
        if km_left <= 200:
            s.alerts.append(f"URGENTE: {s.tipo_prossimo or 'intervento'} tra {km_left} km")
        elif km_left <= 1000:
            s.alerts.append(f"In arrivo: {s.tipo_prossimo or 'intervento'} tra {km_left} km")

    days = s.giorni_mancanti
    if days is not None and days <= 14:
        s.alerts.append(f"Promemoria tempo: intervento entro {days} giorni")

    return s


if __name__ == "__main__":
    s = status()
    print("=== Stato Manutenzione KTM 890 ===")
    print(f"Km attuale:           {s.km_attuale}")
    print(f"Ultimo intervento:    {s.ultimo_km} km — {s.ultimo_data}")
    print(f"Prossimo intervento:  {s.tipo_prossimo} @ {s.km_prossimo_intervento} km — {s.data_prossimo_intervento}")
    print(f"Km mancanti:          {s.km_mancanti}")
    print(f"Giorni mancanti:      {s.giorni_mancanti}")
    if s.alerts:
        print("\nAlert attivi:")
        for a in s.alerts:
            print(f"  • {a}")
    else:
        print("\nNessun alert attivo")
