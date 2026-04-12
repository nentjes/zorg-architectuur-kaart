# Entities — Zorg Architectuur Kaart ontologie v0.1

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

De bestandsnaam zonder extensie is gelijk aan het `id`-veld. Elke YAML
bevat een `type:`-veld dat overeenkomt met de entiteitsoort. Dit is
redundant met de folder, maar expliciet is beter dan impliciet — en het
maakt schema-validatie per-file mogelijk zonder folder-context.

Validatie tegen `/schema/schema.yaml` is verplicht en wordt door de CI
afgedwongen op elke PR.

## De zeven entiteiten

1. **Organization** — een juridische of operationele zorg-entiteit
2. **System** — een softwaresysteem (EPD, ECD, HIS, AIS, portal, hub)
3. **Vendor** — een leverancier van een of meerdere `System`s
4. **Region** — een geografische of bestuurlijke regio-indeling
5. **Network** — een uitwisselingsnetwerk of afsprakenstelsel
6. **Standard** — een interoperabiliteits-standaard (Zib, FHIR, HL7, terminologie)
7. **Connection** — een geverifieerde data-uitwisselingsrelatie tussen twee
   `Organization`s via een `Network`, optioneel met een `Standard`

De eerste zes zijn **nodes** in de graaf. **Connection is de edge**, en die
entiteit is wat deze kaart uniek maakt — zonder Connections is het een
sticker-album; met Connections is het een interoperabiliteitskaart.

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
`country_origin`, `standards_supported`, `aliases`, `confidence`

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
De juridische leverancier van één of meerdere `System`s. Apart van System
omdat één vendor meerdere systemen kan leveren, en systemen kunnen van
eigenaar wisselen (M&A, carve-out, rebranding).

### Wat het NIET is
- Een consultancy of integratiepartner die geen eigen product levert
- Een dochterbedrijf dat geen eigen juridische entiteit is
- Een generieke dienstverlener (hosting, telecom)

### Verplichte velden
`id`, `type: vendor`, `name`, `sources`

### Optionele velden
`country`, `parent_company`, `website`, `aliases`

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
`operator`, `standards_used`, `established`, `aliases`

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
`confidence`, `needs_verification`

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
