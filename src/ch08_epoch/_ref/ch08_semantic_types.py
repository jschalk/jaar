from src.ch07_belief_logic._ref.ch07_semantic_types import LabelTerm, RopeTerm


class EpochLabel(LabelTerm):
    "EpochLabel is required for every EpochUnit. It is a LabelTerm that must not contain the knot."

    pass


class EpochPoint(int):
    pass
