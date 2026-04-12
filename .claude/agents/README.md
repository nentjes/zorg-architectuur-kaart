# Agent-roster — Zorg Architectuur Kaart

Dit zijn gespecialiseerde subagents voor het Zorg Architectuur Kaart-project.
Elke agent heeft een eng afgebakend kennisdomein en een strikt output-contract.
Ze bestaan omdat de Nederlandse zorg-IT te versnipperd is voor één allround-persoon
— en voor één allround-LLM.

## Waarom agents

De kennis over "welke huisartspraktijk draait op Medicom vs Promedico", "welke
apotheek-keten gebruikt Pharmacom of Aposys", en "welke ziekenhuizen zijn
aangesloten op welke XDS-omgeving" is verspreid over honderden documenten,
leveranciers, regio-organisaties en jaarverslagen. Geen mens krijgt dit in zijn
hoofd. Maar een groep gespecialiseerde AI-agents die elk één domein bewaken —
en elkaars werk kruis-valideren — kán dit wel.

## Opbouw

Bestandsnamen volgen het patroon `<categorie>-<specialisatie>.md`:

- `governance-*` — meta-agents die ontologie, bronverplichting en schema bewaken
- `sector-*` — specialisten per zorgsector (huisarts, ziekenhuis, apotheek, …)
- `system-*` — specialisten per softwaresysteem (HiX, Epic, Medicom, Nedap Ons, …)
- `network-*` — specialisten per uitwisselingsnetwerk (LSP, Zorgmail, Twiin, …)
- `standards-*` — specialisten per interoperabiliteits-standaard (Zibs, FHIR, HL7, …)
- `region-*` — specialisten per IZA-regio (nu: één template; per-regio-agents volgen)

## Regels die voor iedere agent gelden

1. **Ontologie-first.** Geen veld of entiteit die nog niet in `/schema/` staat.
   Wil je iets nieuws? Stel eerst een schema-wijziging voor.
2. **Bronverplicht.** Geen datapunt zonder `source_id` in `/sources/sources.yaml`.
   De bron gaat ALTIJD eerst in het bronnenregister, dán het datapunt.
3. **Publiek en verifieerbaar.** Geen scraping van login-gated of auteursrechtelijk
   afgeschermde bronnen. Respecteer `robots.txt` en rate limits.
4. **Geen persoonsgegevens.** We karteren organisaties en systemen, geen personen.
5. **Bij twijfel:** `confidence: low` en `needs_verification: true`. Liever een
   eerlijk gat dan een gegokt feit.
6. **Non-profit, non-vendor.** Geen agent promoot een leverancier. Ook de
   leverancier-agents zijn neutraal — ze kennen het product, ze verkopen het niet.
7. **Kruis-validatie.** Elke claim over "organisatie X gebruikt systeem Y" moet
   idealiter door twee agents bevestigd zijn: de sector-agent en de system-agent.

## Index

### Governance
- `governance-ontology-guard` — bewaakt entiteit- en relatiedefinities
- `governance-bron-validator` — controleert bronverwijzingen
- `governance-schema-auditor` — valideert YAML tegen `schema.yaml`

### Sectoren
- `sector-huisarts`, `sector-ziekenhuis`, `sector-apotheek`, `sector-vvt`,
  `sector-ggz`, `sector-zbc`, `sector-gemeente`, `sector-jeugdzorg`,
  `sector-ambulance`, `sector-geboortezorg`, `sector-paramedisch`

### Systemen
- Ziekenhuis-EPD: `system-chipsoft-hix`, `system-epic`, `system-nexus`
- Huisartsen-HIS: `system-cgm-medicom`, `system-promedico`, `system-tetrahis`
- Apotheek-AIS: `system-pharmacom`, `system-aposys`
- VVT-ECD: `system-nedap-ons`, `system-pinkroccade-mozaik`, `system-ecare`

### Netwerken
- `network-lsp`, `network-zorgmail`, `network-zorgdomein`, `network-twiin`,
  `network-cumuluz`, `network-xds-rso`, `network-nuts`, `network-mitz`,
  `network-edifact`

### Standaarden
- `standards-zibs` — Nictiz Zorginformatiebouwstenen
- `standards-fhir` — HL7 FHIR en Nederlandse profielen (nl-core)
- `standards-hl7` — HL7 v2 messaging
- `standards-terminology` — SNOMED CT, LOINC, G-standaard

### Regio's
- `region-iza-template` — template; per-regio-agents volgen zodra de regioplannen
  binnen zijn

## Schaal-uitdaging: gemeentes en regio's

Er zijn 342 gemeentes en ~26 IZA-regio's. Een agent-file per gemeente is
onwerkbaar en niet de juiste abstractie: gemeentes verschillen nauwelijks in
*soort* kennis die je erover nodig hebt. De aanpak:

- **Eén** `sector-gemeente`-agent die de *algemene* kennis over Nederlandse
  gemeentes, VNG-structuren, Jeugdwet/Wmo-inkoop en GGD-regio's kent.
- **Eén** `region-iza-template` dat beschrijft wat een per-regio-agent moet
  kennen. Per regio wordt dit pas naar een apart file geïnstantieerd als er een
  echte aanleiding is (bijvoorbeeld: Roel levert het regioplan aan, dan maken
  we `region-iza-<naam>.md`).
- De regio-data zelf leeft in `/data/regions/*.yaml`, niet in agent-files.

## Volwassenheid

Dit roster is v0.1. Het zal evolueren. Voeg geen agents toe zonder eerst te
overwegen of een bestaande agent uitgebreid kan worden. Splits pas wanneer twee
domeinen aantoonbaar uit elkaar lopen.
