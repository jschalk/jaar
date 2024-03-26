from src._road.road import PartyID, default_road_delimiter_if_none, validate_roadnode
from src._road.finance import default_planck_if_none
from dataclasses import dataclass
from src.instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None


class InvalidPartyException(Exception):
    pass


class InvalidDepotLinkException(Exception):
    pass


class _planck_RatioException(Exception):
    pass


@dataclass
class PartyCore:
    party_id: PartyID = None
    _road_delimiter: str = None
    _planck: float = None

    def set_party_id(self, x_party_id: PartyID):
        self.party_id = validate_roadnode(x_party_id, self._road_delimiter)


@dataclass
class PartyUnit(PartyCore):
    creditor_weight: int = None
    debtor_weight: int = None
    depotlink_type: str = None
    _agenda_credit: float = None
    _agenda_debt: float = None
    _agenda_intent_credit: float = None
    _agenda_intent_debt: float = None
    _agenda_intent_ratio_credit: float = None
    _agenda_intent_ratio_debt: float = None
    _creditor_operational: bool = None
    _debtor_operational: bool = None
    _treasury_due_paid: float = None
    _treasury_due_diff: float = None
    _output_agenda_meld_order: int = None
    _treasury_credit_score: float = None
    _treasury_voice_rank: int = None
    _treasury_voice_hx_lowest_rank: int = None

    def set_planck(self, x_planck: float):
        self._planck = x_planck

    def clear_output_agenda_meld_order(self):
        self._output_agenda_meld_order = None

    def set_output_agenda_meld_order(self, _output_agenda_meld_order: int):
        self._output_agenda_meld_order = _output_agenda_meld_order

    def set_depotlink_type(
        self,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        if depotlink_type not in (list(get_depotlink_types())):
            raise InvalidDepotLinkException(
                f"PartyUnit '{self.party_id}' cannot have type '{depotlink_type}'."
            )
        self.depotlink_type = depotlink_type
        if creditor_weight != None:
            self.set_creditor_weight(creditor_weight)
        if debtor_weight != None:
            self.set_debtor_weight(debtor_weight)

    def del_depotlink_type(self):
        self.depotlink_type = None

    def clear_treasurying_data(self):
        self._treasury_due_paid = None
        self._treasury_due_diff = None
        self._treasury_credit_score = None
        self._treasury_voice_rank = None

    def set_treasurying_data(
        self,
        due_paid: float,
        due_diff: float,
        credit_score: float,
        voice_rank: int,
    ):
        self._treasury_due_paid = due_paid
        self._treasury_due_diff = due_diff
        self._treasury_credit_score = credit_score
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
            "party_id": self.party_id,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_operational": self._creditor_operational,
            "_debtor_operational": self._debtor_operational,
            "_treasury_due_paid": self._treasury_due_paid,
            "_treasury_due_diff": self._treasury_due_diff,
            "_treasury_credit_score": self._treasury_credit_score,
            "_treasury_voice_rank": self._treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": self._treasury_voice_hx_lowest_rank,
            "depotlink_type": self.depotlink_type,
        }
        if all_attrs:
            x_dict["_agenda_credit"] = self._agenda_credit
            x_dict["_agenda_debt"] = self._agenda_debt
            x_dict["_agenda_intent_credit"] = self._agenda_intent_credit
            x_dict["_agenda_intent_debt"] = self._agenda_intent_debt
            x_dict["_agenda_intent_ratio_credit"] = self._agenda_intent_ratio_credit
            x_dict["_agenda_intent_ratio_debt"] = self._agenda_intent_ratio_debt
            x_dict["_output_agenda_meld_order"] = self._output_agenda_meld_order
        return x_dict

    def set_creditor_weight(self, creditor_weight: int):
        if (creditor_weight / self._planck).is_integer() == False:
            raise _planck_RatioException(
                f"'{creditor_weight}' is not divisible by planck '{self._planck}'"
            )
        self.creditor_weight = creditor_weight

    def set_debtor_weight(self, debtor_weight: int):
        if (debtor_weight / self._planck).is_integer() == False:
            raise _planck_RatioException(
                f"'{debtor_weight}' is not divisible by planck '{self._planck}'"
            )
        self.debtor_weight = debtor_weight

    def get_creditor_weight(self):
        return get_1_if_None(self.creditor_weight)

    def get_debtor_weight(self):
        return get_1_if_None(self.debtor_weight)

    def reset_agenda_credit_debt(self):
        self._agenda_credit = 0
        self._agenda_debt = 0
        self._agenda_intent_credit = 0
        self._agenda_intent_debt = 0
        self._agenda_intent_ratio_credit = 0
        self._agenda_intent_ratio_debt = 0

    def add_agenda_credit_debt(
        self,
        agenda_credit: float,
        agenda_debt,
        agenda_intent_credit: float,
        agenda_intent_debt,
    ):
        self._agenda_credit += agenda_credit
        self._agenda_debt += agenda_debt
        self._agenda_intent_credit += agenda_intent_credit
        self._agenda_intent_debt += agenda_intent_debt

    def set_agenda_intent_ratio_credit_debt(
        self,
        agenda_intent_ratio_credit_sum: float,
        agenda_intent_ratio_debt_sum: float,
        agenda_partyunit_total_creditor_weight: float,
        agenda_partyunit_total_debtor_weight: float,
    ):
        if agenda_intent_ratio_credit_sum == 0:
            self._agenda_intent_ratio_credit = (
                self.get_creditor_weight() / agenda_partyunit_total_creditor_weight
            )
        else:
            self._agenda_intent_ratio_credit = (
                self._agenda_intent_credit / agenda_intent_ratio_credit_sum
            )

        if agenda_intent_ratio_debt_sum == 0:
            self._agenda_intent_ratio_debt = (
                self.get_debtor_weight() / agenda_partyunit_total_debtor_weight
            )
        else:
            self._agenda_intent_ratio_debt = (
                self._agenda_intent_debt / agenda_intent_ratio_debt_sum
            )

    def merge(self, other_partyunit):
        if self.party_id != other_partyunit.party_id:
            raise InvalidPartyException(
                f"merge fail PartyUnit='{self.party_id}' not the same as PartyUnit='{other_partyunit.party_id}"
            )

        self.creditor_weight += other_partyunit.creditor_weight
        self.debtor_weight += other_partyunit.debtor_weight


# class PartyUnitsshop:
def partyunits_get_from_json(partyunits_json: str) -> dict[str:PartyUnit]:
    partyunits_dict = get_dict_from_json(json_x=partyunits_json)
    return partyunits_get_from_dict(x_dict=partyunits_dict)


def partyunits_get_from_dict(x_dict: dict) -> dict[str:PartyUnit]:
    partyunits = {}
    for partyunits_dict in x_dict.values():
        try:
            _treasury_due_paid = partyunits_dict["_treasury_due_paid"]
        except KeyError:
            _treasury_due_paid = None

        try:
            _treasury_due_diff = partyunits_dict["_treasury_due_diff"]
        except KeyError:
            _treasury_due_diff = None

        try:
            _treasury_credit_score = partyunits_dict["_treasury_credit_score"]
        except KeyError:
            _treasury_credit_score = None

        try:
            _treasury_voice_rank = partyunits_dict["_treasury_voice_rank"]
        except KeyError:
            _treasury_voice_rank = None

        try:
            _treasury_voice_hx_lowest_rank = partyunits_dict[
                "_treasury_voice_hx_lowest_rank"
            ]
        except KeyError:
            _treasury_voice_hx_lowest_rank = None

        try:
            depotlink_type = partyunits_dict["depotlink_type"]
        except KeyError:
            depotlink_type = None

        x_partyunit = partyunit_shop(
            party_id=partyunits_dict["party_id"],
            creditor_weight=partyunits_dict["creditor_weight"],
            debtor_weight=partyunits_dict["debtor_weight"],
            _creditor_operational=partyunits_dict["_creditor_operational"],
            _debtor_operational=partyunits_dict["_debtor_operational"],
            depotlink_type=depotlink_type,
        )
        x_partyunit.set_treasurying_data(
            due_paid=_treasury_due_paid,
            due_diff=_treasury_due_diff,
            credit_score=_treasury_credit_score,
            voice_rank=_treasury_voice_rank,
        )
        x_partyunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
        partyunits[x_partyunit.party_id] = x_partyunit
    return partyunits


def partyunit_shop(
    party_id: PartyID,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_operational: bool = None,
    _debtor_operational: bool = None,
    # _agenda_credit: float = None,
    # _agenda_debt: float = None,
    # _agenda_intent_credit: float = None,
    # _agenda_intent_debt: float = None,
    # _agenda_intent_ratio_credit: float = None,
    # _agenda_intent_ratio_debt: float = None,
    # _treasury_due_paid: float = None,
    # _treasury_due_diff: float = None,
    depotlink_type: str = None,
    _road_delimiter: str = None,
    _planck: float = None,
) -> PartyUnit:
    x_partyunit = PartyUnit(
        creditor_weight=get_1_if_None(creditor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _creditor_operational=_creditor_operational,
        _debtor_operational=_debtor_operational,
        _agenda_credit=get_0_if_None(),
        _agenda_debt=get_0_if_None(),
        _agenda_intent_credit=get_0_if_None(),
        _agenda_intent_debt=get_0_if_None(),
        _agenda_intent_ratio_credit=get_0_if_None(),
        _agenda_intent_ratio_debt=get_0_if_None(),
        _treasury_due_paid=None,
        _treasury_due_diff=None,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    x_partyunit.set_party_id(x_party_id=party_id)
    if depotlink_type != None:
        x_partyunit.set_depotlink_type(depotlink_type=depotlink_type)
    return x_partyunit


@dataclass
class PartyLink(PartyCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _agenda_credit: float = None
    _agenda_debt: float = None
    _agenda_intent_credit: float = None
    _agenda_intent_debt: float = None

    def get_dict(self) -> dict[str:str]:
        return {
            "party_id": self.party_id,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_agenda_credit_debt(
        self,
        partylinks_creditor_weight_sum: float,
        partylinks_debtor_weight_sum: float,
        group_agenda_credit: float,
        group_agenda_debt: float,
        group_agenda_intent_credit: float,
        group_agenda_intent_debt: float,
    ):
        group_agenda_credit = get_1_if_None(group_agenda_credit)
        group_agenda_debt = get_1_if_None(group_agenda_debt)
        creditor_ratio = self.creditor_weight / partylinks_creditor_weight_sum
        debtor_ratio = self.debtor_weight / partylinks_debtor_weight_sum

        self._agenda_credit = group_agenda_credit * creditor_ratio
        self._agenda_debt = group_agenda_debt * debtor_ratio
        self._agenda_intent_credit = group_agenda_intent_credit * creditor_ratio
        self._agenda_intent_debt = group_agenda_intent_debt * debtor_ratio

    def reset_agenda_credit_debt(self):
        self._agenda_credit = 0
        self._agenda_debt = 0
        self._agenda_intent_credit = 0
        self._agenda_intent_debt = 0

    def merge(self, other_partylink):
        if self.party_id != other_partylink.party_id:
            raise InvalidPartyException(
                f"merge fail PartyLink='{self.party_id}' not the same as PartyLink='{other_partylink.party_id}"
            )
        self.creditor_weight += other_partylink.creditor_weight
        self.debtor_weight += other_partylink.debtor_weight


# class PartyLinkshop:
def partylinks_get_from_json(partylinks_json: str) -> dict[str:PartyLink]:
    partylinks_dict = get_dict_from_json(json_x=partylinks_json)
    return partylinks_get_from_dict(x_dict=partylinks_dict)


def partylinks_get_from_dict(x_dict: dict) -> dict[str:PartyLink]:
    partylinks = {}
    for partylinks_dict in x_dict.values():
        x_party = partylink_shop(
            party_id=partylinks_dict["party_id"],
            creditor_weight=partylinks_dict["creditor_weight"],
            debtor_weight=partylinks_dict["debtor_weight"],
        )
        partylinks[x_party.party_id] = x_party
    return partylinks


def partylink_shop(
    party_id: PartyID,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
    _agenda_intent_credit: float = None,
    _agenda_intent_debt: float = None,
) -> PartyLink:
    creditor_weight = get_1_if_None(creditor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return PartyLink(
        party_id=party_id,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
        _agenda_intent_credit=_agenda_intent_credit,
        _agenda_intent_debt=_agenda_intent_debt,
    )


@dataclass
class PartyUnitExternalMetrics:
    internal_party_id: PartyID = None
    creditor_operational: bool = None
    debtor_operational: bool = None


def get_depotlink_types() -> dict[str:str]:
    return {
        "blind_trust": "blind_trust",
        "ignore": "ignore",
        "assignment": "assignment",
    }


def get_default_depotlink_type() -> str:
    return get_depotlink_types().get("assignment")
