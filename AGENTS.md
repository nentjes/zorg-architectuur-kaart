# AGENTS.md — conventies voor AI-assistenten die aan deze repo werken

> **Voor elke AI (Claude, Gemini, etc.) die in deze repo werkt:**
> Lees dit bestand eerst. De structuur hieronder is de actuele waarheid,
> ongeacht wat externe briefings of oudere prompts beweren.

## Missie

"Zorg Architectuur Kaart" — een publieke, YAML-in-Git kaart van de
Nederlandse zorg-IT, als beleidsinstrument om dure dubbelingen
(zoals regionale platforms) zichtbaar te maken.

Eigenaar: Roel Nentjes. ICT-manager-achtergrond in huisartsenzorg,
ziekenhuizen (NVZ), revalidatie. Valideert data via zijn netwerk +
LinkedIn.

## Repository-structuur (actueel)

```
zorg-architectuur-kaart/
├── README.md
├── AGENTS.md              ← dit bestand
├── schema/
│   ├── schema.yaml        ← JSON-Schema voor alle entity-types
│   ├── entities.md        ← ontologie-beschrijving v0.2.1
│   ├── relations.md
│   └── maturity-score.yaml ← IZA Maturity Score v0.1.1
├── data/
│   ├── organizations/     ← één YAML per organisatie (zie hieronder)
│   ├── systems/           ← één YAML per informatiesysteem (EPD/HIS/AIS/ECD)
│   ├── vendors/           ← één YAML per leverancier
│   ├── networks/          ← uitwisselings-netwerken (LSP, Twiin, Nuts, ...)
│   ├── standards/         ← HL7/FHIR/Zib/etc.
│   ├── connections/       ← concrete data-uitwisselingen tussen orgs
│   ├── regions/           ← IZA-regio's, ROAZ, GGD
│   ├── usecases/
│   ├── programs/
│   ├── manifests/         ← bulk-ingest manifests (zie pipeline)
│   └── overrides/         ← hand-overrides bovenop manifests
├── scripts/
│   ├── import_manifest.py ← manifest → organizations/*.yaml
│   ├── compute_maturity.py ← bouw viewer/data/maturity_map.json
│   └── seed_*.py          ← éénmalige data-seeds (revalidatie, ggz, ...)
├── sources/
│   └── sources.yaml       ← register van alle bron-tags
└── viewer/
    ├── index.html         ← MapLibre kaart
    └── data/
        └── maturity_map.json ← AUTO-GENERATED, niet committen met de hand
```

## Veel gemaakte fouten (lees dit twee keer)

**Géén** van deze paden bestaat — noem ze niet in instructies:

- ❌ `data/entities/<sector>.yaml` — bestaat niet. Gebruik `data/organizations/<id>.yaml`, één file per org.
- ❌ `data/vendors.yaml` — bestaat niet. Gebruik `data/vendors/<id>.yaml` (folder).
- ❌ `data/systems.yaml` — idem. Gebruik `data/systems/<id>.yaml`.
- ❌ `data/ggz.yaml`, `data/huisartsen.yaml`, etc. — nooit bestaan. Sector zit als veld in elke org-YAML, niet als bestandsnaam.

## Entity-model (8 types + programs)

Elke entity-YAML is een "document" met minimaal `id`, `type`, `name`.
Types in scope voor deze repo:

| Type | Folder | Voorbeeld-id |
|---|---|---|
| organization | `data/organizations/` | `umc-utrecht`, `hus`, `gem-amersfoort` |
| system | `data/systems/` | `chipsoft-hix`, `tenzinger-user` |
| vendor | `data/vendors/` | `chipsoft`, `tenzinger` |
| network | `data/networks/` | `lsp`, `twiin` |
| standard | `data/standards/` | `zib-2020`, `nl-core-r4` |
| connection | `data/connections/` | `hzt-tao-ua-lsp-medicatie` |
| region | `data/regions/` | `iza-midden-nederland` |
| usecase | `data/usecases/` | `medicatieoverdracht-2e-1e-lijn` |
| program | `data/programs/` | `iza-akkoord` |

Schema: zie `schema/schema.yaml` en `schema/entities.md`.

### Organization-YAML template

```yaml
id: my-org
type: organization
name: Mijn Organisatie
aliases: ["Alt naam"]        # optioneel
sector: ziekenhuis           # enum uit schema
subtype: topklinisch         # optioneel
country: NL
locations:
  - city: Utrecht
    province: Utrecht
    country: NL
    coordinates: {lat: 52.0907, lon: 5.1214}
region_iza: iza-midden-nederland   # optioneel
systems:                     # referenties naar data/systems/*.yaml ids
  - chipsoft-hix
networks:                    # referenties naar data/networks/*.yaml ids
  - lsp
sources:                     # bron-tags, zie sources/sources.yaml
  - claude-knowledge-2026-04
confidence: low              # low | medium | high
needs_verification: true     # flip naar false zodra gevalideerd
notes:                       # optioneel, vrij tekstveld
  - "Implementatie datum onbekend"
```

## Data-pipeline voor bulk-import

Voor coarse-grained bulk-ingest: **niet direct 100 YAML-files maken**,
maar één manifest in `data/manifests/<naam>.yaml`:

```yaml
version: 1
default_source: claude-knowledge-2026-04
default_confidence: low
default_needs_verification: true

entities:
  - id: gem-amersfoort
    name: "Gemeente Amersfoort"
    sector: gemeente
    locations:
      - city: Amersfoort
        province: Utrecht
        country: NL
        coordinates: {lat: 52.1561, lon: 5.3878}
    region_iza: iza-midden-nederland
```

Dan:

```bash
python3 scripts/import_manifest.py data/manifests/<naam>.yaml
```

De importer is **idempotent**: bestaande org-files worden niet
overschreven tenzij `--force`. Dat beschermt handmatige edits.

## Confidence-ladder (belangrijk!)

| Confidence | Wanneer | Source-tag bijv. |
|---|---|---|
| `low` | LLM-guess zonder bron-check | `claude-knowledge-2026-04` |
| `medium` | Research-niveau (Gemini/deep research/websearch) | `gemini-ggz-research-2026-04` |
| `high` | Primaire bron (hard adres, PDF, Roel's eigen netwerk/Excel) | `roel-private-excel-2026-04`, plus URL in sources.yaml |

`needs_verification: true` staat default op alles wat niet `high` is.
Flip naar `false` pas als een menselijk netwerk heeft gevalideerd.

## Viewer

`viewer/index.html` is een MapLibre-kaart met PDOK BRT-tiles. Data komt
uit `viewer/data/maturity_map.json`, wat automatisch wordt gegenereerd
door `scripts/compute_maturity.py`. **Niet handmatig editen.**

Lokaal draaien:
```bash
cd viewer
python3 -m http.server 8000
# → http://localhost:8000
```

## Sandbox-beperkingen voor AI-assistenten

Binnen Claude Code (en vergelijkbare sandboxes) zijn deze tools
**niet beschikbaar**:

- Geen externe HTTP-calls → dus **geen PDOK-lookups**, geen
  AGB-register, geen KVK-scraping. Als een briefing "gebruik PDOK"
  zegt, vertaal dat naar: "gebruik bekende coords of markeer
  `needs_verification: true`".
- Geen GitHub CLI — GitHub-operations gaan via de MCP-integratie als
  die beschikbaar is, anders niet.

Voor geografie: hand-coded city-coords zijn de workaround. Voor later:
een offline CBS-gemeente-coord-bestand in `data/` checken als seed.

## Prompt-patroon voor nieuwe data-toevoegingen

Als je een AI vraagt om data toe te voegen, verwijs naar dit bestand:

> "Voeg de GGZ-EPD-data hieronder toe volgens `AGENTS.md`:
> - nieuwe systems → `data/systems/<id>.yaml`
> - nieuwe vendors → `data/vendors/<id>.yaml`
> - updates op orgs → `data/organizations/<id>.yaml`
> - `source:` tag + juiste `confidence`
>
> [plak hier de tabel]"

Dat voorkomt dat de AI naar niet-bestaande paden schrijft.

## Commit-stijl

Sprint-commits met prefix `Sprint <nummer>[letter]:`. Voorbeeld:
```
Sprint 4a: apotheek-ketens + GGZ + huisartsen-zorggroepen + VVT
Sprint 4a+: revalidatie-EPDs uit Roel's privé-Excel
Sprint 4a++: GGZ EPD-mapping uit Gemini-research
```

Altijd meegeven in de body:
- wat veranderde
- de `confidence`-niveau
- kaart-groei (x → y orgs)
- source-tag
