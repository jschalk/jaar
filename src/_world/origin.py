from contextlib import suppress as contextlib_suppress
from src._world.char import CharID
from src._instrument.python import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginLink:
    char_id: CharID
    weight: float

    def get_dict(self) -> dict[str, str]:
        return {
            "char_id": self.char_id,
            "weight": self.weight,
        }


def originlink_shop(char_id: CharID, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(char_id=char_id, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[CharID, OriginLink] = None

    def set_originlink(self, char_id: CharID, weight: float):
        self._links[char_id] = originlink_shop(char_id=char_id, weight=weight)

    def del_originlink(self, char_id: CharID):
        self._links.pop(char_id)

    def get_dict(self) -> dict[str, str]:
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.char_id] = originlink_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[CharID, OriginLink] = None) -> OriginUnit:
    return OriginUnit(_links=get_empty_dict_if_none(_links))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originlinks_dict = x_dict["_links"]
        for originlink_dict in originlinks_dict.values():
            originunit_x.set_originlink(
                char_id=originlink_dict["char_id"], weight=originlink_dict["weight"]
            )
    return originunit_x
