from src.agenda.road import (
    RoadUnit,
    is_sub_road,
    RoadNode,
    create_road,
    get_diff_road,
    default_road_delimiter_if_none,
    get_terminus_node_from_road,
    get_parent_road_from_road,
)
from src.agenda.belief import BeliefUnit, create_beliefunit
from src.agenda.group import GroupBrand
from src.agenda.idea import idea_kid_shop, IdeaUnit, ideaattrfilter_shop
from src.agenda.y_func import get_empty_dict_if_none
from src.economy.economy import EconomyID
from src.world.pain import PainGenus
from src.world.person import PersonID
from dataclasses import dataclass


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class DealUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _beliefunits: dict[RoadUnit:BeliefUnit] = None


def dealunit_shop(_author: PersonID, _reader: PersonID):
    return DealUnit(
        _author=_author, _reader=_reader, _beliefunits=get_empty_dict_if_none(None)
    )


# def create_dealunit(
#     src_requestee_pid: PersonID, # also dst_requestee_pid
#     dst_requestee_pid: PersonID, # also src_requester_pid
#     src_wantunit: WantUnit,
#     dst_wantunit: WantUnit = None,
#     src_requestee_group: GroupBrand = None,
#     src_fix_weight: int = None, # also same as dst_fix_weight
#     dst_requestee_group: GroupBrand = None,
# ):
#     src_requestunit = create_requestunit(
#         wantunit=src_wantunit,
#         requestee_pid=src_requestee_pid,
#         requestee_group=src_requestee_group,
#         requester_pid=src_requester_pid,
#         fix_weight=src_fix_weight,
#     )
#     dst_requestunit = create_requestunit(
#         wantunit=dst_wantunit,
#         requestee_pid=dst_requestee_pid,
#         requestee_group=dst_requestee_group,
#         requester_pid=dst_requester_pid,
#         fix_weight=dst_fix_weight,
#     )
#     x_dealunit

#     return
