"""Which shape checks which normative statement of BPMN 2.0.2 (numbering of
sources/bpmn-connection-rules.json, constraints[]). A value that
starts with "bpmnsh:" is checked; any other value says why it is not."""

M = "A permission (MAY): encoded as permitted cells in bpmn-matrix.ttl; there is nothing to violate."
DI = "Depends on where a shape sits in the diagram (diagram interchange), which stays in the XML."
SCOPE = "Scope statement: says where the rules apply, constrains nothing."

DEKKING: dict[int, str] = {
    1: DI, 2: SCOPE, 3: "bpmnsh:SequenceFlowContainerShape", 4: SCOPE,
    5: "bpmnsh:MessageFlowSamePoolShape", 6: "bpmnsh:SequenceFlowContainerShape",
    7: "bpmnsh:MatrixNoCellShape", 8: "bpmnsh:MatrixNoCellShape", 9: "bpmnsh:MatrixNoCellShape",
    10: "bpmnsh:MatrixNoCellShape", 11: "bpmnsh:FlowEndsShape, bpmnsh:MatrixNoCellShape",
    12: "bpmnsh:ConditionalFromActivityShape", 13: "bpmnsh:ConditionFromGatewayShape",
    14: "bpmnsh:MessageFlowSamePoolShape", 15: M, 16: M, 17: "bpmnsh:MessageFlowSamePoolShape",
    18: M, 19: M, 20: "bpmnsh:EventSubProcessShape", 21: "bpmnsh:MatrixForbiddenShape", 22: DI,
    23: "bpmnsh:StartEventSourceShape", 24: "bpmnsh:StartEventConditionShape", 25: M,
    26: "bpmnsh:MatrixNoCellShape", 27: "bpmnsh:EndEventTargetShape", 28: "bpmnsh:MatrixForbiddenShape",
    29: DI, 30: "bpmnsh:MatrixNoCellShape", 31: M, 32: "bpmnsh:MatrixNoCellShape",
    33: "bpmnsh:BoundaryEventIncomingShape", 34: "bpmnsh:BoundaryEventSourceShape",
    35: "bpmnsh:CompensationOutgoingShape", 36: M, 37: "bpmnsh:IntermediateInFlowShape",
    38: "bpmnsh:IntermediateInFlowShape", 39: "bpmnsh:IntermediateInFlowShape",
    40: "bpmnsh:LinkBothWaysShape", 41: "bpmnsh:LinkBothWaysShape", 42: "bpmnsh:LinkPairShape", 43: M,
    44: "bpmnsh:LinkSingleTargetShape", 45: M, 46: M, 47: "bpmnsh:MessageEventOneWayShape", 48: M, 49: M,
    50: "bpmnsh:GatewaySplitsOrMergesShape", 51: "bpmnsh:GatewayDirectionShape",
    52: "bpmnsh:GatewayDirectionShape", 53: "bpmnsh:EventGatewayShape", 54: "bpmnsh:ConditionFromGatewayShape",
    55: "bpmnsh:EventGatewayTargetShape", 56: "bpmnsh:EventGatewayMixShape",
    57: "bpmnsh:EventGatewayReceiveTaskShape", 58: "bpmnsh:EventGatewayTargetShape",
    59: "bpmnsh:EventGatewayTargetShape",
}
