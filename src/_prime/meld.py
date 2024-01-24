class MeldStrategy(str):
    pass


class IneligibleMeldStrategyException(Exception):
    pass


def get_meld_weight(
    src_weight: float,
    src_meld_strategy: MeldStrategy,
    other_weight: float,
    other_meld_strategy: MeldStrategy,
) -> float:
    output_float = 0
    if src_meld_strategy == "default" and other_meld_strategy == "override":
        output_float = other_weight
    elif src_meld_strategy != "default" or other_meld_strategy == "ignore":
        output_float = src_weight + other_weight
    else:
        output_float = src_weight
    return output_float


def get_meld_strategys() -> dict[MeldStrategy:None]:
    """
    match: melder and meldee will have equal weight or error thrown
    sum: melder and meldee sum weights
    ignore: melder ignores weight from meldee
    override: meldee overwrites melder weight (only works on meldee=default)
    default: meldee ignores meldee unless meldee is override
    """
    return {"default", "match", "sum", "accept", "override"}


def get_meld_default() -> MeldStrategy:
    return "default"


def validate_meld_strategy(meld_strategy: MeldStrategy) -> MeldStrategy:
    if meld_strategy not in get_meld_strategys():
        raise IneligibleMeldStrategyException(
            f"'{meld_strategy}' is ineligible meld_strategy."
        )
    return meld_strategy
