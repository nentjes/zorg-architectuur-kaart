# Viewer — Zorg Architectuur Kaart

Statische MapLibre GL JS viewer die de data uit `/data/` via
`compute_maturity.py` op een kaart zet. Achtergrond: PDOK
BRT-Achtergrondkaart (Kadaster, CC-BY). Geen Google, geen Mapbox.

## Lokaal bekijken

De viewer is een statische HTML+JS app maar moet via een HTTP-server
gedraaid worden (niet via `file://`) zodat `fetch()` werkt.

```bash
# 1. Genereer de data uit YAML
python3 scripts/compute_maturity.py
# → schrijft viewer/data/maturity_map.json

# 2. Start een lokale webserver vanuit de repo-root
cd viewer
python3 -m http.server 8000

# 3. Open in je browser
open http://localhost:8000
```

## Wat je ziet

- **Cirkels** = organisaties. Grootte = `total_score` (som van alle
  connection-scores waarin de org participeert). Grijze cirkels =
  orgs zonder gescoorde connections.
- **Lijnen** = connections. Kleur = `data_topology` van het netwerk:
  - 🟢 groen = federated (Trijn-model)
  - 🔵 blauw = hybrid (LSP)
  - 🔴 rood = centralized (vendor-lock-in risico)
- **Lijndikte** = `final_score` van de connection.
- **Lijnpatroon** = status: volle lijn voor production, streepjes
  voor pilot, dots voor planned.

Klik op een cirkel of lijn voor details.

## Dependencies

- **MapLibre GL JS v4.7.1** — via unpkg CDN (kan later lokaal
  geserveerd worden voor volledig air-gapped gebruik)
- **PDOK BRT WMTS-tiles** — direct van
  `service.pdok.nl/brt/achtergrondkaart/wmts/v2_0`

Geen npm build-stap, geen bundler, geen framework.
