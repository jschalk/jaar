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
    popen: float  # within 0 and pdivisor, can be more than pnigh
    pnigh: float  # within 0 and pdivisor, can be less than popen
    pdivisor: float  # greater than zero
    fopen_full: float  # less than fnigh
    fnigh_full: float  # less than fnigh

    def check_attr(self):
        if None in (
            self.popen,
            self.pnigh,
            self.pdivisor,
            self.fopen_full,
            self.fnigh_full,
        ):
            raise PremiseStatusFinderException("No parameter can be None")

        if self.fopen_full > self.fnigh_full:
            raise PremiseStatusFinderException(
                f"{self.fopen_full=} cannot be greater than {self.fnigh_full=}"
            )

        if self.pdivisor <= 0:
            raise PremiseStatusFinderException(
                f"{self.pdivisor=} cannot be less/equal to zero"
            )

        if self.popen < 0 or self.popen > self.pdivisor:
            raise PremiseStatusFinderException(
                f"{self.popen=} cannot be less than zero or greater than {self.pdivisor=}"
            )

        if self.pnigh < 0 or self.pnigh > self.pdivisor:
            raise PremiseStatusFinderException(
                f"{self.pnigh=} cannot be less than zero or greater than {self.pdivisor=}"
            )

    def bo(self) -> float:
        return self.fopen_full % self.pdivisor

    def bn(self) -> float:
        return self.fnigh_full % self.pdivisor

    def po(self) -> float:
        return self.popen

    def pn(self) -> float:
        return self.pnigh

    def pd(self) -> float:
        return self.pdivisor

    def get_active(self) -> bool:
        if self.fnigh_full - self.fopen_full > self.pdivisor:
            return True
        # Case B1
        elif get_range_less_than_pdivisor_active(
            bo=self.bo(), bn=self.bn(), po=self.po(), pn=self.pn()
        ):
            return True

        return False

    def get_task_status(self) -> bool:
        return bool(
            (
                self.get_active()
                and get_collasped_fact_range_active(
                    self.popen,
                    self.pnigh,
                    self.pdivisor,
                    self.fnigh_full,
                )
                is False
            )
        )


def get_range_less_than_pdivisor_active(bo, bn, po, pn):
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
    popen: float,
    pnigh: float,
    pdivisor: float,
    fnigh_full: float,
) -> bool:
    x_pbsd = premisestatusfinder_shop(
        popen=popen,
        pnigh=pnigh,
        pdivisor=pdivisor,
        fopen_full=fnigh_full,
        fnigh_full=fnigh_full,
    )
    return x_pbsd.get_active()


def premisestatusfinder_shop(
    popen: float,
    pnigh: float,
    pdivisor: float,
    fopen_full: float,
    fnigh_full: float,
):
    x_premisestatusfinder = PremiseStatusFinder(
        popen,
        pnigh,
        pdivisor,
        fopen_full,
        fnigh_full,
    )
    x_premisestatusfinder.check_attr()
    return x_premisestatusfinder


@dataclass
class PremiseUnit:
    pbranch: WayStr
    popen: float = None
    pnigh: float = None
    pdivisor: int = None
    _status: bool = None
    _task: bool = None
    bridge: str = None

    def get_obj_key(self):
        return self.pbranch

    def get_dict(self) -> dict[str, str]:
        x_dict = {"pbranch": self.pbranch}
        if self.popen is not None:
            x_dict["popen"] = self.popen
        if self.pnigh is not None:
            x_dict["pnigh"] = self.pnigh

        if self.pdivisor is not None:
            x_dict["pdivisor"] = self.pdivisor

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
            self.pdivisor is not None
            and self.popen is not None
            and self.pnigh is not None
        )

    def _is_range(self):
        return (
            self.pdivisor is None and self.popen is not None and self.pnigh is not None
        )

    def _get_task_status(self, factheir: FactHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = factheir.fnigh > self.pnigh
        elif self._status and self._is_segregate():
            segr_obj = premisestatusfinder_shop(
                popen=self.popen,
                pnigh=self.pnigh,
                pdivisor=self.pdivisor,
                fopen_full=factheir.fopen,
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
            popen=self.popen,
            pnigh=self.pnigh,
            pdivisor=self.pdivisor,
            fopen_full=factheir.fopen,
            fnigh_full=factheir.fnigh,
        )
        return segr_obj.get_active()

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (self.popen <= factheir.fopen and self.pnigh > factheir.fopen)
            or (self.popen <= factheir.fnigh and self.pnigh > factheir.fnigh)
            or (self.popen >= factheir.fopen and self.pnigh < factheir.fnigh)
        )

    def find_replace_way(self, old_way: WayStr, new_way: WayStr):
        self.pbranch = rebuild_way(self.pbranch, old_way, new_way)


# class premisesshop:
def premiseunit_shop(
    pbranch: WayStr,
    popen: float = None,
    pnigh: float = None,
    pdivisor: float = None,
    bridge: str = None,
) -> PremiseUnit:
    return PremiseUnit(
        pbranch=pbranch,
        popen=popen,
        pnigh=pnigh,
        pdivisor=pdivisor,
        bridge=default_bridge_if_None(bridge),
    )


def premises_get_from_dict(x_dict: dict) -> dict[str, PremiseUnit]:
    premises = {}
    for premise_dict in x_dict.values():
        try:
            x_popen = premise_dict["popen"]
        except KeyError:
            x_popen = None
        try:
            x_pnigh = premise_dict["pnigh"]
        except KeyError:
            x_pnigh = None
        try:
            x_pdivisor = premise_dict["pdivisor"]
        except KeyError:
            x_pdivisor = None

        premise_x = premiseunit_shop(
            pbranch=premise_dict["pbranch"],
            popen=x_popen,
            pnigh=x_pnigh,
            pdivisor=x_pdivisor,
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
        popen: float = None,
        pnigh: float = None,
        pdivisor: int = None,
    ):
        self.premises[premise] = premiseunit_shop(
            pbranch=premise,
            popen=popen,
            pnigh=pnigh,
            pdivisor=pdivisor,
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
                popen=x_premiseunit.popen,
                pnigh=x_premiseunit.pnigh,
                pdivisor=x_premiseunit.pdivisor,
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
