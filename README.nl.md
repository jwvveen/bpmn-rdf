# BPMN 2.0 in RDF (concept)

Een concept-ontologie in OWL met SHACL-validatie voor BPMN 2.0.2 (OMG,
formal/13-12-09), op dezelfde manier gebouwd als
[ArchiMate 4.0 in RDF](https://github.com/jwvveen/archimate-rdf). De regels uit
de specificatie zijn data. Validatie staat los van betekenis. Elke stroom is
een eigen resource. En een procesmodel sluit aan op architectuur, begrippen en
regels. Het artikel "BPMN 2.0 in RDF: the matrix is data" legt de keuzes uit.

*English version: [README.md](README.md).*

Status: **0.1.0-concept**. Een stuk voor de discussie, geen standaard. BPMN is
een specificatie van de Object Management Group; dit is geen publicatie van
OMG, en OMG heeft geen officiële RDF-vorm van BPMN. De namespace
`https://w3id.org/bpmn#` is voorgesteld en wordt geregistreerd bij w3id.org.

## Bestanden

| Bestand | Rol |
|---|---|
| `bpmn.ttl` | **Gegenereerd** uit het metamodel van OMG zelf (`BPMN20.cmof`): 146 klassen met hun hiërarchie, 212 eigenschappen met domein en bereik, 9 opsommingen. Alleen de Nederlandse labels zijn met de hand gemaakt |
| `bpmn-matrix.ttl` | **Gegenereerd**: tabel 7.3 (Sequence Flow) en 7.4 (Message Flow) van BPMN 2.0.2. De gedrukte tabellen hebben elk 36 cellen; uitgeschreven over de metamodelklassen geeft dat 81 cellen voor sequence flows (64 toegestaan) en 56 voor message flows (42 toegestaan), elk met de gedrukte cel als herkomst |
| `bpmn-rules.ttl` | **Gegenereerd**: de 59 normatieve zinnen over verbindingen, letterlijk met paragraaf en pagina, elk met de shape die ze controleert of de reden waarom niet |
| `bpmn-archimate.ttl` | Brug naar ArchiMate 4.0, begrippen en regels: zes eigenschappen en 24 brugregels als data, elk toegestaan of afgeraden |
| `bpmn-alignments.ttl` | **Gegenereerd**: `skos:exactMatch` naar sBPMN 2.0, de FBK BPMN 2.0-ontologie en BBO |
| `shacl/` | Integriteit en normatieve zinnen, twee generieke matrixregels, en de brugcontroles |
| `example.ttl` | Een klein model dat met opzet fout is; geeft precies tien meldingen |
| `validate.py` | Validatie van RDF- of BPMN-XML-modellen, per model of samen |
| `scripts/` | De converter van BPMN-XML naar RDF en de generatoren |
| `sources/` | Waar elk feit vandaan komt, plus een overzicht van eerdere BPMN-ontologieën |
| `corpus/miwg/` | 21 referentiemodellen van de BPMN Model Interchange Working Group als testset (CC BY 3.0) |

## Ontwerpkeuzes in het kort

* **Elke stroom is een resource.** Een directe verbinding tussen twee stappen
  (`bpmn:flowsTo`) is afgeleide suiker, met een CONSTRUCT te maken.
* **Het metamodel is data.** Termen komen uit de CMOF, niet uit het XML-schema.
* **De matrix is data, en de tekst ook.** 42 van de 59 zinnen worden door een
  shape gecontroleerd, 12 zijn toestemmingen die al als toegestane cel in de
  matrix staan, 3 hangen af van de tekening en 2 beschrijven alleen de reikwijdte.
* **De brug is data**, met drie controles over de notaties heen.
* **Ontologie en validatie zijn gescheiden**, en alles is **tweetalig**.
* **Een drukfout in de specificatie.** In de BPMN 2.0.2-PDF staan in tien cellen
  een promilleteken of een accent circonflexe in plaats van een pijl: de hele
  kolom van de gewone activiteitsvorm (een taak) in tabel 7.3 en de hele kolom
  Message Start Event in tabel 7.4. Het defect staat open als OMG-issue
  [BPMN21-453](https://issues.omg.org/issues/BPMN21-453) (april 2026). De
  matrix neemt ze op als toegestaan, met het bewijs in de cel.

## Valideren

```
pip install rdflib pyshacl
python validate.py
python validate.py corpus/miwg/*.bpmn
```

Het voorbeeld geeft tien meldingen (zes overtredingen, vier waarschuwingen);
het MIWG-corpus geeft 0 overtredingen en 5 waarschuwingen. Laad bij een eigen
opzet ontologie, matrix en gegevens in **dezelfde graaf**: met de ont-graph-optie
van pyshacl zien de SPARQL-regels de matrix niet, en wordt elke stroom als fout
gemeld.

## Licentie

Ontologie en gegevens (`*.ttl`): CC BY 4.0. Code: Apache 2.0, zie
[LICENSE](LICENSE). De referentiemodellen in `corpus/miwg/` vallen onder CC BY
3.0 van hun makers.
