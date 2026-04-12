# Relations — Zorg Architectuur Kaart edge-model v0.1

## Graph overview

De kaart is een graaf. **Nodes** zijn de zes entiteiten uit `entities.md`
(Organization, System, Vendor, Region, Network, Standard). **Edges** zijn
de relaties tussen die nodes.

We onderscheiden twee soorten edges:

- **Inline edges** — een veld op een node dat verwijst naar de `id` van
  een andere node. Eenvoudig, direct diff-baar, geen aparte file.
- **Entity edges** — een `Connection`-entiteit in een eigen YAML-file
  onder `/data/connections/`. Alleen nodig wanneer de edge zelf rijke
  metadata heeft die onafhankelijk valideerbaar en bron-gebonden moet zijn.

## Inline edges

| Edge | Source | Target | Cardinaliteit | Waar opgeslagen | Bron-eis |
|---|---|---|---|---|---|
| USES_SYSTEM | Organization | System | many-to-many | `systems: [<id>]` op Organization | inherent via Organization.sources |
| LOCATED_IN_IZA | Organization | Region | many-to-one | `region_iza: <id>` op Organization | inherent |
| LOCATED_IN_ROAZ | Organization | Region | many-to-one | `region_roaz: <id>` op Organization | inherent |
| LOCATED_IN_GGD | Organization | Region | many-to-one | `region_ggd: <id>` op Organization | inherent |
| SUBSIDIARY_OF | Organization | Organization | many-to-one | `parent_organization: <id>` | inherent |
| SUPPLIED_BY | System | Vendor | many-to-one | `vendor: <id>` op System | inherent |
| IMPLEMENTS_STANDARD | System | Standard | many-to-many | `standards_supported: [<id>]` op System | **leveranciers-PR mag niet enige bron zijn** |
| OPERATES_NETWORK | Organization | Network | one-to-one per network | `operator: <id>` op Network | inherent |
| NETWORK_USES_STANDARD | Network | Standard | many-to-many | `standards_used: [<id>]` op Network | inherent |
| PARTICIPATES_IN_NETWORK | Organization | Network | many-to-many | `networks: [<id>]` op Organization | **vereist publieke bron die de specifieke aansluiting noemt** |
| LEAD_OF_REGION | Region | Organization | one-to-one | `lead_organization: <id>` op Region | inherent |
| PARTICIPATES_IN_REGION | Region | Organization | many-to-many | `participating_organizations: [<id>]` op Region | inherent |

Inline edges worden door de schema-validator gecheckt op:
1. Bestaat het target-`id` als file in de juiste `/data/<type>/` folder?
2. Is het type van het target correct (bijv. `systems: [<id>]` moet naar
   System verwijzen, niet naar Vendor)?

## Entity edges: Connection

Een `Connection` is de enige edge die als zelfstandige entiteit leeft.
Redenen:

1. **Bron-eisen zijn strenger.** Een Connection claimt dat *twee specifieke
   organisaties* data uitwisselen — dat verdient één of meer bronnen per
   edge, niet alleen per node.
2. **Rijke metadata.** Status, datatypes, validatiedatum, richting — dat
   past niet in een inline list.
3. **Onafhankelijk valideerbaar.** Een Connection kan `needs_verification:
   true` krijgen zonder dat de organisaties-entiteiten daarmee verdacht
   worden.
4. **Telbaar voor de IZA Maturity Score.** De score leest uit
   `/data/connections/`, niet uit inline-lijsten op organisaties.

### Wanneer moet iets een `Connection` zijn?

Als het antwoord op minstens één van deze vragen ja is:
- Is de claim "organisatie A wisselt specifiek met organisatie B data uit"?
- Heeft de claim eigen metadata (datum, status, datatypes)?
- Moet de claim apart valideerbaar en bron-gebonden zijn?

Zo nee → inline edge.
Zo ja → `Connection`-file in `/data/connections/`.

### Cardinaliteits-regels voor Connection

- `organization_a` en `organization_b` zijn altijd *verschillend*
- De volgorde is lexicografisch: `organization_a < organization_b` als
  strings, zodat een connection-tussen-A-en-B maar één keer in de data kan
  staan (geen duplicates)
- Interne koppelingen binnen één organisatie horen niet op deze kaart

## Consistentie en dangling references

De schema-auditor (`governance-schema-auditor`) controleert bij elke PR:

- Elke inline edge verwijst naar een bestaande entiteit van het juiste type
- Elke Connection-edge verwijst naar bestaande Organizations en een
  bestaand Network
- Er zijn geen circulaire `parent_organization`-ketens
- Er zijn geen duplicate IDs over entity types heen

## IZA Maturity Score — de structuur

De score voor een `Organization` is een functie van de `Connection`s
waaraan die organisatie deelneemt:

    score(org) = Σ weighted_value(conn)
                 over alle conn waar org ∈ {conn.organization_a, conn.organization_b}

waarbij `weighted_value` een functie is van:

- **Network-type gewicht** — bijv. een landelijke hub (LSP) weegt anders
  dan een regionale XDS
- **Data-type gewicht** — bijv. volledige care transfer weegt meer dan een
  enkele afspraak
- **Status multiplier** — `active` weegt vol, `planned` weegt fractioneel,
  `deprecated` weegt nul of negatief
- **Recentheids-factor** — `validated_at` ouder dan 12 maanden schaalt af
- **Standaard-conformiteit bonus** — Connections met een gespecificeerde
  `standard:` die door beide systemen wordt ondersteund krijgen een bonus

De exacte gewichten (numbers) staan **niet** in dit document. Ze horen in
`/schema/maturity-score.yaml`, een apart file dat door de
**Strategische Architect** (Gemini) wordt gevuld en onderhouden. Dat file
is in v0.1 opzettelijk leeg met alleen een `TODO:`-structuur.

Reden voor de splitsing: de ontologie (dit document) is neutraal en
feitelijk. De scoring-logica is methodologie en heeft aparte
bron-onderbouwing nodig. Twee verschillende reviewers, twee verschillende
discussies.

## Geen verborgen edges

Alle relaties die in de graaf bestaan, moeten expliciet in een YAML-bestand
staan. Er mogen **geen** afgeleide relaties zijn die alleen in de viewer,
de build-laag of een cache-laag bestaan. Dit is de kern van "onvervalsbaar":
de graaf zoals die op de kaart verschijnt, is één-op-één de graaf zoals die
in git staat.

Als een build-script (bijv. `yaml_to_duckdb.py`) edges *afleidt*, moeten
die afleidingen deterministisch zijn en herleidbaar naar de YAML-bron, en
moeten ze in de viewer-UI duidelijk herkenbaar zijn als afgeleid in plaats
van als primair feit.
