#!/usr/bin/env python3
"""
compute_maturity.py — IZA Maturity Score engine

Leest alle entities uit /data/ en de gewichten uit
/schema/maturity-score.yaml, berekent per connection een
final_score volgens de formule in §9 van dat bestand, en
aggregeert per organization.

Output: /build/maturity.json met structuur:
  {
    "meta": {...},
    "connections": [{id, organization_a, organization_b, network,
                     breakdown: {paradigm_w, topology_w, ...},
                     raw_score, final_score}, ...],
    "organizations": [{id, name, total_score, participating_in: [...]}, ...]
  }

Usage:
  python3 scripts/compute_maturity.py                 # → build/maturity.json
  python3 scripts/compute_maturity.py --stdout        # → stdout
  python3 scripts/compute_maturity.py --verbose       # print breakdown

Dependencies: PyYAML
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from statistics import mean
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
SCHEMA_FILE = REPO_ROOT / "schema" / "maturity-score.yaml"
VIEWER_DATA_DIR = REPO_ROOT / "viewer" / "data"
OUTPUT_FILE = VIEWER_DATA_DIR / "maturity_map.json"

SCHEMA_VERSION = "0.1.1"

# Hardcoded geocode voor cities in de huidige dataset.
# v0.3-issue: vervangen door PDOK Locatieserver lookup met caching.
# Coördinaten in [lon, lat] WGS84 (GeoJSON-conventie).
CITY_COORDS: dict[str, list[float]] = {
    "Enschede":   [6.8937, 52.2215],
    "Hengelo":    [6.7930, 52.2661],
    "Almelo":     [6.6604, 52.3508],
    "Utrecht":    [5.1214, 52.0907],
    "Nieuwegein": [5.0806, 52.0296],
    "Hilversum":  [5.1760, 52.2292],
    "Blaricum":   [5.2500, 52.2711],
    "Naarden":    [5.1612, 52.2967],
}


# ---------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------

def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


ENTITY_DIRS = {
    "organizations",
    "systems",
    "vendors",
    "regions",
    "networks",
    "standards",
    "connections",
    "usecases",
    "programs",
}


def load_entities_by_type() -> dict[str, dict[str, dict]]:
    """Return {entity_type: {id: entity}} for all /data/ subdirs."""
    result: dict[str, dict[str, dict]] = {}
    for subdir in sorted(DATA_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        if subdir.name not in ENTITY_DIRS:
            # Skip non-entity folders like manifests/ and overrides/
            continue
        entity_type = subdir.name.rstrip("s")  # organizations → organization
        result[entity_type] = {}
        for yaml_file in sorted(subdir.glob("*.yaml")):
            entity = load_yaml(yaml_file)
            if entity is None:
                continue
            entity_id = entity.get("id")
            if not entity_id:
                raise ValueError(f"{yaml_file}: entity has no 'id' field")
            result[entity_type][entity_id] = entity
    return result


def load_weights() -> dict:
    schema = load_yaml(SCHEMA_FILE)
    if schema.get("version") != SCHEMA_VERSION:
        print(
            f"WARNING: maturity-score.yaml version is "
            f"{schema.get('version')}, script targets {SCHEMA_VERSION}",
            file=sys.stderr,
        )
    return schema


# ---------------------------------------------------------------
# Axis: transport paradigm
# ---------------------------------------------------------------

def resolve_paradigm(network: dict, weights: dict) -> tuple[str, float]:
    """Apply mapping rules in order; first match wins."""
    mapping = weights["transport_paradigm_mapping"]
    paradigm_weights = weights["transport_paradigm_weights"]

    standards_used = network.get("standards_used") or []
    network_type = network.get("network_type")
    network_id = network.get("id")

    for rule in mapping:
        if "else" in rule:
            paradigm = rule["else"]
            return paradigm, paradigm_weights[paradigm]

        condition = rule["if"]
        match = True
        if "standards_used_contains_any" in condition:
            needed = condition["standards_used_contains_any"]
            if not any(s in standards_used for s in needed):
                match = False
        if "network_type" in condition and match:
            if condition["network_type"] != network_type:
                match = False
        if "id" in condition and match:
            if condition["id"] != network_id:
                match = False

        if match:
            paradigm = rule["then"]
            return paradigm, paradigm_weights[paradigm]

    raise RuntimeError(
        f"No paradigm rule matched for network {network_id} — "
        f"mapping must always have an 'else' rule"
    )


# ---------------------------------------------------------------
# Axis: recency decay
# ---------------------------------------------------------------

def compute_recency_weight(connection: dict, weights: dict) -> float:
    decay = weights["recency_decay"]
    if decay.get("type") != "stepped":
        raise NotImplementedError("Only 'stepped' recency_decay supported")

    validated_at = connection.get("validated_at")
    if not validated_at:
        return decay["default_if_missing"]

    if isinstance(validated_at, str):
        ref_date = datetime.strptime(validated_at, "%Y-%m-%d").date()
    elif isinstance(validated_at, date):
        ref_date = validated_at
    else:
        return decay["default_if_missing"]

    today = date.today()
    months_old = (today.year - ref_date.year) * 12 + (today.month - ref_date.month)

    for step in decay["steps"]:
        max_months = step["max_months"]
        if max_months is None or months_old <= max_months:
            return step["weight"]
    return 0.0


# ---------------------------------------------------------------
# Axis: standard conformance
# ---------------------------------------------------------------

def compute_conformance_weight(
    connection: dict,
    entities: dict,
    weights: dict,
) -> float:
    bonus = weights["standard_conformance_bonus"]
    default = bonus["fallback_if_no_standard"]
    multiplier = bonus["multiplier"]

    standard_id = connection.get("standard")
    if not standard_id:
        return default

    org_a = entities["organization"].get(connection["organization_a"])
    org_b = entities["organization"].get(connection["organization_b"])
    if not org_a or not org_b:
        return default

    def org_supports_standard(org: dict, standard: str) -> bool:
        system_ids = org.get("systems") or []
        for sid in system_ids:
            system = entities["system"].get(sid)
            if system and standard in (system.get("standards_supported") or []):
                return True
        return False

    if org_supports_standard(org_a, standard_id) and org_supports_standard(
        org_b, standard_id
    ):
        return multiplier
    return default


# ---------------------------------------------------------------
# Axis: open standard bonus
# ---------------------------------------------------------------

def compute_open_standard_weight(connection: dict, weights: dict) -> float:
    bonus = weights["open_standard_bonus"]
    trigger = set(bonus["trigger_standards"])
    multiplier = bonus["multiplier"]

    standard_id = connection.get("standard")
    if standard_id and standard_id in trigger:
        return multiplier
    return 1.0


# ---------------------------------------------------------------
# Axis: data type
# ---------------------------------------------------------------

def compute_data_type_weight(connection: dict, weights: dict) -> float:
    data_weights = weights["data_type_weights"]
    data_types = connection.get("data_types") or []
    if not data_types:
        return data_weights.get("other", 0.2)
    values = [data_weights.get(dt, data_weights.get("other", 0.2)) for dt in data_types]
    return mean(values)


# ---------------------------------------------------------------
# Score per connection
# ---------------------------------------------------------------

def score_connection(
    connection: dict,
    entities: dict,
    weights: dict,
) -> dict:
    network_id = connection["network"]
    network = entities["network"].get(network_id)
    if not network:
        raise ValueError(
            f"Connection {connection['id']} references unknown network {network_id}"
        )

    paradigm_label, paradigm_w = resolve_paradigm(network, weights)
    topology_w = weights["topology_multipliers"][network["data_topology"]]
    status_w = weights["status_multipliers"][connection["status"]]
    data_w = compute_data_type_weight(connection, weights)
    recency_w = compute_recency_weight(connection, weights)
    conform_w = compute_conformance_weight(connection, entities, weights)
    open_w = compute_open_standard_weight(connection, weights)

    raw = paradigm_w * topology_w * status_w * data_w * recency_w
    final = raw * conform_w * open_w

    return {
        "id": connection["id"],
        "organization_a": connection["organization_a"],
        "organization_b": connection["organization_b"],
        "network": network_id,
        "network_name": network.get("name", network_id),
        "data_topology": network.get("data_topology"),
        "status": connection["status"],
        "data_types": connection.get("data_types") or [],
        "breakdown": {
            "paradigm_label": paradigm_label,
            "paradigm_w": round(paradigm_w, 4),
            "topology_w": round(topology_w, 4),
            "status_w": round(status_w, 4),
            "data_w": round(data_w, 4),
            "recency_w": round(recency_w, 4),
            "conform_w": round(conform_w, 4),
            "open_w": round(open_w, 4),
        },
        "raw_score": round(raw, 4),
        "final_score": round(final, 4),
    }


# ---------------------------------------------------------------
# Aggregation per organization
# ---------------------------------------------------------------

def geocode_organization(org: dict) -> list[float] | None:
    """Return [lon, lat] for the organization — primary location only.

    Used as a single-point anchor (e.g. connection lines between two orgs).
    For rendering all physical sites of an org, use extract_all_coords().
    """
    coords_list = extract_all_coords(org)
    return coords_list[0] if coords_list else None


def extract_all_coords(org: dict) -> list[list[float]]:
    """Return a list of [lon, lat] for EVERY location of the organization.

    Schema v0.2.1+ supports multi-site orgs (OLVG Oost + West, Reade,
    Merem Hilversum + Almere, ...). Each explicit `coordinates` block is
    used directly; for locations with only a `city`, CITY_COORDS is used
    as a fallback. Locations without any resolvable coord are skipped.
    """
    result: list[list[float]] = []
    for loc in org.get("locations") or []:
        coords = loc.get("coordinates")
        if coords and "lat" in coords and "lon" in coords:
            result.append([coords["lon"], coords["lat"]])
            continue
        city = loc.get("city")
        if city and city in CITY_COORDS:
            result.append(CITY_COORDS[city])
    # De-duplicate while preserving order (two locations may share the same
    # fallback city coord — don't render them as two identical dots).
    seen: set[tuple[float, float]] = set()
    unique: list[list[float]] = []
    for c in result:
        key = (c[0], c[1])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return unique


def aggregate_per_organization(
    scored_connections: list[dict],
    entities: dict,
) -> list[dict]:
    """Include ALL organizations, also those without connections."""
    totals: dict[str, dict] = {}

    # Step 1: seed with ALL organizations (score 0 if no connections)
    for org_id, org in entities.get("organization", {}).items():
        totals[org_id] = {
            "id": org_id,
            "name": org.get("name", org_id),
            "sector": org.get("sector"),
            "subtype": org.get("subtype"),
            "region_iza": org.get("region_iza"),
            "coord": geocode_organization(org),  # [lon, lat] or None (primary)
            "coords": extract_all_coords(org),   # all locations (multi-site)
            "total_score": 0.0,
            "participating_in": [],
        }

    # Step 2: accumulate scores from connections
    for conn in scored_connections:
        for role in ("organization_a", "organization_b"):
            org_id = conn[role]
            if org_id not in totals:
                # connection references an unknown org — should not happen
                # if cross-refs are valid, but degrade gracefully
                totals[org_id] = {
                    "id": org_id,
                    "name": org_id,
                    "sector": None,
                    "subtype": None,
                    "region_iza": None,
                    "coord": None,
                    "coords": [],
                    "total_score": 0.0,
                    "participating_in": [],
                }
            totals[org_id]["total_score"] += conn["final_score"]
            totals[org_id]["participating_in"].append(conn["id"])

    for org in totals.values():
        org["total_score"] = round(org["total_score"], 4)

    return sorted(totals.values(), key=lambda o: o["total_score"], reverse=True)


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

def _git(*args: str) -> str | None:
    """Run a git command and return stripped stdout, or None on failure."""
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def build_output(entities: dict, weights: dict) -> dict:
    connections = list(entities.get("connection", {}).values())
    scored = [score_connection(c, entities, weights) for c in connections]
    scored_sorted = sorted(scored, key=lambda c: c["final_score"], reverse=True)
    orgs = aggregate_per_organization(scored, entities)

    git_sha = _git("rev-parse", "--short", "HEAD")
    git_branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    git_dirty = bool(_git("status", "--porcelain"))

    return {
        "meta": {
            "schema_version": weights.get("version"),
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "git_sha": git_sha,
            "git_branch": git_branch,
            "git_dirty": git_dirty,
            "n_connections": len(scored),
            "n_organizations_scored": len(orgs),
            "formula": weights.get("formula"),
        },
        "connections": scored_sorted,
        "organizations": orgs,
    }


def print_summary(output: dict, verbose: bool) -> None:
    print(f"schema_version:   {output['meta']['schema_version']}", file=sys.stderr)
    print(f"connections:      {output['meta']['n_connections']}", file=sys.stderr)
    print(f"organizations:    {output['meta']['n_organizations_scored']}", file=sys.stderr)
    print("", file=sys.stderr)
    print("Top connections by final_score:", file=sys.stderr)
    for c in output["connections"][:10]:
        label = f"{c['organization_a']} ↔ {c['organization_b']} via {c['network']}"
        print(f"  {c['final_score']:.3f}  {label}  [{c['status']}]", file=sys.stderr)
        if verbose:
            b = c["breakdown"]
            print(
                f"          paradigm={b['paradigm_label']}({b['paradigm_w']}) "
                f"topo={b['topology_w']} status={b['status_w']} "
                f"data={b['data_w']} rec={b['recency_w']} "
                f"conf={b['conform_w']} open={b['open_w']}",
                file=sys.stderr,
            )
    print("", file=sys.stderr)
    print("Top organizations by total_score:", file=sys.stderr)
    for o in output["organizations"][:10]:
        print(
            f"  {o['total_score']:.3f}  {o['name']} "
            f"({o['sector']}, {o['region_iza']})",
            file=sys.stderr,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="Write JSON to stdout instead of build/maturity.json")
    parser.add_argument("--verbose", action="store_true", help="Print per-axis breakdown")
    args = parser.parse_args()

    entities = load_entities_by_type()
    weights = load_weights()
    output = build_output(entities, weights)

    if args.stdout:
        json.dump(output, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        VIEWER_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with OUTPUT_FILE.open("w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote {OUTPUT_FILE.relative_to(REPO_ROOT)}", file=sys.stderr)

    print_summary(output, args.verbose)
    return 0


if __name__ == "__main__":
    sys.exit(main())
