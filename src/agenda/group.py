from dataclasses import dataclass
from src.agenda.party import (
    PartyID,
    PartyLink,
    partylinks_get_from_dict,
    partylink_shop,
)
from src.agenda.meld import get_meld_weight
from src.instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import RoadUnit, default_road_delimiter_if_none, validate_roadnode


class InvalidGroupException(Exception):
    pass


class GroupID(str):  # Created to help track the concept
    pass


@dataclass
class GroupCore:
    group_id: GroupID = None


@dataclass
class GroupUnit(GroupCore):
    _party_mirror: bool = None  # set by AgendaUnit.set_partyunit()
    _partys: dict[PartyID:PartyLink] = None
    _agenda_credit: float = None  # calculated by AgendaUnit.set_agenda_metrics()
    _agenda_debt: float = None  # calculated by AgendaUnit.set_agenda_metrics()
    _agenda_intent_credit: float = None  # calculated by AgendaUnit.set_agenda_metrics()
    _agenda_intent_debt: float = None  # calculated by AgendaUnit.set_agenda_metrics()
    _treasury_partylinks: RoadUnit = None
    _road_delimiter: str = None

    def set_group_id(self, group_id: GroupID = None):
        if group_id != None:
            if self._party_mirror:
                self.group_id = validate_roadnode(group_id, self._road_delimiter)
            else:
                self.group_id = validate_roadnode(
                    group_id, self._road_delimiter, not_roadnode_required=True
                )

    def set_attr(self, _treasury_partylinks: RoadUnit):
        if _treasury_partylinks != None:
            self._treasury_partylinks = _treasury_partylinks

    def get_dict(self) -> dict[str:str]:
        x_dict = {"group_id": self.group_id}
        if self._party_mirror:
            x_dict["_party_mirror"] = self._party_mirror
        if self._partys not in [{}, None]:
            x_dict["_partys"] = self.get_partys_dict()
        if self._treasury_partylinks != None:
            x_dict["_treasury_partylinks"] = self._treasury_partylinks

        return x_dict

    def reset_agenda_credit_debt(self):
        self._agenda_credit = 0
        self._agenda_debt = 0
        self._agenda_intent_credit = 0
        self._agenda_intent_debt = 0
        for partylink in self._partys.values():
            partylink.reset_agenda_credit_debt()

    def _set_partylink_agenda_credit_debt(self):
        partylinks_creditor_weight_sum = sum(
            partylink.creditor_weight for partylink in self._partys.values()
        )
        partylinks_debtor_weight_sum = sum(
            partylink.debtor_weight for partylink in self._partys.values()
        )

        for partylink in self._partys.values():
            partylink.set_agenda_credit_debt(
                partylinks_creditor_weight_sum=partylinks_creditor_weight_sum,
                partylinks_debtor_weight_sum=partylinks_debtor_weight_sum,
                group_agenda_credit=self._agenda_credit,
                group_agenda_debt=self._agenda_debt,
                group_agenda_intent_credit=self._agenda_intent_credit,
                group_agenda_intent_debt=self._agenda_intent_debt,
            )

    def clear_partylinks(self):
        self._partys = {}

    def get_partys_dict(self) -> dict[str:str]:
        partys_x_dict = {}
        for party in self._partys.values():
            party_dict = party.get_dict()
            partys_x_dict[party_dict["party_id"]] = party_dict
        return partys_x_dict

    def set_partylink(self, partylink: PartyLink):
        self._partys[partylink.party_id] = partylink

    def edit_partylink(
        self, party_id: PartyID, creditor_weight: int = None, debtor_weight: int = None
    ):
        x_partylink = self.get_partylink(party_id)
        if creditor_weight != None:
            x_partylink.creditor_weight = creditor_weight
        if debtor_weight != None:
            x_partylink.debtor_weight = debtor_weight

    def get_partylink(self, party_id: PartyID) -> PartyLink:
        return self._partys.get(party_id)

    def partylink_exists(self, partylink_party_id: PartyID) -> bool:
        return self.get_partylink(partylink_party_id) != None

    def del_partylink(self, party_id):
        self._partys.pop(party_id)

    def _shift_partylink(
        self, to_delete_party_id: PartyID, to_absorb_party_id: PartyID
    ):
        old_group_partylink = self.get_partylink(to_delete_party_id)
        new_partylink_creditor_weight = old_group_partylink.creditor_weight
        new_partylink_debtor_weight = old_group_partylink.debtor_weight

        new_partylink = self.get_partylink(to_absorb_party_id)
        if new_partylink != None:
            new_partylink_creditor_weight += new_partylink.creditor_weight
            new_partylink_debtor_weight += new_partylink.debtor_weight

        self.set_partylink(
            partylink=partylink_shop(
                party_id=to_absorb_party_id,
                creditor_weight=new_partylink_creditor_weight,
                debtor_weight=new_partylink_debtor_weight,
            )
        )
        self.del_partylink(party_id=to_delete_party_id)

    def merge(self, other_group):
        self._merge_attributes_that_must_be_equal(other_group=other_group)
        self.merge_partylinks(other_group=other_group)

    def merge_partylinks(self, other_group):
        for oba in other_group._partys.values():
            if self._partys.get(oba.party_id) is None:
                self._partys[oba.party_id] = oba
            else:
                self._partys[oba.party_id].merge(oba)

    def _merge_attributes_that_must_be_equal(self, other_group):
        xl = [("group_id", self.group_id, other_group.group_id)]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidGroupException(
                    f"merge fail GroupUnit {self.group_id} .{attrs[0]}='{attrs[1]}' not the same as .{attrs[0]}='{attrs[2]}"
                )

        # if self.group_id != other_group.group_id:
        #     raise InvalidGroupException(
        #             f"merge fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {other_idea.get_road()} {attrs[0]}:{attrs[2]}"
        #     )


# class GroupUnitsshop:
def get_from_json(groupunits_json: str) -> dict[GroupID:GroupUnit]:
    groupunits_dict = get_dict_from_json(json_x=groupunits_json)
    return get_from_dict(x_dict=groupunits_dict)


def get_from_dict(x_dict: dict) -> dict[GroupID:GroupUnit]:
    groupunits = {}
    for groupunit_dict in x_dict.values():
        x_group = groupunit_shop(
            group_id=groupunit_dict["group_id"],
            _party_mirror=get_obj_from_groupunit_dict(groupunit_dict, "_party_mirror"),
            _partys=get_obj_from_groupunit_dict(groupunit_dict, "_partys"),
            _treasury_partylinks=get_obj_from_groupunit_dict(
                groupunit_dict, "_treasury_partylinks"
            ),
        )
        groupunits[x_group.group_id] = x_group
    return groupunits


def get_obj_from_groupunit_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_partys":
        return partylinks_get_from_dict(x_dict[dict_key])
    elif dict_key in {"_party_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def groupunit_shop(
    group_id: GroupID,
    _party_mirror: bool = None,
    _partys: dict[PartyID:PartyLink] = None,
    _treasury_partylinks: RoadUnit = None,
    _road_delimiter: str = None,
) -> GroupUnit:
    if _party_mirror and _treasury_partylinks != None:
        raise InvalidGroupException(
            f"_treasury_partylinks cannot be '{_treasury_partylinks}' for a single_party GroupUnit. It must have no value."
        )

    if _party_mirror is None:
        _party_mirror = False
    x_groupunit = GroupUnit(
        _party_mirror=_party_mirror,
        _partys=get_empty_dict_if_none(_partys),
        _agenda_credit=get_0_if_None(),
        _agenda_debt=get_0_if_None(),
        _agenda_intent_credit=get_0_if_None(),
        _agenda_intent_debt=get_0_if_None(),
        _treasury_partylinks=_treasury_partylinks,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_groupunit.set_group_id(group_id=group_id)
    return x_groupunit


@dataclass
class BalanceLink(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str:str]:
        return {
            "group_id": self.group_id,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def meld(
        self,
        other_balancelink,
        other_meld_strategy: str,
        src_meld_strategy: str,
    ):
        self.creditor_weight = get_meld_weight(
            src_weight=self.creditor_weight,
            src_meld_strategy=src_meld_strategy,
            other_weight=other_balancelink.creditor_weight,
            other_meld_strategy=other_meld_strategy,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_meld_strategy=src_meld_strategy,
            other_weight=other_balancelink.debtor_weight,
            other_meld_strategy=other_meld_strategy,
        )


# class BalanceLinksshop:
def balancelinks_get_from_json(balancelinks_json: str) -> dict[GroupID, BalanceLink]:
    balancelinks_dict = get_dict_from_json(json_x=balancelinks_json)
    return balancelinks_get_from_dict(x_dict=balancelinks_dict)


def balancelinks_get_from_dict(x_dict: dict) -> dict[GroupID, BalanceLink]:
    balancelinks = {}
    for balancelinks_dict in x_dict.values():
        x_group = balancelink_shop(
            group_id=balancelinks_dict["group_id"],
            creditor_weight=balancelinks_dict["creditor_weight"],
            debtor_weight=balancelinks_dict["debtor_weight"],
        )
        balancelinks[x_group.group_id] = x_group
    return balancelinks


def balancelink_shop(
    group_id: GroupID, creditor_weight: float = None, debtor_weight: float = None
) -> BalanceLink:
    creditor_weight = get_1_if_None(creditor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BalanceLink(
        group_id=group_id, creditor_weight=creditor_weight, debtor_weight=debtor_weight
    )


@dataclass
class BalanceHeir(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _agenda_credit: float = None
    _agenda_debt: float = None

    def set_agenda_credit_debt(
        self,
        idea_agenda_importance,
        balanceheirs_creditor_weight_sum: float,
        balanceheirs_debtor_weight_sum: float,
    ):
        self._agenda_credit = idea_agenda_importance * (
            self.creditor_weight / balanceheirs_creditor_weight_sum
        )
        self._agenda_debt = idea_agenda_importance * (
            self.debtor_weight / balanceheirs_debtor_weight_sum
        )


def balanceheir_shop(
    group_id: GroupID,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
) -> BalanceHeir:
    creditor_weight = get_1_if_None(creditor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BalanceHeir(
        group_id=group_id,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
    )


@dataclass
class BalanceLine(GroupCore):
    _agenda_credit: float = None
    _agenda_debt: float = None

    def add_agenda_credit_debt(self, agenda_credit: float, agenda_debt: float):
        self.set_agenda_credit_debt_zero_if_null()
        self._agenda_credit += agenda_credit
        self._agenda_debt += agenda_debt

    def set_agenda_credit_debt_zero_if_null(self):
        if self._agenda_credit is None:
            self._agenda_credit = 0
        if self._agenda_debt is None:
            self._agenda_debt = 0


def balanceline_shop(group_id: GroupID, _agenda_credit: float, _agenda_debt: float):
    return BalanceLine(
        group_id=group_id, _agenda_credit=_agenda_credit, _agenda_debt=_agenda_debt
    )
