from src.f00_instrument.dict_toolbox import get_empty_set_if_none
from dataclasses import dataclass


@dataclass
class PidginRow:
    face_id: str
    event_id: int
    otx_wall: str
    inx_wall: str
    unknown_word: str


@dataclass
class PidginCore:
    face_id: set[str] = None
    event_id: set[int] = None
    otx_walls: set[str] = None
    inx_walls: set[str] = None
    unknown_words: set[str] = None

    def add_otx_wall(self, otx_wall: str):
        if None in self.otx_walls and otx_wall != None:
            self.otx_walls.remove(None)

        if otx_wall is None and self.otx_walls == set():
            self.otx_walls.add(otx_wall)
        elif otx_wall != None:
            self.otx_walls.add(otx_wall)

    def add_inx_wall(self, inx_wall: str):
        if None in self.inx_walls and inx_wall != None:
            self.inx_walls.remove(None)

        if inx_wall is None and self.inx_walls == set():
            self.inx_walls.add(inx_wall)
        elif inx_wall != None:
            self.inx_walls.add(inx_wall)

    def add_unknown_word(self, unknown_word: str):
        if None in self.unknown_words and unknown_word != None:
            self.unknown_words.remove(None)

        if unknown_word is None and self.unknown_words == set():
            self.unknown_words.add(unknown_word)
        elif unknown_word != None:
            self.unknown_words.add(unknown_word)

    def is_valid(self) -> bool:
        return (
            len(self.otx_walls) == 1
            and len(self.inx_walls) == 1
            and len(self.unknown_words) == 1
        )

    def get_valid_pidginrow(self) -> PidginRow:
        if self.is_valid():
            return PidginRow(
                face_id=self.face_id,
                event_id=self.event_id,
                otx_wall=min(self.otx_walls),
                inx_wall=min(self.inx_walls),
                unknown_word=min(self.unknown_words),
            )


def pidgincore_shop(
    face_id: str,
    event_id: int,
    otx_walls: set[str] = None,
    inx_walls: set[str] = None,
    unknown_words: set[str] = None,
) -> PidginCore:
    return PidginCore(
        face_id,
        event_id,
        get_empty_set_if_none(otx_walls),
        get_empty_set_if_none(inx_walls),
        get_empty_set_if_none(unknown_words),
    )


def create_pidgincore(
    face_id: str, event_id: int, otx_wall: str, inx_wall: str, unknown_word: str
) -> PidginCore:
    x_pidgincore = pidgincore_shop(face_id, event_id)
    x_pidgincore.add_otx_wall(otx_wall)
    x_pidgincore.add_inx_wall(inx_wall)
    x_pidgincore.add_unknown_word(unknown_word)
    return x_pidgincore


@dataclass
class PidginAggBook:
    objs: dict[tuple[str, int], PidginCore] = None

    def _overwrite_pidgincore(self, x_pidgincore: PidginCore):
        x_key = (x_pidgincore.face_id, x_pidgincore.event_id)
        self.objs[x_key] = x_pidgincore

    def pidgincore_exists(self, x_key: tuple[str, int]):
        return self.objs.get(x_key) != None

    def get_pidgincore(self, x_key: tuple[str, int]) -> PidginCore:
        return self.objs.get(x_key)

    def eval_pidginrow(self, x_pidginrow: PidginRow):
        pidgincore_key = (x_pidginrow.face_id, x_pidginrow.event_id)
        if self.pidgincore_exists(pidgincore_key):
            pidgincore_val = self.get_pidgincore(pidgincore_key)
            pidgincore_val.add_otx_wall(x_pidginrow.otx_wall)
            pidgincore_val.add_inx_wall(x_pidginrow.inx_wall)
            pidgincore_val.add_unknown_word(x_pidginrow.unknown_word)
        else:
            pidgincore_val = create_pidgincore(
                face_id=x_pidginrow.face_id,
                event_id=x_pidginrow.event_id,
                otx_wall=x_pidginrow.otx_wall,
                inx_wall=x_pidginrow.inx_wall,
                unknown_word=x_pidginrow.unknown_word,
            )
            self.objs[pidgincore_key] = pidgincore_val


def pidginaggbook_shop() -> PidginAggBook:
    return PidginAggBook(objs={})
