# BPMN 2.0.2 sources

Retrieved 2 November 2026. Companion file: `bpmn-connection-rules.json`.

## Specification

- Business Process Model and Notation (BPMN), Version 2.0.2, OMG document formal/13-12-09 (title page: formal/2013-12-09), December 2013.
- PDF: https://www.omg.org/spec/BPMN/2.0.2/PDF (532 pages, 7.3 MB). Spec page: https://www.omg.org/spec/BPMN/2.0.2/
- Page numbers below and in the JSON are the numbers printed in the page footer. PDF page = printed page + 30.

Section numbering: in 2.0.2 the connection rules are clause **7.6** (7.6.1 Sequence Flow, 7.6.2 Message Flow). In BPMN 2.0 (formal/11-01-03) the same content is clause 7.5 (7.5.1, 7.5.2). Table numbers (7.3, 7.4) are the same in both.

## Where each fact came from

| Fact | Section | Printed page |
|---|---|---|
| Table 7.3 Sequence Flow Connection Rules, intro text and note under the table | 7.6.1 | 40 to 41 |
| Table 7.4 Message Flow Connection Rules, intro text and note under the table | 7.6.2 | 41 to 42 |
| Sequence Flow may not cross a Pool boundary; expanded Sub-Process contents not connectable to outside | 7.6.1 | 40 |
| Message Flows cannot connect objects in the same Pool | 7.6.2; 9.4 | 41; 119 |
| Process flow contained within the Pool | 7.2.1; 10.2.1.1 | 21; 147 to 148 |
| Artifacts are never source or target of Sequence Flow or Message Flow | 8.4.1 | 65 |
| Allowed Sequence Flow source/target element kinds; conditional flow rules; source Gateway not Parallel or Event (for conditional flow) | 8.4.13 | 95 |
| Activity Sequence Flow and Message Flow connections | 10.3 | 151 to 152 |
| Event Sub-Process has no incoming or outgoing Sequence Flows | 10.3.5 | 174 |
| Start Event: no incoming Sequence Flow (boundary exception for expanded Sub-Process), must be a source; may be Message Flow target, never Message Flow source | 10.5.2 | 244 to 245 |
| End Event: must be a target, no outgoing Sequence Flow (boundary exception); no incoming Message Flow, may send Message Flow | 10.5.3 | 248 |
| Intermediate Event: boundary events are never Sequence Flow targets; Compensation boundary event has no outgoing Sequence Flow; Cancel and Error not in normal flow; Link event rules; Message Intermediate Event has one in or one out Message Flow, not both | 10.5.4 | 258 to 259 |
| Gateway Sequence Flow rules (merge or split, gatewayDirection) | 10.6.1 | 288 to 289 |
| Event-Based Gateway: two or more outgoing flows, no conditions, targets are Intermediate Events or Receive Tasks (not mixed with Message Intermediate Events), valid triggers, no extra incoming flows on targets | 10.6.6 | 296 to 297 |

Every sentence in the JSON `constraints` array is quoted verbatim from the PDF text layer (whitespace normalised, bullet glyphs removed).

## Matrix result

- Table 7.3 (rows = source, columns = target, order as in the spec): Start Event, Task, collapsed Sub-Process, Gateway, Intermediate Event, End Event. 36 cells, 25 allowed. Nothing may target a Start Event; an End Event is never a source; every other combination is allowed, including Start Event to End Event.
- Table 7.4: Message Start Event, Pool, Task, collapsed Sub-Process, Message Intermediate Event, Message End Event. 36 cells, 25 allowed. A Message Start Event is never a source; a Message End Event is never a target; every other combination is allowed, always only across different Pools.
- Neither table has numbered footnotes. The "footnotes" in the JSON are the explanatory paragraphs printed directly before and after each table.

## Ambiguities and how they were handled

1. **Glyph defect (10 cells).** In every non-empty row of Table 7.3 the cell in the Task column is printed as a per mille sign (U+2030, ArialMT) instead of the Wingdings arrow used in the other cells. In Table 7.4 the cell in the Message Start Event column is printed as a circumflex (U+02C6, ArialMT). This is a font rendering defect: the same characters appear in the BPMN 2.0 PDF (formal/11-01-03) and in the 2.0.2 changebar PDF. These cells are recorded as `"allowed": true` with a note, because (a) the matching cells in BPMN 1.2 (https://www.omg.org/spec/BPMN/1.2/PDF, formal/09-01-03, Tables 8.4 and 8.5, pages 30 to 31) show the normal symbol, and (b) the normative text says "An Activity MAY be a target for Sequence Flows" (p. 151) and "A Start Event MAY be the target for a Message Flow" (p. 245). If you want strictly literal reading, treat these 10 cells as unconfirmed.
2. **Event subtypes are not in the tables.** The tables use generic shapes. The Intermediate Event column of Table 7.3 is valid only for events in normal flow; boundary events are never targets (p. 258). Link, Compensation and Event-Based Gateway restrictions come from the text, not the table.
3. **Message Intermediate Event row vs column.** In Table 7.4 the column header shows the catching form (open envelope), the row header the throwing form (filled envelope). The table does not say this explicitly; the text (p. 259) says a Message Intermediate Event has one incoming or one outgoing Message Flow, but not both.
4. **Pool to Pool and object to own Pool.** Table 7.4 marks Pool, Task, Sub-Process and Intermediate Event as mutually connectable, but only between different Pools. Whether an object may send a Message Flow to the boundary of its own Pool is excluded by "MUST NOT connect two objects within the same Pool" (p. 119); the JSON notes this on every allowed cell.
5. **Choreography.** Table 7.3 also applies to Choreography diagrams (Activity shapes then mean Choreography Activities). Choreography specific rules in clause 11 were not extracted.
6. **Not covered by either table:** Association, Data Association, Conversation Link, Lane, Data Object, Group, Text Annotation. Gateways are not valid Message Flow ends.
7. **Semantic.cmof.** The title page lists http://www.omg.org/spec/BPMN/20100502/Semantic.cmof as a machine consumable file, but https://www.omg.org/spec/BPMN/20100502/Semantic.cmof returned HTTP 404 on 2 November 2026. BPMN20.cmof (20100501) contains the full semantic metamodel.

## Machine-readable metamodel

All URLs below returned HTTP 200 on 2 November 2026 (listed on the 2.0.2 title page and on the spec page).

| File | URL | Notes |
|---|---|---|
| BPMN20.cmof | https://www.omg.org/spec/BPMN/20100501/BPMN20.cmof | CMOF/XMI 2.1, package uri `http://www.omg.org/spec/BPMN/20100524/MODEL-XMI` |
| Infrastructure.cmof | https://www.omg.org/spec/BPMN/20100502/Infrastructure.cmof | |
| BPMNDI.cmof | https://www.omg.org/spec/BPMN/20100501/BPMNDI.cmof | |
| DC.cmof | https://www.omg.org/spec/BPMN/20100501/DC.cmof | |
| DI.cmof | https://www.omg.org/spec/BPMN/20100501/DI.cmof | |
| BPMN20.xsd | https://www.omg.org/spec/BPMN/20100501/BPMN20.xsd | root schema; includes Semantic.xsd, imports BPMNDI.xsd |
| Semantic.xsd | https://www.omg.org/spec/BPMN/20100501/Semantic.xsd | |
| BPMNDI.xsd | https://www.omg.org/spec/BPMN/20100501/BPMNDI.xsd | imports DC.xsd, DI.xsd |
| DC.xsd | https://www.omg.org/spec/BPMN/20100501/DC.xsd | |
| DI.xsd | https://www.omg.org/spec/BPMN/20100501/DI.xsd | |
| BPMN20-FromXMI.xslt | https://www.omg.org/spec/BPMN/20100501/BPMN20-FromXMI.xslt | XMI to XSD-format transform |

Examples archive (not metamodel): https://www.omg.org/cgi-bin/doc?dtc/10-06-03.zip

XML namespaces (from the XSD `targetNamespace` attributes):

- Model: `http://www.omg.org/spec/BPMN/20100524/MODEL` (BPMN20.xsd, Semantic.xsd)
- BPMN DI: `http://www.omg.org/spec/BPMN/20100524/DI`
- DC: `http://www.omg.org/spec/DD/20100524/DC`
- DI: `http://www.omg.org/spec/DD/20100524/DI`

Note: the files live under the path `20100501` but declare `20100524` namespaces.

## Copyright and licensing

The PDF carries copyright notices of OMG (2013) and the submitting companies (2010: Axway, BizAgi, Bruce Silver Associates, IDS Scheer, IBM, MEGA, Model Driven Solutions, Oracle, PNA Group, SAP, Software AG, TIBCO, Unisys). The licence grants a royalty free right to use the specification to create and distribute software based on it. Copies of the document itself may only be made with the copyright and permission notice attached, for informational purposes, unmodified, and not posted on a network or resold. Practical consequence: implementing these rules in software is fine; the JSON quotes short normative sentences with attribution, and the full PDF should not be redistributed. The machine readable files carry no separate licence text; treat them as part of the same OMG specification.
