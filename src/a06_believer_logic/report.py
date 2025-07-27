from pandas import DataFrame
from src.a01_term_logic.rope import RopeTerm
from src.a06_believer_logic.believer_main import BelieverUnit


def get_believer_partnerunits_dataframe(x_believer: BelieverUnit) -> DataFrame:
    if x_believer.partners == {}:
        return DataFrame(
            columns=[
                "partner_name",
                "partner_cred_points",
                "partner_debt_points",
                "_fund_give",
                "_fund_take",
                "_fund_agenda_give",
                "_fund_agenda_take",
                "_fund_agenda_ratio_give",
                "_fund_agenda_ratio_take",
            ]
        )
    x_partnerunits_list = list(
        x_believer.get_partnerunits_dict(all_attrs=True).values()
    )
    return DataFrame(x_partnerunits_list)


def get_believer_agenda_dataframe(
    x_believer: BelieverUnit, r_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_believer.get_agenda_dict(necessary_r_context=r_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "believer_name",
                "fund_ratio",
                "plan_label",
                "parent_rope",
                "begin",
                "close",
                "addin",
                "denom",
                "numor",
                "morph",
            ]
        )
    x_plan_list = []
    for x_plan in agenda_dict.values():
        plan_dict = {
            "believer_name": x_believer.believer_name,
            "fund_ratio": x_plan._fund_ratio,
            "plan_label": x_plan.plan_label,
            "parent_rope": x_plan.parent_rope,
            "begin": x_plan.begin,
            "close": x_plan.close,
            "addin": x_plan.addin,
            "denom": x_plan.denom,
            "numor": x_plan.numor,
            "morph": x_plan.morph,
        }
        x_plan_list.append(plan_dict)
    return DataFrame(x_plan_list)
