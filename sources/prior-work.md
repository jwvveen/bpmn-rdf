# Prior work: BPMN 2.0 in RDF, OWL and SHACL

Survey date: 2 November 2026. Purpose: let the new BPMN 2.0 RDF ontology (`https://w3id.org/bpmn#`, generated from `BPMN20.cmof`) align with existing efforts instead of duplicating them.

Method. Every claim below was checked against a primary source: the ontology file itself (downloaded and parsed with rdflib 7.6), the repository (GitHub API: commits, licence, file tree), the paper (Crossref record, CEUR or preprint PDF) or an archived copy of the project page (Internet Archive). Class and property counts are counts of named `owl:Class`, `owl:ObjectProperty` and `owl:DatatypeProperty` in the ontology namespace, measured by us. Where a fact could not be checked it says "not verified". Discovery used the GitHub search API, Crossref, CEUR and the Wayback CDX index, so smaller efforts outside GitHub may be missing.

## 1. Comparison table

| # | Effort | Year | Namespace IRI | Licence | Coverage | Style | Validation | Files online | Last activity |
|---|---|---|---|---|---|---|---|---|---|
| 1 | FBK BPMN 1.1 Ontology (Rospocher, Ghidini, Serafini) | 2009 (v1.01), paper 2014 | `http://dkm.fbk.eu/index.php/BPMN_Ontology#` | CC BY-NC-SA (project page, archived) | BPMN 1.1 full element/attribute set (Annex B): process, pools, lanes, message flow, artifacts | OWL 2 DL, SHOIN(D), 463 class axioms (paper); lowercase snake_case names | OWL reasoning; integrity constraint semantics discussed | No (dkm.fbk.eu returns HTTP 500/404); archived copy yes | 2014 |
| 2 | FBK BPMN 2.0 Ontology v0.4 | about 2011 to 2014 | `http://dkm.fbk.eu/index.php/BPMN2_Ontology#` | CC BY-NC-SA (same page) | BPMN 2.0 semantic model incl. collaboration, choreography, conversation, and DI (BPMNDiagram, BPMNShape, Bounds) | Generated from the OMG XSDs; 187 classes, 131 object, 57 datatype properties; 466 qualified cardinality restrictions; `has_` prefixed properties; no disjointness | OWL reasoning only | Original no; archived copy yes; mirror in InES-Mannheim/spa-core | Never refined beyond "work in progress" |
| 3 | BBO, BPMN 2.0 Based Ontology (Annane, Aussenac-Gilles, Kamel, IRIT MELODI) | 2019 | Three IRIs in circulation (see 3.3) | GPL-3.0 (repo) | Process fragment (BPMN chapter 10) plus resources, agents, manufacturing, units | OWL 2 DL with rich axioms: 155 classes, 106 object, 34 datatype properties, 148 restrictions, 59 disjointWith, property chains | 212 SHACL NodeShapes (domain/range only) | Yes (GitHub, irit.fr, w3id fork) | Original repo 2019-06-26; fork 2025-02-24 |
| 4 | sBPMN (SUPER project, Abramowicz et al.) | 2007 | not verified | not verified | BPMN 1.0, 95 concepts, over 50 axioms (paper) | WSML, not RDF/OWL | WSML reasoning | No (only the paper) | 2007 to 2009 |
| 5 | Natschläger, "Towards a BPMN 2.0 Ontology" | 2011 | not verified | not verified | BPMN 2.0 (paper) | OWL (per paper title; file not found) | not verified | No file found | 2011 |
| 6 | sBPMN 2.0 (Krause, Paulheim, Vázquez, Espert) | 2025 | `https://sBPMN.github.io/2.0/classes#`, `.../properties#` | CC BY 4.0 (declared in ontology; repo has no LICENSE file) | BPMN 2.0 semantic model incl. collaboration, choreography, conversation; no DI | Light OWL: 166 classes, 126 object, 44 datatype properties, 31 restrictions; domain/range; lowerCamel names mirroring the XSD | 83 SHACL NodeShapes (cardinalities, defaults, enumerations) | Yes | 2026-03-25 |
| 7 | FH Joanneum BPMN 2.0 ontology (Martina Reiter; tester by hoedlale16) | 2018 to 2019 | `http://www.reiter.at/ontology/bpmn2.0#` | Apache-2.0 (repo) | BPMN 2.0 incl. DI, conformance classes, execution instance state | OWL; 264 classes, 174 object, 68 datatype properties; 454 restrictions | Java test tool against the BPMN MIWG test suite | Yes | 2019-01-29 |
| 8 | IDPO, Information Delivery Processes Ontology (RUB) | 2020 | `https://w3id.org/idpo#` | CC BY-SA 4.0 in the ontology, CC-BY-4.0 on the repo (mismatch) | Construction information delivery on top of BPMN tasks and data objects | Small OWL, subclasses PROV-O; refers to BPMN via `bpmn2:` = `http://www.omg.org/spec/BPMN/20100524/MODEL#` | SHACL templates | Yes | 2022-01-23 |

Not an ontology, but relevant converters and users are listed in section 4.

## 2. Related standards to link to

| Resource | IRI or URL | Verified | Relevance |
|---|---|---|---|
| OMG BPMN 2.0.2 specification page | https://www.omg.org/spec/BPMN/2.0.2/ | yes (200) | Normative text |
| OMG BPMN semantic metamodel (CMOF) | https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof | yes (200) | Source of the new ontology; also `BPMNDI.cmof`, `DI.cmof`, `DC.cmof`, `Infrastructure.cmof` (20100502) listed on the spec page |
| OMG XML schemas | https://www.omg.org/spec/BPMN/20100501/BPMN20.xsd, `Semantic.xsd`, `BPMNDI.xsd`, `DC.xsd`, `DI.xsd` | yes (200) | Interchange format; FBK 2.0 and sBPMN 2.0 were derived from these |
| BPMN XML namespace | `http://www.omg.org/spec/BPMN/20100524/MODEL` | returns 404 (not dereferenceable) | Used by IDPO as an RDF namespace with `#`; an OMG XML namespace, not an RDF vocabulary |
| W3C PROV-O | `http://www.w3.org/ns/prov#`, doc https://www.w3.org/ns/prov-o | yes (200) | Execution traces: process instance as `prov:Activity`; used by IDPO |
| P-Plan | `http://purl.org/net/p-plan#` | PURL resolves (303) to vocab.linkeddata.es, which did not respond; mirror https://www.opmw.org/model/p-plan/ responds | Plans and steps linked to PROV; used with the FBK BPMN 2.0 namespace in fairworkflows |
| ArchiMate 3.2 ontology (Alberto D. Mendoza) | ontology IRI `https://purl.org/archimate/owl`, README namespace `https://purl.org/archimate#`; repo AlbertoDMendoza/archimate_ontology | yes; Apache-2.0; pushed 2026-10-20 | Contains no BPMN terms (0 matches for "bpmn"). Has SHACL validation and derivation rules |
| archimate2rdf (bp4mc2) | `http://bp4mc2.org/def/archimate#`; repo bp4mc2/archimate2rdf | yes; no licence; last commit 2019-06-25 | Generated from the exchange-format XSD; no BPMN terms. Same XSD-to-OWL approach as FBK 2.0 |
| ArchiMate 4.0 draft ontology (jwvveen/archimate-rdf) | own namespace `https://w3id.org/archimate#` (until 0.2.0 `https://purl.org/archimate#`); aligned to the 3.2 ontology with `skos:exactMatch` | yes; Apache-2.0 | Sibling effort; relationship-as-resource pattern worth keeping consistent with the BPMN ontology |
| The Open Group guidance on ArchiMate with BPMN | publications.opengroup.org | catalogue search for "ArchiMate BPMN" returns 4 items: D049 "Hybrid EA Frameworks: TOGAF + ArchiMate + BPMN + MoDAF/DoDAF", D182 "The Advantages of Combining the ArchiMate, UML, and BPMN Modeling Standards", D236 "Combining BPMN and the ArchiMate Standard for an Enhanced BPM Modeling Support" (webinar), D084 "Integrating Models to Improve Performance". | There are "How to Use the ArchiMate Language with UML" and "with BMM" guides, but a white paper titled "Using the ArchiMate Language with BPMN" was not found. The content of D182 and D236 (whether they contain an element mapping) was not verified. No machine-readable ArchiMate to BPMN mapping from The Open Group was found |

## 3. Details per effort

### 3.1 FBK BPMN 1.1 Ontology

- Authors: Marco Rospocher, Chiara Ghidini, Luciano Serafini, Fondazione Bruno Kessler (DKM unit).
- Paper: "An ontology for the Business Process Modelling Notation", FOIS 2014, Frontiers in AI and Applications vol. 267, pp. 133 to 146, IOS Press, DOI 10.3233/978-1-61499-438-1-133 (Crossref verified). Preprint read from the archived `dkm-static.fbk.eu/resources/ontologies/BPMN/BPMNontology.pdf`.
- Important correction: the FOIS 2014 paper describes the **BPMN 1.1** ontology (footnote 2 and section 7: "The current version ... covers version 1.1 of BPMN. We are currently updating it to ... BPMN 2.02"). It is not a BPMN 2.0 ontology.
- Metrics (paper, table): DL expressivity SHOIN(D), 117 classes, 463 class axioms, 123 object and 48 datatype properties, 104 individuals. Our parse of the archived file counts 94 named classes, 101 object and 70 datatype properties in the namespace, 321 restrictions, 65 equivalentClass axioms; the difference with the paper is not explained.
- Modelling: property names repeat the owner (`has_connecting_object_source_ref`, `has_sequence_flow_condition_type`); sequence flow, message flow and association are classes under `connecting_object`, linked to nodes with source and target object properties (reified flows). Attribute values are enumerated individuals. Links to DOLCE via separate "merging axioms" (technical report 2009).
- Licence: archived project page (2016 capture of http://dkm.fbk.eu/bpmn-ontology) says Creative Commons "Attribution Non-commercial Share Alike". The OWL files carry no licence triple.
- Availability: http://dkm.fbk.eu/bpmn-ontology was live until 2021 and is 404 or 500 since; https://dkm-static.fbk.eu/ does not respond. Wayback captures of both OWL files exist. An OntoHub entry is referenced (https://ontohub.org/fois-ontology-competition/BPMN_Ontology); the page answers 200 but did not render usable content.

### 3.2 FBK BPMN 2.0 Ontology v0.4

- Same group. The archived project page states it "has been automatically built (script by Chiara Di Francescomarino) starting from the XML schemas contained in the BPMN 2.0 specifications ... The ontology, which is a work-in-progress, will be manually refined and enriched." Version label v0.4. No later version was found.
- Namespace `http://dkm.fbk.eu/index.php/BPMN2_Ontology#`; no `owl:versionInfo`, no comments, no licence triple.
- Coverage: all of the semantic model plus DI (`BPMNDiagram`, `BPMNPlane`, `BPMNShape`, `BPMNEdge`, `BPMNLabel`, `Bounds`, `Point`, `Font`). Separate subclasses for event variants such as `startMessageEvent`, `endErrorEvent`, `intermediateTimerEvent`.
- Style: lowerCamel class names copied from XSD element names (`sequenceFlow`, `exclusiveGateway`); object properties prefixed `has_` (`has_sourceRef`, `has_targetRef`, `has_flowElement`). Flows are reified resources: `sequenceFlow` has exactly one `has_sourceRef` and one `has_targetRef` (qualified cardinality 1 on `flowNode`). All 466 restrictions are qualified cardinalities (min, max, exact); no disjointness at all, so OWL reasoning finds few inconsistencies.
- Still in use as a namespace: fair-workflows/fairworkflows (Apache-2.0, pushed 2025-08-06) binds `BPMN = http://dkm.fbk.eu/index.php/BPMN2_Ontology#` next to P-Plan, PROV and DUL; the LogMap matcher parameter files reference it too.
- Mirror: InES-Mannheim/spa-core (2016, no licence) ships `BPMN_2.0_ontology.owl` in the same namespace with two extra object properties and one extra datatype property (`has_incoming`, `has_outgoing`, `gatewayDirection`), so copies differ.

### 3.3 BBO, BPMN 2.0 Based Ontology

- Authors: Amina Annane, Nathalie Aussenac-Gilles, Mouna Kamel (IRIT, MELODI team, Toulouse). Paper: "BBO: BPMN 2.0 Based Ontology for Business Process Representation", 20th European Conference on Knowledge Management (ECKM 2019), pp. 49 to 59, DOI 10.34190/km.19.113 (Crossref verified).
- Repository: https://github.com/AminaANNANE/BBO_BPMNbasedOntology, GPL-3.0, created 2019-04-03, last commit 2019-06-26, 14 stars. Files: `BBO.owl`, `BPMNbasedOntologyV1_2.owl`, `SHACLshapes.ttl`, competency questions, a document listing natural-language BPMN constraints formalised in OWL, and `uo.owl`.
- Three namespaces exist for the same ontology, which hurts alignment:
  1. `http://BPMNbasedOntology#` in the GitHub `BBO.owl` (versionInfo 1.0).
  2. `https://www.irit.fr/recherches/MELODI/ontologies/BBO#`, served live at that URL (versionInfo 1.0.0). The RML rules in bdefante/Rules_BPMN2RDF use this one.
  3. `http://w3id.org/bbo#`: https://w3id.org/bbo/ redirects to the fork https://github.com/ProfTuan/BBO (Tuan Amith, GPL-3.0, versionInfo 1.5, last commit 2025-02-24). The README asks to cite the original authors.
- Scope: the README and ontology comment say the core is a fragment of BPMN 2.0, "mainly Chapter 10" (Process). It adds `Resource` with subclasses (`HumanResource`, `MaterialResource`, `SoftwareResource`, `DataResource`, `Tool`, `SparePart`, `ConsumableResource`), organisation (`Agent`, `Person`, `Role`, `Job`, `Group`), manufacturing locations (`Factory`, `ManufacturingFacility`, `Shop`, `Station`, `Cell`), documents (`WorkProcedureDocument`, `TechnicalDocument`, `UserManual`), parameters with units via the OBO Units Ontology import, and finer event and gateway taxonomies (`InterruptingBoundaryEvent`, `ConvergingGateway`, `ConditionalSequenceFlow`, `DefaultSequenceFlow`).
- Not covered (no such classes): Collaboration, Participant, Lane, LaneSet, MessageFlow, Choreography, Conversation, DataObject (replaced by `DataResource`), and all DI.
- Style: OWL 2 DL with real axioms: 148 restrictions, 59 `disjointWith`, complement classes, and property chains (for example `has_nextFlowNode` is defined as `has_outgoing o has_targetRef`, inverse `has_previousFlowNode`). Flows are reified (`SequenceFlow` with exactly one `has_sourceRef` and one `has_targetRef`). Property names use `has_` prefix and snake case mixed with camel case.
- Validation: `SHACLshapes.ttl` has 212 NodeShapes, all of the form `sh:targetSubjectOf p ; sh:class C` (SHACL rendering of rdfs:domain and rdfs:range), no cardinalities.
- Users: ProfTuan/BPMN-Knowledge-Graph-Rendering-Engine (GPL-3.0, 2024 to 2025, builds OWL KGs of clinical processes from spreadsheets), bdefante/Rules_BPMN2RDF (RML from BPMN XML to BBO, 2023), j0t4/bpmn-ontology-pipeline (2026).

### 3.4 sBPMN, SUPER project (2007)

- Paper: W. Abramowicz, A. Filipowska, M. Kaczmarek, T. Kaczmarek, "Semantically enhanced Business Process Modelling Notation", position paper, SBPM 2007 workshop at ESWC 2007, CEUR-WS Vol-251, paper 11 (https://ceur-ws.org/Vol-251/paper11.pdf, verified).
- Facts from the paper: based on the then latest BPMN specification (1.0), formalised in WSML (not OWL), "95 concepts and over 50 axioms", available at the SUPER project website (ip-super.org). The FOIS 2014 paper cites a later SUPER deliverable D1.5 "SUPER Process Ontology Stack, Evolved Version" (2009).
- Namespace, licence, files: not verified; no copy found. Relevant only historically. Note the name clash with sBPMN 2.0 (3.6), which is unrelated.

### 3.5 Natschläger 2011 and other early proposals

- C. Natschläger, "Towards a BPMN 2.0 Ontology", BPMN 2011 workshop, LNBIP vol. 95, pp. 1 to 15, Springer, DOI 10.1007/978-3-642-25160-3_1 (Crossref verified). The FOIS paper describes it as built "according to similar principles". Ontology file, namespace and licence: not verified (no copy found; probed SCCH URLs return 404 or no response).
- The FOIS paper also mentions proposals by Linus Chow (2011), Mohamed Keshk (2009) and Hui Liu (2011, taxonomy only); none were available then and none were found now.
- "OntoBPMN": the only trace found is a Wayback index entry for https://dkm.fbk.eu/images/2/23/OntoBPMN.owl, captured with status 404. Content not verified.

### 3.6 sBPMN 2.0 (Krause et al., 2025)

- Paper: F. Krause, H. Paulheim, A. Vázquez, A. Espert, "sBPMN: A Framework for Capturing Business Process Semantics in Dynamic Knowledge Graphs", K-CAP 2025, DOI 10.1145/3731443.3771361 (University of Mannheim).
- Site https://sbpmn.github.io/2.0/ (pyLODE style page, WebVOWL), files `ontology.ttl`, `.owl`, `.jsonld`, `.nt` and `shacl.ttl`; repository https://github.com/sBPMN/2.0, created 2025-10-01, last commit 2026-03-25, no LICENSE file; the ontology declares `dcterms:license` CC BY 4.0 and `dcterms:creator` "Franz Krause". No version IRI.
- Two namespaces: classes `https://sBPMN.github.io/2.0/classes#` (prefix `sbpmnc`), properties `https://sBPMN.github.io/2.0/properties#` (prefix `sbpmnp`), split because XSD elements and attributes share local names. Names are lowerCamel and identical to the XSD (`sequenceFlow`, `sourceRef`, `flowElement`).
- Coverage: semantic model including collaboration, choreography and conversation; adds derived subclasses for enumerated attribute values (`divergingDirectionGateway`, `parallelAdHocSubProcess`, `oneWayAssociation`). No DI classes.
- Style: light OWL (domain, range, 31 restrictions, 31 equivalentClass, no disjointness). Flows are reified (`sequenceFlow` with `sourceRef` and `targetRef`).
- Validation: `shacl.ttl` with 83 NodeShapes and 161 property shapes carrying XSD cardinalities, defaults (`sh:defaultValue`) and enumerations.
- Tooling: Docker stack with Camunda 7, Ontop (OBDA mapping of Camunda history tables to RDF) and Comunica federation; this is the only Camunda to RDF bridge found. Adopted by kchub212/bpmn-rdf-transformer (2026, BPMN XML to RDF with rdflib, Flask, Fuseki, bpmn-js; its decision record 0006 documents the choice).

### 3.7 Other GitHub projects (2018 or later)

| Repository | What | Target vocabulary | Licence | Last push |
|---|---|---|---|---|
| bdefante/Rules_BPMN2RDF | RML rules (XPath over BPMN XML) | BBO, IRIT namespace | none | 2023-09-11 |
| ProfTuan/BPMN-Knowledge-Graph-Rendering-Engine | Java, spreadsheet to OWL KG | BBO (w3id fork) | GPL-3.0 | 2025-04-03 |
| kchub212/bpmn-rdf-transformer | Python BPMN XML to RDF and back | sBPMN 2.0 | none | 2026-10-27 |
| hoedlale16/BPMN20OntologyTester | Tests a BPMN 2.0 ontology against the MIWG test suite; ships `BPMN20_v1.0.x.owl` | own (`reiter.at`) | Apache-2.0 | 2019-01-29 |
| SzabinaFodor/BPMN2OWL, HribernigNikolaus/BPMN2OWL, ololx/bpmn2owl-converter | BPMN to OWL converters (small) | own | GPL-3.0 / GPL-3.0 / Apache-2.0 | 2024 / 2018 / 2021 |
| zahraShahsavan/bpmn-ontology-owl2.0 | Toy OWL 2 ontology of core elements | own | none | 2025-02-27 |
| reiterma13/BPMN-to-S-BPM-Ontology, I2PM/BPMN2OWL | BPMN to S-BPM/PASS translation | PASS | none / GPL-3.0 | 2018 / 2023 |
| CaSkade-Automation/CaSkade-MES | MES that executes BPMN against a skill KG | not inspected | none | 2025-07-04 |

No project named "bpmn-to-rdf" or a YARRRML mapping for BPMN was found. No Signavio or Camunda knowledge graph export (other than the sBPMN 2.0 Ontop demo) was found.

## 4. Alignment feasibility

| Target | Mapping to the CMOF-based ontology | Notes |
|---|---|---|
| FBK BPMN 2.0 | `owl:equivalentClass` or `skos:exactMatch` is feasible class by class: same element set, local name equals the CMOF name with a lowercase first letter. Properties map via `has_X` to `X`. | DI classes map to the BPMN DI module. Licence is NC-SA: mapping triples that only cite FBK IRIs are fine; copying axioms or labels is not compatible with CC BY 4.0. Because there is no disjointness, equivalence will not cause inconsistencies. |
| FBK BPMN 1.1 | `skos:closeMatch` at most. | Different BPMN version; several elements renamed or restructured (gate, pool as class, event details). |
| sBPMN 2.0 | `owl:equivalentClass` for classes, `owl:equivalentProperty` for properties; near one to one, same names. | CC BY 4.0, compatible. Their value-based subclasses (`divergingDirectionGateway`) map to classes defined by restriction on the enumeration, or to `skos:narrowMatch`. Prefer `skos:exactMatch` in a separate alignment file so users do not have to import their TBox. |
| BBO | Mixed: core flow classes `owl:equivalentClass` (`Activity`, `Task`, `SequenceFlow`, `ExclusiveGateway`); `has_sourceRef` and `has_targetRef` `owl:equivalentProperty`. Resource and manufacturing classes have no counterpart: leave them to BBO. `DataResource` is not `DataObject`: use `skos:relatedMatch` or nothing. | Pick one BBO IRI. The w3id fork (`http://w3id.org/bbo#`) is the most stable resolver; the IRIT IRI is what RML users target. Equivalence with BBO imports its 59 disjointness axioms and complement classes, so test with a reasoner before publishing `owl:equivalentClass`. GPL-3.0 on an ontology is unusual; mappings by IRI do not copy BBO content. |
| IDPO and OMG XML namespace | Consider `rdfs:seeAlso` or an `owl:equivalentClass` bridge to `http://www.omg.org/spec/BPMN/20100524/MODEL#Task` etc. | Only if people already publish data with the OMG XML namespace used as RDF namespace; IDPO does. |
| PROV-O, P-Plan | Not equivalence. A process definition is a plan (`p-plan:Plan`), a task definition a step (`p-plan:Step`), a process instance or task instance a `prov:Activity`. | Keep definition level and execution level apart. |

## 5. What to reuse, what to do differently

Reuse:
- The generation approach. FBK 2.0, sBPMN 2.0, archimate2rdf and the new ontology all derive terms from OMG or Open Group machine-readable artefacts. Generating from the CMOF instead of the XSD is better: CMOF carries the abstract classes, property ownership, `isComposite` and multiplicities that the XSD only implies.
- Local names identical to the OMG metamodel, so that `skos:exactMatch` tables to FBK 2.0 and sBPMN 2.0 can be produced mechanically.
- SHACL for metamodel conformance (sBPMN 2.0 shows XSD cardinalities, defaults and enumerations as shapes) rather than OWL cardinality restrictions under the open world assumption, which FBK and BBO rely on and which rarely flag errors.
- BBO's ideas that go beyond syntax: derived convenience properties defined by property chain (`has_nextFlowNode = has_outgoing o has_targetRef`), disjointness between flow node kinds, and the explicit list of natural-language BPMN constraints formalised; these can become SHACL rules or SPARQL constraints in a separate rules module.
- PROV-O and P-Plan for the execution layer, as IDPO and fairworkflows do.

Do differently:
- One stable, resolvable namespace with a version IRI. BBO has three IRIs, FBK's are dead, sBPMN 2.0 uses a GitHub Pages IRI with mixed case and no version. `https://w3id.org/bpmn` is not registered yet (returns 404 today); register it before publishing.
- A permissive, explicit licence inside the ontology file (FBK files have none and the page says NC-SA; BBO is GPL-3.0). CC BY 4.0 as now declared fits reuse best.
- Full BPMN 2.0.2 coverage including Collaboration, Choreography, Conversation and DI as separate modules. BBO covers only Process; sBPMN 2.0 lacks DI; FBK 2.0 has DI but was never maintained.
- No `has_` prefixes and no owner-repeating property names (FBK 1.1); no mixing of snake and camel case (BBO).
- Keep flows reified as resources (every effort above does this, and it is needed because sequence flows carry conditions, names and DI edges), and offer the direct node to node shortcut as a derived property, not as the primary representation.
- Publish the alignments to FBK 2.0, sBPMN 2.0 and BBO as a separate mapping file with `skos:exactMatch`, `skos:closeMatch` and `skos:narrowMatch`, and only promote to `owl:equivalentClass` after a reasoner run, so importing the core never drags in foreign axioms.
- Mention that this is not an OMG publication and that no official RDF form of BPMN exists, as bp4mc2 did for ArchiMate.

## 6. Sources checked

- FBK project page (archived): https://web.archive.org/web/20160604051938/http://dkm.fbk.eu/bpmn-ontology
- FBK files (archived): `https://dkm-static.fbk.eu/resources/ontologies/BPMN/BPMN_2.0_ontology.owl`, `BPMN_1.1_ontology.owl`, `BPMNontology.pdf` via web.archive.org
- FBK 2.0 mirror: https://github.com/InES-Mannheim/spa-core/blob/master/core/src/main/resources/ontologies/BPMN_2.0_ontology.owl
- FOIS 2014: https://doi.org/10.3233/978-1-61499-438-1-133
- BBO: https://github.com/AminaANNANE/BBO_BPMNbasedOntology ; https://www.irit.fr/recherches/MELODI/ontologies/BBO ; https://w3id.org/bbo/ ; https://github.com/ProfTuan/BBO ; https://doi.org/10.34190/km.19.113
- sBPMN 2007: https://ceur-ws.org/Vol-251/paper11.pdf
- Natschläger 2011: https://doi.org/10.1007/978-3-642-25160-3_1
- sBPMN 2.0: https://sbpmn.github.io/2.0/ ; https://github.com/sBPMN/2.0
- FH Joanneum: https://github.com/hoedlale16/BPMN20OntologyTester
- IDPO: https://w3id.org/idpo ; https://github.com/RUB-Informatik-im-Bauwesen/idpo
- fairworkflows: https://github.com/fair-workflows/fairworkflows/blob/main/fairworkflows/namespaces.py
- RML rules: https://github.com/bdefante/Rules_BPMN2RDF
- OMG: https://www.omg.org/spec/BPMN/2.0.2/
- PROV-O: https://www.w3.org/ns/prov-o ; P-Plan: http://purl.org/net/p-plan
- ArchiMate: https://github.com/AlbertoDMendoza/archimate_ontology ; https://github.com/bp4mc2/archimate2rdf ; https://github.com/jwvveen/archimate-rdf
- The Open Group catalogue: https://publications.opengroup.org/catalogsearch/result/?q=ArchiMate+BPMN
