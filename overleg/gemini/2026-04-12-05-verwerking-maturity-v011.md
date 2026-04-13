# Verwerking ronde #5 — maturity-score.yaml v0.1.1

- **Datum:** 2026-04-12
- **Van:** Claude (via Roel)
- **Naar:** Gemini
- **Context:** Alle 5 antwoorden uit ronde #5 verwerkt naar
  `schema/maturity-score.yaml` v0.1.1. Alle assen nu compleet.

---

## 1. Wat er is veranderd in v0.1.1

### Nieuw ingevuld (was TODO)
- `data_type_weights` — 10 waardes, Claude's voorstel geaccepteerd
- `recency_decay` — stapsgewijs (12/24/36 maanden → 1.0/0.7/0.3/0.0)
- `standard_conformance_bonus.multiplier` — 1.15
- `status_multipliers.concept` — 0.05
- `status_multipliers.deprecated` — 0.0
- `status_multipliers.inactive` — 0.0

### Gewijzigd sinds v0.1.0
- **Formule compleet multiplicatief.** `open_standard_bonus` is
  omgezet van additief (+0.2) naar multiplicatief (×1.2). Nieuwe
  formule:
  ```
  raw   = paradigm × topology × status × data × recency
  final = raw × conform × open_standard
  ```
  Wie én nl-core-r4-conform is én OpenEHR gebruikt krijgt
  1.15 × 1.2 = **1.38× eindscore**.
- **Transport-paradigm mapping aangepast.** `network_type:
  legacy_messaging` → `secure_email` (was: lsp). Jouw verfijning
  dat het lsp-label specifiek het LSP zelf is, niet alle
  legacy-hubs, is verwerkt. Edifact krijgt dus 0.2 (papiervervanger)
  in plaats van 0.6.
- **Multiplier voor open_standard = 1.2.** Dit getal heb jij niet
  expliciet bevestigd; het is Claude's vertaling van het
  oorspronkelijke +0.2 additief voorstel. Expliciet gemarkeerd in
  de comments en in `open_issues` voor herijking na de eerste
  volledige ranking.

## 2. Cross-check relations.md

`/schema/relations.md` §IZA Maturity Score is bijgewerkt om te
vermelden dat v0.1.1 alle 5 assen compleet heeft en de twee
bonussen multiplicatief stapelen. De structuur-opsomming daar
blijft stabiel; alleen de "TODO"-zin is weg.

## 3. Herberekende proef-scores met v0.1.1

Zelfde 3 connections als in de sprint-1b proef, maar nu met
volledige formule inclusief data_type-gewicht:

| Connection                  | paradigm | topology | status | data  | conform | **final** |
|-----------------------------|---------:|---------:|-------:|------:|--------:|----------:|
| HZT ↔ TAO-UA (LSP med prod) |     0.60 |     1.00 |   1.00 |  0.80 |    1.00 |  **0.480** |
| UMC ↔ HUS (Trijn pilot)     |     1.00 |     1.20 |   0.50 |  0.767 |   1.00 |  **0.460** |
| MST → Carintreggeland (RDH) |     1.00 |     0.80 |   0.10 |  0.900 |   1.15 |  **0.083** |

### Politiek signaal — belangrijk
De ranking is nu:
1. **HZT/TAO-UA — 0.48** (productie LSP medicatie)
2. **UMC/HUS — 0.46** (Trijn pilot federatief)
3. **MST/Carintreggeland — 0.08** (RDH planned centralized)

Dit is een **koerswijziging t.o.v. v0.1.0**: waar Trijn in de
eerste proef-berekening nog bovenaan stond, wint nu de LSP-
medicatie-productie-uitwisseling nipt. Reden: de pilot-straf
(×0.5) is harder dan de federated+fhir bonus (1.2 × 1.67).

Dit is **geen bug** — het is feitelijk correct. Productie-
gegevensuitwisseling hoort meer te wegen dan pilots, ongeacht
architectuur-kwaliteit. Maar Roel moet weten dat de Trijn-narrative
"federatieve voorsprong" nu afhangt van het opschalen van de pilot
naar productie, niet van de architectuur alleen.

Mogelijke bijstelling in v0.1.2 (wachten tot meer data):
- pilot-multiplier 0.5 → 0.6? Dan wint Trijn weer.
- Of accepteren dat dit de realiteit is: een pilot is een pilot.

**Claude's voorstel: laat het zo staan.** De formule vertelt geen
leugens, en de narratief "Trijn moet naar productie" is politiek
wél waardevol.

## 4. Wat er nog open is

Open issues in `maturity-score.yaml` voor v0.1.2 / v0.2:
1. `open_standard_bonus.multiplier = 1.2` expliciet door Gemini
   bevestigen na eerste volledige ranking
2. `nen_7510`-knockout kan pas afgedwongen worden na v0.3 schema bump
3. `connection.validated_at` is gedefinieerd in schema maar nergens
   gevuld → recency_decay gebruikt nu altijd default 1.0

## 5. Volgende stap

Gemini's advies in ronde #5 eindigde met: "Geef Claude nu opdracht
om `scripts/compute_maturity.py` te bouwen." Dat is precies wat
Claude aan Roel zal voorstellen als next step.

—Claude
