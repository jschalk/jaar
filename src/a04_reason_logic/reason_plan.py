from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from src.a00_data_toolbox.dict_toolbox import get_empty_dict_if_None
from src.a01_term_logic.rope import (
    RopeTerm,
    default_knot_if_None,
    find_replace_rope_key_dict,
    is_heir_rope,
    rebuild_rope,
    replace_knot,
)


class InvalidReasonException(Exception):
    pass


@dataclass
class FactCore:
    f_context: RopeTerm = None
    f_state: RopeTerm = None
    f_lower: float = None
    f_upper: float = None

    def get_dict(self) -> dict[str,]:
        x_dict = {
            "f_context": self.f_context,
            "f_state": self.f_state,
        }
        if self.f_lower is not None:
            x_dict["f_lower"] = self.f_lower
        if self.f_upper is not None:
            x_dict["f_upper"] = self.f_upper
        return x_dict

    def set_range_null(self):
        self.f_lower = None
        self.f_upper = None

    def set_attr(
        self, f_state: RopeTerm = None, f_lower: float = None, f_upper: float = None
    ):
        if f_state is not None:
            self.f_state = f_state
        if f_lower is not None:
            self.f_lower = f_lower
        if f_upper is not None:
            self.f_upper = f_upper

    def set_f_state_to_f_context(self):
        self.set_attr(f_state=self.f_context)
        self.f_lower = None
        self.f_upper = None

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.f_context = rebuild_rope(self.f_context, old_rope, new_rope)
        self.f_state = rebuild_rope(self.f_state, old_rope, new_rope)

    def get_obj_key(self) -> RopeTerm:
        return self.f_context

    def get_tuple(self) -> tuple[RopeTerm, RopeTerm, float, float]:
        return (self.f_context, self.f_state, self.f_lower, self.f_upper)


@dataclass
class FactUnit(FactCore):
    pass


def factunit_shop(
    f_context: RopeTerm = None,
    f_state: RopeTerm = None,
    f_lower: float = None,
    f_upper: float = None,
) -> FactUnit:
    return FactUnit(
        f_context=f_context, f_state=f_state, f_lower=f_lower, f_upper=f_upper
    )


def factunits_get_from_dict(x_dict: dict) -> dict[RopeTerm, FactUnit]:
    facts = {}
    for fact_dict in x_dict.values():
        x_f_context = fact_dict["f_context"]
        x_f_state = fact_dict["f_state"]

        try:
            x_f_lower = fact_dict["f_lower"]
        except KeyError:
            x_f_lower = None
        try:
            x_f_upper = fact_dict["f_upper"]
        except KeyError:
            x_f_upper = None

        x_fact = factunit_shop(
            f_context=x_f_context,
            f_state=x_f_state,
            f_lower=x_f_lower,
            f_upper=x_f_upper,
        )

        facts[x_fact.f_context] = x_fact
    return facts


def get_factunit_from_tuple(
    fact_tuple: tuple[RopeTerm, RopeTerm, float, float],
) -> FactUnit:
    return factunit_shop(fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3])


def get_dict_from_factunits(
    factunits: dict[RopeTerm, FactUnit],
) -> dict[RopeTerm, dict[str,]]:
    return {fact.f_context: fact.get_dict() for fact in factunits.values()}


@dataclass
class FactHeir(FactCore):
    def mold(self, factunit: FactUnit):
        x_bool = self.f_lower and factunit.f_lower and self.f_upper
        if (
            x_bool
            and self.f_lower <= factunit.f_lower
            and self.f_upper >= factunit.f_lower
        ):
            self.f_lower = factunit.f_lower

    def is_range(self):
        return self.f_lower is not None and self.f_upper is not None


def factheir_shop(
    f_context: RopeTerm = None,
    f_state: RopeTerm = None,
    f_lower: float = None,
    f_upper: float = None,
) -> FactHeir:
    return FactHeir(
        f_context=f_context, f_state=f_state, f_lower=f_lower, f_upper=f_upper
    )


class PremiseStatusFinderException(Exception):
    pass


@dataclass
class PremiseStatusFinder:
    p_lower: float  # between 0 and p_divisor, can be more than p_upper
    p_upper: float  # between 0 and p_divisor, can be less than p_lower
    p_divisor: float  # greater than zero
    f_lower_full: float  # less than f_upper
    f_upper_full: float  # less than f_upper

    def check_attr(self):
        if None in (
            self.p_lower,
            self.p_upper,
            self.p_divisor,
            self.f_lower_full,
            self.f_upper_full,
        ):
            raise PremiseStatusFinderException("No parameter can be None")

        if self.f_lower_full > self.f_upper_full:
            raise PremiseStatusFinderException(
                f"{self.f_lower_full=} cannot be greater than {self.f_upper_full=}"
            )

        if self.p_divisor <= 0:
            raise PremiseStatusFinderException(
                f"{self.p_divisor=} cannot be less/equal to zero"
            )

        if self.p_lower < 0 or self.p_lower > self.p_divisor:
            raise PremiseStatusFinderException(
                f"{self.p_lower=} cannot be less than zero or greater than {self.p_divisor=}"
            )

        if self.p_upper < 0 or self.p_upper > self.p_divisor:
            raise PremiseStatusFinderException(
                f"{self.p_upper=} cannot be less than zero or greater than {self.p_divisor=}"
            )

    def bo(self) -> float:
        return self.f_lower_full % self.p_divisor

    def bn(self) -> float:
        return self.f_upper_full % self.p_divisor

    def po(self) -> float:
        return self.p_lower

    def pn(self) -> float:
        return self.p_upper

    def pd(self) -> float:
        return self.p_divisor

    def get_active(self) -> bool:
        if self.f_upper_full - self.f_lower_full > self.p_divisor:
            return True
        elif get_range_less_than_p_divisor_active(
            bo=self.bo(), bn=self.bn(), po=self.po(), pn=self.pn()
        ):
            return True

        return False

    def get_chore_status(self) -> bool:
        return bool(
            (
                self.get_active()
                and get_collasped_fact_range_active(
                    self.p_lower,
                    self.p_upper,
                    self.p_divisor,
                    self.f_upper_full,
                )
                is False
            )
        )


def get_range_less_than_p_divisor_active(bo, bn, po, pn):
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
    p_lower: float,
    p_upper: float,
    p_divisor: float,
    f_upper_full: float,
) -> bool:
    x_pbsd = premisestatusfinder_shop(
        p_lower=p_lower,
        p_upper=p_upper,
        p_divisor=p_divisor,
        f_lower_full=f_upper_full,
        f_upper_full=f_upper_full,
    )
    return x_pbsd.get_active()


def premisestatusfinder_shop(
    p_lower: float,
    p_upper: float,
    p_divisor: float,
    f_lower_full: float,
    f_upper_full: float,
):
    x_premisestatusfinder = PremiseStatusFinder(
        p_lower,
        p_upper,
        p_divisor,
        f_lower_full,
        f_upper_full,
    )
    x_premisestatusfinder.check_attr()
    return x_premisestatusfinder


@dataclass
class PremiseUnit:
    p_state: RopeTerm
    p_lower: float = None
    p_upper: float = None
    p_divisor: int = None
    _status: bool = None
    _chore: bool = None
    knot: str = None

    def get_obj_key(self):
        return self.p_state

    def get_dict(self) -> dict[str, str]:
        x_dict = {"p_state": self.p_state}
        if self.p_lower is not None:
            x_dict["p_lower"] = self.p_lower
        if self.p_upper is not None:
            x_dict["p_upper"] = self.p_upper

        if self.p_divisor is not None:
            x_dict["p_divisor"] = self.p_divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_knot(self, new_knot: str):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.p_state = replace_knot(
            rope=self.p_state, old_knot=old_knot, new_knot=self.knot
        )

    def is_in_lineage(self, fact_f_state: RopeTerm):
        return is_heir_rope(
            src=self.p_state, heir=fact_f_state, knot=self.knot
        ) or is_heir_rope(src=fact_f_state, heir=self.p_state, knot=self.knot)

    def set_status(self, x_factheir: FactHeir):
        self._status = self._get_active(factheir=x_factheir)
        self._chore = self._get_chore_status(factheir=x_factheir)

    def _get_active(self, factheir: FactHeir):
        x_status = None
        # status might be true if premise is in lineage of fact
        if factheir is None:
            x_status = False
        elif self.is_in_lineage(fact_f_state=factheir.f_state):
            if self._is_range_or_segregate() is False:
                x_status = True
            elif self._is_range_or_segregate() and factheir.is_range() is False:
                x_status = False
            elif self._is_range_or_segregate() and factheir.is_range():
                x_status = self._get_range_segregate_status(factheir=factheir)
        elif self.is_in_lineage(fact_f_state=factheir.f_state) is False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return (
            self.p_divisor is not None
            and self.p_lower is not None
            and self.p_upper is not None
        )

    def _is_range(self):
        return (
            self.p_divisor is None
            and self.p_lower is not None
            and self.p_upper is not None
        )

    def _get_chore_status(self, factheir: FactHeir) -> bool:
        x_chore = None
        if self._status and self._is_range():
            x_chore = factheir.f_upper > self.p_upper
        elif self._status and self._is_segregate():
            segr_obj = premisestatusfinder_shop(
                p_lower=self.p_lower,
                p_upper=self.p_upper,
                p_divisor=self.p_divisor,
                f_lower_full=factheir.f_lower,
                f_upper_full=factheir.f_upper,
            )
            x_chore = segr_obj.get_chore_status()
        elif self._status in [True, False]:
            x_chore = False

        return x_chore

    def _get_range_segregate_status(self, factheir: FactHeir) -> bool:
        x_status = None
        if self._is_range():
            x_status = self._get_range_status(factheir=factheir)
        elif self._is_segregate():
            x_status = self._get_segregate_status(factheir=factheir)

        return x_status

    def _get_segregate_status(self, factheir: FactHeir) -> bool:
        segr_obj = premisestatusfinder_shop(
            p_lower=self.p_lower,
            p_upper=self.p_upper,
            p_divisor=self.p_divisor,
            f_lower_full=factheir.f_lower,
            f_upper_full=factheir.f_upper,
        )
        return segr_obj.get_active()

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (self.p_lower <= factheir.f_lower and self.p_upper > factheir.f_lower)
            or (self.p_lower <= factheir.f_upper and self.p_upper > factheir.f_upper)
            or (self.p_lower >= factheir.f_lower and self.p_upper < factheir.f_upper)
        )

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.p_state = rebuild_rope(self.p_state, old_rope, new_rope)


# class premisesshop:
def premiseunit_shop(
    p_state: RopeTerm,
    p_lower: float = None,
    p_upper: float = None,
    p_divisor: float = None,
    knot: str = None,
) -> PremiseUnit:
    return PremiseUnit(
        p_state=p_state,
        p_lower=p_lower,
        p_upper=p_upper,
        p_divisor=p_divisor,
        knot=default_knot_if_None(knot),
    )


def premises_get_from_dict(x_dict: dict) -> dict[str, PremiseUnit]:
    premises = {}
    for premise_dict in x_dict.values():
        try:
            x_p_lower = premise_dict["p_lower"]
        except KeyError:
            x_p_lower = None
        try:
            x_p_upper = premise_dict["p_upper"]
        except KeyError:
            x_p_upper = None
        try:
            x_p_divisor = premise_dict["p_divisor"]
        except KeyError:
            x_p_divisor = None

        premise_x = premiseunit_shop(
            p_state=premise_dict["p_state"],
            p_lower=x_p_lower,
            p_upper=x_p_upper,
            p_divisor=x_p_divisor,
        )
        premises[premise_x.p_state] = premise_x
    return premises


@dataclass
class ReasonCore:
    r_context: RopeTerm
    premises: dict[RopeTerm, PremiseUnit]
    r_plan_active_requisite: bool = None
    knot: str = None

    def set_knot(self, new_knot: str):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.r_context = replace_knot(self.r_context, old_knot, new_knot)

        new_premises = {}
        for premise_rope, premise_obj in self.premises.items():
            new_premise_rope = replace_knot(
                rope=premise_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            premise_obj.set_knot(self.knot)
            new_premises[new_premise_rope] = premise_obj
        self.premises = new_premises

    def get_obj_key(self):
        return self.r_context

    def get_premises_count(self):
        return sum(1 for _ in self.premises.values())

    def set_premise(
        self,
        premise: RopeTerm,
        p_lower: float = None,
        p_upper: float = None,
        p_divisor: int = None,
    ):
        self.premises[premise] = premiseunit_shop(
            p_state=premise,
            p_lower=p_lower,
            p_upper=p_upper,
            p_divisor=p_divisor,
            knot=self.knot,
        )

    def premise_exists(self, p_state: RopeTerm) -> bool:
        return self.premises.get(p_state) != None

    def get_premise(self, premise: RopeTerm) -> PremiseUnit:
        return self.premises.get(premise)

    def del_premise(self, premise: RopeTerm):
        try:
            self.premises.pop(premise)
        except KeyError as e:
            raise InvalidReasonException(f"Reason unable to delete premise {e}") from e

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.r_context = rebuild_rope(self.r_context, old_rope, new_rope)
        self.premises = find_replace_rope_key_dict(
            dict_x=self.premises, old_rope=old_rope, new_rope=new_rope
        )


def reasoncore_shop(
    r_context: RopeTerm,
    premises: dict[RopeTerm, PremiseUnit] = None,
    r_plan_active_requisite: bool = None,
    knot: str = None,
):
    return ReasonCore(
        r_context=r_context,
        premises=get_empty_dict_if_None(premises),
        r_plan_active_requisite=r_plan_active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def get_dict(self) -> dict[str, str]:
        premises_dict = {
            premise_rope: premise.get_dict()
            for premise_rope, premise in self.premises.items()
        }
        x_dict = {"r_context": self.r_context}
        if premises_dict != {}:
            x_dict["premises"] = premises_dict
        if self.r_plan_active_requisite is not None:
            x_dict["r_plan_active_requisite"] = self.r_plan_active_requisite
        return x_dict


def reasonunit_shop(
    r_context: RopeTerm,
    premises: dict[RopeTerm, PremiseUnit] = None,
    r_plan_active_requisite: bool = None,
    knot: str = None,
):
    return ReasonUnit(
        r_context=r_context,
        premises=get_empty_dict_if_None(premises),
        r_plan_active_requisite=r_plan_active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonHeir(ReasonCore):
    _status: bool = None
    _chore: bool = None
    _rplan_active_value: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_premises = {}
        for x_premiseunit in x_reasonunit.premises.values():
            premise_x = premiseunit_shop(
                p_state=x_premiseunit.p_state,
                p_lower=x_premiseunit.p_lower,
                p_upper=x_premiseunit.p_upper,
                p_divisor=x_premiseunit.p_divisor,
            )
            x_premises[premise_x.p_state] = premise_x
        self.premises = x_premises

    def clear_status(self):
        self._status = None
        for premise in self.premises.values():
            premise.clear_status()

    def _set_premise_status(self, factheir: FactHeir):
        for premise in self.premises.values():
            premise.set_status(factheir)

    def _get_f_context(self, factheirs: dict[RopeTerm, FactHeir]) -> FactHeir:
        f_context = None
        factheirs = get_empty_dict_if_None(factheirs)
        for y_factheir in factheirs.values():
            if self.r_context == y_factheir.f_context:
                f_context = y_factheir
        return f_context

    def set_rplan_active_value(self, bool_x: bool):
        self._rplan_active_value = bool_x

    def is_r_plan_active_requisite_operational(self) -> bool:
        return (
            self._rplan_active_value is not None
            and self._rplan_active_value == self.r_plan_active_requisite
        )

    def is_any_premise_true(self) -> tuple[bool, bool]:
        any_premise_true = False
        any_chore_true = False
        for x_premiseunit in self.premises.values():
            if x_premiseunit._status:
                any_premise_true = True
                if x_premiseunit._chore:
                    any_chore_true = True
        return any_premise_true, any_chore_true

    def _set_attr_status(self, any_premise_true: bool):
        self._status = any_premise_true or self.is_r_plan_active_requisite_operational()

    def _set_attr_chore(self, any_chore_true: bool):
        self._chore = True if any_chore_true else None
        if self._status and self._chore is None:
            self._chore = False

    def set_status(self, factheirs: dict[RopeTerm, FactHeir]):
        self.clear_status()
        self._set_premise_status(self._get_f_context(factheirs))
        any_premise_true, any_chore_true = self.is_any_premise_true()
        self._set_attr_status(any_premise_true)
        self._set_attr_chore(any_chore_true)


def reasonheir_shop(
    r_context: RopeTerm,
    premises: dict[RopeTerm, PremiseUnit] = None,
    r_plan_active_requisite: bool = None,
    _status: bool = None,
    _chore: bool = None,
    _rplan_active_value: bool = None,
    knot: str = None,
):
    return ReasonHeir(
        r_context=r_context,
        premises=get_empty_dict_if_None(premises),
        r_plan_active_requisite=r_plan_active_requisite,
        _status=_status,
        _chore=_chore,
        _rplan_active_value=_rplan_active_value,
        knot=default_knot_if_None(knot),
    )


# class Reasonsshop:
def reasons_get_from_dict(reasons_dict: dict) -> dict[RopeTerm, ReasonUnit]:
    x_dict = {}
    for reason_dict in reasons_dict.values():
        x_reasonunit = reasonunit_shop(r_context=reason_dict["r_context"])
        if reason_dict.get("premises") is not None:
            x_reasonunit.premises = premises_get_from_dict(
                x_dict=reason_dict["premises"]
            )
        if reason_dict.get("r_plan_active_requisite") is not None:
            x_reasonunit.r_plan_active_requisite = reason_dict.get(
                "r_plan_active_requisite"
            )
        x_dict[x_reasonunit.r_context] = x_reasonunit
    return x_dict
