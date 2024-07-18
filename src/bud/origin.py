from contextlib import suppress as contextlib_suppress
from src.bud.char import CharID
from src._instrument.python import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginHold:
    char_id: CharID
    weight: float

    def get_dict(self) -> dict[str, str]:
        return {
            "char_id": self.char_id,
            "weight": self.weight,
        }


def originhold_shop(char_id: CharID, weight: float = None) -> OriginHold:
    weight = 1 if weight is None else weight
    return OriginHold(char_id=char_id, weight=weight)


@dataclass
class OriginUnit:
    _originholds: dict[CharID, OriginHold] = None

    def set_originhold(self, char_id: CharID, weight: float):
        self._originholds[char_id] = originhold_shop(char_id=char_id, weight=weight)

    def del_originhold(self, char_id: CharID):
        self._originholds.pop(char_id)

    def get_dict(self) -> dict[str, str]:
        return {"_originholds": self.get_originholds_dict()}

    def get_originholds_dict(self):
        x_dict = {}
        if self._originholds is not None:
            for originhold_x in self._originholds.values():
                x_dict[originhold_x.char_id] = originhold_x.get_dict()
        return x_dict


def originunit_shop(_originholds: dict[CharID, OriginHold] = None) -> OriginUnit:
    return OriginUnit(_originholds=get_empty_dict_if_none(_originholds))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originholds_dict = x_dict["_originholds"]
        for originhold_dict in originholds_dict.values():
            originunit_x.set_originhold(
                char_id=originhold_dict["char_id"], weight=originhold_dict["weight"]
            )
    return originunit_x
