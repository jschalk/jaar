from dataclasses import dataclass
from src._prime.road import (
    RoadUnit,
    change_road,
    find_replace_road_key_dict,
    replace_road_delimiter,
    is_heir_road,
    default_road_delimiter_if_none,
)
from src.tools.python import get_empty_dict_if_none
from copy import deepcopy as copy_deepcopy


class InvalidRequiredException(Exception):
    pass


@dataclass
class AcptFactCore:
    base: RoadUnit
    pick: RoadUnit
    open: float = None
    nigh: float = None

    def get_dict(self):
        x_dict = {
            "base": self.base,
            "pick": self.pick,
        }
        if self.open != None:
            x_dict["open"] = self.open
        if self.nigh != None:
            x_dict["nigh"] = self.nigh
        return x_dict

    def set_range_null(self):
        self.open = None
        self.nigh = None

    def set_attr(self, pick: RoadUnit = None, open: float = None, nigh: float = None):
        if pick != None:
            self.pick = pick
        if open != None:
            self.open = open
        if nigh != None:
            self.nigh = nigh

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = change_road(self.base, old_road, new_road)
        self.pick = change_road(self.pick, old_road, new_road)

    def get_obj_key(self):
        return self.base

    def meld(self, other_acptfactcore, same_required: bool = False):
        if same_required and other_acptfactcore.base != self.base:
            raise InvalidRequiredException(
                f"Meld fail: base={other_acptfactcore.base} is different {self.base=}"
            )
        elif same_required and other_acptfactcore.pick != self.pick:
            raise InvalidRequiredException(
                f"Meld fail: pick={other_acptfactcore.pick} is different {self.pick=}"
            )
        elif same_required and other_acptfactcore.open != self.open:
            raise InvalidRequiredException(
                f"Meld fail: base={other_acptfactcore.base} open={other_acptfactcore.open} is different {self.open=}"
            )
        elif same_required and other_acptfactcore.nigh != self.nigh:
            raise InvalidRequiredException(
                f"Meld fail: base={other_acptfactcore.base} nigh={other_acptfactcore.nigh} is different {self.nigh=}"
            )
        else:
            self.base = other_acptfactcore.base
            self.pick = other_acptfactcore.pick
            self.open = other_acptfactcore.open
            self.nigh = other_acptfactcore.nigh
        return self


@dataclass
class AcptFactUnit(AcptFactCore):
    pass


# class AcptFactUnitsshop:
def acptfactunits_get_from_dict(x_dict: dict):
    acptfacts = {}
    for acptfact_dict in x_dict.values():
        x_base = acptfact_dict["base"]
        x_pick = acptfact_dict["pick"]

        try:
            x_open = acptfact_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = acptfact_dict["nigh"]
        except KeyError:
            x_nigh = None

        x_acptfact = acptfactunit_shop(
            base=x_base,
            pick=x_pick,
            open=x_open,
            nigh=x_nigh,
        )

        acptfacts[x_acptfact.base] = x_acptfact
    return acptfacts


def acptfactunit_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> AcptFactUnit:
    return AcptFactUnit(base=base, pick=pick, open=open, nigh=nigh)


@dataclass
class AcptFactHeir(AcptFactCore):
    def transform(self, acptfactunit: AcptFactUnit):
        if (
            (self.open != None and acptfactunit.open != None and self.nigh != None)
            and self.open <= acptfactunit.open
            and self.nigh >= acptfactunit.open
        ):
            self.open = acptfactunit.open

    def is_range(self):
        return self.open != None and self.nigh != None


def acptfactheir_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> AcptFactHeir:
    return AcptFactHeir(base=base, pick=pick, open=open, nigh=nigh)


@dataclass
class SuffFactStatusFinder:
    acptfact_open: float
    acptfact_nigh: float
    sufffact_open: float
    sufffact_nigh: float
    sufffact_divisor: int
    _active_status: bool = None
    _task_status: bool = None
    _in_range_count: int = None

    def __post_init__(self):
        self._active_status = False
        self._task_status = False

        self._acptfact_range_len = None
        if self.acptfact_nigh >= self.acptfact_open:
            self._acptfact_range_len = self.acptfact_nigh - self.acptfact_open

        # create transformed sufffact_open and sufffact_nigh that can be compared to acptfacts
        open_multipler = int(self.acptfact_open / self.sufffact_divisor)
        nigh_multipler = int(self.acptfact_nigh / self.sufffact_divisor)
        self.sufffact_open_trans = (
            self.sufffact_divisor * open_multipler
        ) + self.sufffact_open
        self.sufffact_nigh_trans = (
            self.sufffact_divisor * nigh_multipler
        ) + self.sufffact_nigh

        if (
            self.sufffact_nigh_trans_in_acptfact_range()
            or self.sufffact_open_trans_equal_acptfact_open()
            # or self.acptfact_range_len_is_greater_than_divisor()
            or self.sufffact_x_range_inside_acptfact_range()
            or self.acptfact_range_inside_sufffact_x_range()
            or self.sufffact_open_trans_in_acptfact_range()
        ):
            self._active_status = True

            if self.acptfact_nigh_mod_div_outside_need_range():
                self._task_status = True

        # no features use this
        self._in_range_count = None

    def acptfact_range_len_is_greater_than_divisor(self) -> bool:
        return self._acptfact_range_len >= self.sufffact_divisor

    def get_acptfact_open_mod_div(self):
        return self.acptfact_open % self.sufffact_divisor

    def get_acptfact_nigh_mod_div(self):
        return self.acptfact_nigh % self.sufffact_divisor

    def acptfact_nigh_mod_div_outside_need_range(self) -> bool:
        return (
            self.get_acptfact_nigh_mod_div() < self.sufffact_open
            or self.get_acptfact_nigh_mod_div() >= self.sufffact_nigh
        )

    def sufffact_nigh_trans_in_acptfact_range(self) -> bool:
        return (
            self.sufffact_open_trans < self.acptfact_open
            and self.sufffact_nigh_trans >= self.acptfact_open
            and self.sufffact_nigh_trans < self.acptfact_nigh
        )

    def sufffact_open_trans_equal_acptfact_open(self) -> bool:
        return self.sufffact_open_trans == self.acptfact_open

    def sufffact_x_range_inside_acptfact_range(self) -> bool:
        return (
            self.sufffact_open_trans > self.acptfact_open
            and self.sufffact_nigh_trans < self.acptfact_nigh
        )

    def acptfact_range_inside_sufffact_x_range(self) -> bool:
        return (
            self.sufffact_open_trans <= self.acptfact_open
            and self.sufffact_nigh_trans > self.acptfact_nigh
        )

    def sufffact_open_trans_in_acptfact_range(self) -> bool:
        return (
            self.sufffact_open_trans > self.acptfact_open
            and self.sufffact_open_trans < self.acptfact_nigh
            and self.sufffact_nigh_trans > self.acptfact_nigh
        )


@dataclass
class SuffFactUnit:
    need: RoadUnit
    open: float = None
    nigh: float = None
    divisor: int = None
    _status: bool = None
    _task: bool = None
    delimiter: str = None

    def get_obj_key(self):
        return self.need

    def get_dict(self):
        x_dict = {"need": self.need}
        if self.open != None:
            x_dict["open"] = self.open
        if self.nigh != None:
            x_dict["nigh"] = self.nigh

        if self.divisor != None:
            x_dict["divisor"] = self.divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_delimiter(self, new_delimiter: str):
        old_delimiter = copy_deepcopy(self.delimiter)
        self.delimiter = new_delimiter
        self.need = replace_road_delimiter(
            road=self.need, old_delimiter=old_delimiter, new_delimiter=self.delimiter
        )

    def is_in_lineage(self, acptfact_pick: RoadUnit):
        return is_heir_road(
            src=self.need, heir=acptfact_pick, delimiter=self.delimiter
        ) or is_heir_road(src=acptfact_pick, heir=self.need, delimiter=self.delimiter)

    def set_status(self, acptfactheir: AcptFactHeir):
        self._status = self._get_active_status(acptfactheir=acptfactheir)
        self._task = self._get_task_status(acptfactheir=acptfactheir)

    def _get_active_status(self, acptfactheir: AcptFactHeir):
        x_status = None
        # status might be true if sufffact is in lineage of acptfact
        if acptfactheir is None:
            x_status = False
        elif self.is_in_lineage(acptfact_pick=acptfactheir.pick) == True:
            if self._is_range_or_segregate() == False:
                x_status = True
            elif self._is_range_or_segregate() and acptfactheir.is_range() == False:
                x_status = False
            elif self._is_range_or_segregate() and acptfactheir.is_range() == True:
                x_status = self._get_range_segregate_status(acptfactheir=acptfactheir)
        elif self.is_in_lineage(acptfact_pick=acptfactheir.pick) == False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return self.divisor != None and self.open != None and self.nigh != None

    def _is_range(self):
        return self.divisor is None and self.open != None and self.nigh != None

    def _get_task_status(self, acptfactheir: AcptFactHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = acptfactheir.nigh > self.nigh
        elif self._status and self._is_segregate():
            segr_obj = SuffFactStatusFinder(
                acptfact_open=acptfactheir.open,
                acptfact_nigh=acptfactheir.nigh,
                sufffact_open=self.open,
                sufffact_nigh=self.nigh,
                sufffact_divisor=self.divisor,
            )
            x_task = segr_obj._task_status
        elif self._status in [True, False]:
            x_task = False

        return x_task

    def _get_range_segregate_status(self, acptfactheir: AcptFactHeir) -> bool:
        x_status = None
        if self._is_range():
            x_status = self._get_range_status(acptfactheir=acptfactheir)
        elif self._is_segregate():
            x_status = self._get_segregate_status(acptfactheir=acptfactheir)

        return x_status

    def _get_segregate_status(self, acptfactheir: AcptFactHeir) -> bool:
        segr_obj = SuffFactStatusFinder(
            acptfact_open=acptfactheir.open,
            acptfact_nigh=acptfactheir.nigh,
            sufffact_open=self.open,
            sufffact_nigh=self.nigh,
            sufffact_divisor=self.divisor,
        )
        return segr_obj._active_status

    def _get_range_status(self, acptfactheir: AcptFactHeir) -> bool:
        return (
            (self.open <= acptfactheir.open and self.nigh > acptfactheir.open)
            or (self.open <= acptfactheir.nigh and self.nigh > acptfactheir.nigh)
            or (self.open >= acptfactheir.open and self.nigh < acptfactheir.nigh)
        )

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.need = change_road(self.need, old_road, new_road)

    def meld(self, other_sufffact):
        if other_sufffact.need != self.need:
            raise InvalidRequiredException(
                f"Meld fail: need={other_sufffact.need} is different {self.need=}"
            )
        elif other_sufffact.open != self.open:
            raise InvalidRequiredException(
                f"Meld fail: need={other_sufffact.need} open={other_sufffact.open} is different {self.open=}"
            )
        elif other_sufffact.nigh != self.nigh:
            raise InvalidRequiredException(
                f"Meld fail: need={other_sufffact.need} nigh={other_sufffact.nigh} is different {self.nigh=}"
            )
        elif other_sufffact.divisor != self.divisor:
            raise InvalidRequiredException(
                f"Meld fail: need={other_sufffact.need} divisor={other_sufffact.divisor} is different {self.divisor=}"
            )

        return self


# class sufffactsshop:
def sufffactunit_shop(
    need: RoadUnit,
    open: float = None,
    nigh: float = None,
    divisor: float = None,
    delimiter: str = None,
) -> SuffFactUnit:
    return SuffFactUnit(
        need=need,
        open=open,
        nigh=nigh,
        divisor=divisor,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


def sufffacts_get_from_dict(x_dict: dict) -> dict[str:SuffFactUnit]:
    sufffacts = {}
    for sufffact_dict in x_dict.values():
        try:
            x_open = sufffact_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = sufffact_dict["nigh"]
        except KeyError:
            x_nigh = None
        try:
            x_divisor = sufffact_dict["divisor"]
        except KeyError:
            x_divisor = None

        sufffact_x = sufffactunit_shop(
            need=sufffact_dict["need"],
            open=x_open,
            nigh=x_nigh,
            divisor=x_divisor,
        )
        sufffacts[sufffact_x.need] = sufffact_x
    return sufffacts


@dataclass
class RequiredCore:
    base: RoadUnit
    sufffacts: dict[RoadUnit:SuffFactUnit]
    # None: ignore,
    # True: base idea._active_status required be True,
    # False: base idea._active_status required be False
    suff_idea_active_status: bool = None
    delimiter: str = None

    def set_delimiter(self, new_delimiter: str):
        old_delimiter = copy_deepcopy(self.delimiter)
        self.delimiter = new_delimiter
        self.base = replace_road_delimiter(self.base, old_delimiter, new_delimiter)

        new_sufffacts = {}
        for sufffact_road, sufffact_obj in self.sufffacts.items():
            new_sufffact_road = replace_road_delimiter(
                road=sufffact_road,
                old_delimiter=old_delimiter,
                new_delimiter=self.delimiter,
            )
            sufffact_obj.set_delimiter(self.delimiter)
            new_sufffacts[new_sufffact_road] = sufffact_obj
        self.sufffacts = new_sufffacts

    def get_obj_key(self):
        return self.base

    def get_sufffacts_count(self):
        return sum(1 for _ in self.sufffacts.values())

    def set_sufffact(
        self,
        sufffact: RoadUnit,
        open: float = None,
        nigh: float = None,
        divisor: int = None,
    ):
        self.sufffacts[sufffact] = sufffactunit_shop(
            need=sufffact,
            open=open,
            nigh=nigh,
            divisor=divisor,
            delimiter=self.delimiter,
        )

    def del_sufffact(self, sufffact: RoadUnit):
        try:
            self.sufffacts.pop(sufffact)
        except KeyError as e:
            raise InvalidRequiredException(
                f"Required unable to delete sufffact {e}"
            ) from e

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = change_road(self.base, old_road, new_road)
        self.sufffacts = find_replace_road_key_dict(
            dict_x=self.sufffacts, old_road=old_road, new_road=new_road
        )

    def meld(self, other_required):
        for sufffact_x in other_required.sufffacts.values():
            if self.sufffacts.get(sufffact_x.need) is None:
                self.sufffacts[sufffact_x.need] = sufffact_x
            else:
                self.sufffacts.get(sufffact_x.need).meld(sufffact_x)
        if other_required.base != self.base:
            raise InvalidRequiredException(
                f"Meld fail: required={other_required.base} is different {self.base=}"
            )

        # TODO get rid of this return self
        return self


def requiredcore_shop(
    base: RoadUnit,
    sufffacts: dict[RoadUnit:SuffFactUnit] = None,
    suff_idea_active_status: bool = None,
    delimiter: str = None,
):
    return RequiredCore(
        base=base,
        sufffacts=get_empty_dict_if_none(sufffacts),
        suff_idea_active_status=suff_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


@dataclass
class RequiredUnit(RequiredCore):
    def get_dict(self):
        sufffacts_dict = {
            sufffact_road: sufffact.get_dict()
            for sufffact_road, sufffact in self.sufffacts.items()
        }
        return {
            "base": self.base,
            "sufffacts": sufffacts_dict,
        }


def requiredunit_shop(
    base: RoadUnit,
    sufffacts: dict[RoadUnit:SuffFactUnit] = None,
    suff_idea_active_status: bool = None,
    delimiter: str = None,
):
    return RequiredUnit(
        base=base,
        sufffacts=get_empty_dict_if_none(sufffacts),
        suff_idea_active_status=suff_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


@dataclass
class RequiredHeir(RequiredCore):
    _status: bool = None
    _task: bool = None
    _curr_idea_active_status: bool = None

    def inherit_from_requiredheir(self, x_requiredunit: RequiredUnit):
        x_sufffacts = {}
        for w in x_requiredunit.sufffacts.values():
            sufffact_x = sufffactunit_shop(
                need=w.need,
                open=w.open,
                nigh=w.nigh,
                divisor=w.divisor,
            )
            x_sufffacts[sufffact_x.need] = sufffact_x
        self.sufffacts = x_sufffacts

    def clear_status(self):
        self._status = None
        for sufffact in self.sufffacts.values():
            sufffact.clear_status()

    def _set_sufffact_status(self, acptfactheir: AcptFactHeir):
        for sufffact in self.sufffacts.values():
            sufffact.set_status(acptfactheir=acptfactheir)

    def _get_base_acptfact(self, acptfacts: dict[RoadUnit:AcptFactHeir]):
        x_acptfact = None
        if acptfacts is None:
            acptfacts = {}

        for acptfact in acptfacts.values():
            if self.base == acptfact.base:
                x_acptfact = acptfact

        return x_acptfact

    def set_curr_idea_active_status(self, bool_x: bool):
        self._curr_idea_active_status = bool_x

    def set_status(self, acptfacts: dict[RoadUnit:AcptFactHeir]):
        self.clear_status()
        acptfact = self._get_base_acptfact(acptfacts=acptfacts)
        self._set_sufffact_status(acptfactheir=acptfact)

        # if a single one is true return true (OR operator)
        is_single_sufffact_true = False
        is_single_task_true = False
        for sufffact in self.sufffacts.values():
            if sufffact._status == True:
                is_single_sufffact_true = True
                if sufffact._task == True:
                    is_single_task_true = True

        self._status = bool(
            is_single_sufffact_true
            or (
                self._curr_idea_active_status != None
                and self._curr_idea_active_status == self.suff_idea_active_status
            )
        )
        self._task = True if is_single_task_true else None
        if self._status and self._task is None:
            self._task = False


def requiredheir_shop(
    base: RoadUnit,
    sufffacts: dict[RoadUnit:SuffFactUnit] = None,
    suff_idea_active_status: bool = None,
    _status: bool = None,
    _task: bool = None,
    _curr_idea_active_status: bool = None,
    delimiter: str = None,
):
    return RequiredHeir(
        base=base,
        sufffacts=get_empty_dict_if_none(sufffacts),
        suff_idea_active_status=suff_idea_active_status,
        _status=_status,
        _task=_task,
        _curr_idea_active_status=_curr_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


# class Requiredsshop:
def requireds_get_from_dict(requireds_dict: dict) -> dict[RequiredUnit]:
    requireds = {}
    for required_dict in requireds_dict.values():
        x_required = requiredunit_shop(
            base=required_dict["base"],
            sufffacts=sufffacts_get_from_dict(x_dict=required_dict["sufffacts"]),
        )
        requireds[x_required.base] = x_required
    return requireds
