#!/usr/bin/env python3
"""
import_manifest.py — Generic manifest → organization YAML importer

Leest een manifest-YAML (zie data/manifests/*.yaml) en genereert
per entity een YAML-bestand in data/organizations/. Ondersteunt
een optioneel overrides-bestand dat per org-id systeem- en
netwerk-info toevoegt die niet uit het manifest komt.

Manifest-structuur:
  version: 1
  default_source: claude-knowledge-2026-04
  default_confidence: low
  default_needs_verification: true
  entities:
    - id: amersfoort
      name: Gemeente Amersfoort
      sector: gemeente
      locations:
        - city: Amersfoort
          province: Utrecht
          country: NL
          coordinates:
            lat: 52.1561
            lon: 5.3878
      region_iza: iza-midden-nederland
      # optioneel: sources, confidence, needs_verification override
      # de defaults uit bovenaan het manifest

Overrides-structuur (optioneel):
  version: 1
  overrides:
    hus:
      systems: [medicom]
      confidence: high
      needs_verification: false
    huisartsen-eemland:
      systems: [medicom]

Usage:
  python3 scripts/import_manifest.py data/manifests/utrecht-v1.yaml
  python3 scripts/import_manifest.py data/manifests/utrecht-v1.yaml \
      --overrides data/overrides/utrecht.yaml

Regels voor idempotentie:
- Als data/organizations/<id>.yaml al bestaat: NIET overschrijven,
  alleen skip met melding (en rapporteer conflict). Dit beschermt
  handmatige edits en bestaande Sprint 1/1b data.
- --force vlag overschrijft wel (gebruik met zorg).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ORGS_DIR = REPO_ROOT / "data" / "organizations"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(data: dict, path: Path) -> None:
    """Write YAML with a stable, human-friendly field order."""
    # Preserve insertion order
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            data,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100,
        )


def build_org(
    entity: dict,
    defaults: dict,
    override: dict | None,
) -> dict:
    """Merge entity + manifest defaults + overrides into final org dict."""
    org: dict[str, Any] = {
        "id": entity["id"],
        "type": "organization",
        "name": entity["name"],
    }

    if entity.get("aliases"):
        org["aliases"] = entity["aliases"]

    org["sector"] = entity["sector"]

    if entity.get("subtype"):
        org["subtype"] = entity["subtype"]
    if entity.get("parent_organization"):
        org["parent_organization"] = entity["parent_organization"]

    org["country"] = entity.get("country", "NL")

    if entity.get("locations"):
        org["locations"] = entity["locations"]

    if entity.get("region_iza"):
        org["region_iza"] = entity["region_iza"]
    if entity.get("region_roaz"):
        org["region_roaz"] = entity["region_roaz"]
    if entity.get("region_ggd"):
        org["region_ggd"] = entity["region_ggd"]

    # Systems: entity > override > none
    systems = entity.get("systems")
    if override and "systems" in override:
        systems = override["systems"]
    if systems:
        org["systems"] = systems

    # Networks: idem
    networks = entity.get("networks")
    if override and "networks" in override:
        networks = override["networks"]
    if networks:
        org["networks"] = networks

    # Sources: entity > default (override cannot replace, only extend)
    sources = entity.get("sources") or [defaults.get("default_source")]
    if override and override.get("extra_sources"):
        sources = list(dict.fromkeys([*sources, *override["extra_sources"]]))
    org["sources"] = sources

    # Confidence / needs_verification: entity > override > default
    confidence = entity.get("confidence") or defaults.get("default_confidence")
    if override and "confidence" in override:
        confidence = override["confidence"]
    if confidence:
        org["confidence"] = confidence

    needs_ver = entity.get("needs_verification")
    if needs_ver is None:
        needs_ver = defaults.get("default_needs_verification", True)
    if override and "needs_verification" in override:
        needs_ver = override["needs_verification"]
    org["needs_verification"] = needs_ver

    return org


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Manifest YAML file")
    parser.add_argument(
        "--overrides",
        type=Path,
        help="Optional overrides YAML file",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing organization YAML files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be written, don't write",
    )
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"ERROR: manifest not found: {args.manifest}", file=sys.stderr)
        return 1

    manifest = load_yaml(args.manifest)
    defaults = {
        "default_source": manifest.get("default_source", "claude-knowledge-2026-04"),
        "default_confidence": manifest.get("default_confidence", "low"),
        "default_needs_verification": manifest.get("default_needs_verification", True),
    }

    overrides: dict[str, dict] = {}
    if args.overrides and args.overrides.exists():
        overrides_doc = load_yaml(args.overrides)
        overrides = overrides_doc.get("overrides", {}) or {}
        print(f"Loaded {len(overrides)} overrides from {args.overrides}", file=sys.stderr)

    entities = manifest.get("entities") or []
    if not entities:
        print("ERROR: manifest has no 'entities' list", file=sys.stderr)
        return 1

    ORGS_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    conflicts = 0

    for entity in entities:
        org_id = entity.get("id")
        if not org_id:
            print(f"WARNING: entity without id: {entity.get('name', '?')}", file=sys.stderr)
            continue

        target = ORGS_DIR / f"{org_id}.yaml"
        override = overrides.get(org_id)

        if target.exists() and not args.force:
            # Don't touch existing files
            existing = load_yaml(target)
            existing_sources = set(existing.get("sources") or [])
            manifest_source = defaults["default_source"]
            if manifest_source not in existing_sources:
                # Different provenance — flag
                print(
                    f"SKIP  {org_id} (exists from {sorted(existing_sources)})",
                    file=sys.stderr,
                )
            else:
                print(f"SKIP  {org_id} (already imported)", file=sys.stderr)
            skipped += 1
            continue

        org = build_org(entity, defaults, override)

        if args.dry_run:
            print(f"DRY   {org_id}", file=sys.stderr)
        else:
            dump_yaml(org, target)
            marker = "OVR " if override else "WRITE"
            print(f"{marker} {org_id}", file=sys.stderr)
        written += 1

    print("", file=sys.stderr)
    print(f"Written: {written}   Skipped: {skipped}   Conflicts: {conflicts}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
