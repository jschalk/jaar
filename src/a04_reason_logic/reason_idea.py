from src.a00_data_toolbox.dict_toolbox import get_empty_dict_if_None
from src.a01_way_logic.way import (
    WayStr,
    rebuild_way,
    find_replace_way_key_dict,
    replace_bridge,
    is_heir_way,
    default_bridge_if_None,
)
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class InvalidReasonException(Exception):
    pass


@dataclass
class FactCore:
    fcontext: WayStr
    fbranch: WayStr
    fopen: float = None
    fnigh: float = None

    def get_dict(self) -> dict[str,]:
        x_dict = {
            "fcontext": self.fcontext,
            "fbranch": self.fbranch,
        }
        if self.fopen is not None:
            x_dict["fopen"] = self.fopen
        if self.fnigh is not None:
            x_dict["fnigh"] = self.fnigh
        return x_dict

    def set_range_null(self):
        self.fopen = None
        self.fnigh = None

    def set_attr(
        self, fbranch: WayStr = None, fopen: float = None, fnigh: float = None
    ):
        if fbranch is not None:
            self.fbranch = fbranch
        if fopen is not None:
            self.fopen = fopen
        if fnigh is not None:
            self.fnigh = fnigh

    def set_fbranch_to_fcontext(self):
        self.set_attr(fbranch=self.fcontext)
        self.fopen = None
        self.fnigh = None

    def find_replace_way(self, old_way: WayStr, new_way: WayStr):
        self.fcontext = rebuild_way(self.fcontext, old_way, new_way)
        self.fbranch = rebuild_way(self.fbranch, old_way, new_way)

    def get_obj_key(self) -> WayStr:
        return self.fcontext

    def get_tuple(self) -> tuple[WayStr, WayStr, float, float]:
        return (self.fcontext, self.fbranch, self.fopen, self.fnigh)


@dataclass
class FactUnit(FactCore):
    pass


def factunit_shop(
    fcontext: WayStr = None,
    fbranch: WayStr = None,
    fopen: float = None,
    fnigh: float = None,
) -> FactUnit:
    return FactUnit(fcontext=fcontext, fbranch=fbranch, fopen=fopen, fnigh=fnigh)


def factunits_get_from_dict(x_dict: dict) -> dict[WayStr, FactUnit]:
    facts = {}
    for fact_dict in x_dict.values():
        x_fcontext = fact_dict["fcontext"]
        x_fbranch = fact_dict["fbranch"]

        try:
            x_fopen = fact_dict["fopen"]
        except KeyError:
            x_fopen = None
        try:
            x_fnigh = fact_dict["fnigh"]
        except KeyError:
            x_fnigh = None

        x_fact = factunit_shop(
            fcontext=x_fcontext,
            fbranch=x_fbranch,
            fopen=x_fopen,
            fnigh=x_fnigh,
        )

        facts[x_fact.fcontext] = x_fact
    return facts


def get_factunit_from_tuple(
    fact_tuple: tuple[WayStr, WayStr, float, float],
) -> FactUnit:
    return factunit_shop(fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3])


def get_dict_from_factunits(
    factunits: dict[WayStr, FactUnit],
) -> dict[WayStr, dict[str,]]:
    return {fact.fcontext: fact.get_dict() for fact in factunits.values()}


@dataclass
class FactHeir(FactCore):
    def mold(self, factunit: FactUnit):
        x_bool = self.fopen and factunit.fopen and self.fnigh
        if x_bool and self.fopen <= factunit.fopen and self.fnigh >= factunit.fopen:
            self.fopen = factunit.fopen

    def is_range(self):
        return self.fopen is not None and self.fnigh is not None


def factheir_shop(
    fcontext: WayStr = None,
    fbranch: WayStr = None,
    fopen: float = None,
    fnigh: float = None,
) -> FactHeir:
    return FactHeir(fcontext=fcontext, fbranch=fbranch, fopen=fopen, fnigh=fnigh)


class PremiseStatusFinderException(Exception):
    pass


@dataclass
class PremiseStatusFinder:
    premise_open: float  # within 0 and divisor, can be more than pnigh
    pnigh: float  # within 0 and divisor, can be less than premise_open
    premise_divisor: float  # greater than zero
    fact_open_full: float  # less than fnigh
    fnigh_full: float  # less than fnigh

    def check_attr(self):
        if None in (
            self.premise_open,
            self.pnigh,
            self.premise_divisor,
            self.fact_open_full,
            self.fnigh_full,
        ):
            raise PremiseStatusFinderException("No parameter can be None")

        if self.fact_open_full > self.fnigh_full:
            raise PremiseStatusFinderException(
                f"{self.fact_open_full=} cannot be greater that {self.fnigh_full=}"
            )

        if self.premise_divisor <= 0:
            raise PremiseStatusFinderException(
                f"{self.premise_divisor=} cannot be less/equal to zero"
            )

        if self.premise_open < 0 or self.premise_open > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.premise_open=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

        if self.pnigh < 0 or self.pnigh > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.pnigh=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

    def bo(self) -> float:
        return self.fact_open_full % self.premise_divisor

    def bn(self) -> float:
        return self.fnigh_full % self.premise_divisor

    def po(self) -> float:
        return self.premise_open

    def pn(self) -> float:
        return self.pnigh

    def pd(self) -> float:
        return self.premise_divisor

    def get_active(self) -> bool:
        if self.fnigh_full - self.fact_open_full > self.premise_divisor:
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
                    self.pnigh,
                    self.premise_divisor,
                    self.fnigh_full,
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
    pnigh: float,
    premise_divisor: float,
    fnigh_full: float,
) -> bool:
    x_pbsd = premisestatusfinder_shop(
        premise_open=premise_open,
        pnigh=pnigh,
        premise_divisor=premise_divisor,
        fact_open_full=fnigh_full,
        fnigh_full=fnigh_full,
    )
    return x_pbsd.get_active()


def premisestatusfinder_shop(
    premise_open: float,
    pnigh: float,
    premise_divisor: float,
    fact_open_full: float,
    fnigh_full: float,
):
    x_premisestatusfinder = PremiseStatusFinder(
        premise_open,
        pnigh,
        premise_divisor,
        fact_open_full,
        fnigh_full,
    )
    x_premisestatusfinder.check_attr()
    return x_premisestatusfinder


@dataclass
class PremiseUnit:
    pbranch: WayStr
    open: float = None
    pnigh: float = None
    divisor: int = None
    _status: bool = None
    _task: bool = None
    bridge: str = None

    def get_obj_key(self):
        return self.pbranch

    def get_dict(self) -> dict[str, str]:
        x_dict = {"pbranch": self.pbranch}
        if self.open is not None:
            x_dict["open"] = self.open
        if self.pnigh is not None:
            x_dict["pnigh"] = self.pnigh

        if self.divisor is not None:
            x_dict["divisor"] = self.divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_bridge(self, new_bridge: str):
        old_bridge = copy_deepcopy(self.bridge)
        self.bridge = new_bridge
        self.pbranch = replace_bridge(
            way=self.pbranch, old_bridge=old_bridge, new_bridge=self.bridge
        )

    def is_in_lineage(self, fact_fbranch: WayStr):
        return is_heir_way(
            src=self.pbranch, heir=fact_fbranch, bridge=self.bridge
        ) or is_heir_way(src=fact_fbranch, heir=self.pbranch, bridge=self.bridge)

    def set_status(self, x_factheir: FactHeir):
        self._status = self._get_active(factheir=x_factheir)
        self._task = self._get_task_status(factheir=x_factheir)

    def _get_active(self, factheir: FactHeir):
        x_status = None
        # status might be true if premise is in lineage of fact
        if factheir is None:
            x_status = False
        elif self.is_in_lineage(fact_fbranch=factheir.fbranch):
            if self._is_range_or_segregate() is False:
                x_status = True
            elif self._is_range_or_segregate() and factheir.is_range() is False:
                x_status = False
            elif self._is_range_or_segregate() and factheir.is_range():
                x_status = self._get_range_segregate_status(factheir=factheir)
        elif self.is_in_lineage(fact_fbranch=factheir.fbranch) is False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return (
            self.divisor is not None
            and self.open is not None
            and self.pnigh is not None
        )

    def _is_range(self):
        return self.divisor is None and self.open is not None and self.pnigh is not None

    def _get_task_status(self, factheir: FactHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = factheir.fnigh > self.pnigh
        elif self._status and self._is_segregate():
            segr_obj = premisestatusfinder_shop(
                premise_open=self.open,
                pnigh=self.pnigh,
                premise_divisor=self.divisor,
                fact_open_full=factheir.fopen,
                fnigh_full=factheir.fnigh,
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
            pnigh=self.pnigh,
            premise_divisor=self.divisor,
            fact_open_full=factheir.fopen,
            fnigh_full=factheir.fnigh,
        )
        return segr_obj.get_active()

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (self.open <= factheir.fopen and self.pnigh > factheir.fopen)
            or (self.open <= factheir.fnigh and self.pnigh > factheir.fnigh)
            or (self.open >= factheir.fopen and self.pnigh < factheir.fnigh)
        )

    def find_replace_way(self, old_way: WayStr, new_way: WayStr):
        self.pbranch = rebuild_way(self.pbranch, old_way, new_way)


# class premisesshop:
def premiseunit_shop(
    pbranch: WayStr,
    open: float = None,
    pnigh: float = None,
    divisor: float = None,
    bridge: str = None,
) -> PremiseUnit:
    return PremiseUnit(
        pbranch=pbranch,
        open=open,
        pnigh=pnigh,
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
            x_pnigh = premise_dict["pnigh"]
        except KeyError:
            x_pnigh = None
        try:
            x_divisor = premise_dict["divisor"]
        except KeyError:
            x_divisor = None

        premise_x = premiseunit_shop(
            pbranch=premise_dict["pbranch"],
            open=x_open,
            pnigh=x_pnigh,
            divisor=x_divisor,
        )
        premises[premise_x.pbranch] = premise_x
    return premises


@dataclass
class ReasonCore:
    rcontext: WayStr
    premises: dict[WayStr, PremiseUnit]
    rcontext_idea_active_requisite: bool = None
    bridge: str = None

    def set_bridge(self, new_bridge: str):
        old_bridge = copy_deepcopy(self.bridge)
        self.bridge = new_bridge
        self.rcontext = replace_bridge(self.rcontext, old_bridge, new_bridge)

        new_premises = {}
        for premise_way, premise_obj in self.premises.items():
            new_premise_way = replace_bridge(
                way=premise_way,
                old_bridge=old_bridge,
                new_bridge=self.bridge,
            )
            premise_obj.set_bridge(self.bridge)
            new_premises[new_premise_way] = premise_obj
        self.premises = new_premises

    def get_obj_key(self):
        return self.rcontext

    def get_premises_count(self):
        return sum(1 for _ in self.premises.values())

    def set_premise(
        self,
        premise: WayStr,
        open: float = None,
        pnigh: float = None,
        divisor: int = None,
    ):
        self.premises[premise] = premiseunit_shop(
            pbranch=premise,
            open=open,
            pnigh=pnigh,
            divisor=divisor,
            bridge=self.bridge,
        )

    def premise_exists(self, pbranch: WayStr) -> bool:
        return self.premises.get(pbranch) != None

    def get_premise(self, premise: WayStr) -> PremiseUnit:
        return self.premises.get(premise)

    def del_premise(self, premise: WayStr):
        try:
            self.premises.pop(premise)
        except KeyError as e:
            raise InvalidReasonException(f"Reason unable to delete premise {e}") from e

    def find_replace_way(self, old_way: WayStr, new_way: WayStr):
        self.rcontext = rebuild_way(self.rcontext, old_way, new_way)
        self.premises = find_replace_way_key_dict(
            dict_x=self.premises, old_way=old_way, new_way=new_way
        )


def reasoncore_shop(
    rcontext: WayStr,
    premises: dict[WayStr, PremiseUnit] = None,
    rcontext_idea_active_requisite: bool = None,
    bridge: str = None,
):
    return ReasonCore(
        rcontext=rcontext,
        premises=get_empty_dict_if_None(premises),
        rcontext_idea_active_requisite=rcontext_idea_active_requisite,
        bridge=default_bridge_if_None(bridge),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def get_dict(self) -> dict[str, str]:
        premises_dict = {
            premise_way: premise.get_dict()
            for premise_way, premise in self.premises.items()
        }
        x_dict = {"rcontext": self.rcontext}
        if premises_dict != {}:
            x_dict["premises"] = premises_dict
        if self.rcontext_idea_active_requisite is not None:
            x_dict["rcontext_idea_active_requisite"] = (
                self.rcontext_idea_active_requisite
            )
        return x_dict


def reasonunit_shop(
    rcontext: WayStr,
    premises: dict[WayStr, PremiseUnit] = None,
    rcontext_idea_active_requisite: bool = None,
    bridge: str = None,
):
    return ReasonUnit(
        rcontext=rcontext,
        premises=get_empty_dict_if_None(premises),
        rcontext_idea_active_requisite=rcontext_idea_active_requisite,
        bridge=default_bridge_if_None(bridge),
    )


@dataclass
class ReasonHeir(ReasonCore):
    _status: bool = None
    _task: bool = None
    _rcontext_idea_active_value: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_premises = {}
        for x_premiseunit in x_reasonunit.premises.values():
            premise_x = premiseunit_shop(
                pbranch=x_premiseunit.pbranch,
                open=x_premiseunit.open,
                pnigh=x_premiseunit.pnigh,
                divisor=x_premiseunit.divisor,
            )
            x_premises[premise_x.pbranch] = premise_x
        self.premises = x_premises

    def clear_status(self):
        self._status = None
        for premise in self.premises.values():
            premise.clear_status()

    def _set_premise_status(self, factheir: FactHeir):
        for premise in self.premises.values():
            premise.set_status(factheir)

    def _get_fcontext(self, factheirs: dict[WayStr, FactHeir]) -> FactHeir:
        fcontext = None
        factheirs = get_empty_dict_if_None(factheirs)
        for y_factheir in factheirs.values():
            if self.rcontext == y_factheir.fcontext:
                fcontext = y_factheir
        return fcontext

    def set_rcontext_idea_active_value(self, bool_x: bool):
        self._rcontext_idea_active_value = bool_x

    def is_rcontext_idea_active_requisite_operational(self) -> bool:
        return (
            self._rcontext_idea_active_value is not None
            and self._rcontext_idea_active_value == self.rcontext_idea_active_requisite
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
            any_premise_true or self.is_rcontext_idea_active_requisite_operational()
        )

    def _set_attr_task(self, any_task_true: bool):
        self._task = True if any_task_true else None
        if self._status and self._task is None:
            self._task = False

    def set_status(self, factheirs: dict[WayStr, FactHeir]):
        self.clear_status()
        self._set_premise_status(self._get_fcontext(factheirs))
        any_premise_true, any_task_true = self.is_any_premise_true()
        self._set_attr_status(any_premise_true)
        self._set_attr_task(any_task_true)


def reasonheir_shop(
    rcontext: WayStr,
    premises: dict[WayStr, PremiseUnit] = None,
    rcontext_idea_active_requisite: bool = None,
    _status: bool = None,
    _task: bool = None,
    _rcontext_idea_active_value: bool = None,
    bridge: str = None,
):
    return ReasonHeir(
        rcontext=rcontext,
        premises=get_empty_dict_if_None(premises),
        rcontext_idea_active_requisite=rcontext_idea_active_requisite,
        _status=_status,
        _task=_task,
        _rcontext_idea_active_value=_rcontext_idea_active_value,
        bridge=default_bridge_if_None(bridge),
    )


# class Reasonsshop:
def reasons_get_from_dict(reasons_dict: dict) -> dict[WayStr, ReasonUnit]:
    x_dict = {}
    for reason_dict in reasons_dict.values():
        x_reasonunit = reasonunit_shop(rcontext=reason_dict["rcontext"])
        if reason_dict.get("premises") is not None:
            x_reasonunit.premises = premises_get_from_dict(
                x_dict=reason_dict["premises"]
            )
        if reason_dict.get("rcontext_idea_active_requisite") is not None:
            x_reasonunit.rcontext_idea_active_requisite = reason_dict.get(
                "rcontext_idea_active_requisite"
            )
        x_dict[x_reasonunit.rcontext] = x_reasonunit
    return x_dict
