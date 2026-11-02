"""Generate the BPMN 2.0 core ontology from OMG's own metamodel (BPMN20.cmof).

    py scripts/generate_ontology_ttl.py [pad/naar/BPMN20.cmof]

Without an argument the CMOF is downloaded from
https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof into sources/.cache/
(not committed: the OMG files stay at OMG). Writes bpmn.ttl.

Nothing in bpmn.ttl is typed by hand except the Dutch labels (NL below) and
the ontology header: classes, the class hierarchy, properties, their domains
and ranges and the enumerations all come from the metamodel. The metamodel is
data, just like the ArchiMate relationship matrix.
"""
from __future__ import annotations

import hashlib
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

WORTEL = Path(__file__).resolve().parents[1]
MAP = WORTEL
CMOF_URL = "https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof"
NS = "https://w3id.org/bpmn#"
X = "{http://schema.omg.org/spec/XMI/2.1}"
VERSIE = "0.1.0"

#: Dutch labels for the classes a modeller actually meets. The rest keeps its
#: English label: a wrong Dutch word is worse than an English one.
NL = {
    "Process": "Proces", "SubProcess": "Deelproces", "Transaction": "Transactie",
    "CallActivity": "Aanroepactiviteit", "Task": "Taak", "UserTask": "Gebruikerstaak",
    "ServiceTask": "Servicetaak", "ManualTask": "Handmatige taak", "ScriptTask": "Scripttaak",
    "BusinessRuleTask": "Bedrijfsregeltaak", "SendTask": "Verzendtaak", "ReceiveTask": "Ontvangsttaak",
    "Activity": "Activiteit", "Event": "Gebeurtenis", "StartEvent": "Startgebeurtenis",
    "EndEvent": "Eindgebeurtenis", "IntermediateCatchEvent": "Tussengebeurtenis (vangend)",
    "IntermediateThrowEvent": "Tussengebeurtenis (werpend)", "BoundaryEvent": "Randgebeurtenis",
    "Gateway": "Gateway", "ExclusiveGateway": "Exclusieve gateway", "InclusiveGateway": "Inclusieve gateway",
    "ParallelGateway": "Parallelle gateway", "EventBasedGateway": "Gebeurtenisgestuurde gateway",
    "ComplexGateway": "Complexe gateway", "SequenceFlow": "Volgordestroom", "MessageFlow": "Berichtenstroom",
    "Association": "Associatie", "DataObject": "Gegevensobject", "DataObjectReference": "Verwijzing naar gegevensobject",
    "DataStore": "Gegevensopslag", "DataStoreReference": "Verwijzing naar gegevensopslag",
    "DataInputAssociation": "Gegevensinvoer", "DataOutputAssociation": "Gegevensuitvoer",
    "Participant": "Deelnemer", "Collaboration": "Samenwerking", "Lane": "Baan", "LaneSet": "Banenset",
    "Message": "Bericht", "Signal": "Signaal", "Error": "Fout", "Escalation": "Escalatie",
    "TimerEventDefinition": "Tijdgebeurtenis", "MessageEventDefinition": "Berichtgebeurtenis",
    "SignalEventDefinition": "Signaalgebeurtenis", "ErrorEventDefinition": "Foutgebeurtenis",
    "ConditionalEventDefinition": "Voorwaardelijke gebeurtenis", "LinkEventDefinition": "Koppelgebeurtenis",
    "CompensateEventDefinition": "Compensatiegebeurtenis", "EscalationEventDefinition": "Escalatiegebeurtenis",
    "TerminateEventDefinition": "Beëindigingsgebeurtenis", "CancelEventDefinition": "Annuleringsgebeurtenis",
    "TextAnnotation": "Tekstannotatie", "Group": "Groep", "FlowNode": "Stroomknoop",
    "FlowElement": "Stroomelement", "Artifact": "Artefact", "Definitions": "Definities",
}

_PRIM = {"String": "xsd:string", "Boolean": "xsd:boolean", "Integer": "xsd:integer",
         "Real": "xsd:decimal", "Element": "rdfs:Resource"}


def woorden(naam: str) -> str:
    """SequenceFlow -> 'Sequence flow' (spec style: first word capitalised)."""
    delen = re.findall(r"[A-Z]+(?![a-z])|[A-Z][a-z]*|[a-z]+|\d+", naam)
    if not delen:
        return naam
    return " ".join([delen[0]] + [d if d.isupper() and len(d) > 1 else d.lower() for d in delen[1:]])


def lit(t: str, taal: str = "en") -> str:
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"') + f'"@{taal}'


def lees(pad: Path) -> tuple[dict, dict, dict]:
    r = ET.parse(pad).getroot()
    klassen = {e.attrib["name"]: e for e in r.iter()
               if e.attrib.get(X + "type") == "cmof:Class" and "name" in e.attrib}
    enums = {e.attrib["name"]: [lt.attrib["name"] for lt in e if lt.tag == "ownedLiteral"]
             for e in r.iter() if e.attrib.get(X + "type") == "cmof:Enumeration"}
    return r, klassen, enums


def type_van(attr: ET.Element) -> str:
    t = attr.attrib.get("type")
    if t:
        return t
    for g in attr:
        if g.tag == "type" and "href" in g.attrib:
            return g.attrib["href"].split("#")[-1]
    return "Element"


def genereer(pad: Path) -> str:
    _, klassen, enums = lees(pad)
    sha = hashlib.sha256(pad.read_bytes()).hexdigest()
    uit = [
        f"@prefix bpmn: <{NS}> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix dct: <http://purl.org/dc/terms/> .",
        "@prefix schema: <https://schema.org/> .",
        "",
        "# GENERATED by scripts/generate_ontology_ttl.py from the OMG BPMN 2.0 metamodel",
        f"# ({CMOF_URL}, sha256 {sha}). Do not edit by hand.",
        "",
        f"<{NS.rstrip('#')}> a owl:Ontology ;",
        f"    dct:title {lit('BPMN 2.0 in RDF: core ontology')}, {lit('BPMN 2.0 in RDF: kernontologie', 'nl')} ;",
        f"    dct:description {lit('Classes, properties and enumerations of the BPMN 2.0.2 semantic metamodel, generated from BPMN20.cmof. Concept version for discussion; not a publication of the Object Management Group.')} ;",
        f"    dct:source <{CMOF_URL}> ;",
        "    dct:license <https://creativecommons.org/licenses/by/4.0/> ;",
        f'    owl:versionInfo "{VERSIE}" .',
        "",
        "bpmn:abstract a owl:AnnotationProperty ;",
        f"    rdfs:label {lit('abstract')}, {lit('abstract', 'nl')} ;",
        f"    rdfs:comment {lit('True for metamodel classes that have no instances of their own (isAbstract in the CMOF).')} .",
        "",
        "bpmn:composite a owl:AnnotationProperty ;",
        f"    rdfs:label {lit('composite')} ;",
        f"    rdfs:comment {lit('True for properties that own their values (isComposite in the CMOF): the value lives inside its owner.')} .",
        "",
    ]
    # Classes
    for naam in sorted(klassen):
        e = klassen[naam]
        supers = [s for s in e.attrib.get("superClass", "").split() if s in klassen]
        regels = [f"bpmn:{naam} a owl:Class", f"rdfs:label {lit(woorden(naam))}" +
                  (f", {lit(NL[naam], 'nl')}" if naam in NL else "")]
        regels += [f"rdfs:subClassOf bpmn:{s}" for s in supers]
        if e.attrib.get("isAbstract") == "true":
            regels.append("bpmn:abstract true")
        regels.append(f"rdfs:isDefinedBy <{NS.rstrip('#')}>")
        uit.append(" ;\n    ".join(regels) + " .\n")
    # Enumerations
    for naam, waarden in sorted(enums.items()):
        uit.append(f"bpmn:{naam} a owl:Class ;\n    rdfs:label {lit(woorden(naam))} ;\n"
                   f"    owl:oneOf ( {' '.join(f'bpmn:{naam}-{w}' for w in waarden)} ) .\n")
        for w in waarden:
            uit.append(f"bpmn:{naam}-{w} a bpmn:{naam} ; rdfs:label {lit(woorden(w))} .")
        uit.append("")
    # Properties: one RDF property per name; domains and ranges collected over owners.
    eigenaar: dict[str, set[str]] = defaultdict(set)
    bereik: dict[str, set[str]] = defaultdict(set)
    samengesteld: dict[str, bool] = defaultdict(bool)
    for naam, e in klassen.items():
        for a in e:
            if a.tag != "ownedAttribute" or "name" not in a.attrib:
                continue
            p = a.attrib["name"]
            eigenaar[p].add(naam)
            bereik[p].add(type_van(a))
            samengesteld[p] |= a.attrib.get("isComposite") == "true"
    for p in sorted(eigenaar):
        typen = bereik[p]
        object_ = all(t in klassen or t in enums or t in ("Element", "BPMNDiagram") for t in typen)
        regels = [f"bpmn:{p} a {'owl:ObjectProperty' if object_ else 'owl:DatatypeProperty'}",
                  f"rdfs:label {lit(woorden(p))}"]
        dom = sorted(eigenaar[p])
        regels += [f"rdfs:domain bpmn:{dom[0]}"] if len(dom) == 1 else [f"schema:domainIncludes bpmn:{d}" for d in dom]
        rng = sorted(f"bpmn:{t}" if (t in klassen or t in enums) else _PRIM.get(t, "rdfs:Resource") for t in typen)
        regels += [f"rdfs:range {rng[0]}"] if len(rng) == 1 else [f"schema:rangeIncludes {r}" for r in rng]
        if samengesteld[p]:
            regels.append("bpmn:composite true")
        regels.append(f"rdfs:isDefinedBy <{NS.rstrip('#')}>")
        uit.append(" ;\n    ".join(regels) + " .\n")
    return "\n".join(uit)


def main() -> None:
    if len(sys.argv) > 1:
        pad = Path(sys.argv[1])
    else:
        pad = MAP / "sources" / ".cache" / "BPMN20.cmof"
        if not pad.exists():
            pad.parent.mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(CMOF_URL, timeout=60) as r:  # noqa: S310 - vast adres
                pad.write_bytes(r.read())
    tekst = genereer(pad)
    (MAP / "bpmn.ttl").write_text(tekst, encoding="utf-8", newline="\n")
    print("bpmn.ttl", tekst.count(" a owl:Class"), "klassen,",
          tekst.count("a owl:ObjectProperty") + tekst.count("a owl:DatatypeProperty"), "eigenschappen")


if __name__ == "__main__":
    main()
