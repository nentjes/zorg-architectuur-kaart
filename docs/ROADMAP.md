# Zorg Architectuur Kaart — ROADMAP

**Status**: levend document. Laatste update: 2026-04-13 (na Sprint 4b).

Dit document beschrijft de driefasen-aanpak voor het in kaart brengen van
het Nederlandse IZA-landschap. Het is de **referentie voor alle sessies**
(Claude én Gemini) om te weten waar we staan en waar we naartoe werken.

## De piramide (niet af te wijken van deze volgorde)

```
                    ┌──────────────────────────┐
                    │  FASE 3 — IZA-UITVOERING │
                    │  Use-cases + projecten   │
                    │  Regionaal, per ROAZ     │
                    └──────────────────────────┘
                  ┌────────────────────────────────┐
                  │  FASE 2b — SUBSYSTEMEN         │
                  │  LIS, RIS, PDMS, portals, etc. │
                  │  Parallel met Fase 3           │
                  └────────────────────────────────┘
                ┌────────────────────────────────────┐
                │  FASE 2a — HOOFDSYSTEMEN           │
                │  EPD/ECD/HIS/AIS per organisatie   │
                │  Met self-service correctie-flow   │
                └────────────────────────────────────┘
              ┌────────────────────────────────────────┐
              │  FASE 1 — ALLE IZA-ORGANISATIES        │
              │  Zorgverleners + koepels + financiers  │
              │  Heel NL, breedte-eerst                │
              └────────────────────────────────────────┘
```

## FASE 1 — Alle IZA-organisaties

**Doel**: iedere organisatie die onder een IZA-afspraak valt staat op de
kaart, minimaal met naam + locatie + sector.

### Stand van zaken (Sprint 4b)

| Sector | Op kaart | Dekking | Opmerking |
|---|---|---|---|
| Ziekenhuis | 68 | ~100% | UMCs + STZ + algemene |
| Ambulance | 25 | ~100% | Alle RAV's |
| GGD | 25 | ~100% | Alle GGD's |
| Gemeente | 340 | 100% | Alle NL-gemeenten (post-2022) |
| VVT | 96 | ~85% | Top-concerns, kleine stichtingen missen |
| GGZ | 46 | ~60% | Top-50, lange staart ontbreekt |
| Huisarts | 61 | ~95% | Zorggroepen + koepels |
| Apotheek | 11 | 20% | Alleen ketens |
| Revalidatie | 17 | ~95% | Near-compleet |
| ZBC | 1 | <1% | Honderden ontbreken |
| Paramedisch | 0 | 0% | Nog niet begonnen |
| Jeugdzorg | 0 | 0% | Nog niet begonnen |
| Geboortezorg | 0 | 0% | Nog niet begonnen |
| Koepels/VWS | 0 | 0% | Nog niet begonnen |
| Zorgverzekeraars | 0 | 0% | Nog niet begonnen |

**Totaal nu: 690 orgs. Target na Fase 1: ~1500-1800 orgs.**

### Sprint 5a — Restgaten dichten (bestaande sectoren)
- **GGZ tail**: van 46 → ~80 instellingen (de Nederlandse ggz-ledenlijst)
- **VVT tail**: +~50 kleinere concerns/stichtingen (ActiZ-ledenlijst)
- **ZBC's**: ZKN-ledenlijst, ~200 ZBC's, aggregeren per keten waar mogelijk
- **Apotheken**: uitbreiden naar grotere onafhankelijken + ketens-dekking

### Sprint 5b — Nieuwe sectoren
- **Paramedisch**: koepels (KNGF, NVLF, EN, NVD, NVvP, NVH) + grote
  groepspraktijken/ketens (FysioHolland, etc.) — niet op praktijkniveau
- **Jeugdzorg**: gecertificeerde instellingen (GI's), jeugdbescherming,
  jeugdreclassering — Jeugdzorg Nederland
- **Geboortezorg**: VSV's (~70), kraamzorg (~50), verloskundigen via KNOV

### Sprint 5c — Koepels en bondgenoten
- **Stelselpartijen**: VWS, NZa, IGJ, Nictiz, ZIN, RIVM
- **Brancheverenigingen**: NVZ, NFU, ActiZ, de Nederlandse ggz, LHV,
  KNMP, KNMG, V&VN, InEen
- **Zorgverzekeraars**: 9 verzekeraars + ZN-koepel
- **IZA-gremia**: IZA-stuurgroep, regio-overleg-tafels, programma-orgs

## FASE 2a — Hoofdsystemen per organisatie

**Doel**: per organisatie het primaire registratiesysteem vastleggen +
mogelijkheid tot correctie door de organisatie zelf.

### Stand van zaken
- Revalidatie: 14/17 `confidence: high` (Roel's Excel)
- GGZ: 17/46 `confidence: medium` (Gemini-research)
- Ziekenhuis: ~50/68 `confidence: low` (LLM-knowledge)
- Rest: grotendeels leeg

### Sprint 6 — Data-vulling
- **Ziekenhuizen**: jaarverslagen, ICT&Health, leveranciersreferenties
- **VVT**: Nedap/PinkRoccade/Ecare/CarenZorgt-klantenlijsten
- **HAP/HIS**: op praktijkniveau (Roel's Unicum-data) + zorggroep-trends
- **Apotheek**: Pharmacom/Aposys/Euroclinix per keten
- **GGZ**: Tenzinger/Nexus/Mextra uitbreiden naar de lange staart
- **Paramedisch**: Intramed/James/Abakus — op sector-aggregatie

### Sprint 7 — Self-service correctie-flow

**Besluit**: Optie A (mailto/issue) nu, evolueren naar Optie C (geverifieerde
zelf-edit) zodra volume > 3 correcties/week.

**Optie A — MVP**:
- "Correctie?"-knop op elke org-kaart in de viewer
- Opent voorgevulde `mailto:` of GitHub-issue-template
- Roel/moderator beoordeelt + merged handmatig

**Optie C — schaalbaar (fase 2027)**:
- Webform met zakelijk-emailadres verificatie
- Cloudflare Worker / Supabase Edge Function
- Auto-PR met `confidence: medium` + provenance `self-reported-<domain>`
- CI-validatie → auto-merge

**Optie D (UZI)**: niet voor 2026.

## FASE 2b — Subsystemen voor data-uitwisseling

**Doel**: die systemen in kaart brengen waar interne data vastzit die
eigenlijk uitgewisseld zou moeten worden.

**Loopt parallel met Fase 3** — alleen in kaart brengen wat voor een
concrete use-case relevant is, niet theoretisch uitputten.

### Per sector
- **Ziekenhuis**: LIS, RIS/PACS, ICU/PDMS, OK, anesthesie, patiëntportaal
- **Apotheek**: AMO/robot, BT-systemen, medicatiebewaking
- **VVT**: medicatiemodule, wondzorg-app, cliëntportaal (CarenZorgt)
- **GGZ**: ROM-tools, DBC-registratie, behandelplan
- **Huisarts**: lab-aanvraag, POH-tools, ZorgDomein-integratie
- **Paramedisch**: oefeningen-app, cliëntportaal

### Ontologie-uitbreiding nodig
- `system.subtype`: primair vs. sub-systeem
- `system.data_domain`: lab / medicatie / beeld / cliëntportaal / etc.
- Connection-level: welke data uit welk sub-systeem

## FASE 3 — IZA-uitvoering per regio

**Doel**: per regio laten zien welke concrete gegevensuitwisselings-
projecten lopen, wie meedoet, wat de status is, of het werkt.

### Data-model (gebruikt bestaande `usecase`-entiteit)

```yaml
id: usecase-midnl-medicatieoverdracht-altrecht-umcu
type: usecase
name: "Medicatieoverdracht Altrecht ↔ UMCU"
program: iza-midden-nederland
region: iza-midden-nederland
participating_organizations: [altrecht, umc-utrecht]
networks: [lsp]
standards: [fhir, zib-medicatie]
data_domains: [medicatie]
status: planned
start_date: 2026-Q2
lead_organization: altrecht
sources: [...]
confidence: medium
```

### Regio-volgorde

1. **Sprint 8a — Gooi en Vechtstreek** (aparte regio, wordt later waarschijnlijk
   bij Amsterdam gevoegd) + **Utrecht** (Midden-NL)
2. **Sprint 8b — Amsterdam** (Noord-Holland stedelijk)
3. **Sprint 8c** — ROAZ-gewijs uitrollen (resterende 9 ROAZ-regio's)

### Maturity v0.2
Als use-cases erin komen verandert de maturity-score:
- Orgs scoren hoger bij deelname aan meer productieve projecten
- Regio's scoren hoger als use-cases meer data-domeinen dekken
- Vervangt de huidige `total_score` die alleen op connecties rust

## Werkverdeling

| Taak | Wie |
|---|---|
| Grote documenten lezen (regioplannen, jaarverslagen) | Gemini + Google |
| Ledenlijsten / marktaandelen-onderzoek | Gemini + Google |
| Data-structurering in manifest-YAML | Claude |
| Ontologie-uitbreidingen | Claude |
| Viewer-features | Claude |
| Self-service backend | Claude |
| Ingest-pipelines | Claude |
| PR-review + merge | Roel |
| Architectuur-beslissingen | Roel (met Claude's advies) |

**Kritiek**: Gemini moet per briefing op pad gestuurd worden met
"lees eerst AGENTS.md" om pad-fouten te voorkomen.

## Vaste beslissingen (niet meer ter discussie)

Deze zijn al akkoord gegeven:

1. ✅ **Self-service**: Optie A nu, Optie C over ~3 maanden
2. ✅ **Sprint-volgorde**: sectoraal breed (Fase 1) eerst, dan regionaal
   diep (Fase 3) — niet per regio parallel oppakken
3. ✅ **Scope**: alleen IZA-gerelateerde zorgverleners — tandartsen,
   mondhygiënisten, private klinieken buiten scope
4. ✅ **Gooi en Vechtstreek**: aparte regio in Fase 3 (wordt later
   waarschijnlijk samengevoegd met Amsterdam)
5. ✅ **Praktijkniveau**: alleen waar primaire data beschikbaar is
   (bijv. Roel's Unicum-huisartsendataset); anders koepel/keten/zorggroep
6. ✅ **Zorgverzekeraars**: ja, zijn IZA-ondertekenaar + financier
7. ✅ **Repo blijft onder `nentjes/`** voor persoonlijke associatie;
   transfer naar org `zorg-kaart-nl` is voorbereid (org bestaat al,
   transfer is 30 seconden werk wanneer moment daar is)

## Open vragen (voor latere beslissing)

- **ROAZ als eerste-klas entiteit** naast IZA-regio? (nu 28 IZA-regio's
  vs 11 ROAZ-regio's — beide indelingen opnemen?)
- **Maturity v0.2** nu al uitrollen of eerst Fase 3 vullen?

## Sprint-planning (orde van grootte)

```
Sprint 5 — Fase 1 afronden
  5a  Restgaten bestaande sectoren       (2-3 werkblokken)
  5b  Nieuwe sectoren (param/jeugd/geb)  (3-4 werkblokken)
  5c  Koepels + VWS + zorgverzekeraars   (1-2 werkblokken)

Sprint 6 — Fase 2a hoofdsystemen
  6a  Ziekenhuis-EPD's compleet          (2 blokken)
  6b  VVT-ECD's compleet                 (2 blokken)
  6c  HIS/AIS/GGZ-EPD's compleet         (2 blokken)

Sprint 7 — Self-service infrastructuur
  7a  Optie A: correctie-button + issue  (1 blok)
  7b  Optie C voorbereiden: auth-flow    (3-4 blokken)

Sprint 8 — Fase 3 regio's
  8a  Gooi & Vechtstreek + Midden-NL     (2 blokken)
  8b  Amsterdam                          (2 blokken)
  8c  Rest van NL ROAZ-gewijs            (10+ blokken)
```
