from src._instrument.python import get_1_if_None


class MoneyUnit(float):
    """MoneyUnit inherits from float class"""

    pass


class PennyNum(float):
    """Smallest Unit of Money"""

    pass


class RespectNum(float):
    """RespectNum inherits from float class"""

    pass


class BitNum(float):
    """Smallest Unit of credit_score or debtit_score (RespectNum) ala 'the slightest bit of respect!'"""

    pass


class FundNum(float):
    """FundNum inherits from float class"""

    pass


class FundCoin(float):
    """Smallest Unit of fund_num"""

    pass


class missing_base_residual_Exception(Exception):
    pass


def default_fund_coin_if_none(fund_coin: FundCoin = None) -> FundCoin:
    return get_1_if_None(fund_coin)


def trim_fund_coin_excess(num: float, fund_coin: FundCoin) -> float:
    return fund_coin * int(num / fund_coin)


def default_fund_pool() -> FundNum:
    return FundNum(default_money_magnitude())


def validate_fund_pool(x_fund_pool: FundNum = None) -> FundNum:
    x_fund_pool = default_fund_pool() if x_fund_pool is None else x_fund_pool
    return max(get_1_if_None(x_fund_pool), default_fund_coin_if_none())


def valid_finance_ratio(big_number: float, small_number: float) -> bool:
    """Checks that big_number is wholly divisible by small_number"""
    return (big_number % small_number) == 0


# def validate_fund_pool(x_fund_pool: FundNum = None, x_fund_coin: FundCoin = None) -> int:
#     x_fund_coin = default_fund_coin_if_none() if x_fund_coin is None else x_fund_coin
#     x_fund_pool = default_fund_pool() if x_fund_pool is None else x_fund_pool
#     return max(get_1_if_None(x_fund_pool), default_fund_coin_if_none())


def default_bit_if_none(bit: BitNum = None) -> BitNum:
    return max(get_1_if_None(bit), 1)


def trim_bit_excess(num: float, bit: BitNum) -> float:
    return bit * int(num / bit)


def default_respect_num() -> RespectNum:
    return RespectNum(default_fund_pool())


def validate_respect_num(x_respect_num: RespectNum = None) -> RespectNum:
    x_respect_num = default_respect_num() if x_respect_num is None else x_respect_num
    return max(x_respect_num, default_bit_if_none(x_respect_num))


def default_penny_if_none(penny: PennyNum = None) -> PennyNum:
    return max(get_1_if_None(penny), 1)


def trim_penny_excess(num: MoneyUnit, penny: PennyNum) -> MoneyUnit:
    return penny * int(num / penny)


def default_money_magnitude() -> MoneyUnit:
    return 1000000000


def default_money_magnitude_if_none(money_magnitude: int = None) -> int:
    return default_money_magnitude() if money_magnitude is None else money_magnitude


def _get_missing_scale_list(
    missing_scale: float, grain_unit: float, list_length: int
) -> list[float]:
    if list_length == 0 or missing_scale == 0:
        return []
    missing_avg = missing_scale / list_length
    missing_base_multipler = int(missing_avg / grain_unit)
    missing_base_scale_unit = missing_base_multipler * grain_unit
    missing_scale_list = [missing_base_scale_unit for _ in range(list_length)]
    missing_base_residual = missing_scale - sum(missing_scale_list)

    x_count = 0
    if missing_base_residual > 0:
        while missing_base_residual > 0:
            missing_scale_list[x_count] += grain_unit
            missing_base_residual -= grain_unit
            x_count += 1

            if missing_base_residual < 0:
                raise missing_base_residual_Exception(
                    f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={missing_scale} grain_unit={grain_unit}."
                )
    else:
        while missing_base_residual < 0:
            missing_scale_list[x_count] -= grain_unit
            missing_base_residual += grain_unit
            x_count += 1

            if missing_base_residual > 0:
                raise missing_base_residual_Exception(
                    f"missing_base_residual calculation failed probably due to missing_scale not being a multiple of grain_unit. missing_scale={missing_scale} grain_unit={grain_unit}."
                )

    return missing_scale_list


def _allot_missing_scale(
    ledger: dict[str, float],
    scale_number: float,
    grain_unit: float,
    missing_scale: float,
) -> dict[str, float]:
    missing_scale_list = _get_missing_scale_list(missing_scale, grain_unit, len(ledger))
    changes_ledger_list = []
    if missing_scale != 0:
        x_count = 0
        for x_key, x_float in sorted(ledger.items(), key=lambda kv: (-kv[1], kv[0])):
            delta_scale = missing_scale_list[x_count]
            changes_ledger_list.append([x_key, x_float + delta_scale])
            missing_scale -= delta_scale
            if missing_scale == 0:
                break
            x_count += 1

    for x_ledger_change in changes_ledger_list:
        ledger[x_ledger_change[0]] = x_ledger_change[1]

    allot_sum = sum(ledger.values())
    if ledger != {} and allot_sum != scale_number:
        raise ValueError(
            f"Summation of output allots '{allot_sum}' is not equal to scale '{scale_number}'."
        )
    return ledger


def _calc_allot_value(obj, total_credit_score, scale_number, grain_unit):
    if total_credit_score == 0:
        return 0
    # Determine the allot based on credit_score
    allot_amt = (obj / total_credit_score) * scale_number
    # Adjust to the nearest grain unit
    return round(allot_amt / grain_unit) * grain_unit


def _create_allot_dict(
    ledger: dict[str, float], scale_number: float, grain_unit: float
) -> dict[str, float]:
    # Calculate the total credit_score
    total_credit_score = sum(ledger.values())
    return {
        x_key: _calc_allot_value(x_obj, total_credit_score, scale_number, grain_unit)
        for x_key, x_obj in ledger.items()
    }


def allot_scale(ledger: dict[str, float], scale_number: float, grain_unit: float):
    """
    allots the scale_number among credorledgers with credit_scoreed attributes with a resolution of the grain unit.

    :param credorledgers: Dictionary of credorledgers with 'credit_score' attribute.
    :param scale_number: The total number to allot.
    :param grain_unit: The smallest unit of distribution.
    :raises ValueError: If the scale number is not a multiple of the grain unit.
    :return: Dictionary with alloted values.
    """
    # Check if the scale number is a multiple of the grain unit
    if scale_number % grain_unit != 0:
        raise ValueError(
            f"The scale number '{scale_number}' must be a multiple of the grain unit '{grain_unit}'."
        )
    if not ledger:
        return {}
    # any ledger key with value zero will be not be alloted any scale_number
    zero_values = {x_key for x_key, x_value in ledger.items() if x_value == 0}
    for x_key in zero_values:
        ledger.pop(x_key)
    allot_dict = _create_allot_dict(ledger, scale_number, grain_unit)
    x_missing = scale_number - sum(allot_dict.values())
    allot_dict = _allot_missing_scale(allot_dict, scale_number, grain_unit, x_missing)
    # add back in ledger keys that by definition were to have    value zero
    for x_key in zero_values:
        allot_dict[x_key] = 0
    return allot_dict
