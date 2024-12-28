from contextlib import suppress as contextlib_suppress
from src.f02_bud.acct import AcctName
from src.f00_instrument.dict_toolbox import get_empty_dict_if_None
from dataclasses import dataclass


@dataclass
class OriginHold:
    acct_name: AcctName
    importance: float

    def get_dict(self) -> dict[str, str]:
        return {
            "acct_name": self.acct_name,
            "importance": self.importance,
        }


def originhold_shop(acct_name: AcctName, importance: float = None) -> OriginHold:
    importance = 1 if importance is None else importance
    return OriginHold(acct_name=acct_name, importance=importance)


@dataclass
class OriginUnit:
    _originholds: dict[AcctName, OriginHold] = None

    def set_originhold(self, acct_name: AcctName, importance: float):
        self._originholds[acct_name] = originhold_shop(
            acct_name=acct_name, importance=importance
        )

    def del_originhold(self, acct_name: AcctName):
        self._originholds.pop(acct_name)

    def get_dict(self) -> dict[str, str]:
        return {"_originholds": self.get_originholds_dict()}

    def get_originholds_dict(self):
        x_dict = {}
        if self._originholds is not None:
            for originhold_x in self._originholds.values():
                x_dict[originhold_x.acct_name] = originhold_x.get_dict()
        return x_dict


def originunit_shop(_originholds: dict[AcctName, OriginHold] = None) -> OriginUnit:
    return OriginUnit(_originholds=get_empty_dict_if_None(_originholds))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originholds_dict = x_dict["_originholds"]
        for originhold_dict in originholds_dict.values():
            originunit_x.set_originhold(
                acct_name=originhold_dict["acct_name"],
                importance=originhold_dict["importance"],
            )
    return originunit_x
