"""Generate the BPMN connection matrix and the rule catalogue as RDF.

    py scripts/generate_matrix_ttl.py

Source: sources/bpmn-connection-rules.json, extracted from the
BPMN 2.0.2 specification (Tables 7.3 and 7.4, plus the normative sentences
around them). Writes:

  bpmn-matrix.ttl   every cell of both tables, spelled out over
                                  the metamodel classes, permitted or not
  bpmn-rules.ttl    the normative sentences as a catalogue, each
                                  with the SHACL shape that checks it, or the
                                  reason it is not checked
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

WORTEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORTEL / "scripts"))
from generate_ontology_ttl import NS, lit  # noqa: E402

MAP = WORTEL
SPEC = "https://www.omg.org/spec/BPMN/2.0.2/PDF"
SH = "https://w3id.org/bpmn/shapes#"

#: Which metamodel classes a symbol in the tables stands for, and which
#: trigger (event definition) it needs. Tasks stand for every Task subtype
#: and for a Call Activity drawn as a task; Sub-Process includes Transaction
#: and Ad-Hoc Sub-Process through the class hierarchy.
SEQUENCE = {
    "StartEvent": [("StartEvent", None)],
    "Task": [("Task", None), ("CallActivity", None)],
    "SubProcess": [("SubProcess", None)],
    "Gateway": [("Gateway", None)],
    "IntermediateEvent": [("IntermediateCatchEvent", None), ("IntermediateThrowEvent", None),
                          ("BoundaryEvent", None)],
    "EndEvent": [("EndEvent", None)],
}
#: For Message Flow the row is the sending side and the column the receiving
#: side: a throwing intermediate event sends, a catching one receives.
MESSAGE_BRON = {
    "MessageStartEvent": [("StartEvent", "MessageEventDefinition")],
    "Pool": [("Participant", None)],
    "Task": [("Task", None), ("CallActivity", None)],
    "SubProcess": [("SubProcess", None)],
    "MessageIntermediateEvent": [("IntermediateThrowEvent", "MessageEventDefinition")],
    "MessageEndEvent": [("EndEvent", "MessageEventDefinition")],
}
MESSAGE_DOEL = dict(MESSAGE_BRON, MessageIntermediateEvent=[
    ("IntermediateCatchEvent", "MessageEventDefinition"), ("BoundaryEvent", "MessageEventDefinition")])

#: Which shape checks which normative sentence (by its position in the JSON),
#: or why no shape does. Filled in by hand: this is the coverage of the work.
DEKKING: dict[int, str] = {}


def _cellen(soort: str, tabel: dict, bron_map: dict, doel_map: dict, kop: str) -> list[str]:
    uit = []
    labels = {o["id"]: o["label"] for o in tabel["objects"]}
    for regel in tabel["rules"]:
        for bk, btrig in bron_map[regel["from"]]:
            for dk, dtrig in doel_map[regel["to"]]:
                iri = f"bpmn:rule-{soort}-{bk}-{dk}" + (f"-{btrig[:-15]}" if btrig else "") + \
                      (f"-to-{dtrig[:-15]}" if dtrig else "")
                paren = [
                    "a bpmn:ConnectionRule",
                    f"bpmn:flowType bpmn:{'SequenceFlow' if soort == 'sf' else 'MessageFlow'}",
                    f"bpmn:sourceType bpmn:{bk}",
                    f"bpmn:targetType bpmn:{dk}",
                    f"bpmn:permitted {'true' if regel['allowed'] else 'false'}",
                    f"bpmn:specCell {lit(kop + ', row ' + labels[regel['from']] + ', column ' + labels[regel['to']])}",
                    f"dct:source <{SPEC}>",
                ]
                if btrig:
                    paren.append(f"bpmn:sourceTrigger bpmn:{btrig}")
                if dtrig:
                    paren.append(f"bpmn:targetTrigger bpmn:{dtrig}")
                if regel.get("note"):
                    paren.append(f"rdfs:comment {lit(regel['note'])}")
                uit.append(f"{iri} " + " ;\n    ".join(paren) + " .\n")
    return uit


KOP = [
    f"@prefix bpmn: <{NS}> .",
    "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
    "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
    "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
    "@prefix dct: <http://purl.org/dc/terms/> .",
    f"@prefix bpmnsh: <{SH}> .",
    "",
]

VOCAB = f"""# The matrix vocabulary. Not part of the OMG metamodel.
bpmn:ConnectionRule a owl:Class ;
    rdfs:label {lit('Connection rule')}, {lit('Verbindingsregel', 'nl')} ;
    rdfs:comment {lit('One cell of the BPMN connection tables, spelled out over metamodel classes: may a flow of this type run from this kind of element to that kind?')} .
bpmn:flowType a owl:ObjectProperty ; rdfs:label {lit('flow type')} ; rdfs:domain bpmn:ConnectionRule .
bpmn:sourceType a owl:ObjectProperty ; rdfs:label {lit('source type')} ; rdfs:domain bpmn:ConnectionRule .
bpmn:targetType a owl:ObjectProperty ; rdfs:label {lit('target type')} ; rdfs:domain bpmn:ConnectionRule .
bpmn:sourceTrigger a owl:ObjectProperty ; rdfs:label {lit('source trigger')} ;
    rdfs:comment {lit('The event definition the source must carry, for the message events of Table 7.4.')} .
bpmn:targetTrigger a owl:ObjectProperty ; rdfs:label {lit('target trigger')} .
bpmn:permitted a owl:DatatypeProperty ; rdfs:label {lit('permitted')}, {lit('toegestaan', 'nl')} ; rdfs:range xsd:boolean .
bpmn:specCell a owl:DatatypeProperty ; rdfs:label {lit('specification cell')} ;
    rdfs:comment {lit('Where this cell is printed in the specification.')} .

"""


def matrix() -> str:
    d = json.loads((MAP / "sources" / "bpmn-connection-rules.json").read_text(encoding="utf-8"))
    uit = list(KOP) + [
        "# GENERATED by scripts/generate_matrix_ttl.py from sources/bpmn-connection-rules.json",
        "# (BPMN 2.0.2, formal/13-12-09, Tables 7.3 and 7.4). Do not edit by hand.", "", VOCAB]
    uit += _cellen("sf", d["sequenceFlow"], SEQUENCE, SEQUENCE, "BPMN 2.0.2 Table 7.3 (7.6.1)")
    uit += _cellen("mf", d["messageFlow"], MESSAGE_BRON, MESSAGE_DOEL, "BPMN 2.0.2 Table 7.4 (7.6.2)")
    return "\n".join(uit)


def regels(dekking: dict[int, str]) -> str:
    d = json.loads((MAP / "sources" / "bpmn-connection-rules.json").read_text(encoding="utf-8"))
    uit = list(KOP) + [
        "# GENERATED by scripts/generate_matrix_ttl.py: the normative sentences of BPMN 2.0.2",
        "# about connections, each with the shape that checks it. Do not edit by hand;",
        "# the coverage is kept in scripts/coverage.py.", "",
        f"""bpmn:NormativeStatement a owl:Class ;
    rdfs:label {lit('Normative statement')}, {lit('Normatieve uitspraak', 'nl')} ;
    rdfs:comment {lit('A sentence from the BPMN specification that constrains models, quoted verbatim with its clause and page.')} .
bpmn:checkedBy a owl:ObjectProperty ; rdfs:label {lit('checked by')} ; rdfs:domain bpmn:NormativeStatement .
bpmn:notCheckedBecause a owl:DatatypeProperty ; rdfs:label {lit('not checked because')} .
bpmn:clause a owl:DatatypeProperty ; rdfs:label {lit('clause')} .
bpmn:page a owl:DatatypeProperty ; rdfs:label {lit('page')} .
bpmn:verbatim a owl:DatatypeProperty ; rdfs:label {lit('verbatim text')} .
"""]
    for i, c in enumerate(d["constraints"], start=1):
        paren = ["a bpmn:NormativeStatement", f"bpmn:clause {lit(str(c['section']))}",
                 f"bpmn:page {lit(str(c['page']))}", f"bpmn:verbatim {lit(c['text'])}",
                 f"dct:source <{SPEC}>"]
        waarde = dekking.get(i, "")
        if waarde.startswith("bpmnsh:"):
            paren += [f"bpmn:checkedBy {s.strip()}" for s in waarde.split(",")]
        elif waarde:
            paren.append(f"bpmn:notCheckedBecause {lit(waarde)}")
        uit.append(f"bpmn:statement-{i:02d} " + " ;\n    ".join(paren) + " .\n")
    return "\n".join(uit)


def main() -> None:
    from coverage import DEKKING

    dekking = DEKKING

    (MAP / "bpmn-matrix.ttl").write_text(matrix(), encoding="utf-8", newline="\n")
    (MAP / "bpmn-rules.ttl").write_text(regels(dekking), encoding="utf-8", newline="\n")
    d = json.loads((MAP / "sources" / "bpmn-connection-rules.json").read_text(encoding="utf-8"))
    n = len(d["constraints"])
    gedekt = sum(1 for i in range(1, n + 1) if dekking.get(i, "").startswith("bpmnsh:"))
    print(f"matrix en regelcatalogus geschreven; {gedekt} van {n} uitspraken gecontroleerd door een shape")


if __name__ == "__main__":
    main()
