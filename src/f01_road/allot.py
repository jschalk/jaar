from src.f00_instrument.dict_toolbox import get_0_if_None


class missing_base_residual_Exception(Exception):
    pass


class get_net_Exception(Exception):
    pass


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
            difference_scale = missing_scale_list[x_count]
            changes_ledger_list.append([x_key, x_float + difference_scale])
            missing_scale -= difference_scale
            if missing_scale == 0:
                break
            x_count += 1

    for x_ledger_change in changes_ledger_list:
        ledger[x_ledger_change[0]] = x_ledger_change[1]

    allot_sum = sum(ledger.values())
    if ledger != {} and allot_sum != scale_number:
        raise ValueError(
            f"Summation of allots '{allot_sum}' is not equal to scale '{scale_number}'."
        )
    return ledger


def _calc_allot_value(obj, total_credit_belief, scale_number, grain_unit):
    if total_credit_belief == 0:
        return 0
    # calculate the allot based on credit_belief
    allot_amt = (obj / total_credit_belief) * scale_number
    # Adjust to the nearest grain unit
    return round(allot_amt / grain_unit) * grain_unit


def _create_allot_dict(
    ledger: dict[str, float], scale_number: float, grain_unit: float
) -> dict[str, float]:
    # Calculate the total credit_belief
    total_credit_belief = sum(ledger.values())
    return {
        x_key: _calc_allot_value(x_obj, total_credit_belief, scale_number, grain_unit)
        for x_key, x_obj in ledger.items()
    }


def allot_scale(
    ledger: dict[str, float], scale_number: float, grain_unit: float
) -> dict[str, int]:
    """
    allots the scale_number among ledger with float values with a resolution of the grain unit.

    :param ledger: Dictionary of str key with a relative strength attribute.
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
