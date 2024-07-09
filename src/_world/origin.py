from contextlib import suppress as contextlib_suppress
from src._world.char import CharID
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
    if weight is None:
        weight = 1
    return OriginHold(char_id=char_id, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[CharID, OriginHold] = None

    def set_originhold(self, char_id: CharID, weight: float):
        self._links[char_id] = originhold_shop(char_id=char_id, weight=weight)

    def del_originhold(self, char_id: CharID):
        self._links.pop(char_id)

    def get_dict(self) -> dict[str, str]:
        return {"_links": self.get_originholds_dict()}

    def get_originholds_dict(self):
        x_dict = {}
        if self._links != None:
            for originhold_x in self._links.values():
                x_dict[originhold_x.char_id] = originhold_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[CharID, OriginHold] = None) -> OriginUnit:
    return OriginUnit(_links=get_empty_dict_if_none(_links))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originholds_dict = x_dict["_links"]
        for originhold_dict in originholds_dict.values():
            originunit_x.set_originhold(
                char_id=originhold_dict["char_id"], weight=originhold_dict["weight"]
            )
    return originunit_x
