from src._road.road import RoadUnit
from src._world.world import WorldUnit
from pandas import DataFrame


def get_world_charunits_dataframe(x_world: WorldUnit) -> DataFrame:
    if x_world._chars == {}:
        return DataFrame(
            columns=[
                "char_id",
                "credor_weight",
                "debtor_weight",
                "_world_cred",
                "_world_debt",
                "_world_agenda_cred",
                "_world_agenda_debt",
                "_world_agenda_ratio_cred",
                "_world_agenda_ratio_debt",
            ]
        )
    x_charunits_list = list(x_world.get_charunits_dict(all_attrs=True).values())
    return DataFrame(x_charunits_list)


def get_world_agenda_dataframe(x_world: WorldUnit, base: RoadUnit = None) -> DataFrame:
    agenda_dict = x_world.get_agenda_dict(necessary_base=base)
    if agenda_dict == {}:
        return DataFrame(
            columns=[
                "owner_id",
                "bud_ratio",
                "_label",
                "_parent_road",
                "_begin",
                "_close",
                "_addin",
                "_denom",
                "_numor",
                "_reest",
            ]
        )
    x_idea_list = []
    for x_idea in agenda_dict.values():
        idea_dict = {
            "owner_id": x_world._owner_id,
            "bud_ratio": x_idea._bud_ratio,
            "_label": x_idea._label,
            "_parent_road": x_idea._parent_road,
            "_begin": x_idea._begin,
            "_close": x_idea._close,
            "_addin": x_idea._addin,
            "_denom": x_idea._denom,
            "_numor": x_idea._numor,
            "_reest": x_idea._reest,
        }
        x_idea_list.append(idea_dict)
    return DataFrame(x_idea_list)
