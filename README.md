# Zorg Architectuur Kaart

**Een open, publiek controleerbare kaart van het Nederlandse zorg-IT-landschap.**

Welke ziekenhuizen draaien op Chipsoft, welke op Epic of Nexus?
Welke VVT-instellingen delen gegevens met hun regionale huisartsen?
Waar staat het Integraal Zorgakkoord (IZA) in de praktijk — en waar blijft
het bij papieren beloften?

Dit project brengt in kaart wat tot nu toe versnipperd, verborgen of
leveranciers-gebonden was: de **daadwerkelijke digitale architectuur**
van de Nederlandse zorg.

## Waarom

Nederland praat al jaren over "regionale samenwerking" en
"databeheerschap", maar niemand heeft de topografie van het
zorglandschap echt in kaart. Zonder kaart vaar je zonder kompas.
Beleidsmakers, bestuurders, onderzoekers én burgers verdienen
inzicht in wie met wie verbonden is — en wie niet.

## Principes

- 🔓 **Open** — alle data onder CC-BY-SA, alle code onder MIT
- 🔍 **Transparant** — elke wijziging staat in de git-historie
- 📎 **Bronverplicht** — geen datapunt zonder publieke bron
- 🤝 **Community-gedreven** — iedereen kan bijdragen via Pull Requests
- ⚖️ **Onvervalsbaar** — branch protection + verplichte review + CI-validatie
- 💶 **Non-profit** — geen verdienmodel, geen vendor-belangen

## Status

🚧 **In opbouw.** We bouwen nu het ontologie-schema, de seed-dataset
(grootste NL ziekenhuizen) en het bronnenregister. Bijdragen welkom
zodra de eerste milestone is gepubliceerd.

## Structuur

    /schema/      Ontologie: entiteiten, relaties, veldendefinities
    /data/        De kaart zelf (YAML per entiteit)
    /sources/     Bronnenregister — elke datapunt verwijst hiernaar
    /viewer/      Interactieve visualisatie (GitHub Pages)
    /.github/     CI-checks: bronverplichting, schema-validatie

## Bijdragen

Zie [`CONTRIBUTING.md`](CONTRIBUTING.md). Kort: fork, voeg of corrigeer
een entiteit, voeg de bron toe, open een PR. De bot checkt automatisch
of je bronvermelding klopt.

## Licentie

- **Data:** [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- **Code:** [MIT](LICENSE)

---

*Dit project is een onafhankelijk, non-profit initiatief. Geen band met
VWS, Nictiz, NZa of enige leverancier.*
