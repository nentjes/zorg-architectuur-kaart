#!/usr/bin/env python3
"""
seed_revalidatie_epds.py — Harde data van Roel's Excel (april 2026)

Bron: privé-Excel van Roel (ex-ICT-manager Unicum + revalidatie-NVZ).
Dit is GEEN LLM-knowledge maar harde feiten vanuit zijn netwerk.
Daarom: confidence: high, needs_verification: false.

Doet:
1. Voegt 4 nieuwe systems toe: medicore, ecaris, sdb-reflex, amriq
2. Update bestaande revalidatie-orgs met systems + high confidence
3. Voegt 2 nieuwe revalidatie-orgs toe: capri-hartrevalidatie, mrc-aardenburg
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
ORGS = REPO / "data" / "organizations"
SYSTEMS = REPO / "data" / "systems"
SOURCE = "roel-private-excel-2026-04"

# -----------------------------------------------------------
# Nieuwe systems
# -----------------------------------------------------------
NEW_SYSTEMS = {
    "medicore": {
        "id": "medicore",
        "type": "system",
        "name": "Medicore",
        "category": "epd_msz",
        "vendor": "medicore",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "high",
    },
    "ecaris": {
        "id": "ecaris",
        "type": "system",
        "name": "Ecaris",
        "category": "epd_revalidatie",
        "vendor": "ecaris",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "high",
    },
    "sdb-reflex": {
        "id": "sdb-reflex",
        "type": "system",
        "name": "SDB Reflex",
        "aliases": ["Reflex", "SDB/Reflex"],
        "category": "epd_revalidatie",
        "vendor": "sdb-groep",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "high",
    },
    "amriq": {
        "id": "amriq",
        "type": "system",
        "name": "Amriq",
        "category": "epd_revalidatie",
        "vendor": "amriq",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "high",
    },
}

# -----------------------------------------------------------
# Revalidatie-EPD mapping (Roel's Excel)
# -----------------------------------------------------------
# (org_id, [systems], note)
REVAL_EPDS = [
    ("adelante",             ["chipsoft-hix"], None),
    ("basalt",               ["chipsoft-hix"], None),
    ("heliomare",            ["chipsoft-hix"], "implementatie/migratie datum onbekend"),
    ("de-hoogstraat",        ["chipsoft-hix"], None),
    ("klimmendaal",          ["chipsoft-hix"], None),
    ("libra-revalidatie",    ["ecaris"], None),
    ("merem",                ["sdb-reflex"], None),
    ("reade",                ["chipsoft-hix"], None),
    ("revalidatie-friesland",["chipsoft-hix"], None),
    ("revant",               ["chipsoft-hix"], None),
    ("rijndam",              ["chipsoft-hix"], None),
    ("roessingh",            ["chipsoft-hix"], "HiX geimplementeerd, datum onbekend"),
    ("tolbrug",              ["chipsoft-hix"], None),
    ("vogellanden",          ["sdb-reflex"], "implementatiedatum onbekend"),
]

# Nieuwe orgs die nog niet op disk staan
NEW_REVAL_ORGS = [
    {
        "id": "capri-hartrevalidatie",
        "type": "organization",
        "name": "Capri Hartrevalidatie",
        "sector": "revalidatie",
        "country": "NL",
        "locations": [
            {"city": "Rotterdam", "province": "Zuid-Holland", "country": "NL",
             "coordinates": {"lat": 51.9244, "lon": 4.4777}},
        ],
        "systems": ["medicore"],
        "sources": [SOURCE],
        "confidence": "high",
        "needs_verification": False,
    },
    {
        "id": "mrc-aardenburg",
        "type": "organization",
        "name": "MRC Aardenburg (Militair Revalidatie Centrum)",
        "aliases": ["MRC"],
        "sector": "revalidatie",
        "country": "NL",
        "locations": [
            {"city": "Doorn", "province": "Utrecht", "country": "NL",
             "coordinates": {"lat": 52.0400, "lon": 5.3400}},
        ],
        "region_iza": "iza-midden-nederland",
        "systems": ["chipsoft-hix"],
        "sources": [SOURCE],
        "confidence": "high",
        "needs_verification": False,
    },
]


def dump(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False,
                       allow_unicode=True, width=100)


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> int:
    # 1) Systems
    for sid, sdef in NEW_SYSTEMS.items():
        path = SYSTEMS / f"{sid}.yaml"
        if path.exists():
            print(f"SKIP  system {sid} (already exists)")
            continue
        dump(path, sdef)
        print(f"WRITE system {sid}")

    # 2) Update existing reval orgs
    for org_id, systems, note in REVAL_EPDS:
        path = ORGS / f"{org_id}.yaml"
        if not path.exists():
            print(f"MISS  org {org_id} (not on disk)", file=sys.stderr)
            continue
        data = load(path)
        data["systems"] = systems
        sources = list(data.get("sources") or [])
        if SOURCE not in sources:
            sources.append(SOURCE)
        data["sources"] = sources
        data["confidence"] = "high"
        data["needs_verification"] = False
        if note:
            data.setdefault("notes", []).append(note)
        dump(path, data)
        print(f"UPDT  org {org_id:25s} systems={systems}")

    # 3) New reval orgs
    for org in NEW_REVAL_ORGS:
        path = ORGS / f"{org['id']}.yaml"
        if path.exists():
            print(f"SKIP  org {org['id']} (already exists)")
            continue
        dump(path, org)
        print(f"WRITE org {org['id']}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
