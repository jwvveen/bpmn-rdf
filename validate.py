"""Validate BPMN models against the connection matrix and the rule shapes.

    python validate.py                          # the example model
    python validate.py model.ttl other.bpmn     # per model; .bpmn/.xml is converted first
    python validate.py p1.bpmn p2.bpmn am.ttl --together
    python validate.py corpus/miwg/*.bpmn --json

Loads ontology, matrix, bridge and model data into ONE graph: pyshacl's
ont-graph option hides the matrix from the SPARQL constraints in shacl/, and
every flow is then reported as a violation without any warning.

Models are validated one by one by default, because a SPARQL constraint over a
small graph is far faster than over everything at once. Use --together when
the bridge checks must look across models (processes plus an ArchiMate model).

The ArchiMate ontology is read from a clone of archimate-rdf next to this
repository, or from --archimate=DIR. Without it the bridge checks still work
for elements typed directly with an ArchiMate 4.0 class.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import rdflib
from pyshacl import validate

HERE = Path(__file__).resolve().parent
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
sys.path.insert(0, str(HERE / "scripts"))
import bpmn2rdf  # noqa: E402

ARCHIMATE = next((Path(a.split("=", 1)[1]) for a in sys.argv if a.startswith("--archimate=")),
                 HERE.parent / "archimate-rdf")


def load(files: list[Path]) -> rdflib.Graph:
    g = rdflib.Graph()
    for f in ("bpmn.ttl", "bpmn-matrix.ttl", "bpmn-archimate.ttl"):
        g.parse(HERE / f, format="turtle")
    for f in ("archimate.ttl", "archimate-profile-3.2.ttl"):
        if (ARCHIMATE / f).exists():
            g.parse(ARCHIMATE / f, format="turtle")
    for f in files:
        if f.suffix.lower() in (".bpmn", ".xml"):
            model, _ = bpmn2rdf.converteer(f.read_bytes(), f.resolve().as_uri() + "#")
            g += model
        else:
            g.parse(f, format="turtle")
    return g


def shapes() -> rdflib.Graph:
    s = rdflib.Graph()
    for f in sorted((HERE / "shacl").glob("*.ttl")):
        s.parse(f, format="turtle")
    return s


_NL = re.compile(r"\b(een|het|de|van|niet|deze|geen|moet|verbiedt|baan|stroom|staat)\b", re.I)


def _english(messages: list) -> str:
    """The English message: by language tag, else the one with the fewest Dutch words."""
    for m in messages:
        if getattr(m, "language", None) == "en":
            return str(m)
    return sorted((str(m) for m in messages), key=lambda t: len(_NL.findall(t)))[0] if messages else ""


def check(data: rdflib.Graph, shape_graph: rdflib.Graph | None = None) -> list[dict]:
    shape_graph = shape_graph or shapes()
    _, report, _ = validate(data, shacl_graph=shape_graph, inference="none", advanced=True)
    out = []
    for r in report.subjects(rdflib.RDF.type, SH.ValidationResult):
        shape = report.value(r, SH.sourceShape)
        if isinstance(shape, rdflib.BNode):
            # A property shape has no name: report the node shape it belongs to.
            shape = shape_graph.value(predicate=SH.property, object=shape) or shape
        out.append({
            "focus": str(report.value(r, SH.focusNode)),
            "shape": str(shape).split("#")[-1],
            "severity": str(report.value(r, SH.resultSeverity)).split("#")[-1],
            "message": _english(list(report.objects(r, SH.resultMessage))),
        })
    return out


def main() -> None:
    files = [Path(a) for a in sys.argv[1:] if not a.startswith("--")] or [HERE / "example.ttl"]
    shape_graph = shapes()
    results = []
    if "--together" in sys.argv:
        for r in check(load(files), shape_graph):
            r["model"] = "together"
            results.append(r)
    else:
        for f in files:
            for r in check(load([f]), shape_graph):
                r["model"] = f.stem
                results.append(r)
    if "--json" in sys.argv:
        print(json.dumps(results, indent=1, ensure_ascii=False))
        return
    count = Counter((r["severity"], r["shape"]) for r in results)
    for (severity, shape), n in sorted(count.items()):
        print(f"{severity:9} {shape:40} {n}")
    print(f"total {len(results)}")


if __name__ == "__main__":
    main()
