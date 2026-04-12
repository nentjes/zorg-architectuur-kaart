# Relations — Zorg Architectuur Kaart edge-model v0.2

## Graph overview

De kaart is een graaf. **Nodes** zijn de acht non-edge-entiteiten uit
`entities.md` (Organization, System, Vendor, Region, Network, Standard,
UseCase, Program). **Edges** zijn de relaties tussen die nodes.

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
| DEPLOYED_IN | System | Network | many-to-many | `deployed_in: [<id>]` op System *(v0.2)* | inherent via System.sources |
| OPERATES_NETWORK | Organization | Network | one-to-one per network | `operator: <id>` op Network | inherent |
| NETWORK_USES_STANDARD | Network | Standard | many-to-many | `standards_used: [<id>]` op Network | inherent |
| PARTICIPATES_IN_NETWORK | Organization | Network | many-to-many | `networks: [<id>]` op Organization | **vereist publieke bron die de specifieke aansluiting noemt** |
| LEAD_OF_REGION | Region | Organization | one-to-one | `lead_organization: <id>` op Region | inherent |
| PARTICIPATES_IN_REGION | Region | Organization | many-to-many | `participating_organizations: [<id>]` op Region | inherent |
| CHILD_VENDOR_OF | Vendor | Vendor | many-to-one | `parent_vendor: <id>` op Vendor *(v0.2)* | inherent |
| REALIZES_USECASE | Connection | UseCase | many-to-many | `realizes_usecases: [<id>]` op Connection *(v0.2)* | inherent via Connection.sources |
| USECASE_VIA_SYSTEM | UseCase | System | many-to-many | `realized_by_systems: [<id>]` op UseCase *(v0.2)* | inherent via UseCase.sources |
| USECASE_VIA_CONNECTION | UseCase | Connection | many-to-many | `realized_by_connections: [<id>]` op UseCase *(v0.2)* | inherent via UseCase.sources |
| USECASE_IN_REGION | UseCase | Region | many-to-many | `regions: [<id>]` op UseCase *(v0.2)* | inherent |
| USECASE_DRIVEN_BY_PROGRAM | UseCase | Program | many-to-many | `programs: [<id>]` op UseCase *(v0.2)* | inherent |
| ENFORCES_STANDARD | Program | Standard | many-to-many | `enforces_standards: [<id>]` op Program *(v0.2)* | **programma-regeling als bron vereist** |
| PROGRAM_TARGETS_REGION | Program | Region | many-to-many | `target_regions: [<id>]` op Program *(v0.2)* | inherent |

Inline edges worden door de schema-validator gecheckt op:
1. Bestaat het target-`id` als file in de juiste `/data/<type>/` folder?
2. Is het type van het target correct (bijv. `systems: [<id>]` moet naar
   System verwijzen, niet naar Vendor)?
3. Voor `CHILD_VENDOR_OF`: geen circulaire parent_vendor-ketens (A→B→A).

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
- **Network-topology gewicht** — `federated` vs `centralized` vs
  `hybrid` wegen potentieel anders *(v0.2)*
- **Data-type gewicht** — bijv. volledige care transfer weegt meer dan een
  enkele afspraak
- **Status multiplier** — `production` weegt vol, `pilot` gedeeltelijk,
  `planned` fractioneel, `concept` minimaal (intentie), `deprecated` /
  `inactive` nul of negatief *(v0.2: enum uitgebreid met `concept` en
  `pilot`)*
- **Recentheids-factor** — `validated_at` ouder dan 12 maanden schaalt af
- **Standaard-conformiteit bonus** — Connections met een gespecificeerde
  `standard:` die door beide systemen wordt ondersteund krijgen een bonus
- **Open-standaarden bonus** *(v0.2)* — gebruik van open datamodellen
  (OpenEHR, OMOP) boven proprietary (MS CDM) krijgt een duurzaamheids-bonus
- **Compliance knock-out** *(v0.2)* — een `centralized` datahub die
  patiënt-BSN verwerkt zonder aantoonbare NEN 7510 / Wbsn-z conformiteit
  kan de Maturity-score van afhankelijke Connections op 0 zetten, ongeacht
  andere gewichten

De exacte gewichten (numbers) staan **niet** in dit document. Ze horen in
`/schema/maturity-score.yaml`, een apart file dat door de
**Strategische Architect** (Gemini) wordt gevuld en onderhouden. Sinds
v0.1.1 (2026-04-12) zijn alle 5 assen compleet: transport_paradigm,
topology, status, data_type, recency — plus twee multiplicatief-gestapelde
bonussen (standard_conformance ×1.15, open_standard ×1.2).

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
