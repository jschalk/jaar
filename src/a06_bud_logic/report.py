from pandas import DataFrame
from src.a01_term_logic.way import WayTerm
from src.a06_bud_logic.bud import BudUnit


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


def get_bud_agenda_dataframe(x_bud: BudUnit, rcontext: WayTerm = None) -> DataFrame:
    agenda_dict = x_bud.get_agenda_dict(necessary_rcontext=rcontext)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_name",
                "fund_ratio",
                "concept_label",
                "parent_way",
                "begin",
                "close",
                "addin",
                "denom",
                "numor",
                "morph",
            ]
        )
    x_concept_list = []
    for x_concept in agenda_dict.values():
        concept_dict = {
            "owner_name": x_bud.owner_name,
            "fund_ratio": x_concept._fund_ratio,
            "concept_label": x_concept.concept_label,
            "parent_way": x_concept.parent_way,
            "begin": x_concept.begin,
            "close": x_concept.close,
            "addin": x_concept.addin,
            "denom": x_concept.denom,
            "numor": x_concept.numor,
            "morph": x_concept.morph,
        }
        x_concept_list.append(concept_dict)
    return DataFrame(x_concept_list)
