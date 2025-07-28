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
    fact_context: RopeTerm = None
    fact_state: RopeTerm = None
    fact_lower: float = None
    fact_upper: float = None

    def get_dict(self) -> dict[str,]:
        x_dict = {
            "fact_context": self.fact_context,
            "fact_state": self.fact_state,
        }
        if self.fact_lower is not None:
            x_dict["fact_lower"] = self.fact_lower
        if self.fact_upper is not None:
            x_dict["fact_upper"] = self.fact_upper
        return x_dict

    def set_range_null(self):
        self.fact_lower = None
        self.fact_upper = None

    def set_attr(
        self,
        fact_state: RopeTerm = None,
        fact_lower: float = None,
        fact_upper: float = None,
    ):
        if fact_state is not None:
            self.fact_state = fact_state
        if fact_lower is not None:
            self.fact_lower = fact_lower
        if fact_upper is not None:
            self.fact_upper = fact_upper

    def set_fact_state_to_fact_context(self):
        self.set_attr(fact_state=self.fact_context)
        self.fact_lower = None
        self.fact_upper = None

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.fact_context = rebuild_rope(self.fact_context, old_rope, new_rope)
        self.fact_state = rebuild_rope(self.fact_state, old_rope, new_rope)

    def get_obj_key(self) -> RopeTerm:
        return self.fact_context

    def get_tuple(self) -> tuple[RopeTerm, RopeTerm, float, float]:
        return (self.fact_context, self.fact_state, self.fact_lower, self.fact_upper)


@dataclass
class FactUnit(FactCore):
    pass


def factunit_shop(
    fact_context: RopeTerm = None,
    fact_state: RopeTerm = None,
    fact_lower: float = None,
    fact_upper: float = None,
) -> FactUnit:
    return FactUnit(
        fact_context=fact_context,
        fact_state=fact_state,
        fact_lower=fact_lower,
        fact_upper=fact_upper,
    )


def factunits_get_from_dict(x_dict: dict) -> dict[RopeTerm, FactUnit]:
    facts = {}
    for fact_dict in x_dict.values():
        x_fact_context = fact_dict["fact_context"]
        x_fact_state = fact_dict["fact_state"]

        try:
            x_fact_lower = fact_dict["fact_lower"]
        except KeyError:
            x_fact_lower = None
        try:
            x_fact_upper = fact_dict["fact_upper"]
        except KeyError:
            x_fact_upper = None

        x_fact = factunit_shop(
            fact_context=x_fact_context,
            fact_state=x_fact_state,
            fact_lower=x_fact_lower,
            fact_upper=x_fact_upper,
        )

        facts[x_fact.fact_context] = x_fact
    return facts


def get_factunit_from_tuple(
    fact_tuple: tuple[RopeTerm, RopeTerm, float, float],
) -> FactUnit:
    return factunit_shop(fact_tuple[0], fact_tuple[1], fact_tuple[2], fact_tuple[3])


def get_dict_from_factunits(
    factunits: dict[RopeTerm, FactUnit],
) -> dict[RopeTerm, dict[str,]]:
    return {fact.fact_context: fact.get_dict() for fact in factunits.values()}


@dataclass
class FactHeir(FactCore):
    def mold(self, factunit: FactUnit):
        x_bool = self.fact_lower and factunit.fact_lower and self.fact_upper
        if (
            x_bool
            and self.fact_lower <= factunit.fact_lower
            and self.fact_upper >= factunit.fact_lower
        ):
            self.fact_lower = factunit.fact_lower

    def is_range(self):
        return self.fact_lower is not None and self.fact_upper is not None


def factheir_shop(
    fact_context: RopeTerm = None,
    fact_state: RopeTerm = None,
    fact_lower: float = None,
    fact_upper: float = None,
) -> FactHeir:
    return FactHeir(
        fact_context=fact_context,
        fact_state=fact_state,
        fact_lower=fact_lower,
        fact_upper=fact_upper,
    )


class CaseStatusFinderException(Exception):
    pass


@dataclass
class CaseStatusFinder:
    reason_lower: float  # between 0 and reason_divisor, can be more than reason_upper
    reason_upper: float  # between 0 and reason_divisor, can be less than reason_lower
    reason_divisor: float  # greater than zero
    fact_lower_full: float  # less than fact_upper
    fact_upper_full: float  # less than fact_upper

    def check_attr(self):
        if None in (
            self.reason_lower,
            self.reason_upper,
            self.reason_divisor,
            self.fact_lower_full,
            self.fact_upper_full,
        ):
            raise CaseStatusFinderException("No parameter can be None")

        if self.fact_lower_full > self.fact_upper_full:
            raise CaseStatusFinderException(
                f"{self.fact_lower_full=} cannot be greater than {self.fact_upper_full=}"
            )

        if self.reason_divisor <= 0:
            raise CaseStatusFinderException(
                f"{self.reason_divisor=} cannot be less/equal to zero"
            )

        if self.reason_lower < 0 or self.reason_lower > self.reason_divisor:
            raise CaseStatusFinderException(
                f"{self.reason_lower=} cannot be less than zero or greater than {self.reason_divisor=}"
            )

        if self.reason_upper < 0 or self.reason_upper > self.reason_divisor:
            raise CaseStatusFinderException(
                f"{self.reason_upper=} cannot be less than zero or greater than {self.reason_divisor=}"
            )

    def bo(self) -> float:
        return self.fact_lower_full % self.reason_divisor

    def bn(self) -> float:
        return self.fact_upper_full % self.reason_divisor

    def po(self) -> float:
        return self.reason_lower

    def pn(self) -> float:
        return self.reason_upper

    def pd(self) -> float:
        return self.reason_divisor

    def get_active(self) -> bool:
        if self.fact_upper_full - self.fact_lower_full > self.reason_divisor:
            return True
        elif get_range_less_than_reason_divisor_active(
            bo=self.bo(), bn=self.bn(), po=self.po(), pn=self.pn()
        ):
            return True

        return False

    def get_chore_status(self) -> bool:
        return bool(
            (
                self.get_active()
                and get_collasped_fact_range_active(
                    self.reason_lower,
                    self.reason_upper,
                    self.reason_divisor,
                    self.fact_upper_full,
                )
                is False
            )
        )


def get_range_less_than_reason_divisor_active(bo, bn, po, pn):
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
    reason_lower: float,
    reason_upper: float,
    reason_divisor: float,
    fact_upper_full: float,
) -> bool:
    x_pbsd = casestatusfinder_shop(
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        fact_lower_full=fact_upper_full,
        fact_upper_full=fact_upper_full,
    )
    return x_pbsd.get_active()


def casestatusfinder_shop(
    reason_lower: float,
    reason_upper: float,
    reason_divisor: float,
    fact_lower_full: float,
    fact_upper_full: float,
):
    x_casestatusfinder = CaseStatusFinder(
        reason_lower,
        reason_upper,
        reason_divisor,
        fact_lower_full,
        fact_upper_full,
    )
    x_casestatusfinder.check_attr()
    return x_casestatusfinder


@dataclass
class CaseUnit:
    reason_state: RopeTerm
    reason_lower: float = None
    reason_upper: float = None
    reason_divisor: int = None
    _status: bool = None
    _chore: bool = None
    knot: str = None

    def get_obj_key(self):
        return self.reason_state

    def get_dict(self) -> dict[str, str]:
        x_dict = {"reason_state": self.reason_state}
        if self.reason_lower is not None:
            x_dict["reason_lower"] = self.reason_lower
        if self.reason_upper is not None:
            x_dict["reason_upper"] = self.reason_upper

        if self.reason_divisor is not None:
            x_dict["reason_divisor"] = self.reason_divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_knot(self, new_knot: str):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.reason_state = replace_knot(
            rope=self.reason_state, old_knot=old_knot, new_knot=self.knot
        )

    def is_in_lineage(self, fact_fact_state: RopeTerm):
        return is_heir_rope(
            src=self.reason_state, heir=fact_fact_state, knot=self.knot
        ) or is_heir_rope(src=fact_fact_state, heir=self.reason_state, knot=self.knot)

    def set_status(self, x_factheir: FactHeir):
        self._status = self._get_active(factheir=x_factheir)
        self._chore = self._get_chore_status(factheir=x_factheir)

    def _get_active(self, factheir: FactHeir):
        x_status = None
        # status might be true if case is in lineage of fact
        if factheir is None:
            x_status = False
        elif self.is_in_lineage(fact_fact_state=factheir.fact_state):
            if self._is_range_or_segregate() is False:
                x_status = True
            elif self._is_range_or_segregate() and factheir.is_range() is False:
                x_status = False
            elif self._is_range_or_segregate() and factheir.is_range():
                x_status = self._get_range_segregate_status(factheir=factheir)
        elif self.is_in_lineage(fact_fact_state=factheir.fact_state) is False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return (
            self.reason_divisor is not None
            and self.reason_lower is not None
            and self.reason_upper is not None
        )

    def _is_range(self):
        return (
            self.reason_divisor is None
            and self.reason_lower is not None
            and self.reason_upper is not None
        )

    def _get_chore_status(self, factheir: FactHeir) -> bool:
        x_chore = None
        if self._status and self._is_range():
            x_chore = factheir.fact_upper > self.reason_upper
        elif self._status and self._is_segregate():
            segr_obj = casestatusfinder_shop(
                reason_lower=self.reason_lower,
                reason_upper=self.reason_upper,
                reason_divisor=self.reason_divisor,
                fact_lower_full=factheir.fact_lower,
                fact_upper_full=factheir.fact_upper,
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
        segr_obj = casestatusfinder_shop(
            reason_lower=self.reason_lower,
            reason_upper=self.reason_upper,
            reason_divisor=self.reason_divisor,
            fact_lower_full=factheir.fact_lower,
            fact_upper_full=factheir.fact_upper,
        )
        return segr_obj.get_active()

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (
                self.reason_lower <= factheir.fact_lower
                and self.reason_upper > factheir.fact_lower
            )
            or (
                self.reason_lower <= factheir.fact_upper
                and self.reason_upper > factheir.fact_upper
            )
            or (
                self.reason_lower >= factheir.fact_lower
                and self.reason_upper < factheir.fact_upper
            )
        )

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.reason_state = rebuild_rope(self.reason_state, old_rope, new_rope)


# class casesshop:
def caseunit_shop(
    reason_state: RopeTerm,
    reason_lower: float = None,
    reason_upper: float = None,
    reason_divisor: float = None,
    knot: str = None,
) -> CaseUnit:
    return CaseUnit(
        reason_state=reason_state,
        reason_lower=reason_lower,
        reason_upper=reason_upper,
        reason_divisor=reason_divisor,
        knot=default_knot_if_None(knot),
    )


def cases_get_from_dict(x_dict: dict) -> dict[str, CaseUnit]:
    cases = {}
    for case_dict in x_dict.values():
        try:
            x_reason_lower = case_dict["reason_lower"]
        except KeyError:
            x_reason_lower = None
        try:
            x_reason_upper = case_dict["reason_upper"]
        except KeyError:
            x_reason_upper = None
        try:
            x_reason_divisor = case_dict["reason_divisor"]
        except KeyError:
            x_reason_divisor = None

        case_x = caseunit_shop(
            reason_state=case_dict["reason_state"],
            reason_lower=x_reason_lower,
            reason_upper=x_reason_upper,
            reason_divisor=x_reason_divisor,
        )
        cases[case_x.reason_state] = case_x
    return cases


@dataclass
class ReasonCore:
    reason_context: RopeTerm
    cases: dict[RopeTerm, CaseUnit]
    reason_active_requisite: bool = None
    knot: str = None

    def set_knot(self, new_knot: str):
        old_knot = copy_deepcopy(self.knot)
        self.knot = new_knot
        self.reason_context = replace_knot(self.reason_context, old_knot, new_knot)

        new_cases = {}
        for case_rope, case_obj in self.cases.items():
            new_case_rope = replace_knot(
                rope=case_rope,
                old_knot=old_knot,
                new_knot=self.knot,
            )
            case_obj.set_knot(self.knot)
            new_cases[new_case_rope] = case_obj
        self.cases = new_cases

    def get_obj_key(self):
        return self.reason_context

    def get_cases_count(self):
        return sum(1 for _ in self.cases.values())

    def set_case(
        self,
        case: RopeTerm,
        reason_lower: float = None,
        reason_upper: float = None,
        reason_divisor: int = None,
    ):
        self.cases[case] = caseunit_shop(
            reason_state=case,
            reason_lower=reason_lower,
            reason_upper=reason_upper,
            reason_divisor=reason_divisor,
            knot=self.knot,
        )

    def case_exists(self, reason_state: RopeTerm) -> bool:
        return self.cases.get(reason_state) != None

    def get_case(self, case: RopeTerm) -> CaseUnit:
        return self.cases.get(case)

    def del_case(self, case: RopeTerm):
        try:
            self.cases.pop(case)
        except KeyError as e:
            raise InvalidReasonException(f"Reason unable to delete case {e}") from e

    def find_replace_rope(self, old_rope: RopeTerm, new_rope: RopeTerm):
        self.reason_context = rebuild_rope(self.reason_context, old_rope, new_rope)
        self.cases = find_replace_rope_key_dict(
            dict_x=self.cases, old_rope=old_rope, new_rope=new_rope
        )


def reasoncore_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    reason_active_requisite: bool = None,
    knot: str = None,
):
    return ReasonCore(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        reason_active_requisite=reason_active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def get_dict(self) -> dict[str, str]:
        cases_dict = {
            case_rope: case.get_dict() for case_rope, case in self.cases.items()
        }
        x_dict = {"reason_context": self.reason_context}
        if cases_dict != {}:
            x_dict["cases"] = cases_dict
        if self.reason_active_requisite is not None:
            x_dict["reason_active_requisite"] = self.reason_active_requisite
        return x_dict


def reasonunit_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    reason_active_requisite: bool = None,
    knot: str = None,
):
    return ReasonUnit(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        reason_active_requisite=reason_active_requisite,
        knot=default_knot_if_None(knot),
    )


@dataclass
class ReasonHeir(ReasonCore):
    _status: bool = None
    _chore: bool = None
    _rplan_active_value: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_cases = {}
        for x_caseunit in x_reasonunit.cases.values():
            case_x = caseunit_shop(
                reason_state=x_caseunit.reason_state,
                reason_lower=x_caseunit.reason_lower,
                reason_upper=x_caseunit.reason_upper,
                reason_divisor=x_caseunit.reason_divisor,
            )
            x_cases[case_x.reason_state] = case_x
        self.cases = x_cases

    def clear_status(self):
        self._status = None
        for case in self.cases.values():
            case.clear_status()

    def _set_case_status(self, factheir: FactHeir):
        for case in self.cases.values():
            case.set_status(factheir)

    def _get_fact_context(self, factheirs: dict[RopeTerm, FactHeir]) -> FactHeir:
        fact_context = None
        factheirs = get_empty_dict_if_None(factheirs)
        for y_factheir in factheirs.values():
            if self.reason_context == y_factheir.fact_context:
                fact_context = y_factheir
        return fact_context

    def set_rplan_active_value(self, bool_x: bool):
        self._rplan_active_value = bool_x

    def is_reason_active_requisite_operational(self) -> bool:
        return (
            self._rplan_active_value is not None
            and self._rplan_active_value == self.reason_active_requisite
        )

    def is_any_case_true(self) -> tuple[bool, bool]:
        any_case_true = False
        any_chore_true = False
        for x_caseunit in self.cases.values():
            if x_caseunit._status:
                any_case_true = True
                if x_caseunit._chore:
                    any_chore_true = True
        return any_case_true, any_chore_true

    def _set_attr_status(self, any_case_true: bool):
        self._status = any_case_true or self.is_reason_active_requisite_operational()

    def _set_attr_chore(self, any_chore_true: bool):
        self._chore = True if any_chore_true else None
        if self._status and self._chore is None:
            self._chore = False

    def set_status(self, factheirs: dict[RopeTerm, FactHeir]):
        self.clear_status()
        self._set_case_status(self._get_fact_context(factheirs))
        any_case_true, any_chore_true = self.is_any_case_true()
        self._set_attr_status(any_case_true)
        self._set_attr_chore(any_chore_true)


def reasonheir_shop(
    reason_context: RopeTerm,
    cases: dict[RopeTerm, CaseUnit] = None,
    reason_active_requisite: bool = None,
    _status: bool = None,
    _chore: bool = None,
    _rplan_active_value: bool = None,
    knot: str = None,
):
    return ReasonHeir(
        reason_context=reason_context,
        cases=get_empty_dict_if_None(cases),
        reason_active_requisite=reason_active_requisite,
        _status=_status,
        _chore=_chore,
        _rplan_active_value=_rplan_active_value,
        knot=default_knot_if_None(knot),
    )


# class Reasonsshop:
def reasons_get_from_dict(reasons_dict: dict) -> dict[RopeTerm, ReasonUnit]:
    x_dict = {}
    for reason_dict in reasons_dict.values():
        x_reasonunit = reasonunit_shop(reason_context=reason_dict["reason_context"])
        if reason_dict.get("cases") is not None:
            x_reasonunit.cases = cases_get_from_dict(x_dict=reason_dict["cases"])
        if reason_dict.get("reason_active_requisite") is not None:
            x_reasonunit.reason_active_requisite = reason_dict.get(
                "reason_active_requisite"
            )
        x_dict[x_reasonunit.reason_context] = x_reasonunit
    return x_dict
