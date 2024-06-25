from src._road.road import OtherID, default_road_delimiter_if_none, validate_roadnode
from src._road.finance import default_pixel_if_none
from dataclasses import dataclass
from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None


class InvalidOtherException(Exception):
    pass


class _pixel_RatioException(Exception):
    pass


@dataclass
class OtherCore:
    other_id: OtherID = None
    _road_delimiter: str = None
    _pixel: float = None

    def set_other_id(self, x_other_id: OtherID):
        self.other_id = validate_roadnode(x_other_id, self._road_delimiter)


@dataclass
class OtherUnit(OtherCore):
    """This represents the relationship from the WorldUnit._owner_id to the OtherUnit.other_id
    OtherUnit.credor_weight represents how much credor_weight the _owner_id gives the other_id
    OtherUnit.debtor_weight represents how much debtor_weight the _owner_id gives the other_id
    """

    credor_weight: int = None
    debtor_weight: int = None
    # calculated fields
    _irrational_debtor_weight: int = None  # set by listening process
    _inallocable_debtor_weight: int = None  # set by listening process
    # set by World.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None
    _world_agenda_ratio_cred: float = None
    _world_agenda_ratio_debt: float = None
    _credor_operational: bool = None
    _debtor_operational: bool = None
    # set by River process
    _treasury_due_paid: float = None
    _treasury_due_diff: float = None
    _output_world_meld_order: int = None
    _treasury_cred_score: float = None
    _treasury_voice_rank: int = None
    _treasury_voice_hx_lowest_rank: int = None

    def set_pixel(self, x_pixel: float):
        self._pixel = x_pixel

    def clear_output_world_meld_order(self):
        self._output_world_meld_order = None

    def set_output_world_meld_order(self, _output_world_meld_order: int):
        self._output_world_meld_order = _output_world_meld_order

    def set_credor_debtor_weight(
        self,
        credor_weight: float = None,
        debtor_weight: float = None,
    ):
        if credor_weight != None:
            self.set_credor_weight(credor_weight)
        if debtor_weight != None:
            self.set_debtor_weight(debtor_weight)

    def clear_treasurying_data(self):
        self._treasury_due_paid = None
        self._treasury_due_diff = None
        self._treasury_cred_score = None
        self._treasury_voice_rank = None

    def set_treasury_attr(
        self,
        _treasury_due_paid: float,
        _treasury_due_diff: float,
        cred_score: float,
        voice_rank: int,
    ):
        self._treasury_due_paid = _treasury_due_paid
        self._treasury_due_diff = _treasury_due_diff
        self._treasury_cred_score = cred_score
        self.set_treasury_voice_rank(voice_rank)

    def set_treasury_voice_rank(self, voice_rank: int):
        self._treasury_voice_rank = voice_rank
        self._set_treasury_voice_hx_lowest_rank()

    def _set_treasury_voice_hx_lowest_rank(
        self, treasury_voice_hx_lowest_rank: float = None
    ):
        if (
            treasury_voice_hx_lowest_rank != None
            and self._treasury_voice_hx_lowest_rank != None
        ):
            self._treasury_voice_hx_lowest_rank = treasury_voice_hx_lowest_rank

        if self._treasury_voice_hx_lowest_rank is None or (
            self._treasury_voice_hx_lowest_rank > self._treasury_voice_rank
        ):
            self._treasury_voice_hx_lowest_rank = self._treasury_voice_rank

    def get_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {
            "other_id": self.other_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
            "_credor_operational": self._credor_operational,
            "_debtor_operational": self._debtor_operational,
            "_treasury_due_paid": self._treasury_due_paid,
            "_treasury_due_diff": self._treasury_due_diff,
            "_treasury_cred_score": self._treasury_cred_score,
            "_treasury_voice_rank": self._treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": self._treasury_voice_hx_lowest_rank,
        }
        if self._irrational_debtor_weight not in [None, 0]:
            x_dict["_irrational_debtor_weight"] = self._irrational_debtor_weight
        if self._inallocable_debtor_weight not in [None, 0]:
            x_dict["_inallocable_debtor_weight"] = self._inallocable_debtor_weight

        if all_attrs:
            self._all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def _all_attrs_necessary_in_dict(self, x_dict):
        x_dict["_world_cred"] = self._world_cred
        x_dict["_world_debt"] = self._world_debt
        x_dict["_world_agenda_cred"] = self._world_agenda_cred
        x_dict["_world_agenda_debt"] = self._world_agenda_debt
        x_dict["_world_agenda_ratio_cred"] = self._world_agenda_ratio_cred
        x_dict["_world_agenda_ratio_debt"] = self._world_agenda_ratio_debt
        x_dict["_output_world_meld_order"] = self._output_world_meld_order

    def set_credor_weight(self, credor_weight: int):
        if (credor_weight / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"'{credor_weight}' is not divisible by pixel '{self._pixel}'"
            )
        self.credor_weight = credor_weight

    def set_debtor_weight(self, debtor_weight: int):
        if (debtor_weight / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"'{debtor_weight}' is not divisible by pixel '{self._pixel}'"
            )
        self.debtor_weight = debtor_weight

    def get_credor_weight(self):
        return get_1_if_None(self.credor_weight)

    def get_debtor_weight(self):
        return get_1_if_None(self.debtor_weight)

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        self._world_agenda_ratio_cred = 0
        self._world_agenda_ratio_debt = 0

    def add_irrational_debtor_weight(self, x_irrational_debtor_weight: float):
        self._irrational_debtor_weight += x_irrational_debtor_weight

    def add_inallocable_debtor_weight(self, x_inallocable_debtor_weight: float):
        self._inallocable_debtor_weight += x_inallocable_debtor_weight

    def reset_listen_calculated_attrs(self):
        self._irrational_debtor_weight = 0
        self._inallocable_debtor_weight = 0

    def add_world_cred_debt(
        self,
        world_cred: float,
        world_debt,
        world_agenda_cred: float,
        world_agenda_debt,
    ):
        self._world_cred += world_cred
        self._world_debt += world_debt
        self._world_agenda_cred += world_agenda_cred
        self._world_agenda_debt += world_agenda_debt

    def set_world_agenda_ratio_cred_debt(
        self,
        world_agenda_ratio_cred_sum: float,
        world_agenda_ratio_debt_sum: float,
        world_otherunit_total_credor_weight: float,
        world_otherunit_total_debtor_weight: float,
    ):
        if world_agenda_ratio_cred_sum == 0:
            self._world_agenda_ratio_cred = (
                self.get_credor_weight() / world_otherunit_total_credor_weight
            )
        else:
            self._world_agenda_ratio_cred = (
                self._world_agenda_cred / world_agenda_ratio_cred_sum
            )

        if world_agenda_ratio_debt_sum == 0:
            self._world_agenda_ratio_debt = (
                self.get_debtor_weight() / world_otherunit_total_debtor_weight
            )
        else:
            self._world_agenda_ratio_debt = (
                self._world_agenda_debt / world_agenda_ratio_debt_sum
            )

    def meld(self, exterior_otherunit):
        if self.other_id != exterior_otherunit.other_id:
            raise InvalidOtherException(
                f"Meld fail OtherUnit='{self.other_id}' not the equal as OtherUnit='{exterior_otherunit.other_id}"
            )

        self.credor_weight += exterior_otherunit.credor_weight
        self.debtor_weight += exterior_otherunit.debtor_weight
        self._irrational_debtor_weight += exterior_otherunit._irrational_debtor_weight
        self._inallocable_debtor_weight += exterior_otherunit._inallocable_debtor_weight


# class OtherUnitsshop:
def otherunits_get_from_json(otherunits_json: str) -> dict[str:OtherUnit]:
    otherunits_dict = get_dict_from_json(json_x=otherunits_json)
    return otherunits_get_from_dict(x_dict=otherunits_dict)


def otherunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str:OtherUnit]:
    otherunits = {}
    for otherunit_dict in x_dict.values():
        x_otherunit = otherunit_get_from_dict(otherunit_dict, _road_delimiter)
        otherunits[x_otherunit.other_id] = x_otherunit
    return otherunits


def otherunit_get_from_dict(otherunit_dict: dict, _road_delimiter: str) -> OtherUnit:
    _irrational_debtor_weight = otherunit_dict.get("_irrational_debtor_weight", 0)
    _inallocable_debtor_weight = otherunit_dict.get("_inallocable_debtor_weight", 0)
    _treasury_due_paid = otherunit_dict.get("_treasury_due_paid", 0)
    _treasury_due_diff = otherunit_dict.get("_treasury_due_diff", 0)
    _treasury_cred_score = otherunit_dict.get("_treasury_cred_score", 0)
    _treasury_voice_rank = otherunit_dict.get("_treasury_voice_rank", 0)
    _treasury_voice_hx_lowest_rank = otherunit_dict.get(
        "_treasury_voice_hx_lowest_rank", 0
    )

    x_otherunit = otherunit_shop(
        other_id=otherunit_dict["other_id"],
        credor_weight=otherunit_dict["credor_weight"],
        debtor_weight=otherunit_dict["debtor_weight"],
        _credor_operational=otherunit_dict["_credor_operational"],
        _debtor_operational=otherunit_dict["_debtor_operational"],
        _road_delimiter=_road_delimiter,
    )
    x_otherunit.set_treasury_attr(
        _treasury_due_paid=_treasury_due_paid,
        _treasury_due_diff=_treasury_due_diff,
        cred_score=_treasury_cred_score,
        voice_rank=_treasury_voice_rank,
    )
    x_otherunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
    x_otherunit.add_irrational_debtor_weight(get_0_if_None(_irrational_debtor_weight))
    x_otherunit.add_inallocable_debtor_weight(get_0_if_None(_inallocable_debtor_weight))

    return x_otherunit


def otherunit_shop(
    other_id: OtherID,
    credor_weight: int = None,
    debtor_weight: int = None,
    _credor_operational: bool = None,
    _debtor_operational: bool = None,
    _road_delimiter: str = None,
    _pixel: float = None,
) -> OtherUnit:
    x_otherunit = OtherUnit(
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _irrational_debtor_weight=get_0_if_None(),
        _inallocable_debtor_weight=get_0_if_None(),
        _credor_operational=_credor_operational,
        _debtor_operational=_debtor_operational,
        _world_cred=get_0_if_None(),
        _world_debt=get_0_if_None(),
        _world_agenda_cred=get_0_if_None(),
        _world_agenda_debt=get_0_if_None(),
        _world_agenda_ratio_cred=get_0_if_None(),
        _world_agenda_ratio_debt=get_0_if_None(),
        _treasury_due_paid=None,
        _treasury_due_diff=None,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _pixel=default_pixel_if_none(_pixel),
    )
    x_otherunit.set_other_id(x_other_id=other_id)
    return x_otherunit


@dataclass
class OtherLink(OtherCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None

    def get_dict(self) -> dict[str:str]:
        return {
            "other_id": self.other_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_world_cred_debt(
        self,
        otherlinks_credor_weight_sum: float,
        otherlinks_debtor_weight_sum: float,
        belief_world_cred: float,
        belief_world_debt: float,
        belief_world_agenda_cred: float,
        belief_world_agenda_debt: float,
    ):
        belief_world_cred = get_1_if_None(belief_world_cred)
        belief_world_debt = get_1_if_None(belief_world_debt)
        credor_ratio = self.credor_weight / otherlinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / otherlinks_debtor_weight_sum

        self._world_cred = belief_world_cred * credor_ratio
        self._world_debt = belief_world_debt * debtor_ratio
        self._world_agenda_cred = belief_world_agenda_cred * credor_ratio
        self._world_agenda_debt = belief_world_agenda_debt * debtor_ratio

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0

    def meld(self, exterior_otherlink):
        if self.other_id != exterior_otherlink.other_id:
            raise InvalidOtherException(
                f"Meld fail OtherLink='{self.other_id}' not the equal as OtherLink='{exterior_otherlink.other_id}"
            )
        self.credor_weight += exterior_otherlink.credor_weight
        self.debtor_weight += exterior_otherlink.debtor_weight


# class OtherLinkshop:
def otherlinks_get_from_json(otherlinks_json: str) -> dict[str:OtherLink]:
    otherlinks_dict = get_dict_from_json(json_x=otherlinks_json)
    return otherlinks_get_from_dict(x_dict=otherlinks_dict)


def otherlinks_get_from_dict(x_dict: dict) -> dict[str:OtherLink]:
    if x_dict is None:
        x_dict = {}
    otherlinks = {}
    for otherlinks_dict in x_dict.values():
        x_other = otherlink_shop(
            other_id=otherlinks_dict["other_id"],
            credor_weight=otherlinks_dict["credor_weight"],
            debtor_weight=otherlinks_dict["debtor_weight"],
        )
        otherlinks[x_other.other_id] = x_other
    return otherlinks


def otherlink_shop(
    other_id: OtherID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
    _world_agenda_cred: float = None,
    _world_agenda_debt: float = None,
) -> OtherLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return OtherLink(
        other_id=other_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _world_cred=_world_cred,
        _world_debt=_world_debt,
        _world_agenda_cred=_world_agenda_cred,
        _world_agenda_debt=_world_agenda_debt,
    )


@dataclass
class OtherUnitExternalMetrics:
    internal_other_id: OtherID = None
    credor_operational: bool = None
    debtor_operational: bool = None