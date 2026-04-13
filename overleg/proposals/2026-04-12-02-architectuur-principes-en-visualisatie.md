# ADR — Architectuurprincipes + visualisatie-stack

- **Datum:** 2026-04-12
- **Auteur:** Claude (Systeem Architect)
- **Besluit van:** Roel (owner)
- **Status:** vastgesteld
- **Raakt:** alle toekomstige tooling- en leveranciersbeslissingen,
  in het bijzonder de kaart-rendering en geocoding.

---

## Aanleiding

Gemini heeft op 2026-04-12 een briefing geleverd waarin werd voorgesteld
om de visualisatielaag op **Google Maps Platform** te bouwen (Maps JS API,
Places API, Geocoding API, met een mogelijke uitbreiding naar BigQuery
voor visualisatie). De briefing veronderstelde een bestaande
MapLibre-implementatie en een `viewer/`-folder.

Beide bleken niet te bestaan: de repo bevat op het moment van dit besluit
alleen `README.md`, `overleg/`, `referenties/` en `schema/`. Er is dus geen
migratie-kost en de keuze is volledig open.

Dat maakte het een goed moment om niet alleen dit specifieke
visualisatie-besluit te nemen, maar ook de **meta-principes** vast te
leggen waarmee vergelijkbare toekomstige keuzes (database, hosting,
CDN, auth-provider, diagram-renderer, enz.) getoetst worden.

---

## Besluit 1 — Architectuurprincipes voor tooling en leveranciers

Voor elke externe dienst, library of platform die deel wordt van de Zorg
Architectuur Kaart gelden — in deze volgorde — de volgende voorkeuren:

1. **Open source boven proprietary.** Als een open-source alternatief
   bestaat dat de functie voldoende dekt, heeft dat de voorkeur boven
   een gesloten commercieel product, zelfs als het laatste iets
   makkelijker in gebruik is.

2. **Geen runtime vendor lock-in.** Diensten die alleen functioneren
   met een betaalde API-sleutel van één leverancier zijn een rode
   vlag. Als we ze toch gebruiken, dan alleen **at build-time /
   import-time**, nooit in de live-flow naar de bezoeker. Cache of
   materialiseer het resultaat in de YAML-bron.

3. **Herkomst-voorkeur: NL → EU → US → rest.**
   - Eerste voorkeur: Nederlandse publieke of private leverancier
     (PDOK, SURF, Kadaster, Nictiz)
   - Tweede voorkeur: Europese open-source project of leverancier
     onder EU-wetgeving (MapLibre, OpenStreetMap Foundation UK/DE,
     Scaleway, Hetzner, OVH)
   - Derde voorkeur: US-leverancier, mits open source of open
     licentie (GitHub, Cloudflare free tier)
   - Laatste: US-hyperscaler met closed ecosystem en ToS-risico
     (Google Maps Platform, AWS proprietary services, Azure
     proprietary services)

4. **Privacy-by-design.** Geen tracker, geen third-party fingerprinting,
   geen cookies-zonder-consent. De bezoeker van de kaart mag niet
   stilzwijgend aan een US-cloud-leverancier worden doorgegeven.

5. **Reproduceerbaarheid.** De kaart zoals die verschijnt moet
   reconstrueerbaar zijn uit git + open tiles + open fonts. Een
   visualisatie die zonder live API-call naar een commerciële dienst
   niet meer werkt, is niet reproduceerbaar en voldoet niet aan
   "onvervalsbaar".

6. **Kosten-transparantie.** Elke dienst die op verbruik betaalt en
   die bij viraal succes ongelimiteerd kan opschalen, vraagt een
   expliciete billing-cap of een rate-limit. Een governance-project
   mag niet bij één virale tweet faillie gaan.

### Hoe we dit toepassen

Bij élke voorgestelde tool-toevoeging aan dit project wordt in de PR
of het proposal expliciet gescoord op bovenstaande 6 criteria. Een
leverancier die op criterium 2 of 3 laag scoort is niet automatisch
uitgesloten, maar vereist een expliciete onderbouwing waarom de
uitzondering verantwoord is.

---

## Besluit 2 — Visualisatie-stack

**Voorkeursstack (beslissing 2026-04-12):**

| Laag | Keuze | Herkomst | Licentie |
|---|---|---|---|
| Kaart-renderer | **MapLibre GL JS** | EU-fork (OSM Foundation context) | BSD-3 |
| Basemap (tiles) | **PDOK BRT-Achtergrondkaart** | NL (Kadaster) | CC-BY |
| Geocoding (NL-adressen) | **PDOK Locatieserver** | NL (Kadaster) | publiek |
| Geocoding (moeilijke gevallen) | éénmalig bij import — alleen als PDOK faalt | tbd | tbd |
| Fonts | Open fonts (bijv. Inter, Public Sans) | open | OFL/MIT |
| Hosting kaart | GitHub Pages of Cloudflare Pages free tier | US (open platform) | n.v.t. |
| Database (tbd in later ADR) | DuckDB in-browser of SQLite uit git | open | MIT/Apache |

**Niet gekozen:** Google Maps Platform. Reden: faalt op criterium 2
(runtime vendor lock-in via verplichte API-key), criterium 3
(US-hyperscaler), criterium 4 (tracking via Google Analytics stack
is default), criterium 5 (Google Maps ToS verbiedt caching van tiles,
dus de kaart is niet reproduceerbaar zonder live Google-call) en
criterium 6 (open verbruiksmodel met snelle groei boven free tier).

**Wel open gehouden:** Google Geocoding API éénmalig bij import van
moeilijke adressen die PDOK Locatieserver niet kan oplossen (bijv.
buitenlandse adressen, historische adressen, adressen zonder huisnummer).
In dat geval wordt het resultaat **gematerialiseerd in de YAML** als
`coordinates: {lat, lon}` en de runtime-kaart heeft daarna geen
Google-dependency meer. Dit moet per bron gelogd worden.

---

## Besluit 3 — Eerst data, dan kaart

We bouwen **niet** eerst een lege viewer. We bouwen eerst genoeg
skelet-data dat er iets te tonen valt:

1. `/sources/sources.yaml` met de 4 plan-bronnen
2. Eerste 10+ entities: standards, networks, regions, programs, vendors
3. Eerste demo-UseCase (`uc-acp-in-de-keten`, gedeeld tussen Twente en 't
   Gooi — perfecte test-case voor de UseCase-entiteit uit v0.2)
4. *Dan pas* viewer-skelet met MapLibre + PDOK

Reden: tooling kiezen zonder data is speculatief. Met 10 echte entities
op tafel kunnen we zien wat we daadwerkelijk op een kaart willen
projecteren (puntlocaties? regio-polygonen? netwerk-edges?), en dan
pas bepalen of MapLibre überhaupt de juiste primaire layer is (het
zou ook een force-directed graaf kunnen zijn, of een hybride).

---

## Wat betekent dit voor eerder werk?

- v0.2-schema: geen wijziging nodig, de principes zitten al impliciet in
  `vendor_role`, de open-standards-bonus en de NEN 7510 knock-out.
- `/overleg/proposals/2026-04-12-ontology-v0.2.md`: blijft zoals het is.
- README.md: de "Principes"-sectie wordt uitgebreid met een verwijzing
  naar deze ADR zodat bijdragers de tooling-filosofie kennen.

---

## Besluit Roel — 2026-04-12

- [x] **Akkoord met de 6 architectuurprincipes hierboven.**
- [x] **Akkoord met MapLibre + PDOK als voorkeursstack.**
- [x] **Akkoord met "eerst data, dan kaart".**

Letterlijke quote: *"ik wist helemaal niet van die alternatieven op
google maps. maar laten we afspreken dat we als architectuurkeuze
nemen zoveel mogelijk nederlands en dan europees en zo min mogelijk
amerikaans. voor zoveel mogelijk open source en zo min mogelijk vendor
lock in. akkoord, we houden ons aan jouw voorstel, begin maar met
bouwen."*

Volgende stap: sources-registry + skelet-data in deze sessie.
