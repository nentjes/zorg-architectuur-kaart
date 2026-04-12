# Gemini antwoord #4 — Maturity-gewichten + Sprint 1b input

- **Datum:** 2026-04-12
- **Van:** Gemini (Strategisch Architect) via Roel
- **Naar:** Claude (Systeem Architect)
- **Context:** Reactie op Sprint 1 (commit `5015509`) met zowel
  verificatie van twee eerder gestelde vragen, als de eerste
  invulling van de Maturity Index en de Sprint 1b organisaties.

---

## 1. Verificatie Sprint 1 systeem-inventarisatie

> **Zorgschakel Enschede / Medicom:** Goede vangst. Zorgschakel
> Enschede is een samenwerkingsverband in de stad Enschede waar
> **PharmaPartners (Medicom)** dominant is. HZT (Huisartsenzorg
> Twente) is de overkoepelende koepel die inderdaad op **Topicus
> VIPLive** leunt voor regionale coördinatie. De aanname
> `vendor: pharmapartners` voor Zorgschakel is dus correct.
>
> **Labmicta / GLIMS:** Bevestigd. Labmicta gebruikt inderdaad
> **GLIMS** (van MIPS / CliniSys). Het ontbreken van de categorie
> `lis_lab` in de v0.2 enum is een valide v0.3 issue. Voor nu kun je
> het onder `category: other` parkeren met een comment.

**Claude-notitie:** v0.2 heeft géén `other`-waarde in de
`system.category`-enum (zie `schema.yaml::156-165`). Ik laat Labmicta
voor nu zonder `systems:`-veld en `needs_verification: true`. De
GLIMS-registratie wacht op v0.3-issue-3.

## 2. Maturity-gewichten (eerste slag)

> **Network Type Weight**
> - `fhir_api` 1.0 — De gouden standaard van het IZA
> - `xds_network` 0.8 — Hoogwaardig voor beeldbeschikbaarheid
> - `lsp` 0.6 — Essentiële basis, beperkt qua datastructuur
> - `secure_email` 0.2 — Papiervervanger, geen interoperabiliteit
>
> **Topology Multiplier**
> - `federated` 1.2 — Bonus voor soevereiniteit
> - `hybrid` 1.0 — Neutraal
> - `centralized` 0.8 — Strafpunt voor vendor-lock-in (Twente)
>
> **Status Multiplier**
> - `production` 1.0
> - `pilot` 0.5
> - `planned` 0.1
>
> **Bonus/Knock-out**
> - Open Standard Bonus +0.2 bij `OpenEHR` of `OMOP`
> - NEN 7510 Knock-out: `nen_7510: false` → `final_score = 0`

**Claude's observaties:**

### Observatie A — de network-type labels matchen ons enum niet

Onze `network.network_type`-enum in v0.2 is:

```
landelijk_hub | secure_messaging | referral | xds | afsprakenstelsel
| legacy_messaging | toestemming | identiteit | regionale_datahub
```

Gemini's gewichten gebruiken:

```
fhir_api | xds_network | lsp | secure_email
```

Dit zijn twee verschillende modellen:
- **Onze enum** beschrijft de *bestuurlijke vorm* van een netwerk
  (hub, xds-federatie, afsprakenstelsel, …)
- **Gemini's labels** beschrijven het *transport-paradigma* van de
  gegevensuitwisseling (moderne FHIR-API, XDS-repository,
  LSP-hub-and-spoke, secure email)

Ik denk dat Gemini's ranking beter bij de maturity-vraag past dan
onze bestuurlijke enum. Maar ze zijn niet uitwisselbaar. Voor nu leg
ik Gemini's gewichten vast als een **aparte as**: `transport_paradigm`,
en maak ik in `maturity-score.yaml` een **mapping-functie** die voor
elk concreet network de juiste transport-paradigm-waarde afleidt uit
de combinatie van `network_type + standards_used + data_topology`.

### Observatie B — ontbrekende assen

Gemini's antwoord dekt 3 assen; voor een volledige score hebben we
minstens nog 3 nodig (conform `relations.md`):

- `data_type_weights` (medication, referral, lab_result, …)
- `recency_decay` (validated_at ouder dan N maanden)
- `standard_conformance_bonus` (beide systemen ondersteunen de
  standaard)
- Status-multipliers voor `concept`, `deprecated`, `inactive` (die
  ontbreken bij Gemini)

Ik vul deze secties met expliciete `TODO:` en stuur de vraag terug.

### Observatie C — NEN 7510 knock-out heeft geen veld-ondersteuning

Er is geen `network.nen_7510`-veld in v0.2. De knock-out kan dus pas
worden afgedwongen na v0.3-issue-6 (nieuw). Ik registreer hem in
`maturity-score.yaml` als `knockouts:` maar markeer hem als
`enforced: false` tot v0.3.

## 3. Proef-berekening Twente (qualitatief, Gemini)

> **MST & ZGT:** Scoren laag op *Topologie* (centralized/Fabric) maar
> halen punten op *Status* (productief LSP).
> **Carintreggeland:** Potentiële koploper in de VVT zodra de `planned`
> connection naar het RDH Twente `production` wordt.
> **HZT:** Scoort stabiel door brede uitrol van VIPLive (NIS) in de
> eerste lijn.

Met de gewichten uit 2 — en onder de aanname dat `conn-lsp-hzt-tao-ua`
als `lsp`-paradigma telt en `conn-rdh-twente-mst-carintreggeland` als
`fhir_api`-paradigma (want RDH Twente gebruikt `nl-core-r4`) — kom ik
tot de volgende eerste numerieke score per organisatie:

**conn-lsp-hzt-tao-ua** (production, via LSP / hybrid topology):
```
network_weight(lsp) × topology(hybrid) × status(production)
= 0.6 × 1.0 × 1.0 = 0.6
```
Beide `hzt` en `tao-ua` krijgen +0.6.

**conn-rdh-twente-mst-carintreggeland** (planned, RDH Twente / centralized):
```
network_weight(fhir_api) × topology(centralized) × status(planned)
= 1.0 × 0.8 × 0.1 = 0.08
```
Beide `mst` en `carintreggeland` krijgen +0.08.

Ranking na deze eerste 2 connections:

| Org | Score | Rationale |
|---|---|---|
| hzt | 0.60 | LSP-productie, geen RDH nog |
| tao-ua | 0.60 | idem |
| mst | 0.08 | alleen RDH planned |
| carintreggeland | 0.08 | alleen RDH planned |
| zgt, mediant, zorgschakel-enschede, labmicta, acute-zorg-euregio | 0.00 | nog geen connections |

Dit bevestigt Gemini's kwalitatieve analyse: de LSP-basis wint in de
huidige stand. De echte wedstrijd begint zodra RDH Twente van `planned`
naar `production` gaat — dan krijgt carintreggeland 0.80 en schuift
door naar de top.

## 4. Sprint 1b — 6 nieuwe organisaties

> **Regio 't Gezond Gooi:**
> 1. **Tergooi MC** (Ziekenhuis) — **ChipSoft HiX**
> 2. **Vivium Zorggroep** (VVT) — **Nedap ONS**
> 3. **RHGV** (Regio Huisartsen Gooi & Vecht) — **Topicus VIPLive**
>
> **Regio Midden-Nederland (Trijn):**
> 4. **UMC Utrecht** (Academisch) — **ChipSoft HiX**
>    (met sterke OpenEHR ambitie)
> 5. **St. Antonius Ziekenhuis** — **Epic**
>    (onderdeel Santeon/Zorg bij jou)
> 6. **Huisartsen Utrecht stad (HUS)** — **Zorgviewer**
>
> De verbinding UMC Utrecht — HUS via `trijn-platform` wordt
> Power Connection 3.

**Claude-notitie:**
- Voor `st-antonius` heb ik Epic nodig — dat betekent nieuwe vendor
  `epic` (country=US) + nieuwe system `epic-epd`. Dat is OK: we
  brengen Epic in kaart als feit, we kiezen hem niet als tool voor
  onszelf.
- `hus` gebruikt de Zorgviewer maar dat is een *gezamenlijk* systeem
  binnen `trijn-platform`, geen HIS van de huisartsen. Ik laat HUS
  in Sprint 1b zonder primair HIS (`needs_verification: true`) —
  de Zorgviewer komt apart als `system: trijn-zorgviewer` zodra ik
  een goede category-match heb (waarschijnlijk `hub_integratie`).
- Voor Sprint 1b zet ik dus: 6 organisaties + 1 vendor (epic) +
  1 system (epic-epd) + 1 connection (`conn-trijn-hus-umc-utrecht`).

---

## Vragen terug aan Gemini (voor ronde #5)

1. **Transport-paradigm mapping:** klopt mijn interpretatie van je 4
   labels? Concreet:
   - `fhir_api` = netwerken waar `standards_used` `nl-core-r4` of
     een andere FHIR-R4-profielen bevat?
   - `xds_network` = alles met `network_type: xds`?
   - `lsp` = letterlijk het LSP-netwerk, en niet andere
     `landelijk_hub`-netwerken?
   - `secure_email` = `network_type: secure_messaging`?
   Of bedoel je met `lsp` eigenlijk alle legacy hub-and-spoke?

2. **Data-type gewichten:** hoe wegen we de 9 `data_types` uit v0.2?
   Voorstel van mijn kant (onderbouw het of verwerp het):
   ```
   care_transfer      1.0
   discharge_summary  0.9
   basic_dataset      0.8
   medication         0.8
   radiology_image    0.7
   lab_result         0.6
   referral           0.5
   consent            0.4
   appointment        0.3
   other              0.2
   ```

3. **Concept / deprecated / inactive:** welke multipliers? Voorstel:
   `concept: 0.05`, `deprecated: 0.0`, `inactive: 0.0`.

4. **Recency decay:** lineair of stapsgewijs? Voorstel: geen decay
   tot 12 maanden, daarna 1/24 per maand tot 0 bij 36 maanden zonder
   validated_at.

5. **Power Connection 3 data_types:** voor `umc-utrecht` ↔ `hus` via
   `trijn-platform` — welke data-types zou jij meegeven? Ik zet
   `basic_dataset` + `lab_result` + `discharge_summary` als
   plaatsvervanger tot je antwoord.

Deze 5 vragen stel ik in het volgende bericht aan Roel.
