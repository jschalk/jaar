from pandas import DataFrame
from src.a01_term_logic.rope import RopeTerm
from src.a06_belief_logic.belief_main import BeliefUnit


def get_belief_voiceunits_dataframe(x_belief: BeliefUnit) -> DataFrame:
    if x_belief.voices == {}:
        return DataFrame(
            columns=[
                "voice_name",
                "voice_cred_points",
                "voice_debt_points",
                "fund_give",
                "fund_take",
                "fund_agenda_give",
                "fund_agenda_take",
                "fund_agenda_ratio_give",
                "fund_agenda_ratio_take",
            ]
        )
    x_voiceunits_list = list(x_belief.get_voiceunits_dict(all_attrs=True).values())
    return DataFrame(x_voiceunits_list)


def get_belief_agenda_dataframe(
    x_belief: BeliefUnit, reason_context: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_belief.get_agenda_dict(necessary_reason_context=reason_context)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "belief_name",
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
            "belief_name": x_belief.belief_name,
            "fund_ratio": x_plan.fund_ratio,
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
