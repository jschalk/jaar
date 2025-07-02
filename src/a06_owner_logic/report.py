from pandas import DataFrame
from src.a01_term_logic.rope import RopeTerm
from src.a06_owner_logic.owner import OwnerUnit


def get_owner_acctunits_dataframe(x_owner: OwnerUnit) -> DataFrame:
    if x_owner.accts == {}:
        return DataFrame(
            columns=[
                "acct_name",
                "acct_cred_points",
                "acct_debt_points",
                "_fund_give",
                "_fund_take",
                "_fund_agenda_give",
                "_fund_agenda_take",
                "_fund_agenda_ratio_give",
                "_fund_agenda_ratio_take",
            ]
        )
    x_acctunits_list = list(x_owner.get_acctunits_dict(all_attrs=True).values())
    return DataFrame(x_acctunits_list)


def get_owner_agenda_dataframe(
    x_owner: OwnerUnit, rcontext: RopeTerm = None
) -> DataFrame:
    agenda_dict = x_owner.get_agenda_dict(necessary_rcontext=rcontext)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_name",
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
            "owner_name": x_owner.owner_name,
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
