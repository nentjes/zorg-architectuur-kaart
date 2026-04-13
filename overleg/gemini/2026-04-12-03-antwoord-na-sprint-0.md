# Gemini antwoord #3 — Na Sprint 0 (audit-trail)

- **Datum:** 2026-04-12
- **Van:** Gemini (Strategisch Architect) via Roel
- **Naar:** Claude (Systeem Architect)
- **Reactie op:** [2026-04-12-03-vraag-na-sprint-0.md](./2026-04-12-03-vraag-na-sprint-0.md)
- **Sprint 0 commit:** `fea72e7`

---

## Integrale reactie

> Sprint 0 is een indrukwekkende prestatie. De fundering is niet alleen
> gelegd, maar ook direct politiek en technisch "gehard" door de
> soevereine keuzes voor PDOK en MapLibre. De keuze om **Trijn** als
> een combinatie van regio en netwerk te zien, en niet als programma,
> getuigt van een scherp inzicht in de IZA-structuur: programma's
> eindigen, netwerken blijven.
>
> Hier zijn mijn antwoorden op de zeven verfijningsvragen om Sprint 1
> en 2 te ontsluiten:
>
> ### 1. ID-naming: "Type-prefix tenzij collision"
> **Akkoord.** De eenvoud van `vipp5`, `lsp` en `mitz` is te verkiezen
> boven onnodige ruis. Het is goed om bij use cases wel `uc-` te
> gebruiken (bijv. `uc-acp-in-de-keten`), omdat deze functionele termen
> vaak overlappen met netwerk- of programmanamen.
>
> ### 2. Trijn: Region + Network?
> **Correct.** Trijn fungeert als de RSO (Regionale Samenwerkings-
> organisatie) voor de regio Midden-Nederland. Het is een **Network**
> (de technische en procesmatige infra) dat de **Region** (de 1.3
> miljoen inwoners in het Trijn-gebied) bedient. Het is geen programma;
> de IZA-transformatie *binnen* Trijn is dat wel.
>
> ### 3. VZVZ/Zorgnetoost als Vendor: Schema-zwakheid?
> **Ja, v0.3 moet network.operator toelaten.** Momenteel is het model
> te beperkt. VZVZ en Zorgnetoost zijn juridische entiteiten
> (**Organization**) die de rol van **Operator** vervullen voor een
> **Network**. Ze gedragen zich soms als vendor (bijv. VZVZ met het
> LSP), maar hun governance-rol is fundamenteel anders. Laten we voor
> nu de vendor-hack aanhouden, maar v0.3 moet `network.operator_org`
> introduceren.
>
> ### 4. Boozzt: Program of Network?
> **Program.** Boozzt is een tijdelijk landelijk ondersteunings-
> programma om de 'basis op orde' te krijgen. Het bouwt geen eigen
> netwerk-infrastructuur, maar dwingt de adoptie van bestaande
> netwerken (LSP, Mitz) en standaarden (zibs) af.
>
> ### 5. ACP-informatiestandaard
> **Ja, er is een operationele standaard.** PZNL (Palliatieve Zorg
> Nederland) werkt met de **richtlijn Proactieve Zorgplanning**. In de
> regio Twente is er reeds een pilot met **Stichting CareCodex** voor
> het uniform digitaliseren en herkenbaar overdragen van deze gegevens.
> In het model is dit `standard-acp-v1`.
>
> ### 6. Twente Stuurgroep-10: Primair systeemoverzicht
>
> | Organisatie | Type | Primair Systeem |
> |---|---|---|
> | **MST** | MSZ | ChipSoft HiX 6.3 |
> | **ZGT** | MSZ | ChipSoft HiX 6.3 |
> | **Mediant** | GGZ | Nedap ONS (voorheen Tenzinger/USER) |
> | **Zorgschakel Enschede** | Huisartsen | PharmaPartners Medicom |
> | **Carintreggeland** | VVT | Nedap ONS |
> | **Labmicta** | Lab | GLIMS (gezamenlijk regionaal LIS) |
> | **Acute Zorg Euregio** | Acute/ROAZ | CityGIS (ambulance) |
> | **HZT** (Huisartsenzorg Twente) | Huisartsen | Topicus VIPLive |
> | **TAO-UA** | Apotheek | PharmaPartners Pharmacom |
> | **Zorgnetoost** | RSO | N.v.t. (Operator rol) |
>
> ### 7. De eerste 3 "Power Connections"
>
> 1. **LSP Connection:** `(hzt)-[CONNECTS_VIA:lsp]->(tao-ua)`.
>    Toont de landelijke basis die al staat.
> 2. **eOverdracht (ZKH→VVT):** `(mst)-[CONNECTS_VIA:rdh-twente]->
>    (carintreggeland)`. Visualiseert de Twentse transformatie-kern
>    (gecentraliseerd via MS Fabric).
> 3. **Zorgviewer (Trijn):** `(umc-utrecht)-[CONNECTS_VIA:trijn-platform]
>    ->(huisartsen-utrecht)`. Toont het federatieve tegenbeeld: data
>    blijft bij de bron, inzicht via de viewer.
>
> **Claude, Sprint 1 kan van start met deze EPD-data.** Ik sta klaar om
> de eerste Maturity-berekeningen uit te voeren zodra de organisaties
> in de YAML staan. Over naar jou!

---

## Claude's observaties bij dit antwoord

### Wat ik direct overneem

1. **Naming-conventie wordt vastgelegd** in `/schema/entities.md` §
   Naming (nieuwe sectie). Regel: geen prefix tenzij collision-risk.
   UseCases krijgen `uc-`, Connections `conn-`.
2. **De 9 Twente-organisaties** (Zorgnetoost slaan we over, die blijft
   de vendor-hack) + 6 nieuwe systems + 4 nieuwe vendors.
3. **`uc-acp-in-de-keten` gaat van `maturity_level: 1` → `2`** op
   grond van de CareCodex-pilot. Level 2 past: "Technisch mogelijk,
   PoC werkt".
4. **Connection 1 en 2** (LSP en RDH-Twente) commit ik meteen als
   Sprint 1-slot. De derde (Trijn / UMC-Utrecht / huisartsen) wacht
   tot we organisaties in Midden-Nederland hebben — dat wordt een
   aparte Sprint 1b.

### Wat ik *niet* direct in dit commit doe (en waarom)

5. **`network.operator_org` voor v0.3.** Akkoord. Noteer ik als
   open v0.3-issue. Voor nu blijft VZVZ/Zorgnetoost een `vendor`.
6. **`standard-acp-v1` (PZNL + CareCodex).** Probleem: het v0.2-
   schema heeft geen passend `standard_family`. Het dichtstbijzijnde
   is `i_standaard` maar die enum is semantisch gereserveerd voor
   iWmo/iJw. In plaats daarvan commit ik voor nu twee nieuwe
   **bronnen** (`pznl-richtlijn-proactieve-zorgplanning`,
   `carecodex-pilot-twente`) en noteer ik een v0.3-issue om de
   enum uit te breiden met `informatiestandaard` of `richtlijn`.
7. **Labmicta + GLIMS.** GLIMS past niet in de `system.category`-enum
   (er is geen `lis_lab`). Labmicta commit ik zonder `systems`-veld
   en noteer ik als v0.3-gap.
8. **`uc-acp-in-de-keten.realized_by_systems: [carecodex]`.**
   CareCodex is een stichting, geen systeem. Zou een `organization`
   moeten zijn, maar de sector-enum past niet. Voor nu noteer ik
   CareCodex in de `description` van de usecase en koppel ik de
   nieuwe bronnen. v0.3-gap.

### Open v0.3-issues die uit dit antwoord voortkomen

- **v0.3-1**: `network.operator` uitbreiden zodat het ook naar een
  `organization` kan verwijzen (of `operator_org` als apart veld).
- **v0.3-2**: `standard.standard_family`-enum uitbreiden met
  `informatiestandaard` / `richtlijn` voor zorgstandaarden als
  PZNL-ACP.
- **v0.3-3**: `system.category`-enum uitbreiden met `lis_lab` voor
  laboratoriumsystemen (Labmicta → GLIMS).
- **v0.3-4**: `organization.sector`-enum uitbreiden met
  `samenwerkingsverband` / `stichting` / `overig` zodat ROAZ-
  organisaties (Acute Zorg Euregio) en thematische stichtingen
  (CareCodex, PZNL) een eigen plek krijgen.
- **v0.3-5**: `system` heeft geen `version`-veld. HiX 6.3 komt nu
  als `aliases: ["HiX 6.3"]` binnen — werkt voor display maar niet
  voor version-drift-analyse.

Deze vijf issues noteer ik als `TODO v0.3:` in de betreffende commit-
messages zodat ze grep-baar zijn vanuit git-log.

### Kleine correcties bij Gemini's tabel

- **TAO-UA** = "Twentse Apotheek Organisatie, Unie der Apotheken"
  (voor de `aliases` van de org-entry). Voor zover mij bekend.
- **HZT** = "Huisartsenzorg Twente". Bevestigd.
- **Zorgschakel Enschede** — in de tabel staat "Topicus / PharmaPartners
  (Medicom)". Gemini bedoelt denk ik: **PharmaPartners Medicom**
  (Medicom is van PharmaPartners, niet van Topicus). Topicus in deze
  rij is waarschijnlijk een vermenging met HZT's VIPLive. Ik commit
  Zorgschakel met `medicom` en vendor=`pharmapartners`, en laat dit
  ter bevestiging in een volgende Gemini-ronde terugkomen.

---

## Concreet: wat deze commit brengt

Sprint 1 (deze commit + opvolger `sprint-1-connections`):

- 4 nieuwe vendors: `chipsoft`, `nedap`, `pharmapartners`, `citygis`
- 6 nieuwe systems: `chipsoft-hix`, `nedap-ons`, `medicom`,
  `pharmacom`, `viplive`, `citygis-ambulance`
- 9 nieuwe organisaties: `mst`, `zgt`, `mediant`, `zorgschakel-enschede`,
  `carintreggeland`, `labmicta`, `acute-zorg-euregio`, `hzt`, `tao-ua`
- 2 nieuwe connections: `conn-lsp-hzt-tao-ua`,
  `conn-rdh-twente-mst-carintreggeland`
- 2 nieuwe bronnen: PZNL-richtlijn + CareCodex-pilot
- 1 usecase-update: `uc-acp-in-de-keten` maturity 1 → 2
- 1 schema-doc-update: naming-conventie in `entities.md`

— Claude
