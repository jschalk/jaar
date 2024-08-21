from src._road.road import RoadUnit
from src.bud.bud import BudUnit
from pandas import DataFrame


def get_bud_acctunits_dataframe(x_bud: BudUnit) -> DataFrame:
    if x_bud._accts == {}:
        return DataFrame(
            columns=[
                "acct_id",
                "credit_score",
                "debtit_score",
                "_fund_give",
                "_fund_take",
                "_fund_agenda_give",
                "_fund_agenda_take",
                "_fund_agenda_ratio_give",
                "_fund_agenda_ratio_take",
            ]
        )
    x_acctunits_list = list(x_bud.get_acctunits_dict(all_attrs=True).values())
    return DataFrame(x_acctunits_list)


def get_bud_agenda_dataframe(x_bud: BudUnit, base: RoadUnit = None) -> DataFrame:
    agenda_dict = x_bud.get_agenda_dict(necessary_base=base)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_id",
                "fund_ratio",
                "_label",
                "_parent_road",
                "_begin",
                "_close",
                "_addin",
                "_denom",
                "_numor",
                "_morph",
            ]
        )
    x_idea_list = []
    for x_idea in agenda_dict.values():
        idea_dict = {
            "owner_id": x_bud._owner_id,
            "fund_ratio": x_idea._fund_ratio,
            "_label": x_idea._label,
            "_parent_road": x_idea._parent_road,
            "_begin": x_idea._begin,
            "_close": x_idea._close,
            "_addin": x_idea._addin,
            "_denom": x_idea._denom,
            "_numor": x_idea._numor,
            "_morph": x_idea._morph,
        }
        x_idea_list.append(idea_dict)
    return DataFrame(x_idea_list)
