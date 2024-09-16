from contextlib import suppress as contextlib_suppress
from src.s2_bud.acct import AcctID
from src.s0_instrument.python_tool import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginHold:
    acct_id: AcctID
    importance: float

    def get_dict(self) -> dict[str, str]:
        return {
            "acct_id": self.acct_id,
            "importance": self.importance,
        }


def originhold_shop(acct_id: AcctID, importance: float = None) -> OriginHold:
    importance = 1 if importance is None else importance
    return OriginHold(acct_id=acct_id, importance=importance)


@dataclass
class OriginUnit:
    _originholds: dict[AcctID, OriginHold] = None

    def set_originhold(self, acct_id: AcctID, importance: float):
        self._originholds[acct_id] = originhold_shop(
            acct_id=acct_id, importance=importance
        )

    def del_originhold(self, acct_id: AcctID):
        self._originholds.pop(acct_id)

    def get_dict(self) -> dict[str, str]:
        return {"_originholds": self.get_originholds_dict()}

    def get_originholds_dict(self):
        x_dict = {}
        if self._originholds is not None:
            for originhold_x in self._originholds.values():
                x_dict[originhold_x.acct_id] = originhold_x.get_dict()
        return x_dict


def originunit_shop(_originholds: dict[AcctID, OriginHold] = None) -> OriginUnit:
    return OriginUnit(_originholds=get_empty_dict_if_none(_originholds))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originholds_dict = x_dict["_originholds"]
        for originhold_dict in originholds_dict.values():
            originunit_x.set_originhold(
                acct_id=originhold_dict["acct_id"],
                importance=originhold_dict["importance"],
            )
    return originunit_x
