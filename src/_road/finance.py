class PennyUnit(float):
    """Smallest Unit of Money"""

    pass


class PixelUnit(float):
    """Smallest Unit of credor_weight or debtor_weight"""

    pass


class ThinkUnit(float):
    """Smallest Unit of mind"""

    pass


def default_pixel_if_none(pixel: float = None) -> float:
    return pixel if pixel != None else 1


def trim_pixel_excess(num: float, pixel: float) -> float:
    return pixel * int(num / pixel)


def default_penny_if_none(penny: float = None) -> float:
    x_penny = penny if penny != None else 1
    return max(x_penny, 1)


def trim_penny_excess(num: float, pixel: float) -> float:
    return pixel * int(num / pixel)


def default_thinkunit_if_none(thinkunit: ThinkUnit = None) -> ThinkUnit:
    return thinkunit if thinkunit != None else 1


def trim_thinkunit_excess(num: float, thinkunit: ThinkUnit) -> float:
    return thinkunit * int(num / thinkunit)


def default_money_magnitude() -> float:
    return 1000000000


def default_money_magnitude_if_none(money_magnitude: int = None) -> int:
    if money_magnitude is None:
        money_magnitude = default_money_magnitude()
    return money_magnitude


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
