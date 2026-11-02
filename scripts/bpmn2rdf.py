"""BPMN 2.0 XML to RDF in the canonical form of the BPMN 2.0 in RDF ontology.

    py bpmn2rdf.py model.bpmn [--base https://example.org/model/] [--lang en] > model.ttl

Metamodel-driven: which XML element or attribute becomes which RDF property
is read from bpmn.ttl (generated from OMG's BPMN20.cmof), not from a
hand-written mapping. Every element with an id becomes a resource; flows keep
their own identity (bpmn:sourceRef, bpmn:targetRef), so parallel flows never
collapse. Diagram interchange (BPMNDI) is left out on purpose: geometry
belongs in the XML, which stays the round-trip format.

Derivable references are not written: FlowNode.incoming and .outgoing are the
inverse of SequenceFlow.targetRef and .sourceRef.

Extension attributes and elements of other namespaces are passed to an
optional hook (`uitbreiding`), so a tool can map its own extensions (links to
ArchiMate, concepts, rules) without touching the core converter.
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from rdflib import RDF, RDFS, XSD, BNode, Graph, Literal, Namespace, URIRef

HIER = Path(__file__).resolve().parent
BPMN = Namespace("https://w3id.org/bpmn#")
MODEL = "http://www.omg.org/spec/BPMN/20100524/MODEL"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
DI_TAGS = {"BPMNDiagram"}
#: Where the XML schema (Semantic.xsd) names a property differently from the
#: metamodel (BPMN20.cmof). The two files are both normative; the converter
#: follows the metamodel and translates here.
XSD_NAAR_CMOF = {"calledElement": "calledElementRef"}
#: Tool extensions: not BPMN semantics, offered to the hook instead.
UITBREIDING_TAGS = {"extensionElements"}
AFGELEID = {"incoming", "outgoing"}
SCHEMA = URIRef("https://schema.org/")


class Metamodel:
    """What the converter needs from bpmn.ttl: classes, superclasses and properties."""

    def __init__(self, ontologie: Graph) -> None:
        g = ontologie
        self.klassen = {str(s).split("#")[1] for s in g.subjects(RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class"))
                        if str(s).startswith(str(BPMN))}
        self.supers: dict[str, set[str]] = {k: set() for k in self.klassen}
        for s, o in g.subject_objects(RDFS.subClassOf):
            if str(s).startswith(str(BPMN)) and str(o).startswith(str(BPMN)):
                self.supers[str(s).split("#")[1]].add(str(o).split("#")[1])
        self.eigenschappen: dict[str, dict[str, Any]] = {}
        obj = URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")
        for soort in (obj, URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")):
            for p in g.subjects(RDF.type, soort):
                naam = str(p).split("#")[-1]
                dom = {str(o).split("#")[1] for o in g.objects(p, RDFS.domain)} | \
                      {str(o).split("#")[1] for o in g.objects(p, SCHEMA + "domainIncludes")}
                rng = list(g.objects(p, RDFS.range))
                rng += list(g.objects(p, SCHEMA + "rangeIncludes"))
                self.eigenschappen[naam] = {
                    "object": soort == obj, "domein": dom,
                    "bereik": {str(o).split("#")[1] for o in rng if str(o).startswith(str(BPMN))},
                    "xsd": next((o for o in rng if str(o).startswith(str(XSD))), None),
                    "composiet": (p, BPMN.composite, Literal(True)) in g,
                }

    def voorouders(self, klasse: str) -> set[str]:
        uit, rij = {klasse}, [klasse]
        while rij:
            for s in self.supers.get(rij.pop(), ()):
                if s not in uit:
                    uit.add(s)
                    rij.append(s)
        return uit

    def eigenschap_van(self, klasse: str, naam: str) -> str | None:
        """De eigenschap `naam` (of zijn meervoud) die deze klasse of een voorouder heeft."""
        anc = self.voorouders(klasse)
        for kandidaat in (naam, naam + "s", naam + "es"):
            e = self.eigenschappen.get(kandidaat)
            if e and (e["domein"] & anc):
                return kandidaat
        return None

    def bevattend(self, ouder: str, kind: str) -> str | None:
        """De samengestelde eigenschap waarmee `ouder` een `kind` bevat."""
        anc_o, anc_k = self.voorouders(ouder), self.voorouders(kind)
        kandidaten = [n for n, e in self.eigenschappen.items()
                      if e["composiet"] and e["domein"] & anc_o and e["bereik"] & anc_k]
        return sorted(kandidaten, key=len)[0] if kandidaten else None


def _klasse(tag: str, mm: Metamodel) -> str | None:
    lokaal = tag.split("}")[-1]
    k = lokaal[:1].upper() + lokaal[1:]
    return k if k in mm.klassen else None


def _xsi_klasse(el: ET.Element, mm: Metamodel) -> str | None:
    t = el.attrib.get(f"{{{XSI}}}type", "")
    t = t.split(":")[-1]
    if t.startswith("t") and t[1:2].isupper():
        t = t[1:]
    return t if t in mm.klassen else None


_MM: Metamodel | None = None


def laad_metamodel() -> Metamodel:
    """De ontologie naast deze map (bpmn.ttl), of de kopie naast dit
    bestand (in SemanticXL: semanticxl/web/bpmn2rdf_metamodel.ttl)."""
    global _MM
    if _MM is None:
        g = Graph()
        for pad in (HIER.parent / "bpmn.ttl", HIER / "bpmn2rdf_metamodel.ttl"):
            if pad.exists():
                g.parse(pad, format="turtle")
                break
        _MM = Metamodel(g)
    return _MM


def converteer(xml: bytes, base: str, taal: str = "en", mm: Metamodel | None = None,
               uitbreiding: Callable[[Graph, URIRef | BNode, str, ET.Element], None] | None = None,
               ) -> tuple[Graph, Counter[str]]:
    """BPMN-XML naar een graaf. Geeft ook terug wat er niet kon (per tag of attribuut)."""
    mm = mm or laad_metamodel()
    g = Graph()
    g.bind("bpmn", BPMN)
    onbekend: Counter[str] = Counter()
    wortel = ET.fromstring(xml)
    ids = {el.attrib["id"] for el in wortel.iter() if "id" in el.attrib}

    def iri(ident: str) -> URIRef:
        return URIRef(base + ident)

    def literal(waarde: str, eig: dict[str, Any]) -> Literal:
        x = eig.get("xsd")
        if x == XSD.boolean:
            return Literal(waarde.strip().lower() == "true", datatype=XSD.boolean)
        if x == XSD.integer:
            try:
                return Literal(int(waarde), datatype=XSD.integer)
            except ValueError:
                return Literal(waarde)
        return Literal(waarde)

    def verwijzing(waarde: str) -> URIRef:
        w = waarde.split(":")[-1] if ":" in waarde and waarde.split(":")[-1] in ids else waarde
        return iri(w)

    def element(el: ET.Element, klasse: str, onderwerp: URIRef | BNode) -> None:
        g.add((onderwerp, RDF.type, BPMN[klasse]))
        for a, waarde in el.attrib.items():
            if a.startswith("{"):
                if uitbreiding and not a.startswith(f"{{{XSI}}}"):
                    uitbreiding(g, onderwerp, a, el)
                continue
            if a == "id":
                g.add((onderwerp, BPMN.id, Literal(waarde)))
                continue
            p = mm.eigenschap_van(klasse, XSD_NAAR_CMOF.get(a, a))
            if not p:
                onbekend[f"@{klasse}.{a}"] += 1
                continue
            eig = mm.eigenschappen[p]
            if eig["object"] and not (eig["xsd"]):
                for w in waarde.split():
                    g.add((onderwerp, BPMN[p], verwijzing(w)))
            else:
                g.add((onderwerp, BPMN[p], literal(waarde, eig)))
            if a == "name" and waarde.strip():
                g.add((onderwerp, RDFS.label, Literal(waarde, lang=taal)))
        tekst = (el.text or "").strip()
        if tekst:
            for p in ("text", "body"):
                if mm.eigenschap_van(klasse, p):
                    g.add((onderwerp, BPMN[p], Literal(tekst)))
                    break
        for kind in el:
            lokaal = kind.tag.split("}")[-1]
            if not kind.tag.startswith(f"{{{MODEL}}}"):
                if uitbreiding:
                    uitbreiding(g, onderwerp, kind.tag, kind)
                continue
            if lokaal in DI_TAGS or lokaal in AFGELEID:
                continue
            if lokaal in UITBREIDING_TAGS:
                if uitbreiding:
                    for x in kind:
                        uitbreiding(g, onderwerp, x.tag, x)
                continue
            kk = _xsi_klasse(kind, mm) or _klasse(kind.tag, mm)
            p = mm.eigenschap_van(klasse, XSD_NAAR_CMOF.get(lokaal, lokaal))
            if p and not mm.eigenschappen[p]["object"]:
                # Een waarde als element: <text>...</text>
                if (kind.text or "").strip():
                    g.add((onderwerp, BPMN[p], literal((kind.text or "").strip(), mm.eigenschappen[p])))
                continue
            eig = mm.eigenschappen.get(p or "", {})
            if p and eig["object"] and not eig["composiet"] and not len(kind):
                # Een verwijzing als element: <flowNodeRef>Task_1</flowNodeRef>
                if (kind.text or "").strip():
                    g.add((onderwerp, BPMN[p], verwijzing((kind.text or "").strip())))
                continue
            if p and not kk:
                # Geen xsi:type: de meest algemene klasse uit het bereik (Expression
                # boven FormalExpression).
                rng = sorted(mm.eigenschappen[p]["bereik"])
                algemeen = [r for r in rng if all(r in mm.voorouders(o) for o in rng)]
                kk = algemeen[0] if algemeen else (rng[0] if len(rng) == 1 else None)
            if not kk:
                onbekend[f"<{klasse}/{lokaal}>"] += 1
                continue
            p = p or mm.bevattend(klasse, kk)
            if not p:
                onbekend[f"<{klasse}/{lokaal}>"] += 1
                continue
            sub: URIRef | BNode = iri(kind.attrib["id"]) if "id" in kind.attrib else BNode()
            g.add((onderwerp, BPMN[p], sub))
            element(kind, kk, sub)
            if lokaal == "documentation" and (kind.text or "").strip():
                g.add((onderwerp, RDFS.comment, Literal((kind.text or "").strip(), lang=taal)))

    k = _klasse(wortel.tag, mm) or "Definitions"
    element(wortel, k, iri(wortel.attrib.get("id", "definitions")))
    return g, onbekend


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("bestand")
    ap.add_argument("--base", default="")
    ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    pad = Path(a.bestand)
    base = a.base or f"urn:bpmn:{pad.stem}:"
    g, onbekend = converteer(pad.read_bytes(), base, a.lang)
    sys.stdout.buffer.write(g.serialize(format="turtle").encode("utf-8"))
    if onbekend:
        lijst = ", ".join(f"{k} ({n})" for k, n in onbekend.most_common())
        sys.stderr.write("niet omgezet: " + lijst + "\n")


if __name__ == "__main__":
    main()
