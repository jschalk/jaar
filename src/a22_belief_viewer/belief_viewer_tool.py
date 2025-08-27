import dataclasses
from src.a00_data_toolbox.dict_toolbox import make_dict_safe_for_json
from src.a03_group_logic.group import AwardHeir, AwardLine, AwardUnit
from src.a03_group_logic.labor import PartyHeir, PartyUnit
from src.a04_reason_logic.reason import (
    CaseUnit,
    FactHeir,
    FactUnit,
    ReasonHeir,
    ReasonUnit,
)
from src.a05_plan_logic.plan import PlanUnit
from src.a06_belief_logic.belief_main import BeliefUnit
from src.a07_timeline_logic.reason_str_func import (
    get_fact_state_readable_str,
    get_reason_case_readable_str,
)
from typing import Any


def add_small_dot(x_str: str) -> str:
    return f"&nbsp;&nbsp;<small>� {x_str}</small>"


def readable_percent(value: float) -> str:
    # if value is None:
    #     return 0
    pct = value * 100
    if abs(pct) >= 1:  # show as integer percent
        return f"{pct:.0f}%"
    elif abs(pct) >= 0.01:  # show with 2 decimal places
        return f"{pct:.2f}%"
    else:  # very small -> show in scientific-like format
        return f"{pct:.5f}%".rstrip("0").rstrip(".")


def belief_objs_asdict(
    obj: Any, current_belief: BeliefUnit = None, current_reason: ReasonUnit = None
) -> dict:
    # sourcery skip: extract-duplicate-method
    """
    Convert a dataclass-like object to dict,
    including extra keys defined in a custom attribute.
    """
    if dataclasses.is_dataclass(obj):
        if isinstance(obj, BeliefUnit):
            current_belief = obj
        elif isinstance(obj, (ReasonUnit, ReasonHeir)):
            current_reason = obj
        result = {}
        for field in dataclasses.fields(obj):
            value = getattr(obj, field.name)
            result[field.name] = belief_objs_asdict(
                value, current_belief, current_reason
            )
        if isinstance(obj, PlanUnit):
            set_readable_plan_values(obj, result)
        elif isinstance(obj, AwardUnit):
            obj_readable_str = (
                f"{obj.awardee_title}: Take {obj.take_force}, Give {obj.give_force}"
            )
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, AwardHeir):
            obj_readable_str = f"{obj.awardee_title}: Take {obj.take_force} ({obj._fund_take}), Give {obj.give_force} ({obj._fund_give})"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, AwardLine):
            obj_readable_str = f"{obj.awardee_title}: take_fund ({obj._fund_take}), give_fund ({obj._fund_give})"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, (FactUnit, FactHeir)):
            obj_readable_str = get_fact_state_readable_str(obj, None, current_belief)
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, PartyUnit):
            solo_str = " Solo: True" if obj.solo else ""
            obj_readable_str = f"LaborUnit: {obj.party_title}{solo_str}"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, PartyHeir):
            solo_str = " Solo: True" if obj.solo else ""
            obj_readable_str = f"LaborHeir: {obj.party_title}{solo_str}"
            result["readable"] = add_small_dot(obj_readable_str)
        elif isinstance(obj, ReasonUnit):
            reason_case_readable_str = f"ReasonUnit: context is {obj.reason_context}"
            result["readable"] = add_small_dot(reason_case_readable_str)
        elif isinstance(obj, ReasonHeir):
            reason_case_readable_str = f"ReasonHeir: context is {obj.reason_context}"
            result["readable"] = add_small_dot(reason_case_readable_str)
        elif isinstance(obj, CaseUnit):
            reason_case_readable_str = get_reason_case_readable_str(
                reason_context=current_reason.reason_context,
                caseunit=obj,
                timeline_label=None,
                beliefunit=current_belief,
            )
            result["readable"] = f"  {add_small_dot(reason_case_readable_str)}"

        return result
    elif isinstance(obj, (list, tuple)):
        b = current_belief
        r = current_reason
        return [belief_objs_asdict(v, b, r) for v in obj]
    elif isinstance(obj, dict):
        b = current_belief
        r = current_reason
        return {k: belief_objs_asdict(v, b, r) for k, v in obj.items()}
    else:
        return obj


def set_readable_plan_values(x_plan: PlanUnit, result: dict):
    result["parent_rope"] = (
        add_small_dot(x_plan.parent_rope)
        if result.get("parent_rope") != ""
        else add_small_dot("Root Plan parent_rope is empty str")
    )
    result["fund_share"] = x_plan.get_fund_share()
    _all_partner_cred_str = f"all_partner_cred = {x_plan._all_partner_cred}"
    _all_partner_debt_str = f"all_partner_debt = {x_plan._all_partner_debt}"
    _all_partner_cred_str = add_small_dot(_all_partner_cred_str)
    _all_partner_debt_str = add_small_dot(_all_partner_debt_str)
    result["_all_partner_cred"] = _all_partner_cred_str
    result["_all_partner_debt"] = _all_partner_debt_str
    result["_fund_ratio"] = readable_percent(result.get("_fund_ratio"))
    result_gogo_want = result.get("gogo_want")
    result_stop_want = result.get("stop_want")
    result_gogo_calc = result.get("_gogo_calc")
    result_stop_calc = result.get("_stop_calc")
    result["gogo_want"] = add_small_dot(f"gogo_want: {result_gogo_want}")
    result["stop_want"] = add_small_dot(f"stop_want: {result_stop_want}")
    result["_gogo_calc"] = add_small_dot(f"gogo_calc: {result_gogo_calc}")
    result["_stop_calc"] = add_small_dot(f"stop_calc: {result_stop_calc}")
    result_addin = result.get("addin")
    result_begin = result.get("begin")
    result_close = result.get("close")
    result_denom = result.get("denom")
    result_morph = result.get("morph")
    result_numor = result.get("numor")
    result["addin"] = add_small_dot(f"addin: {result_addin}")
    result["begin"] = add_small_dot(f"begin: {result_begin}")
    result["close"] = add_small_dot(f"close: {result_close}")
    result["denom"] = add_small_dot(f"denom: {result_denom}")
    result["morph"] = add_small_dot(f"morph: {result_morph}")
    result["numor"] = add_small_dot(f"numor: {result_numor}")
    result["_active_hx"] = add_small_dot(f"active_hx: {x_plan._active_hx}")


def get_plan_view_dict(x_plan: PlanUnit) -> dict[str,]:
    """Returns a dictionary of only base value types and dictionarys"""

    # return make_dict_safe_for_json(dataclasses_asdict(x_plan))
    return make_dict_safe_for_json(belief_objs_asdict(x_plan))


def get_partners_view_dict(belief: BeliefUnit) -> dict[str,]:
    partners_dict = {}
    for partner in belief.partners.values():

        partner_cred_points_readable = (
            f"partner_cred_points: {partner.partner_cred_points}"
        )
        partner_debt_points_readable = (
            f"partner_debt_points: {partner.partner_debt_points}"
        )
        _memberships_readable = f"_memberships: {partner._memberships}"
        _credor_pool_readable = f"_credor_pool: {partner._credor_pool}"
        _debtor_pool_readable = f"_debtor_pool: {partner._debtor_pool}"
        _irrational_partner_debt_points_readable = f"_irrational_partner_debt_points: {partner._irrational_partner_debt_points}"
        _inallocable_partner_debt_points_readable = f"_inallocable_partner_debt_points: {partner._inallocable_partner_debt_points}"
        _fund_give_readable = f"_fund_give: {partner._fund_give}"
        _fund_take_readable = f"_fund_take: {partner._fund_take}"
        _fund_agenda_give_readable = f"_fund_agenda_give: {partner._fund_agenda_give}"
        _fund_agenda_take_readable = f"_fund_agenda_take: {partner._fund_agenda_take}"
        _fund_agenda_ratio_give_readable = (
            f"_fund_agenda_ratio_give: {partner._fund_agenda_ratio_give}"
        )
        _fund_agenda_ratio_take_readable = (
            f"_fund_agenda_ratio_take: {partner._fund_agenda_ratio_take}"
        )
        x_members_dict = {
            x_membership.group_title: {
                "partner_name": x_membership.partner_name,
                "group_title": x_membership.group_title,
                "group_cred_points": x_membership.group_cred_points,
                "group_debt_points": x_membership.group_debt_points,
                "_credor_pool": x_membership._credor_pool,
                "_debtor_pool": x_membership._debtor_pool,
                "_fund_agenda_give": x_membership._fund_agenda_give,
                "_fund_agenda_ratio_give": x_membership._fund_agenda_ratio_give,
                "_fund_agenda_ratio_take": x_membership._fund_agenda_ratio_take,
                "_fund_agenda_take": x_membership._fund_agenda_take,
                "_fund_give": x_membership._fund_give,
                "_fund_take": x_membership._fund_take,
                "group_title_readable": add_small_dot(
                    f"group_title: {x_membership.group_title}"
                ),
                "group_cred_points_readable": add_small_dot(
                    f"group_cred_points: {x_membership.group_cred_points}"
                ),
                "group_debt_points_readable": add_small_dot(
                    f"group_debt_points: {x_membership.group_debt_points}"
                ),
                "_credor_pool_readable": add_small_dot(
                    f"_credor_pool: {x_membership._credor_pool}"
                ),
                "_debtor_pool_readable": add_small_dot(
                    f"_debtor_pool: {x_membership._debtor_pool}"
                ),
                "_fund_agenda_give_readable": add_small_dot(
                    f"_fund_agenda_give: {x_membership._fund_agenda_give}"
                ),
                "_fund_agenda_ratio_give_readable": add_small_dot(
                    f"_fund_agenda_ratio_give: {x_membership._fund_agenda_ratio_give}"
                ),
                "_fund_agenda_ratio_take_readable": add_small_dot(
                    f"_fund_agenda_ratio_take: {x_membership._fund_agenda_ratio_take}"
                ),
                "_fund_agenda_take_readable": add_small_dot(
                    f"_fund_agenda_take: {x_membership._fund_agenda_take}"
                ),
                "_fund_give_readable": add_small_dot(
                    f"_fund_give: {x_membership._fund_give}"
                ),
                "_fund_take_readable": add_small_dot(
                    f"_fund_take: {x_membership._fund_take}"
                ),
            }
            for x_membership in partner._memberships.values()
        }
        partner_dict = {
            "partner_name": partner.partner_name,
            "partner_cred_points": partner.partner_cred_points,
            "partner_debt_points": partner.partner_debt_points,
            "_memberships": x_members_dict,
            "_credor_pool": partner._credor_pool,
            "_debtor_pool": partner._debtor_pool,
            "_irrational_partner_debt_points": partner._irrational_partner_debt_points,
            "_inallocable_partner_debt_points": partner._inallocable_partner_debt_points,
            "_fund_give": partner._fund_give,
            "_fund_take": partner._fund_take,
            "_fund_agenda_give": partner._fund_agenda_give,
            "_fund_agenda_take": partner._fund_agenda_take,
            "_fund_agenda_ratio_give": partner._fund_agenda_ratio_give,
            "_fund_agenda_ratio_take": partner._fund_agenda_ratio_take,
            "partner_cred_points_readable": partner_cred_points_readable,
            "partner_debt_points_readable": partner_debt_points_readable,
            "_memberships_readable": _memberships_readable,
            "_credor_pool_readable": _credor_pool_readable,
            "_debtor_pool_readable": _debtor_pool_readable,
            "_irrational_partner_debt_points_readable": _irrational_partner_debt_points_readable,
            "_inallocable_partner_debt_points_readable": _inallocable_partner_debt_points_readable,
            "_fund_give_readable": _fund_give_readable,
            "_fund_take_readable": _fund_take_readable,
            "_fund_agenda_give_readable": _fund_agenda_give_readable,
            "_fund_agenda_take_readable": _fund_agenda_take_readable,
            "_fund_agenda_ratio_give_readable": _fund_agenda_ratio_give_readable,
            "_fund_agenda_ratio_take_readable": _fund_agenda_ratio_take_readable,
        }
        partners_dict[partner.partner_name] = partner_dict

    return partners_dict


def get_groups_view_dict(belief: BeliefUnit) -> dict[str,]:
    groups_dict = {}
    # for group in belief._groupunits.values():

    #     group_title_readable_key = f"group_title_readable"
    #     group_cred_points_readable_key = f"group_cred_points_readable"
    #     group_debt_points_readable_key = f"group_debt_points_readable"
    #     _credor_pool_readable_key = f"_credor_pool_readable"
    #     _debtor_pool_readable_key = f"_debtor_pool_readable"
    #     _fund_agenda_give_readable_key = f"_fund_agenda_give_readable"
    #     _fund_agenda_ratio_give_readable_key = f"_fund_agenda_ratio_give_readable"
    #     _fund_agenda_ratio_take_readable_key = f"_fund_agenda_ratio_take_readable"
    #     _fund_agenda_take_readable_key = f"_fund_agenda_take_readable"
    #     _fund_give_readable_key = f"_fund_give_readable"
    #     _fund_take_readable_key = f"_fund_take_readable"

    #     group_group_title_readable = f"group_title_readable: {group.group_title}"
    #     group__memberships_readable = f"_memberships_readable: {group._memberships}"
    #     group__fund_give_readable = f"_fund_give_readable: {group._fund_give}"
    #     group__fund_take_readable = f"_fund_take_readable: {group._fund_take}"
    #     group__fund_agenda_give_readable = (
    #         f"_fund_agenda_give_readable: {group._fund_agenda_give}"
    #     )
    #     group__fund_agenda_take_readable = (
    #         f"_fund_agenda_take_readable: {group._fund_agenda_take}"
    #     )
    #     group__credor_pool_readable = f"_credor_pool_readable: {group._credor_pool}"
    #     group__debtor_pool_readable = f"_debtor_pool_readable: {group._debtor_pool}"

    #     x_members_dict = {
    #         # x_membership.partner_name: {
    #         #     "partner_name": x_membership.partner_name,
    #         #     "group_title": x_membership.group_title,
    #         #     "group_cred_points": x_membership.group_cred_points,
    #         #     "group_debt_points": x_membership.group_debt_points,
    #         #     "_credor_pool": x_membership._credor_pool,
    #         #     "_debtor_pool": x_membership._debtor_pool,
    #         #     "_fund_agenda_give": x_membership._fund_agenda_give,
    #         #     "_fund_agenda_ratio_give": x_membership._fund_agenda_ratio_give,
    #         #     "_fund_agenda_ratio_take": x_membership._fund_agenda_ratio_take,
    #         #     "_fund_agenda_take": x_membership._fund_agenda_take,
    #         #     "_fund_give": x_membership._fund_give,
    #         #     "_fund_take": x_membership._fund_take,
    #         #     "partner_name_readable": add_small_dot(
    #         #         f"partner name: {x_membership.partner_name}"
    #         #     ),
    #         #     "group_cred_points_readable": add_small_dot(
    #         #         f"group_cred_points: {x_membership.group_cred_points}"
    #         #     ),
    #         #     "group_debt_points_readable": add_small_dot(
    #         #         f"group_debt_points: {x_membership.group_debt_points}"
    #         #     ),
    #         #     "_credor_pool_readable": add_small_dot(
    #         #         f"_credor_pool: {x_membership._credor_pool}"
    #         #     ),
    #         #     "_debtor_pool_readable": add_small_dot(
    #         #         f"_debtor_pool: {x_membership._debtor_pool}"
    #         #     ),
    #         #     "_fund_agenda_give_readable": add_small_dot(
    #         #         f"_fund_agenda_give: {x_membership._fund_agenda_give}"
    #         #     ),
    #         #     "_fund_agenda_ratio_give_readable": add_small_dot(
    #         #         f"_fund_agenda_ratio_give: {x_membership._fund_agenda_ratio_give}"
    #         #     ),
    #         #     "_fund_agenda_ratio_take_readable": add_small_dot(
    #         #         f"_fund_agenda_ratio_take: {x_membership._fund_agenda_ratio_take}"
    #         #     ),
    #         #     "_fund_agenda_take_readable": add_small_dot(
    #         #         f"_fund_agenda_take: {x_membership._fund_agenda_take}"
    #         #     ),
    #         #     "_fund_give_readable": add_small_dot(
    #         #         f"_fund_give: {x_membership._fund_give}"
    #         #     ),
    #         #     "_fund_take_readable": add_small_dot(
    #         #         f"_fund_take: {x_membership._fund_take}"
    #         #     ),
    #         # }
    #         # for x_membership in group._memberships.values()
    #     }
    #     group_dict = {
    #         "group_title": group.group_title,
    #         "partner_name": 1,
    #         "group_title": 1,
    #         "group_cred_points": 1,
    #         "group_debt_points": 1,
    #         "_credor_pool": 1,
    #         "_debtor_pool": 1,
    #         "_fund_agenda_give": 1,
    #         "_fund_agenda_ratio_give": 1,
    #         "_fund_agenda_ratio_take": 1,
    #         "_fund_agenda_take": 1,
    #         "_fund_give": 1,
    #         "_fund_take": 1,
    #         group_title_readable_key: 1,
    #         group_cred_points_readable_key: 1,
    #         group_debt_points_readable_key: 1,
    #         _credor_pool_readable_key: 1,
    #         _debtor_pool_readable_key: 1,
    #         _fund_agenda_give_readable_key: 1,
    #         _fund_agenda_ratio_give_readable_key: 1,
    #         _fund_agenda_ratio_take_readable_key: 1,
    #         _fund_agenda_take_readable_key: 1,
    #         _fund_give_readable_key: 1,
    #         _fund_take_readable_key: 1,
    #         # "_memberships": x_members_dict,
    #     }
    #     groups_dict[group.group_title] = group_dict

    return groups_dict


def get_belief_view_dict(belief: BeliefUnit) -> dict[str,]:
    return {
        "planroot": get_plan_view_dict(belief.planroot),
        "partners": get_partners_view_dict(belief),
    }
