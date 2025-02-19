from src.f01_road.road import (
    RoadUnit,
    rebuild_road,
    find_replace_road_key_dict,
    replace_bridge,
    is_heir_road,
    default_bridge_if_None,
)
from src.f00_instrument.dict_toolbox import get_empty_dict_if_None
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class InvalidReasonException(Exception):
    pass


@dataclass
class FactCore:
    base: RoadUnit
    pick: RoadUnit
    fopen: float = None
    fnigh: float = None

    def get_dict(self) -> dict[str,]:
        x_dict = {
            "base": self.base,
            "pick": self.pick,
        }
        if self.fopen is not None:
            x_dict["fopen"] = self.fopen
        if self.fnigh is not None:
            x_dict["fnigh"] = self.fnigh
        return x_dict

    def set_range_null(self):
        self.fopen = None
        self.fnigh = None

    def set_attr(self, pick: RoadUnit = None, fopen: float = None, fnigh: float = None):
        if pick is not None:
            self.pick = pick
        if fopen is not None:
            self.fopen = fopen
        if fnigh is not None:
            self.fnigh = fnigh

    def set_pick_to_base(self):
        self.set_attr(pick=self.base)
        self.fopen = None
        self.fnigh = None

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = rebuild_road(self.base, old_road, new_road)
        self.pick = rebuild_road(self.pick, old_road, new_road)

    def get_obj_key(self) -> RoadUnit:
        return self.base

    def get_tuple(self) -> tuple[RoadUnit, RoadUnit, float, float]:
        return (self.base, self.pick, self.fopen, self.fnigh)


@dataclass
class FactUnit(FactCore):
    pass


def factunit_shop(
    base: RoadUnit = None,
    pick: RoadUnit = None,
    fopen: float = None,
    fnigh: float = None,
) -> FactUnit:
    return FactUnit(base=base, pick=pick, fopen=fopen, fnigh=fnigh)


def factunits_get_from_dict(x_dict: dict) -> dict[RoadUnit, FactUnit]:
    facts = {}
    for fact_dict in x_dict.values():
        x_base = fact_dict["base"]
        x_pick = fact_dict["pick"]

        try:
            x_fopen = fact_dict["fopen"]
        except KeyError:
            x_fopen = None
        try:
            x_fnigh = fact_dict["fnigh"]
        except KeyError:
            x_fnigh = None

        x_fact = factunit_shop(
            base=x_base,
            pick=x_pick,
            fopen=x_fopen,
            fnigh=x_fnigh,
        )

        facts[x_fact.base] = x_fact
    return facts


def get_factunit_from_tuple(
    fact_tuple: tuple[RoadUnit, RoadUnit, float, float]
) -> FactUnit:
    return factunit_shop(fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3])


@dataclass
class FactHeir(FactCore):
    def mold(self, factunit: FactUnit):
        x_bool = self.fopen and factunit.fopen and self.fnigh
        if x_bool and self.fopen <= factunit.fopen and self.fnigh >= factunit.fopen:
            self.fopen = factunit.fopen

    def is_range(self):
        return self.fopen is not None and self.fnigh is not None


def factheir_shop(
    base: RoadUnit = None,
    pick: RoadUnit = None,
    fopen: float = None,
    fnigh: float = None,
) -> FactHeir:
    return FactHeir(base=base, pick=pick, fopen=fopen, fnigh=fnigh)


class PremiseStatusFinderException(Exception):
    pass


@dataclass
class PremiseStatusFinder:
    premise_open: float  # within 0 and divisor, can be more than premise_nigh
    premise_nigh: float  # within 0 and divisor, can be less than premise_open
    premise_divisor: float  # greater than zero
    fact_open_full: float  # less than fact nigh
    fact_nigh_full: float  # less than fact nigh

    def check_attr(self):
        if None in (
            self.premise_open,
            self.premise_nigh,
            self.premise_divisor,
            self.fact_open_full,
            self.fact_nigh_full,
        ):
            raise PremiseStatusFinderException("No parameter can be None")

        if self.fact_open_full > self.fact_nigh_full:
            raise PremiseStatusFinderException(
                f"{self.fact_open_full=} cannot be greater that {self.fact_nigh_full=}"
            )

        if self.premise_divisor <= 0:
            raise PremiseStatusFinderException(
                f"{self.premise_divisor=} cannot be less/equal to zero"
            )

        if self.premise_open < 0 or self.premise_open > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.premise_open=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

        if self.premise_nigh < 0 or self.premise_nigh > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.premise_nigh=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

    def bo(self) -> float:
        return self.fact_open_full % self.premise_divisor

    def bn(self) -> float:
        return self.fact_nigh_full % self.premise_divisor

    def po(self) -> float:
        return self.premise_open

    def pn(self) -> float:
        return self.premise_nigh

    def pd(self) -> float:
        return self.premise_divisor

    def get_active(self) -> bool:
        if self.fact_nigh_full - self.fact_open_full > self.premise_divisor:
            return True
        # Case B1
        elif get_range_less_than_divisor_active(
            bo=self.bo(), bn=self.bn(), po=self.po(), pn=self.pn()
        ):
            return True

        return False

    def get_task_status(self) -> bool:
        return bool(
            (
                self.get_active()
                and get_collasped_fact_range_active(
                    self.premise_open,
                    self.premise_nigh,
                    self.premise_divisor,
                    self.fact_nigh_full,
                )
                is False
            )
        )


def get_range_less_than_divisor_active(bo, bn, po, pn):
    # x_bool = False
    # if bo <= bn and po <= pn:
    #     if (
    #         (bo >= po and bo < pn)
    #         or (bn > po and bn < pn)
    #         or (bo < po and bn > pn)
    #         or (bo == po)
    #     ):
    #         x_bool = True
    # elif bo > bn and po <= pn:
    #     if (bn > po) or (bo < pn) or (bo == po):
    #         x_bool = True
    # elif bo <= bn and po > pn:
    #     if (bo < pn) or (bn > po) or (bo == po):
    #         x_bool = True
    # elif bo > bn and po > pn:
    #     if (bn <= pn) or (bn > pn):
    #         x_bool = True
    # return x_bool
    x_bool = False
    if bo <= bn and po <= pn:
        if (
            (bo >= po and bo < pn)
            or (bn > po and bn < pn)
            or (bo < po and bn > pn)
            or (bo == po)
        ):
            x_bool = True
    elif bo > bn and po <= pn:
        if (bn > po) or (bo < pn) or (bo == po):
            x_bool = True
    elif bo <= bn:
        if (bo < pn) or (bn > po) or (bo == po):
            x_bool = True
    else:
        x_bool = True
    return x_bool


def get_collasped_fact_range_active(
    premise_open: float,
    premise_nigh: float,
    premise_divisor: float,
    fact_nigh_full: float,
) -> bool:
    x_pbsd = premisestatusfinder_shop(
        premise_open=premise_open,
        premise_nigh=premise_nigh,
        premise_divisor=premise_divisor,
        fact_open_full=fact_nigh_full,
        fact_nigh_full=fact_nigh_full,
    )
    return x_pbsd.get_active()


def premisestatusfinder_shop(
    premise_open: float,
    premise_nigh: float,
    premise_divisor: float,
    fact_open_full: float,
    fact_nigh_full: float,
):
    x_premisestatusfinder = PremiseStatusFinder(
        premise_open,
        premise_nigh,
        premise_divisor,
        fact_open_full,
        fact_nigh_full,
    )
    x_premisestatusfinder.check_attr()
    return x_premisestatusfinder


@dataclass
class PremiseUnit:
    need: RoadUnit
    open: float = None
    nigh: float = None
    divisor: int = None
    _status: bool = None
    _task: bool = None
    bridge: str = None

    def get_obj_key(self):
        return self.need

    def get_dict(self) -> dict[str, str]:
        x_dict = {"need": self.need}
        if self.open is not None:
            x_dict["open"] = self.open
        if self.nigh is not None:
            x_dict["nigh"] = self.nigh

        if self.divisor is not None:
            x_dict["divisor"] = self.divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_bridge(self, new_bridge: str):
        old_bridge = copy_deepcopy(self.bridge)
        self.bridge = new_bridge
        self.need = replace_bridge(
            road=self.need, old_bridge=old_bridge, new_bridge=self.bridge
        )

    def is_in_lineage(self, fact_pick: RoadUnit):
        return is_heir_road(
            src=self.need, heir=fact_pick, bridge=self.bridge
        ) or is_heir_road(src=fact_pick, heir=self.need, bridge=self.bridge)

    def set_status(self, x_factheir: FactHeir):
        self._status = self._get_active(factheir=x_factheir)
        self._task = self._get_task_status(factheir=x_factheir)

    def _get_active(self, factheir: FactHeir):
        x_status = None
        # status might be true if premise is in lineage of fact
        if factheir is None:
            x_status = False
        elif self.is_in_lineage(fact_pick=factheir.pick):
            if self._is_range_or_segregate() is False:
                x_status = True
            elif self._is_range_or_segregate() and factheir.is_range() is False:
                x_status = False
            elif self._is_range_or_segregate() and factheir.is_range():
                x_status = self._get_range_segregate_status(factheir=factheir)
        elif self.is_in_lineage(fact_pick=factheir.pick) is False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return (
            self.divisor is not None and self.open is not None and self.nigh is not None
        )

    def _is_range(self):
        return self.divisor is None and self.open is not None and self.nigh is not None

    def _get_task_status(self, factheir: FactHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = factheir.fnigh > self.nigh
        elif self._status and self._is_segregate():
            segr_obj = premisestatusfinder_shop(
                premise_open=self.open,
                premise_nigh=self.nigh,
                premise_divisor=self.divisor,
                fact_open_full=factheir.fopen,
                fact_nigh_full=factheir.fnigh,
            )
            x_task = segr_obj.get_task_status()
        elif self._status in [True, False]:
            x_task = False

        return x_task

    def _get_range_segregate_status(self, factheir: FactHeir) -> bool:
        x_status = None
        if self._is_range():
            x_status = self._get_range_status(factheir=factheir)
        elif self._is_segregate():
            x_status = self._get_segregate_status(factheir=factheir)

        return x_status

    def _get_segregate_status(self, factheir: FactHeir) -> bool:
        segr_obj = premisestatusfinder_shop(
            premise_open=self.open,
            premise_nigh=self.nigh,
            premise_divisor=self.divisor,
            fact_open_full=factheir.fopen,
            fact_nigh_full=factheir.fnigh,
        )
        return segr_obj.get_active()

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (self.open <= factheir.fopen and self.nigh > factheir.fopen)
            or (self.open <= factheir.fnigh and self.nigh > factheir.fnigh)
            or (self.open >= factheir.fopen and self.nigh < factheir.fnigh)
        )

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.need = rebuild_road(self.need, old_road, new_road)


# class premisesshop:
def premiseunit_shop(
    need: RoadUnit,
    open: float = None,
    nigh: float = None,
    divisor: float = None,
    bridge: str = None,
) -> PremiseUnit:
    return PremiseUnit(
        need=need,
        open=open,
        nigh=nigh,
        divisor=divisor,
        bridge=default_bridge_if_None(bridge),
    )


def premises_get_from_dict(x_dict: dict) -> dict[str, PremiseUnit]:
    premises = {}
    for premise_dict in x_dict.values():
        try:
            x_open = premise_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = premise_dict["nigh"]
        except KeyError:
            x_nigh = None
        try:
            x_divisor = premise_dict["divisor"]
        except KeyError:
            x_divisor = None

        premise_x = premiseunit_shop(
            need=premise_dict["need"],
            open=x_open,
            nigh=x_nigh,
            divisor=x_divisor,
        )
        premises[premise_x.need] = premise_x
    return premises


@dataclass
class ReasonCore:
    base: RoadUnit
    premises: dict[RoadUnit, PremiseUnit]
    base_item_active_requisite: bool = None
    bridge: str = None

    def set_bridge(self, new_bridge: str):
        old_bridge = copy_deepcopy(self.bridge)
        self.bridge = new_bridge
        self.base = replace_bridge(self.base, old_bridge, new_bridge)

        new_premises = {}
        for premise_road, premise_obj in self.premises.items():
            new_premise_road = replace_bridge(
                road=premise_road,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            premise_obj.set_bridge(self.bridge)
            new_premises[new_premise_road] = premise_obj
        self.premises = new_premises

    def get_obj_key(self):
        return self.base

    def get_premises_count(self):
        return sum(1 for _ in self.premises.values())

    def set_premise(
        self,
        premise: RoadUnit,
        open: float = None,
        nigh: float = None,
        divisor: int = None,
    ):
        self.premises[premise] = premiseunit_shop(
            need=premise,
            open=open,
            nigh=nigh,
            divisor=divisor,
            bridge=self.bridge,
        )

    def premise_exists(self, x_need: RoadUnit) -> bool:
        return self.premises.get(x_need) != None

    def get_premise(self, premise: RoadUnit) -> PremiseUnit:
        return self.premises.get(premise)

    def del_premise(self, premise: RoadUnit):
        try:
            self.premises.pop(premise)
        except KeyError as e:
            raise InvalidReasonException(f"Reason unable to delete premise {e}") from e

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = rebuild_road(self.base, old_road, new_road)
        self.premises = find_replace_road_key_dict(
            dict_x=self.premises, old_road=old_road, new_road=new_road
        )


def reasoncore_shop(
    base: RoadUnit,
    premises: dict[RoadUnit, PremiseUnit] = None,
    base_item_active_requisite: bool = None,
    bridge: str = None,
):
    return ReasonCore(
        base=base,
        premises=get_empty_dict_if_None(premises),
        base_item_active_requisite=base_item_active_requisite,
        bridge=default_bridge_if_None(bridge),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def get_dict(self) -> dict[str, str]:
        premises_dict = {
            premise_road: premise.get_dict()
            for premise_road, premise in self.premises.items()
        }
        x_dict = {"base": self.base}
        if premises_dict != {}:
            x_dict["premises"] = premises_dict
        if self.base_item_active_requisite is not None:
            x_dict["base_item_active_requisite"] = self.base_item_active_requisite
        return x_dict


def reasonunit_shop(
    base: RoadUnit,
    premises: dict[RoadUnit, PremiseUnit] = None,
    base_item_active_requisite: bool = None,
    bridge: str = None,
):
    return ReasonUnit(
        base=base,
        premises=get_empty_dict_if_None(premises),
        base_item_active_requisite=base_item_active_requisite,
        bridge=default_bridge_if_None(bridge),
    )


@dataclass
class ReasonHeir(ReasonCore):
    _status: bool = None
    _task: bool = None
    _base_item_active_value: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_premises = {}
        for x_premiseunit in x_reasonunit.premises.values():
            premise_x = premiseunit_shop(
                need=x_premiseunit.need,
                open=x_premiseunit.open,
                nigh=x_premiseunit.nigh,
                divisor=x_premiseunit.divisor,
            )
            x_premises[premise_x.need] = premise_x
        self.premises = x_premises

    def clear_status(self):
        self._status = None
        for premise in self.premises.values():
            premise.clear_status()

    def _set_premise_status(self, factheir: FactHeir):
        for premise in self.premises.values():
            premise.set_status(factheir)

    def _get_base_fact(self, factheirs: dict[RoadUnit, FactHeir]) -> FactHeir:
        base_fact = None
        factheirs = get_empty_dict_if_None(factheirs)
        for y_factheir in factheirs.values():
            if self.base == y_factheir.base:
                base_fact = y_factheir
        return base_fact

    def set_base_item_active_value(self, bool_x: bool):
        self._base_item_active_value = bool_x

    def is_base_item_active_requisite_operational(self) -> bool:
        return (
            self._base_item_active_value is not None
            and self._base_item_active_value == self.base_item_active_requisite
        )

    def is_any_premise_true(self) -> tuple[bool, bool]:
        any_premise_true = False
        any_task_true = False
        for x_premiseunit in self.premises.values():
            if x_premiseunit._status:
                any_premise_true = True
                if x_premiseunit._task:
                    any_task_true = True
        return any_premise_true, any_task_true

    def _set_attr_status(self, any_premise_true: bool):
        self._status = (
            any_premise_true or self.is_base_item_active_requisite_operational()
        )

    def _set_attr_task(self, any_task_true: bool):
        self._task = True if any_task_true else None
        if self._status and self._task is None:
            self._task = False

    def set_status(self, factheirs: dict[RoadUnit, FactHeir]):
        self.clear_status()
        self._set_premise_status(self._get_base_fact(factheirs))
        any_premise_true, any_task_true = self.is_any_premise_true()
        self._set_attr_status(any_premise_true)
        self._set_attr_task(any_task_true)


def reasonheir_shop(
    base: RoadUnit,
    premises: dict[RoadUnit, PremiseUnit] = None,
    base_item_active_requisite: bool = None,
    _status: bool = None,
    _task: bool = None,
    _base_item_active_value: bool = None,
    bridge: str = None,
):
    return ReasonHeir(
        base=base,
        premises=get_empty_dict_if_None(premises),
        base_item_active_requisite=base_item_active_requisite,
        _status=_status,
        _task=_task,
        _base_item_active_value=_base_item_active_value,
        bridge=default_bridge_if_None(bridge),
    )


# class Reasonsshop:
def reasons_get_from_dict(reasons_dict: dict) -> dict[RoadUnit, ReasonUnit]:
    x_dict = {}
    for reason_dict in reasons_dict.values():
        x_reasonunit = reasonunit_shop(base=reason_dict["base"])
        if reason_dict.get("premises") is not None:
            x_reasonunit.premises = premises_get_from_dict(
                x_dict=reason_dict["premises"]
            )
        if reason_dict.get("base_item_active_requisite") is not None:
            x_reasonunit.base_item_active_requisite = reason_dict.get(
                "base_item_active_requisite"
            )
        x_dict[x_reasonunit.base] = x_reasonunit
    return x_dict
