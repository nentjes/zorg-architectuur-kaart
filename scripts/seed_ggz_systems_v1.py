#!/usr/bin/env python3
"""
seed_ggz_systems_v1.py — GGZ EPD-mapping uit Gemini-research (Top 20)

Bron: Gemini research-rapport v0.2.2, forwarded door Roel (april 2026).
Dit is research-niveau — niet Roel's verified netwerk. Daarom:
confidence: medium, needs_verification: true.
Source: gemini-ggz-research-2026-04

Doet:
1. Voegt nieuwe systems toe: tenzinger-user, tenzinger-fier, mextra, nexus
2. Voegt nieuwe vendors toe: tenzinger, mextra-bv, nexus-ag
3. Update bestaande GGZ-orgs met systems + medium confidence
4. Voegt 3 nieuwe GGZ-orgs toe: ggz-ingeest, reinier-van-arkel, eleos
"""
from __future__ import annotations
import sys
from pathlib import Path
import yaml

REPO = Path(__file__).resolve().parent.parent
ORGS = REPO / "data" / "organizations"
SYSTEMS = REPO / "data" / "systems"
VENDORS = REPO / "data" / "vendors"
SOURCE = "gemini-ggz-research-2026-04"

# -----------------------------------------------------------
# Nieuwe vendors
# -----------------------------------------------------------
NEW_VENDORS = {
    "tenzinger": {
        "id": "tenzinger",
        "type": "vendor",
        "name": "Tenzinger",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "medium",
    },
    "mextra-bv": {
        "id": "mextra-bv",
        "type": "vendor",
        "name": "Mextra",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "medium",
    },
    "nexus-ag": {
        "id": "nexus-ag",
        "type": "vendor",
        "name": "Nexus AG",
        "country_origin": "DE",
        "sources": [SOURCE],
        "confidence": "medium",
    },
}

# -----------------------------------------------------------
# Nieuwe systems
# -----------------------------------------------------------
NEW_SYSTEMS = {
    "tenzinger-user": {
        "id": "tenzinger-user",
        "type": "system",
        "name": "Tenzinger User",
        "aliases": ["User"],
        "category": "epd_ggz",
        "vendor": "tenzinger",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "medium",
    },
    "tenzinger-fier": {
        "id": "tenzinger-fier",
        "type": "system",
        "name": "Tenzinger Fier",
        "aliases": ["Fier"],
        "category": "epd_ggz",
        "vendor": "tenzinger",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "medium",
    },
    "mextra": {
        "id": "mextra",
        "type": "system",
        "name": "Mextra",
        "category": "ecd_begeleid_wonen",
        "vendor": "mextra-bv",
        "country_origin": "NL",
        "sources": [SOURCE],
        "confidence": "medium",
    },
    "nexus-kis": {
        "id": "nexus-kis",
        "type": "system",
        "name": "Nexus KIS",
        "aliases": ["Nexus"],
        "category": "epd_msz",
        "vendor": "nexus-ag",
        "country_origin": "DE",
        "sources": [SOURCE],
        "confidence": "medium",
    },
}

# -----------------------------------------------------------
# GGZ EPD-mapping (Gemini Top 20)
# (org_id, [systems], strategic_note_or_None)
# -----------------------------------------------------------
GGZ_EPDS = [
    ("parnassia-groep",   ["tenzinger-user", "tenzinger-fier"], "grootste GGZ-speler NL"),
    ("arkin",             ["tenzinger-user"], "Amsterdam stedelijk"),
    ("ggz-centraal",      ["mextra", "tenzinger-fier"], "regio Midden-NL"),
    ("altrecht",          ["tenzinger-user"], "Utrechtse GGZ-reus; key connection naar UMCU HiX"),
    ("ggz-oost-brabant",  ["nexus-kis", "tenzinger-fier"], "Nexus voor klinisch"),
    ("lentis",            ["tenzinger-user"], "Noord-NL dominant"),
    ("ggnet",             ["chipsoft-hix"], "uitzondering: HiX i.p.v. Tenzinger"),
    ("dimence",           ["tenzinger-user"], "Overijssel/Deventer"),
    ("vincent-van-gogh",  ["nedap-ons", "tenzinger-fier"], "focus op VVT-connectie"),
    ("ggze",              ["tenzinger-fier"], "GGZ Eindhoven, innovatie + cliëntportalen"),
    ("pro-persona",       ["tenzinger-user"], "Gelderse regio"),
    ("karakter",          ["tenzinger-user"], "kind-en-jeugd specialistisch"),
    ("ggz-nhn",           ["nedap-ons"], "uitzondering: volledig op Nedap"),
    ("mondriaan",         ["tenzinger-user"], "Zuid-Limburg"),
    ("kwintes",           ["mextra"], "begeleid wonen"),
    ("ggz-drenthe",       ["tenzinger-user"], "Drentse keten"),
    ("emergis",           ["tenzinger-user"], "GGZ Zeeland"),
]

# -----------------------------------------------------------
# Nieuwe GGZ-orgs (niet op disk)
# -----------------------------------------------------------
NEW_GGZ_ORGS = [
    {
        "id": "ggz-ingeest",
        "type": "organization",
        "name": "GGZ inGeest",
        "sector": "ggz",
        "subtype": "geintegreerd",
        "country": "NL",
        "locations": [
            {"city": "Amsterdam", "province": "Noord-Holland", "country": "NL",
             "coordinates": {"lat": 52.3344, "lon": 4.8661}},
        ],
        "systems": ["epic-epd"],
        "sources": [SOURCE],
        "confidence": "medium",
        "needs_verification": True,
        "notes": ["Uitzondering: draait mee op Epic-stack van Amsterdam UMC"],
    },
    {
        "id": "reinier-van-arkel",
        "type": "organization",
        "name": "Reinier van Arkel",
        "sector": "ggz",
        "subtype": "geintegreerd",
        "country": "NL",
        "locations": [
            {"city": "'s-Hertogenbosch", "province": "Noord-Brabant", "country": "NL",
             "coordinates": {"lat": 51.6978, "lon": 5.3037}},
        ],
        "systems": ["tenzinger-user"],
        "sources": [SOURCE],
        "confidence": "medium",
        "needs_verification": True,
    },
    {
        "id": "eleos",
        "type": "organization",
        "name": "Eleos",
        "aliases": ["De Hoop/Eleos"],
        "sector": "ggz",
        "subtype": "confessioneel",
        "country": "NL",
        "locations": [
            {"city": "Amersfoort", "province": "Utrecht", "country": "NL",
             "coordinates": {"lat": 52.1561, "lon": 5.3878}},
        ],
        "systems": ["tenzinger-user"],
        "sources": [SOURCE],
        "confidence": "medium",
        "needs_verification": True,
        "notes": ["Christelijke GGZ, landelijk verspreid"],
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
    # 1) Vendors
    VENDORS.mkdir(parents=True, exist_ok=True)
    for vid, vdef in NEW_VENDORS.items():
        path = VENDORS / f"{vid}.yaml"
        if path.exists():
            print(f"SKIP  vendor  {vid}")
            continue
        dump(path, vdef)
        print(f"WRITE vendor  {vid}")

    # 2) Systems
    for sid, sdef in NEW_SYSTEMS.items():
        path = SYSTEMS / f"{sid}.yaml"
        if path.exists():
            print(f"SKIP  system  {sid}")
            continue
        dump(path, sdef)
        print(f"WRITE system  {sid}")

    # 3) Update existing GGZ orgs
    for org_id, systems, note in GGZ_EPDS:
        path = ORGS / f"{org_id}.yaml"
        if not path.exists():
            print(f"MISS  org     {org_id} (not on disk)", file=sys.stderr)
            continue
        data = load(path)
        data["systems"] = systems
        sources = list(data.get("sources") or [])
        if SOURCE not in sources:
            sources.append(SOURCE)
        data["sources"] = sources
        data["confidence"] = "medium"
        data["needs_verification"] = True
        if note:
            notes = data.get("notes") or []
            if note not in notes:
                notes.append(note)
            data["notes"] = notes
        dump(path, data)
        print(f"UPDT  org     {org_id:22s} systems={systems}")

    # 4) New GGZ orgs
    for org in NEW_GGZ_ORGS:
        path = ORGS / f"{org['id']}.yaml"
        if path.exists():
            print(f"SKIP  org     {org['id']} (already exists)")
            continue
        dump(path, org)
        print(f"WRITE org     {org['id']}")

    print("\nDone.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
