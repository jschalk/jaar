from src.f00_instrument.dict_toolbox import get_empty_set_if_none
from dataclasses import dataclass


@dataclass
class PidginHeartRow:
    face_id: str
    event_id: int
    otx_wall: str
    inx_wall: str
    unknown_word: str


@dataclass
class PidginHeartCore:
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

    def get_valid_pidginheartrow(self) -> PidginHeartRow:
        if self.is_valid():
            return PidginHeartRow(
                face_id=self.face_id,
                event_id=self.event_id,
                otx_wall=min(self.otx_walls),
                inx_wall=min(self.inx_walls),
                unknown_word=min(self.unknown_words),
            )


def pidginheartcore_shop(
    face_id: str,
    event_id: int,
    otx_walls: set[str] = None,
    inx_walls: set[str] = None,
    unknown_words: set[str] = None,
) -> PidginHeartCore:
    return PidginHeartCore(
        face_id,
        event_id,
        get_empty_set_if_none(otx_walls),
        get_empty_set_if_none(inx_walls),
        get_empty_set_if_none(unknown_words),
    )


def create_pidginheartcore(
    face_id: str, event_id: int, otx_wall: str, inx_wall: str, unknown_word: str
) -> PidginHeartCore:
    x_pidginheartcore = pidginheartcore_shop(face_id, event_id)
    x_pidginheartcore.add_otx_wall(otx_wall)
    x_pidginheartcore.add_inx_wall(inx_wall)
    x_pidginheartcore.add_unknown_word(unknown_word)
    return x_pidginheartcore


@dataclass
class PidginHeartBook:
    pidginheartcores: dict[tuple[str, int], PidginHeartCore] = None

    def _overwrite_pidginheartcore(self, x_pidginheartcore: PidginHeartCore):
        x_key = (x_pidginheartcore.face_id, x_pidginheartcore.event_id)
        self.pidginheartcores[x_key] = x_pidginheartcore

    def pidginheartcore_exists(self, x_key: tuple[str, int]):
        return self.pidginheartcores.get(x_key) != None

    def get_pidginheartcore(self, x_key: tuple[str, int]) -> PidginHeartCore:
        return self.pidginheartcores.get(x_key)

    def eval_pidginheartrow(self, x_pidginheartrow: PidginHeartRow):
        pidginheartcore_key = (x_pidginheartrow.face_id, x_pidginheartrow.event_id)
        if self.pidginheartcore_exists(pidginheartcore_key):
            pidginheartcore_obj = self.get_pidginheartcore(pidginheartcore_key)
            pidginheartcore_obj.add_otx_wall(x_pidginheartrow.otx_wall)
            pidginheartcore_obj.add_inx_wall(x_pidginheartrow.inx_wall)
            pidginheartcore_obj.add_unknown_word(x_pidginheartrow.unknown_word)
        else:
            pidginheartcore_obj = create_pidginheartcore(
                face_id=x_pidginheartrow.face_id,
                event_id=x_pidginheartrow.event_id,
                otx_wall=x_pidginheartrow.otx_wall,
                inx_wall=x_pidginheartrow.inx_wall,
                unknown_word=x_pidginheartrow.unknown_word,
            )
            self.pidginheartcores[pidginheartcore_key] = pidginheartcore_obj


def pidginheartbook_shop() -> PidginHeartBook:
    return PidginHeartBook(pidginheartcores={})
