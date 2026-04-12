# Entities — Zorg Architectuur Kaart ontologie v0.2

## Waarom een ontologie

De kaart heeft slechts betekenis als iedereen die eraan bijdraagt dezelfde
concepten gebruikt. Zonder strakke ontologie wordt een "ziekenhuis" hier een
juridische entiteit, daar een gebouw, en ergens anders een afdeling — en dan
kan het systeem nooit consistente antwoorden geven op vragen als "hoeveel
ziekenhuizen draaien op HiX?".

Daarom definiëren we eerst, precies, wat elke entiteit **is** en wat er
expliciet **niet** onder valt. Daarna mag er pas data bij.

## Fysiek bestandsmodel

Elke entiteit-instance leeft als één YAML-bestand onder
`/data/<type>/<id>.yaml`:

    /data/
      organizations/   amsterdam-umc.yaml
      systems/         chipsoft-hix.yaml
      vendors/         chipsoft.yaml
      regions/         iza-amsterdam.yaml
      networks/        lsp.yaml
      standards/       fhir-r4-nl-core.yaml
      connections/     conn-amsterdam-umc-amsterdam-huisartsen-lsp.yaml
      usecases/        uc-360-graden-beeld.yaml
      programs/        vipp5.yaml

De bestandsnaam zonder extensie is gelijk aan het `id`-veld. Elke YAML
bevat een `type:`-veld dat overeenkomt met de entiteitsoort. Dit is
redundant met de folder, maar expliciet is beter dan impliciet — en het
maakt schema-validatie per-file mogelijk zonder folder-context.

Validatie tegen `/schema/schema.yaml` is verplicht en wordt door de CI
afgedwongen op elke PR.

## De negen entiteiten

1. **Organization** — een juridische of operationele zorg-entiteit
2. **System** — een softwaresysteem (EPD, ECD, HIS, AIS, portal, hub)
3. **Vendor** — een leverancier van een of meerdere `System`s
4. **Region** — een geografische of bestuurlijke regio-indeling
5. **Network** — een uitwisselingsnetwerk of afsprakenstelsel
6. **Standard** — een interoperabiliteits-standaard (Zib, FHIR, HL7, terminologie)
7. **Connection** — een geverifieerde data-uitwisselingsrelatie tussen twee
   `Organization`s via een `Network`, optioneel met een `Standard`
8. **UseCase** — een zorgfunctionele behoefte die door meerdere organisaties
   gedeeld wordt (de "vraag", gerealiseerd via `Connection`s en `System`s)
9. **Program** — een landelijk of regionaal financieringsprogramma dat
   `Standards` afdwingt bij deelnemende `Organization`s (VIPP5, InZicht, OPEN)

De eerste zes en de twee laatste zijn **nodes** in de graaf.
**Connection is de enige edge-entiteit**, en die is wat deze kaart uniek
maakt — zonder Connections is het een sticker-album; met Connections is het
een interoperabiliteitskaart.

`UseCase` en `Program` zijn nieuw in v0.2. Ze bestaan omdat regio's
identieke use cases (360-graden beeld, ACP in de keten) met radicaal
verschillende techniek oplossen; en omdat VIPP-programma's de werkelijke
drijvende kracht achter standaard-adoptie zijn. Zonder deze twee entiteiten
zijn regio-overstijgende vergelijking en financieringsprikkel-analyse niet
zichtbaar in de kaart.

---

## 1. Organization

### Wat het IS
Een juridische of operationeel samenhangende zorgverlenende entiteit.
"Operationeel samenhangend" betekent: één besluitvormingslaag, één IT-beleid,
één inkooplijn.

### Wat het NIET is
- Een individueel zorgverlener (arts, verpleegkundige) — we karteren geen
  personen
- Een enkele locatie/gebouw, tenzij die locatie juridisch zelfstandig is
- Een afdeling binnen een ziekenhuis (die hoort bij de ziekenhuis-organisatie)
- Een samenwerkingsverband zonder eigen IT-beleid (dat is een `Region`)

### Verplichte velden
`id`, `type: organization`, `name`, `sector`, `sources`

### Optionele velden
`aliases`, `subtype`, `parent_organization`, `country`, `locations`,
`region_iza`, `region_roaz`, `region_ggd`, `systems`, `networks`,
`confidence`, `needs_verification`

### Voorbeeld

```yaml
id: amsterdam-umc
type: organization
name: Amsterdam UMC
sector: ziekenhuis
subtype: academisch
country: NL
locations:
  - city: Amsterdam
    address: Meibergdreef 9
    postcode: "1105 AZ"
    coordinates:
      lat: 52.3324
      lon: 4.9471
  - city: Amsterdam
    address: De Boelelaan 1117
    postcode: "1081 HV"
    coordinates:
      lat: 52.3345
      lon: 4.8709
region_iza: iza-amsterdam
region_roaz: roaz-amsterdam
systems:
  - epic
sources:
  - nfu-leden-2024
  - amsterdam-umc-jaarverslag-2023
```

---

## 2. System

### Wat het IS
Een softwareproduct dat door een of meerdere `Organization`s wordt gebruikt
voor het primaire zorgproces of de zorg-IT. Inclusief EPD, ECD, HIS, AIS,
PGO-portal en integratie-hubs.

### Wat het NIET is
- Een individuele installatie of deployment (die is afgeleid uit de
  Organization → System relatie)
- Een module of add-on die niet zelfstandig als product bestaat
- Infrastructuur-software (OS, database, storage) die niet zorg-specifiek is

### Verplichte velden
`id`, `type: system`, `name`, `category`, `vendor`, `sources`

### Optionele velden
`country_origin`, `standards_supported`, `aliases`, `confidence`,
`deployed_in` *(nieuw in v0.2 — lijst van `Network`-ids waarin dit systeem
is uitgerold; bijv. Microsoft Fabric `deployed_in: [rdh-twente]`)*

### Voorbeeld

```yaml
id: chipsoft-hix
type: system
name: ChipSoft HiX
category: epd_ziekenhuis
vendor: chipsoft
country_origin: NL
standards_supported:
  - hl7-v2-5
  - fhir-r4-nl-core
  - zib-2020
sources:
  - chipsoft-productpagina
  - nictiz-interoperabiliteitsregister
```

---

## 3. Vendor

### Wat het IS
Een partij die in de zorg-IT-stack één of meer van de volgende rollen
vervult: `product_vendor` (bezit en ontwikkelt een `System`),
`platform_provider` (levert het onderliggende cloud- of
infrastructuur-platform waarop een `System` draait), `implementation_partner`
(integreert, configureert en implementeert de oplossing bij een klant), of
`operator` (voert het operationeel beheer op de regionale uitrol).

Apart van `System` omdat één vendor meerdere systemen kan leveren, en
systemen kunnen van eigenaar wisselen (M&A, carve-out, rebranding). En
nieuw in v0.2: een datahub zoals RDH Twente kent tegelijkertijd drie
vendors in drie verschillende rollen — Microsoft als `platform_provider`,
KPMG als `implementation_partner`, Zorgnetoost als `operator`. Die
onderscheiden maakt de kaart voor vendor-lock-in-analyse.

### Wat het NIET is
- Een dochterbedrijf dat geen eigen juridische entiteit is — gebruik
  `parent_vendor` of `parent_company`
- Een generieke dienstverlener die geen zorg-IT-rol heeft (hosting,
  telecom)

### Verplichte velden
`id`, `type: vendor`, `name`, `sources`

### Optionele velden
`country`, `parent_company`, `parent_vendor` *(nieuw in v0.2 — verwijst
naar een andere `Vendor`-id als de parent zelf ook als vendor-entry
bestaat; anders gebruik `parent_company: string`)*, `vendor_role`
*(nieuw in v0.2, default `product_vendor`, enum:
`product_vendor | platform_provider | implementation_partner | operator`)*,
`website`, `aliases`

---

## 4. Region

### Wat het IS
Een geografische of bestuurlijke indeling die in de zorg een regelmatige rol
speelt: IZA-regio, ROAZ-regio, GGD-regio, jeugdhulpregio, Wmo-inkoopregio,
RSO-verzorgingsgebied, XDS-affinity-domain.

### Wat het NIET is
- Een provincie of gemeente als zodanig (die staan al in Kadaster/CBS-bronnen)
- Een ad-hoc samenwerking zonder vastgesteld verzorgingsgebied
- Een juridische entiteit die IT-beleid voert (dat is een `Organization`)

### Verplichte velden
`id`, `type: region`, `name`, `region_type`, `sources`

### Optionele velden
`covers_gemeentes`, `lead_organization`, `participating_organizations`,
`parent_region`

---

## 5. Network

### Wat het IS
Een uitwisselingsinfrastructuur, berichtennetwerk, afsprakenstelsel of
toestemmingenvoorziening die meerdere organisaties gebruiken om data uit te
wisselen.

Voorbeelden: LSP, Zorgmail, ZorgDomein, Twiin, Cumuluz, een RSO-XDS-omgeving,
Mitz, Nuts.

### Wat het NIET is
- Een point-to-point koppeling tussen twee organisaties (dat is een
  `Connection`)
- Een standaard zonder infrastructuur (dat is een `Standard`)
- Een leverancier die een netwerk beheert (de leverancier is een `Vendor`;
  het netwerk zelf is deze entiteit)

### Verplichte velden
`id`, `type: network`, `name`, `network_type`, `sources`

### Optionele velden
`operator`, `standards_used`, `established`, `aliases`, `data_topology`
*(nieuw in v0.2, enum: `centralized | federated | hybrid`)*,
`deployed_systems` *(afgeleid — lijst van `System`-ids die
`deployed_in: [<dit network>]` hebben; niet in YAML, alleen in afgeleide
views)*

### `data_topology` — betekenis

- **`centralized`** — data vloeit naar één centrale store. Voorbeelden:
  RDH Twente (Microsoft Fabric als datahub), een klassieke RSO-XDS
  repository.
- **`federated`** — data blijft bij de bron; het netwerk is een dunne
  laag eroverheen die on-demand bevraagt. Voorbeelden: Trijn (CumuluZ),
  Nuts-gebaseerde federaties, MedMij PGO-flow.
- **`hybrid`** — mix van beide binnen één netwerk. Voorbeeld: LSP,
  waar medicatiegegevens centraal worden gesynchroniseerd (push) maar
  dossier-fetch federated on-demand gebeurt.

Dit veld is in v0.2 optioneel. Het wordt in v0.3 verplicht.

---

## 6. Standard

### Wat het IS
Een gepubliceerde, versiegebaseerde interoperabiliteitsstandaard:
informatie­model, uitwisselingsprotocol of terminologie.

### Wat het NIET is
- Een interne stijlgids van één leverancier
- Een tijdelijk profiel zonder publieke publicatie

### Verplichte velden
`id`, `type: standard`, `name`, `standard_family`, `sources`

### Optionele velden
`version`, `publisher`, `supersedes`, `superseded_by`

---

## 7. Connection (de edge)

### Wat het IS
Een **aangetoonde** data-uitwisselingsrelatie tussen twee `Organization`s
over een specifiek `Network`, optioneel met een gespecificeerde `Standard`.

Een Connection is de meeteenheid voor de IZA Maturity Score.

Een Connection claimt **niet** dat er op dit moment data vloeit — die claim
vereist realtime-monitoring dat we niet hebben. Een Connection claimt dat
er een productieve, aangetoonde mogelijkheid tot uitwisseling bestaat,
onderbouwd door minstens één publieke bron die **beide** organisaties
noemt binnen het genoemde netwerk.

### Wat het NIET is
- Een intentieverklaring, een LOI, een voornemen ("wij gaan Twiin aansluiten
  in 2025")
- Een eenmalige historische uitwisseling die niet herhaalbaar is
- Een ongefundeerde aanname ("het zal wel via Zorgmail gaan")

### Verplichte velden
`id`, `type: connection`, `organization_a`, `organization_b`, `network`,
`status`, `sources`

### Optionele velden
`standard`, `direction`, `data_types`, `established`, `validated_at`,
`confidence`, `needs_verification`, `realizes_usecases` *(nieuw in v0.2 —
lijst van `UseCase`-ids die deze Connection helpt realiseren)*

### Status-enum (uitgebreid in v0.2)

De status-enum is in v0.2 verrijkt met `concept` en `pilot`, aansluitend
op de UseCase-ladder:

- `concept` — staat in een plan, nog geen concreet ontwerp
- `planned` — ontwerp rond, budget toegekend, nog niet live
- `pilot` — live in testopstelling of bij beperkt aantal partijen
- `production` — operationeel
- `deprecated` — vervangen maar nog niet afgeschakeld
- `inactive` — afgeschakeld

De numerieke weging van deze waardes in de IZA Maturity Score hoort in
`/schema/maturity-score.yaml`, niet hier.

### Voorbeeld

```yaml
id: conn-amsterdam-umc-huisartsenkring-amsterdam-lsp
type: connection
organization_a: amsterdam-umc
organization_b: huisartsenkring-amsterdam
network: lsp
standard: hl7-v3-professionele-samenvatting
direction: bidirectional
data_types:
  - medication
  - basic_dataset
status: active
established: "2019-06-01"
validated_at: "2025-11-12"
sources:
  - vzvz-aansluitregister-2025-q3
  - amsterdam-umc-jaarverslag-2023
confidence: high
```

---

## 8. UseCase

### Wat het IS
Een zorgfunctionele behoefte — een "vraag" vanuit het primaire zorgproces
— die door meerdere organisaties in meerdere regio's wordt gedeeld, en die
via `Connection`s en/of `System`s wordt gerealiseerd. Voorbeelden: "360-
graden beeld patiënt in de acute keten", "ACP in de keten", "Regionaal
capaciteitsinzicht", "Gekoppelde thuismonitoring".

UseCases zijn de gemeenschappelijke taal tussen regio's. Twente en Trijn
noemen allebei het 360-graden beeld, maar lossen het op met radicaal
verschillende techniek (centralized Microsoft Fabric vs. federatief
CumuluZ). Door de UseCase als eerste-klas entiteit te modelleren kun je
die vergelijking maken zonder de techniek-keuze met de functionele
behoefte te verwarren.

### Wat het NIET is
- Een project, programma of initiatief — dat is een `Program`
- Een feature van één systeem — die hoort op het `System` zelf
- Een losse ambitie zonder minstens één bronplan dat hem benoemt

### Verplichte velden
`id`, `type: usecase`, `name`, `domain`, `sources`

### Optionele velden
`description`, `maturity_level` (1-4), `realized_by_connections`,
`realized_by_systems`, `regions`, `programs`, `iza_goal_link`

### `domain`-enum
`acute_zorg | chronische_zorg | ouderenzorg | ggz | geboortezorg |
medicatie | preventie | capaciteit | pgo | overig`

### UseCase maturity-ladder

| Level | Naam | Bewijs dat je nodig hebt |
|---|---|---|
| 1 | Papier | De use case staat in minstens één regioplan of transformatieplan |
| 2 | Technisch mogelijk | PoC werkt, of systemen die de use case zouden realiseren ondersteunen de benodigde standaarden |
| 3 | Regionaal operationeel | Pilot draait in minstens één IZA-regio voor ≥1 keten, met aantoonbaar gebruik |
| 4 | Landelijk herbruikbaar | Minstens één andere IZA-regio heeft de oplossing (code, datamodel, integratie) daadwerkelijk overgenomen |

Claude berekent `maturity_level` niet zelf. De waarde wordt gezet op
basis van `sources` en de status van de `realized_by_connections`.

### Voorbeeld

```yaml
id: uc-360-graden-beeld
type: usecase
name: "360-graden beeld patiënt in de acute keten"
domain: acute_zorg
description: >
  Zorgverleners in de acute keten (huisartsenpost, ambulance,
  ziekenhuis-SEH, VVT-doorstroom) hebben binnen vijf minuten een volledig
  beeld van medicatie, allergieën, behandelbeperkingen, recente contacten
  en actuele labuitslagen van een patiënt.
maturity_level: 2
realized_by_connections:
  - conn-twente-rdh-360-graden
realized_by_systems:
  - microsoft-fabric-rdh-twente
regions:
  - iza-twente
  - iza-midden-nederland
programs:
  - vipp5
iza_goal_link: "passende zorg — de juiste zorg op de juiste plek"
sources:
  - transformatieplan-rdh-twente-2025
  - transformatieplan-trijn-midden-nederland-2025
```

---

## 9. Program

### Wat het IS
Een landelijk of regionaal financieringsprogramma dat één of meer
`Standards` afdwingt bij deelnemende `Organization`s. Programma's zijn
de werkelijke drijvende kracht achter standaard-adoptie in de Nederlandse
zorg — ze verklaren waarom organisaties op hetzelfde moment massaal aan
dezelfde Zibs gaan.

Voorbeelden: VIPP5 (ziekenhuizen), InZicht (VVT), OPEN (huisartsen),
BabyConnect (geboortezorg), VIPP GGZ, VIPP Farmacie.

### Wat het NIET is
- Een wet of ministeriële regeling als zodanig (die staat in de
  `sources` en wordt via `funder` genoemd)
- Een softwareproduct of -bundel
- Een tijdelijke subsidie zonder verplichte standaard-adoptie

### Verplichte velden
`id`, `type: program`, `name`, `scope`, `sources`

### Optionele velden
`funder`, `start_date`, `end_date`, `budget_eur`, `enforces_standards`,
`target_sectors`, `target_regions`, `website`

### `scope`-enum
`landelijk | regionaal | sector`

### Voorbeeld

```yaml
id: vipp5
type: program
name: VIPP5
scope: landelijk
funder: "Ministerie van VWS"
start_date: "2020-01-01"
end_date: "2024-12-31"
budget_eur: 75000000
enforces_standards:
  - zib-2020
  - fhir-r4-nl-core
  - mp9
target_sectors:
  - ziekenhuis
website: "https://www.dus-i.nl/subsidies/vipp-5"
sources:
  - dusi-vipp5-regeling-2020
```

---

## Gedeelde conventies

### Identifiers (`id`)
- Kebab-case, alleen `[a-z0-9-]`, minimaal 2 tekens
- Globaal uniek over alle entiteit-types heen
- Stabiel: een `id` verandert nooit — gebruik `aliases` voor naamswijzigingen
- Gelijk aan de bestandsnaam zonder extensie

### Bronnen (`sources`)
- Verplicht voor elke entiteit. Minimaal één `source_id` die bestaat in
  `/sources/sources.yaml`
- Leveranciers-PR mag nooit de enige bron zijn voor een klant-claim (zie
  `governance-bron-validator`)
- Bronnen ouder dan 36 maanden krijgen `stale: true` en triggeren
  `needs_verification: true` op afhankelijke datapunten

### Vertrouwen (`confidence`, `needs_verification`)
- `confidence: high | medium | low` — subjectief, maar eerlijk
- `needs_verification: true` signaleert dat menselijke validatie gewenst is
- Een entiteit mag in de data staan met lage confidence, zolang het
  als zodanig gemarkeerd is. Liever een eerlijk gat dan een gegokt feit.

### Grensgebieden (DE/BE)
- Het `country`-veld markeert Duitse of Belgische entiteiten die als
  referentie in de kaart staan voor grensregio-uitwisseling
- Systemen uit die landen (Dedalus Orbis, CGM AIS Duitsland, Xperthis)
  krijgen `country_origin` overeenkomstig
- De kaart-ambitie is niet om DE/BE volledig te karteren, maar om zichtbaar
  te maken waar de Nederlandse zorg-digitalisering stopt en waar grenzen
  liggen — de "digitale grensmuur"

### Lege toekomst-velden
Sommige velden zijn nu al gedefinieerd maar worden pas in latere milestones
gevuld (bijvoorbeeld `validated_at` op Connections vóór de eerste v0.5
seeding). Dat is oké — de schema-validator accepteert afwezige optionele
velden. De ontologie-guard waarschuwt alleen bij velden die in geen enkele
entiteit-definitie voorkomen.

## Naming-conventies voor `id`

Vastgesteld 2026-04-12 in overleg met Gemini (zie
[`/overleg/gemini/2026-04-12-03-antwoord-na-sprint-0.md`](../overleg/gemini/2026-04-12-03-antwoord-na-sprint-0.md)).

**Kernregel:** *geen type-prefix, tenzij de naam anders collision-risico
heeft met een andere entiteit.*

- **Program, Standard, Network, Vendor, Region, System, Organization:**
  geen prefix. De folder `/data/<type>/` geeft het type al aan, en de
  korte vorm is URL- en grep-vriendelijker.
  Voorbeelden: `vipp5`, `zib-2020`, `lsp`, `mitz`, `microsoft-nl`,
  `iza-twente`, `chipsoft-hix`, `mst`.

- **UseCase:** verplicht prefix `uc-`. Use-case-namen zijn functioneel
  ("ACP in de keten", "360-graden beeld") en botsen anders met
  organisaties of locaties. Voorbeelden: `uc-acp-in-de-keten`,
  `uc-360-graden-beeld`.

- **Connection:** verplicht prefix `conn-`. Een connection-id is
  synthetisch (geen eigen menselijke naam) en moet herkenbaar zijn
  als edge. Voorbeelden: `conn-lsp-hzt-tao-ua`,
  `conn-rdh-twente-mst-carintreggeland`.

- **Regio's van type `iza`:** mogen het natuurlijke prefix `iza-`
  gebruiken als het de leesbaarheid verbetert (`iza-twente`,
  `iza-gooi-en-vechtstreek`, `iza-midden-nederland`) — dat is geen
  type-prefix maar een semantische prefix (het regio-regime).
  Regio's van andere types (`roaz`, `ggd`, `rso`) volgen dezelfde
  logica: `roaz-euregio`, `ggd-twente`, etc.

- **Multi-sector systemen (bijv. Nedap Ons):** één system-entry per
  productnaam, niet één per sector. Als in v0.2 de `category`-enum
  geen passende waarde heeft, kiezen we de *dominante* sector en
  markeren we het gat voor v0.3. Nedap Ons → `ecd_vvt`, ook al
  wordt het bij Mediant in GGZ-configuratie gebruikt.

Deze conventies worden afgedwongen door de `governance-ontology-guard`
bij PR-review, niet door JSON Schema (want JSON Schema heeft geen
cross-entity-patronen per type).

## Open v0.3-issues

Uit de Sprint 0/1-ervaring zijn de volgende schema-gaten vastgesteld
die in v0.3 opgelost worden:

- **v0.3-1** `network.operator` uitbreiden zodat het ook naar een
  `organization` kan verwijzen (of `operator_org` als apart veld).
  Reden: VZVZ en Zorgnetoost zijn juridische samenwerkingsverbanden,
  geen leveranciers. Voor nu: vendor-hack met `vendor_role: operator`.
- **v0.3-2** `standard.standard_family`-enum uitbreiden met
  `informatiestandaard` / `richtlijn`. Reden: de PZNL-richtlijn
  Proactieve Zorgplanning past nergens in de huidige enum.
- **v0.3-3** `system.category`-enum uitbreiden met `lis_lab`. Reden:
  Labmicta / GLIMS kan nu niet als system worden vastgelegd.
- **v0.3-4** `organization.sector`-enum uitbreiden met
  `samenwerkingsverband` (of `overig` + `subtype`). Reden: ROAZ'en
  zoals Acute Zorg Euregio en thematische stichtingen (CareCodex,
  PZNL) hebben geen passende sector.
- **v0.3-5** `system.version`-veld toevoegen. Voor nu gebruiken we
  `aliases: ["HiX 6.3"]` — werkt voor display maar niet voor
  version-drift-analyse.
entiteit-definitie voorkomen.
