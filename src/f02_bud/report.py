from src.f01_road.road import RoadUnit
from src.f02_bud.bud import BudUnit
from pandas import DataFrame


def get_bud_acctunits_dataframe(x_bud: BudUnit) -> DataFrame:
    if x_bud.accts == {}:
        return DataFrame(
            columns=[
                "acct_name",
                "credit_belief",
                "debtit_belief",
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
                "owner_name",
                "fund_ratio",
                "item_title",
                "_parent_road",
                "begin",
                "close",
                "addin",
                "denom",
                "numor",
                "morph",
            ]
        )
    x_item_list = []
    for x_item in agenda_dict.values():
        item_dict = {
            "owner_name": x_bud.owner_name,
            "fund_ratio": x_item._fund_ratio,
            "item_title": x_item.item_title,
            "_parent_road": x_item._parent_road,
            "begin": x_item.begin,
            "close": x_item.close,
            "addin": x_item.addin,
            "denom": x_item.denom,
            "numor": x_item.numor,
            "morph": x_item.morph,
        }
        x_item_list.append(item_dict)
    return DataFrame(x_item_list)
