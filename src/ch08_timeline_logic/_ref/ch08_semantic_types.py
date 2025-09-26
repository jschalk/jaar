from src.ch02_rope_logic._ref.ch02_semantic_types import LabelTerm, RopeTerm


class TimeLineLabel(LabelTerm):
    "TimeLineLabel is required for every TimeLineUnit. It is a LabelTerm that must not contain the knot."

    pass


class TimeLinePoint(int):
    pass
