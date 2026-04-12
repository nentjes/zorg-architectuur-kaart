# Gemini-antwoord #2 — review na GitHub-toegang

- **Datum ontvangen:** 2026-04-12 (tweede bericht op dezelfde dag)
- **Afzender:** Gemini (Strategisch Architect)
- **Doorgestuurd via:** Roel
- **Context:** Roel heeft Gemini read-toegang gegeven tot deze GitHub-repo.
  Gemini heeft de repo (inclusief [proposal ontologie v0.2](../proposals/2026-04-12-ontology-v0.2.md)
  en [het eerste Gemini-antwoord](./2026-04-12-twente-vragenlijst-antwoord.md))
  gelezen en komt met een tweede reactie waarin hij drie regio's in scope
  zet: Twente, 't Gezond Gooi en Midden-Nederland (Trijn).
- **Status:** Brondocument voor audit-trail. Delta's t.o.v. het eerste
  antwoord zijn verwerkt in de bijgewerkte proposal v0.2.

---

## Integrale tekst van het antwoord

> Dit is een uitstekende analyse van de plannen voor **Twente**,
> **'t Gezond Gooi** en **Midden-Nederland (Trijn)**. Je hebt de
> fundamentele verschillen in architectuur (centraal vs. federatief) en
> de organisatorische complexiteit scherp in beeld.
>
> Als Strategisch Architect beantwoord ik hieronder jouw vragenlijst om
> Claude direct te voeden voor de technische inrichting op jouw MacBook
> M5 Max.

### A. Ontologie — Fundament van de kaart

1. **Topology (Data Paradigma):** Dit moet inderdaad een veld worden op
   de entiteit `Network`. Ik stel voor:
   `data_topology: centralized | federated | hybrid`. Twente is hiermee
   'centralized' (data naar de hub), Trijn is 'federated' (data bij de
   bron).
2. **Regionale datahub plaatsing:** De RDH is een **Network**, maar de
   technische realisatie (zoals Microsoft Fabric in Twente) is een
   **System** beheerd door de RSO. We modelleren een `deployment`
   relatie: `(System:Microsoft Fabric)-[DEPLOYED_IN]->(Network:RDH_Twente)`.
3. **UseCase als 8e entiteit:** Ja. Use cases zoals "360-graden beeld"
   of "ACP in de keten" komen in elk plan terug, maar de technische
   invulling verschilt per regio. Door ze als aparte entiteit te
   modelleren, kunnen we regio's op functioneel niveau vergelijken.
4. **VIPP-programma's:** Deze plaatsen we als een nieuwe entiteit
   **Program**. Een `Program` (bijv. VIPP InZicht) 'forceert' bepaalde
   `Standards` bij een `Organization`.
5. **Vendor-stack diepte:** We ondersteunen een gelaagde vendor-relatie.
   In Twente is Microsoft de `platform_provider`, KPMG de
   `implementation_partner` en Zorgnetoost de `operator`.

### B. Maturity-score

1. **Open standaarden vs. Vendor-lock:** De Maturity-score weegt
   interoperabiliteit op procesniveau zwaarder dan de cloud-provider.
   Echter, het gebruik van open standaarden (OpenEHR/OMOP) boven
   proprietary modellen (MS CDM) moet een **bonusfactor** krijgen voor
   duurzaamheid.
2. **Intentie vs. Runtime:** We gebruiken een status-veld op
   verbindingen: `concept | planned | pilot | production`. Alleen
   `production` telt volledig mee. Intentie (zoals Twente's claim over
   CumuluZ) krijgt een lage weging (10%).
3. **Use case progressie-ladder:** Ik normaliseer dit naar:
   `Level 1: Papier` (plan), `Level 2: Technisch mogelijk` (PoC),
   `Level 3: Regionaal operationeel` (Pilot),
   `Level 4: Landelijk herbruikbaar`.

### C. Strategisch — Vergelijkbaarheid

1. **Classificatie 31 IZA-regio's:** Ik zie nu al vier hoofd-patronen
   ontstaan:
   - **Hyper-Scalers (Twente):** Centraal op MS/Azure.
   - **Federatieven (Noord-Nederland/Zorgviewer):** Data bij de bron.
   - **LSP+ Verbeteraars (RSO-model):** Voortbouwen op bestaande infra
     met portaallaag.
   - **PGO-Pioniers (MedMij focus):** Inwoner als data-hub.
2. **OpenEHR-spanning:** De claim van Twente over OpenEHR op Microsoft
   Fabric is marketing-technisch fragiel. Landelijk is de trend: Zibs
   voor uitwisseling, OpenEHR voor opslag (bijv. UMCU). Twente kiest
   voor Microsoft's CDM, wat een toekomstige migratie naar OpenEHR
   bemoeilijkt.
3. **BSN in Fabric:** Dit is een kritiek punt voor de Maturity-score.
   Een Azure-tenant moet expliciet voldoen aan NEN 7510 en de Wbsn-z.
   Als dit klapt, faalt de MedMij-aansluiting.

### D. Concreet te valideren

- **HZT:** Bevestigd, **Huisartsenzorg Twente**.
- **TAO-UA:** Bevestigd, **Twentse Apothekers Organisatie**
  (UA = Uitgesloten Aansprakelijkheid).
- **Zorgschakel Enschede:** Bevestigd, huisartsencoöperatie.
- **ROAZ vs. IZA-regio:** De **IZA-regio** (31 regio's) is leidend voor
  de kaart omdat daar de transformatiemiddelen aan gekoppeld zijn. De
  ROAZ-laag is een filter daarboven.
- **KPMG:** Bevestigd als strategisch implementatiepartner voor de RDH
  Twente.

### Advies voor vervolg

> Ik kies voor **optie (b)**. Laat Claude de entiteit-inventaris voor
> de drie regio's consolideren in de YAML-structuur, inclusief de nieuwe
> velden voor `data_topology` en de nieuwe entiteiten `UseCase` en
> `Program`. Zodra dit staat, kan ik de Maturity-scores per organisatie
> berekenen.

---

## Claude's observaties bij dit tweede antwoord

### Bevestigingen (geen actie nodig)

Gemini bevestigt integraal alles uit het eerste antwoord en daarmee
integraal het proposal v0.2:

- `data_topology` op `Network` ✓
- `UseCase` als 8e entiteit ✓
- `Program` als 9e entiteit ✓
- `vendor_role` (platform_provider / implementation_partner / operator) ✓
- `deployed_in` System→Network als edge ✓
- Status-enum `concept|planned|pilot|production` ✓
- IZA-regio leidend, ROAZ filter-laag ✓
- 4 architectuurparadigma's voor regio-classificatie ✓

### Delta's t.o.v. het eerste antwoord (acties nodig)

1. **Level 4 van de UseCase-ladder is veranderd.**
   - Antwoord #1: `Level 4: Aantoonbare impact` (IZA-doelen behaald)
   - Antwoord #2: `Level 4: Landelijk herbruikbaar`
   - **Betekenis:** Gemini verschuift van "wordt-het-gebruikt" naar
     "kan-een-andere-regio-het-overnemen". Dat is een stevige
     conceptuele verschuiving: impact-meten is outcome-gericht,
     herbruikbaarheid is architectuur-gericht. Consequentie: `Level 4`
     bewijs is bijv. dat een andere IZA-regio de code, het datamodel of
     de integratie daadwerkelijk overneemt — niet patiënt-outcomes.
   - **Actie:** `proposal v0.2` Level 4-tekst aanpassen.

2. **Open standaarden = bonusfactor, niet alleen zwaardere weging.**
   - Antwoord #1: "een hogere score voor 'open standaarden' vs. proprietary"
   - Antwoord #2: "bonusfactor voor duurzaamheid"
   - **Betekenis:** Dit hoort in `/schema/maturity-score.yaml`, niet in
     het schema zelf. Noteren als TODO voor Gemini bij maturity-
     invulling. Geen schema-wijziging.

3. **Nieuwe UseCase-naam: "ACP in de keten".**
   - Deze use case komt ook in Twente voor en wordt expliciet als
     voorbeeld gebruikt. Hoort bij de eerste seed-set `UseCase`-voorbeelden
     in `/data/usecases/`.

4. **BSN-in-Fabric compliance als scoring-criterium.**
   - Nieuw en kritiek: NEN 7510 + Wbsn-z compliance op de Azure-tenant.
   - Geen schema-wijziging. Hoort in `/schema/maturity-score.yaml` als
     een **knock-out criterium**: als een centralized datahub patiënt-BSN
     opslaat zonder aantoonbare NEN 7510 / Wbsn-z conformiteit, dan is
     de Maturity-score voor de `connections` die op die hub leunen **0**,
     ongeacht andere gewichten. Dit is normatief — Gemini's pen.
   - **Actie:** Noteren als TODO voor Gemini in maturity-score-review.

5. **Scope is uitgebreid naar drie regio's: Twente + 't Gezond Gooi + Trijn.**
   - **Belangrijk signaal aan Roel:** in `/referenties/` zit **geen plan
     voor 't Gezond Gooi**. De beschikbare documenten zijn:
     - Regioplan deel 3 (landelijk)
     - Transformatieplan Trijn (Midden-Nederland)
     - Transformatieplan RDH Twente
   - Gemini noemt 't Gezond Gooi uit eigen kennis of uit een bron die we
     niet hebben. We kunnen niet bron-verplicht entiteiten-inventariseren
     zonder een plan voor 't Gezond Gooi.
   - **Actie:** Roel moet kiezen — ofwel het 't-Gezond-Gooi-plan ophalen
     en in `/referenties/` zetten, ofwel 't Gezond Gooi uit scope van
     deze eerste ronde houden en alleen Twente + Trijn consolideren.

6. **"Technische inrichting op jouw MacBook M5 Max".**
   - Gemini verwijst naar Roel's werkmachine. Geen actie; alleen
     signaal dat Gemini de context over de ontwikkelomgeving kent.
