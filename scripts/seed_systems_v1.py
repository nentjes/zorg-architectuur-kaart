#!/usr/bin/env python3
"""
seed_systems_v1.py — één-shot LLM-kennis-seed voor Sprint 3 systemen

Vult per org welk EPD/HIS/AIS/ECD ze draaien, op basis van mijn
(Claude's) kennis t/m april 2026. Alles blijft confidence: low +
needs_verification: true zodat Roel's netwerk het kan valideren.

Scope:
- Ziekenhuizen NL: HiX default, Epic uitzonderingen (±10 stuks)
- Huisartsen Utrecht-regio: Medicom (dominant in deze regio)
- RAVU: CityGIS (landelijke ambulance-standaard)

Niet in dit script (onzeker):
- GGZ (User/Glims/Epic mix)
- VVT (Nedap/Mozaïk/Ecare mix)
- MUMC, UMCG soms niet-HiX (laat open tot bevestigd)
- Landelijke RAVs anders dan RAVU

Run: python3 scripts/seed_systems_v1.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ORGS_DIR = REPO_ROOT / "data" / "organizations"

# -------------------------------------------------------------
# Epic-NL ziekenhuizen (zekere kennis 2024-2026)
# -------------------------------------------------------------
EPIC_HOSPITALS = [
    "amsterdam-umc",       # AMC + VUmc beiden Epic
    "radboudumc",          # Epic sinds 2018
    "catharina-ziekenhuis",
    "isala",               # gemigreerd naar Epic
    "mmc",                 # Máxima MC Epic
    "rijnstate",
    "bernhoven",
    "haga",
    "st-jansdal",
    "umcg",                # Epic-implementatie doorgevoerd
]

# -------------------------------------------------------------
# HiX-default: alle overige NL ziekenhuizen waar HiX dominant is.
# UMCU en St Antonius staan niet in deze lijst want die hebben al
# systems gezet in Sprint 1/1b.
# -------------------------------------------------------------
HIX_HOSPITALS = [
    # Utrecht provincie (uit utrecht-v1.yaml)
    "diakonessenhuis",
    "meander-mc",
    "prinses-maxima-centrum",
    # NL UMC's (non-Epic)
    "erasmus-mc",
    "lumc",
    # STZ
    "amphia",
    "albert-schweitzer",
    "cwz",
    "deventer-ziekenhuis",
    "etz",
    "gelre-ziekenhuizen",
    "jbz",
    "martini-ziekenhuis",
    "maasstad",
    "mcl",
    "nwz",
    "olvg",
    "reinier-de-graaf",
    "slingeland",
    "spaarne-gasthuis",
    "viecuri",
    "zuyderland-mc",
    # Algemeen NVZ
    "adrz",
    "antonius-zh-sneek",
    "bravis",
    "dijklander",
    "elkerliek",
    "flevoziekenhuis",
    "franciscus",
    "hmc",
    "ikazia",
    "ijsselland",
    "lange-land",
    "laurentius",
    "maasziekenhuis-pantein",
    "nij-smellinghe",
    "ozg",
    "rivas-beatrix",
    "rkz",
    "saxenburgh",
    "st-anna",
    "skb",
    "tjongerschans",
    "treant",
    "van-weel-bethesda",
    "wza",
    "zaans-mc",
    "ziekenhuis-amstelland",
    "zgv",
    # Categoraal
    "avl",
    "oogziekenhuis-rotterdam",
    "sint-maartenskliniek",
]

# -------------------------------------------------------------
# Medicom-dominante huisartsen­zorggroepen in de Utrecht-regio
# -------------------------------------------------------------
MEDICOM_HUISARTSEN = [
    "hus",
    "huisartsen-eemland",
    "leidsche-rijn-julius-gc",
    "unicum-huisartsenzorg",
    "huw",
    "zorggroep-regio-amersfoort",
]

# -------------------------------------------------------------
# CityGIS ambulance (RAVU zeker; landelijke uitrol deels)
# -------------------------------------------------------------
CITYGIS_RAVS = ["ravu"]


def load_org(org_id: str) -> dict | None:
    path = ORGS_DIR / f"{org_id}.yaml"
    if not path.exists():
        print(f"MISS  {org_id} (yaml niet gevonden)", file=sys.stderr)
        return None
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_org(org_id: str, data: dict) -> None:
    path = ORGS_DIR / f"{org_id}.yaml"
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100,
        )


def seed_org(org_id: str, systems: list[str], networks: list[str]) -> None:
    data = load_org(org_id)
    if data is None:
        return

    # Merge systems
    existing_systems = set(data.get("systems") or [])
    new_systems = existing_systems | set(systems)
    if new_systems != existing_systems:
        data["systems"] = sorted(new_systems)

    # Merge networks
    existing_networks = set(data.get("networks") or [])
    new_networks = existing_networks | set(networks)
    if new_networks != existing_networks:
        data["networks"] = sorted(new_networks)

    # Zorg dat needs_verification op true blijft (seed-status)
    # en source claude-knowledge erbij staat
    sources = set(data.get("sources") or [])
    sources.add("claude-knowledge-2026-04")
    data["sources"] = sorted(sources)
    data.setdefault("confidence", "low")
    data["needs_verification"] = True

    save_org(org_id, data)
    print(f"SEED  {org_id:40s} systems={systems} networks={networks}")


def main() -> int:
    total = 0

    print("=== Epic-ziekenhuizen NL ===")
    for h in EPIC_HOSPITALS:
        seed_org(h, ["epic-epd"], ["lsp"])
        total += 1

    print("\n=== HiX-ziekenhuizen NL (default) ===")
    for h in HIX_HOSPITALS:
        seed_org(h, ["chipsoft-hix"], ["lsp"])
        total += 1

    print("\n=== Medicom-huisartsen Utrecht ===")
    for h in MEDICOM_HUISARTSEN:
        seed_org(h, ["medicom"], ["lsp"])
        total += 1

    print("\n=== CityGIS ambulance ===")
    for h in CITYGIS_RAVS:
        seed_org(h, ["citygis-ambulance"], ["lsp"])
        total += 1

    print(f"\nSeeded {total} orgs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
