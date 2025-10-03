from src.ch01_data_toolbox.dict_toolbox import get_0_if_None, get_1_if_None
from src.ch03_finance_logic._ref.ch03_semantic_types import (
    FundGrain,
    FundNum,
    MoneyUnit,
    PennyNum,
    RespectGrain,
    RespectNum,
)


class get_net_Exception(Exception):
    pass


def get_net(x_give: float, x_take: float) -> float:
    x_give = get_0_if_None(x_give)
    x_take = get_0_if_None(x_take)
    if x_give < 0 or x_take < 0:
        if x_give < 0 and x_take >= 0:
            parameters_str = f"get_net x_give={x_give}."
        elif x_give >= 0:
            parameters_str = f"get_net x_take={x_take}."
        else:
            parameters_str = f"get_net x_give={x_give} and x_take={x_take}."
        exception_str = f"{parameters_str} Only non-negative numbers allowed."
        raise get_net_Exception(exception_str)
    return x_give - x_take


def default_fund_grain_if_None(fund_grain: FundGrain = None) -> FundGrain:
    return get_1_if_None(fund_grain)


def get_whole_grainunit_ratio(num: float, grainunit: float) -> float:
    return grainunit * int(num / grainunit)


def default_fund_pool() -> FundNum:
    return FundNum(1000000000.0)


def validate_fund_pool(x_fund_pool: FundNum = None) -> FundNum:
    x_fund_pool = default_fund_pool() if x_fund_pool is None else x_fund_pool
    return max(get_1_if_None(x_fund_pool), default_fund_grain_if_None())


def valid_finance_ratio(big_number: float, small_number: float) -> bool:
    """Checks that big_number is wholly divisible by small_number"""
    return (big_number % small_number) == 0


def default_RespectGrain_if_None(respect_grain: RespectGrain = None) -> RespectGrain:
    return max(get_1_if_None(respect_grain), 1)


def default_respect_num() -> RespectNum:
    return RespectNum(default_fund_pool())


def validate_respect_num(x_respect_num: RespectNum = None) -> RespectNum:
    x_respect_num = default_respect_num() if x_respect_num is None else x_respect_num
    return max(x_respect_num, default_RespectGrain_if_None(x_respect_num))


def filter_penny(penny: PennyNum = None) -> PennyNum:
    """Penny must be greater than 1"""
    return max(get_1_if_None(penny), 1)
