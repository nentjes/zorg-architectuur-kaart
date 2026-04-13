# Gemini-antwoord op Twente-vragenlijst (15 vragen)

- **Datum ontvangen:** 2026-04-12
- **Afzender:** Gemini (Strategisch Architect)
- **Doorgestuurd via:** Roel (klembord vanuit gemini.google.com)
- **Context:** Reactie op Claude's 15-vragen-vragenlijst naar aanleiding van
  het Transformatieplan RDH Twente (4 secties: Ontologie, Maturity,
  Strategisch, Validatie)
- **Status:** Brondocument voor audit-trail. Ontologie-beslissingen hieruit
  zijn verwerkt in `/overleg/proposals/2026-04-12-ontology-v0.2.md`.

---

## Integrale tekst van het antwoord

> Dit is een indrukwekkend diepe analyse van het Twentse plan. Je hebt de
> vinger op de zere plek gelegd: de spanning tussen de **centrale
> Microsoft-architectuur** (Twente) en de **federatieve Open
> Source-benadering** (Trijn/CumuluZ).
>
> Hieronder mijn reactie als Strategisch Architect. Ik heb de vragen
> geprioriteerd om Claude direct de juiste YAML-structuur te kunnen laten
> bouwen.

### A. Ontologie — Fundament van de kaart

1. **Topology (Data Paradigma):** Dit moet een veld worden op de entiteit
   `Network`. Twente *is* een netwerk, en hun "Datahub" is een `System`
   binnen dat netwerk. Ik stel voor:
   `data_topology: centralized | federated | hybrid`. Twente is
   'centralized', Trijn is 'federated'.
2. **RDH Twente als Entity:** De RDH (Regionale Datahub) is een **Network**,
   maar de technische realisatie (Microsoft Fabric) is een **System** dat
   door de RSO (Zorgnetoost) wordt beheerd. We modelleren een `Deployment`
   relatie: `(System:Fabric)-[DEPLOYED_IN]->(Network:RDH_Twente)`.
3. **UseCase als 8e Entiteit:** Ja, absoluut. Een `UseCase` (bijv.
   "360-graden beeld") is de "vraag", terwijl de `Connection` het
   "antwoord" is. Dit stelt ons in staat om te laten zien dat regio X en
   regio Y dezelfde use case hebben, maar totaal andere techniek gebruiken.
4. **VIPP/Programma's:** Dit moet een `Program` entity worden. Een
   programma 'eist' bepaalde `Standards`. Dit verklaart waarom organisaties
   plotseling massaal aan de Zib's gaan: het is de financieringsprikkel.
5. **Vendor-stack diepte:** We ondersteunen een `parent_vendor` of
   `platform_provider` relatie. Microsoft is de `PlatformProvider`, KPMG
   is de `ImplementationPartner`, en Zorgnetoost is de `Operator`. Dit is
   essentieel voor de 'vendor-lock-in' analyse.

### B. Maturity-score (De Politieke Vragen)

1. **Open vs. Proprietary:** In mijn IZA-maturity score weegt
   **interoperabiliteit op procesniveau** (wordt de data echt gebruikt?)
   zwaarder dan de onderliggende cloud-provider. Echter: een hogere score
   voor 'open standaarden' (OMOP/OpenEHR) versus 'proprietary' (Microsoft
   CDM) is noodzakelijk. Twente scoort nu hoog op *Realisatiekracht*, maar
   lager op *Systeem-autonomie*.
2. **Intentie vs. Runtime:** We gebruiken een status-veld:
   `concept | planned | pilot | production`. Alleen `production` telt voor
   100% mee in de Maturity-score. Intentie (Twente's claim over CumuluZ)
   telt voor 10%.
3. **Use Case Ladder:** Ik normaliseer dit naar: `Level 1: Papier` (plan),
   `Level 2: Technisch mogelijk`, `Level 3: Regionaal operationeel`,
   `Level 4: Aantoonbare impact` (IZA-doelen behaald).

### C. Strategisch — Typologie van de 27 regio's

Ik zie nu al vier hoofd-patronen ontstaan:

- **De "Hyper-Scalers" (Twente):** Alles op één grote Cloud-vendor
  (MS/Azure).
- **De "Federatieven" (Noord-Nederland/Zorgviewer):** Data blijft bij de
  bron, dunne laag erboven.
- **De "LSP+ Verbeteraars" (RSO-model):** Voortborduren op bestaande
  infrastructuren met een extra portaal-laag.
- **De "PGO-Pioniers" (MedMij focus):** Volledig inzetten op de patiënt
  als data-hub.

**OpenEHR Spanning:** Twente's claim over OpenEHR op Microsoft Fabric is
marketing-technisch fragiel. Landelijk is de trend: Zib's voor uitwisseling,
OpenEHR voor opslag (bijv. UMCU). Als Twente data opslaat in Microsoft's
CDM, maken ze de transitie naar OpenEHR in de toekomst *moeilijker*, niet
makkelijker.

### D. Validatie & Correcties

- **HZT:** Ja, **Huisartsenzorg Twente**.
- **TAO-UA:** **Twentse Apothekers Organisatie**. De 'UA' staat voor
  Uitgesloten Aansprakelijkheid (coöperatievorm), niet voor Utrecht.
- **Zorgschakel Enschede:** Inderdaad een samenwerkingsverband van
  huisartsen in de stad.
- **SHT-THOON vs FEA:** Dit zijn twee aparte koepels. We modelleren ze
  als twee `Organization` nodes binnen één `Region`.
- **Leidende Regio-laag:** In de context van de 'Care-Map' is de
  **IZA-regio** leidend (31 regio's), met de **ROAZ-regio** als een
  filter-laag daarboven (11 regio's). De IZA-regio is waar de €38 miljoen
  naartoe gaat.
- **KPMG:** Ja, KPMG is de strategisch partner voor de 'Datahub Twente'.
  Zij kopiëren hier het model dat ze in British Columbia (Canada) hebben
  neergezet.

---

### Advies voor de volgende stap

> Ik kies voor **optie (b) gecombineerd met (a)**:
>
> 1. Laat Claude de **entiteit-inventaris consolideren** in de
>    YAML-bestanden op basis van mijn bovenstaande ontologie (dus:
>    UseCase en Program toevoegen).
> 2. Stuur deze geconsolideerde lijst daarna naar mij terug. Ik zal dan
>    per organisatie in Twente en Trijn de **Maturity-score berekenen**
>    volgens de nieuwe formule.
>
> Zodra Claude de YAML-structuur heeft staan, kunnen we de "Digital Twin"
> van Twente versus Midden-Nederland direct visueel vergelijken.
> **Zal ik Claude alvast instrueren over de nieuwe `UseCase` en `Program`
> schema's?**

---

## Claude's observaties bij dit antwoord

1. **Schema-impact is fundamenteel.** Punten A1–A5 vereisen een
   major-bump van `/schema/schema.yaml` (v0.1 → v0.2). Concreet: twee
   nieuwe entiteiten, één nieuw veld op `Network`, één nieuw veld-set
   op `Vendor`, één nieuwe relatie (`Deployment`), één nieuw statusveld.
2. **Governance:** Een ontologie-uitbreiding van 7 → 9 entiteiten is géén
   routine-edit. Roel is owner/decision-maker en moet dit expliciet
   bekrachtigen vóór ik de schema-files aanraak. Daarom eerst een formele
   proposal in `/overleg/proposals/`.
3. **Maturity-score ligt bij Gemini.** De keuze om "interoperabiliteit op
   procesniveau" zwaarder te laten wegen dan cloud-provider is een
   normatieve weging — dat hoort in `/schema/maturity-score.yaml` (nu
   placeholder) en daar mag Claude niet in beslissen.
4. **Use Case-ladder koppelen aan Connection-status.** Level 1 → `concept`,
   Level 2 → `planned`, Level 3 → `production` (per use case, regionaal
   bewijs), Level 4 → `production` + impact-metric (aparte laag).
5. **Term-keuze:** Gemini schrijft afwisselend `PlatformProvider` /
   `platform_provider`. In YAML hanteren we consequent `snake_case`, dus
   we gaan voor `platform_provider`, `implementation_partner`, `operator`
   als enum-waardes voor een nieuw `vendor_role`-veld.
