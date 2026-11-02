# BPMN 2.0 in RDF (draft)

A draft OWL ontology and SHACL validation set for BPMN 2.0.2 (OMG,
formal/13-12-09), built the same way as
[ArchiMate 4.0 in RDF](https://github.com/jwvveen/archimate-rdf): the rules of
the specification are data, validation is separate from meaning, every flow is
a resource, and process models connect to architecture, concepts and rules.
The accompanying article, "BPMN 2.0.2 in RDF: the matrix is data", explains the
reasoning.

*Nederlandse versie: [README.nl.md](README.nl.md).*

Status: **0.1.0-concept**. A discussion piece, not a standard. BPMN is a
specification of the Object Management Group; this is not an OMG publication,
and OMG has no official RDF form of BPMN. The namespace
`https://w3id.org/bpmn#` is proposed and is being registered at w3id.org.

## Files

| File | Role |
|---|---|
| `bpmn.ttl` | **Generated** from OMG's own metamodel (`BPMN20.cmof`): 146 classes with their hierarchy, 212 properties with domain and range, 9 enumerations, `bpmn:abstract` and `bpmn:composite` annotations. Nothing is typed by hand except the Dutch labels |
| `bpmn-matrix.ttl` | **Generated**: Tables 7.3 (Sequence Flow) and 7.4 (Message Flow) of BPMN 2.0.2. The printed tables have 36 cells each; spelled out over the metamodel classes that gives 81 sequence-flow cells (64 permitted) and 56 message-flow cells (42 permitted), each with the printed cell as provenance |
| `bpmn-rules.ttl` | **Generated**: the 59 normative sentences about connections, verbatim with clause and page, each with the shape that checks it or the reason nothing does |
| `bpmn-archimate.ttl` | Bridge to ArchiMate 4.0 (`https://purl.org/archimate#`), concepts and rules: six properties (`elaborates`, `supportedBy`, `performedBy`, `meaning`, `involves`, `appliesRule`) and 24 bridge rules as data, each permitted or discouraged |
| `bpmn-alignments.ttl` | **Generated**: `skos:exactMatch` to sBPMN 2.0, the FBK BPMN 2.0 ontology and BBO, only to terms that exist in their files |
| `shacl/bpmn-shapes.ttl` | Graph integrity and the normative sentences the tables cannot express: pools, containers, events, links, gateways, conditions |
| `shacl/bpmn-matrix-shapes.ttl` | Two generic SPARQL constraints that read the matrix cells as data |
| `shacl/bpmn-archimate-shapes.ttl` | One generic constraint over the bridge rules, and three consistency checks across the notations (warnings) |
| `example.ttl` | A small model that is wrong on purpose; yields exactly ten results |
| `validate.py` | Validation of RDF or BPMN XML models, one by one or together |
| `scripts/bpmn2rdf.py` | Converter from BPMN 2.0 XML to the canonical form, driven by the metamodel |
| `scripts/generate_*.py`, `scripts/coverage.py` | The generators, and which shape covers which normative sentence |
| `sources/` | Where every fact came from: the extracted tables and sentences (`bpmn-connection-rules.json`), notes on the specification, and a survey of earlier BPMN ontologies (`prior-work.md`) |
| `corpus/miwg/` | 21 reference models of the BPMN Model Interchange Working Group, as a test set (CC BY 3.0, see the notice there) |

## Design choices

* **Every flow is a resource.** BPMN already gives flows their own identity,
  with `sourceRef` and `targetRef`. The canonical form keeps that, so two flows
  between the same gateway and end event never collapse, and names and
  conditions stay on the flow:

  ```turtle
  ex:Flow_7 a bpmn:SequenceFlow ;
      bpmn:sourceRef ex:CheckRegistration ;
      bpmn:targetRef ex:IsValid ;
      bpmn:name "number provided" .
  ```

  A direct predicate between flow nodes is derived sugar, one CONSTRUCT away:

  ```sparql
  CONSTRUCT { ?a bpmn:flowsTo ?b }
  WHERE { ?f a bpmn:SequenceFlow ; bpmn:sourceRef ?a ; bpmn:targetRef ?b }
  ```

  `incoming` and `outgoing` are not written (they are the inverse of
  `targetRef` and `sourceRef`). Diagram interchange is left out on purpose:
  geometry belongs in the XML, which stays the round-trip format.

* **The metamodel is data.** Terms are generated from the CMOF, not from the
  XML schema. The CMOF knows which classes are abstract, which class owns a
  property and which containment is composite. Where the schema and the
  metamodel use different names (`calledElement` against `calledElementRef`),
  the converter follows the metamodel.

* **The matrix is data, and so is the prose.** The connection tables are in
  the graph as cells, read by two generic constraints. The normative sentences
  are in the graph too: 42 of the 59 are checked by a shape, 12 are
  permissions already encoded as permitted cells, 3 depend on diagram
  geometry and 2 only describe scope.

* **The bridge is data.** Which BPMN element may be linked to which ArchiMate
  concept is a set of bridge rules, read by one generic constraint. Three
  checks look across the notations: a lane whose role is not assigned to the
  process in ArchiMate, a task whose application does not serve the process,
  and a message between pools whose actors have no relationship.

* **Ontology and validation are separate**, and everything is **bilingual**
  (English and Dutch).

* **A printing error in the specification.** In the published BPMN 2.0.2 PDF,
  ten cells show a per mille sign or a circumflex where an arrow belongs: the
  whole column of the plain activity shape (a task) in Table 7.3, and the whole
  Message Start Event column of Table 7.4. Read literally, no sequence flow may
  enter a task. The defect is open OMG issue
  [BPMN21-453](https://issues.omg.org/issues/BPMN21-453) (April 2026). The matrix
  records these cells as permitted, with the evidence (BPMN 1.2 and the
  normative text) in the cell.

## Validating

```
pip install rdflib pyshacl
python validate.py
```

Expected results on `example.ttl`, ten in total:

1. **Violation** `pl-back`: Table 7.3 forbids a Sequence Flow into a Start Event.
2. **Violation** `pl-to-note`: no cell permits a flow to a Text Annotation (8.4.1).
3. **Violation** `mf-same-pool` (twice): a Message Flow inside one pool (9.4), and no cell permits it.
4. **Violation** `mf-from-start`: no cell permits a Message Flow out of a plain Start Event.
5. **Violation** `pl-start`: no bridge rule lets a Start Event be supported by an application.
6. **Warnings** (four): two message flows between pools whose actors have no
   relationship in ArchiMate, and two steps whose application does not serve
   the process.

The reference corpus, converted on the fly:

```
python validate.py corpus/miwg/*.bpmn
```

Result: 0 violations, 5 warnings (activities without a name). Models are
validated one by one; that takes about two minutes for all 21. Use
`--together` when the bridge checks must see processes and an ArchiMate model
in one graph, and `--archimate=DIR` to point to a clone of archimate-rdf (by
default it is looked for next to this repository).

Load ontology, matrix and data into the **same graph** when you build your own
validation: with pyshacl's ont-graph option the SPARQL constraints cannot see
the matrix, and every flow is reported as a violation. Two more traps: an
element can carry more than one `rdf:type` (match the matrix through
`rdfs:subClassOf` on any of them), and SHACL-SPARQL constraints may not contain
a `VALUES` clause.

## Converting

```
python scripts/bpmn2rdf.py model.bpmn --base https://example.org/model/ > model.ttl
```

Tool extensions can be mapped through an optional hook, without touching the
core converter.

## Regenerating

```
python scripts/generate_ontology_ttl.py       # downloads BPMN20.cmof from OMG into sources/.cache
python scripts/generate_matrix_ttl.py
python scripts/generate_alignments.py DIR     # DIR with sbpmn.ttl, fbk.owl, bbo.owl
```

The generated files are committed; the scripts are the only way to change
them. The OMG metamodel and the earlier ontologies are not redistributed here.

## Earlier work

This builds on, and aligns with, earlier BPMN ontologies: the FBK BPMN 1.1
and 2.0 ontologies, BBO, and sBPMN 2.0 (Krause, 2025), which is the closest
to this draft. `sources/prior-work.md` compares them. The alignment file uses
`skos:exactMatch` only; no `owl:equivalentClass`, so loading it never imports
another ontology's axioms.

## Contributing

Disagreement is welcome, especially on the design choices above. If you
maintain one of the earlier ontologies, build BPMN tooling, or have a corpus
that breaks these rules, open an issue.

## License

Ontology and data files (`*.ttl`): CC BY 4.0, as declared in the ontology.
Code: Apache 2.0, see [LICENSE](LICENSE). The ontology is derived from OMG's
machine-readable BPMN metamodel; BPMN is a standard of the Object Management
Group. The MIWG reference models in `corpus/miwg/` are licensed CC BY 3.0 by
their authors. ArchiMate is a registered trademark of The Open Group.
