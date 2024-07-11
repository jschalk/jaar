from src._instrument.python import get_1_if_None
from dataclasses import dataclass


class PennyNum(float):
    """Smallest Unit of Money"""

    pass


class MoneyUnit(float):
    """MoneyUnit inherits from float class"""

    pass


class PixelNum(float):
    """Smallest Unit of credor_weight or debtor_weight"""

    pass


class CoinNum(float):
    """Smallest Unit of budget"""

    pass


class BudgetNum(float):
    """BudgetNum inherits from float class"""

    pass


def default_coin_if_none(coin: CoinNum = None) -> CoinNum:
    return get_1_if_None(coin)


def trim_coin_excess(num: float, coin: CoinNum) -> float:
    return coin * int(num / coin)


def default_budget() -> BudgetNum:
    return BudgetNum(default_money_magnitude())


def validate_budget(x_budget: int = None) -> int:
    if x_budget is None:
        return default_budget()
    return max(get_1_if_None(x_budget), default_coin_if_none())


def default_pixel_if_none(pixel: PixelNum = None) -> PixelNum:
    return get_1_if_None(pixel)


def trim_pixel_excess(num: float, pixel: PixelNum) -> float:
    return pixel * int(num / pixel)


def default_penny_if_none(penny: PennyNum = None) -> PennyNum:
    return max(get_1_if_None(penny), 1)


def trim_penny_excess(num: MoneyUnit, penny: PennyNum) -> MoneyUnit:
    return penny * int(num / penny)


def default_money_magnitude() -> MoneyUnit:
    return 1000000000


def default_money_magnitude_if_none(money_magnitude: int = None) -> int:
    if money_magnitude is None:
        return default_money_magnitude()
    return money_magnitude


@dataclass
class FiscalUnit:
    _budget: BudgetNum = None
    _coin: CoinNum = None
    _pixel: PixelNum = None
    _penny: PennyNum = None


def allot_scale(ledger: dict[str, float], scale_number: float, grain_unit: float):
    """
    allots the scale_number across credorledgers with credor_weighted attributes with a resolution of the grain unit.

    :param credorledgers: Dictionary of credorledgers with 'credor_weight' attribute.
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

    # Calculate the total credor_weight
    total_credor_weight = sum(ledger.values())

    # Calculate the distribution
    x_dict = {}
    for key, obj in ledger.items():
        # Determine the allot based on credor_weight
        allot = (obj / total_credor_weight) * scale_number

        # Adjust to the nearest grain unit
        alloted_value = round(allot / grain_unit) * grain_unit
        x_dict[key] = alloted_value

    return x_dict
