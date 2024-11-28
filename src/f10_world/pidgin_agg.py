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
    face_id: str = None
    event_id: int = None
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
    pidginheartcores: dict[int, PidginHeartCore] = None

    def _overwrite_pidginheartcore(self, x_pidginheartcore: PidginHeartCore):
        self.pidginheartcores[x_pidginheartcore.event_id] = x_pidginheartcore

    def pidginheartcore_exists(self, event_id: int):
        return self.pidginheartcores.get(event_id) != None

    def get_pidginheartcore(self, event_id: int) -> PidginHeartCore:
        return self.pidginheartcores.get(event_id)

    def eval_pidginheartrow(self, x_pidginheartrow: PidginHeartRow):
        if self.pidginheartcore_exists(x_pidginheartrow.event_id):
            pidginheartcore_obj = self.get_pidginheartcore(x_pidginheartrow.event_id)
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
            self.pidginheartcores[x_pidginheartrow.event_id] = pidginheartcore_obj


def pidginheartbook_shop() -> PidginHeartBook:
    return PidginHeartBook(pidginheartcores={})


@dataclass
class PidginBodyRow:
    face_id: str
    event_id: int
    otx_str: str
    inx_str: str


@dataclass
class PidginBodyCore:
    face_id: str = None
    event_id: int = None
    otx_str: str = None
    inx_strs: set[str] = None

    def add_inx_str(self, inx_str: str):
        if None in self.inx_strs and inx_str != None:
            self.inx_strs.remove(None)

        if inx_str is None and self.inx_strs == set():
            self.inx_strs.add(inx_str)
        elif inx_str != None:
            self.inx_strs.add(inx_str)

    def is_valid(self) -> bool:
        return len(self.inx_strs) == 1

    def get_valid_pidginbodyrow(self) -> PidginBodyRow:
        if self.is_valid():
            return PidginBodyRow(
                face_id=self.face_id,
                event_id=self.event_id,
                otx_str=self.otx_str,
                inx_str=min(self.inx_strs),
            )


def pidginbodycore_shop(
    face_id: str,
    event_id: int,
    otx_str: str,
    inx_strs: set[str] = None,
) -> PidginBodyCore:
    return PidginBodyCore(face_id, event_id, otx_str, get_empty_set_if_none(inx_strs))


def create_pidginbodycore(
    face_id: str, event_id: int, otx_str: str, inx_str: str
) -> PidginBodyCore:
    x_pidginbodycore = pidginbodycore_shop(face_id, event_id, otx_str)
    x_pidginbodycore.add_inx_str(inx_str)
    return x_pidginbodycore


@dataclass
class PidginBodyBook:
    pidginbodycores: dict[tuple[int, str], PidginBodyCore] = None

    def _overwrite_pidginbodycore(self, x_pidginbodycore: PidginBodyCore):
        x_key = (x_pidginbodycore.event_id, x_pidginbodycore.otx_str)
        self.pidginbodycores[x_key] = x_pidginbodycore

    def pidginbodycore_exists(self, event_id_otx: tuple[int, str]):
        return self.pidginbodycores.get(event_id_otx) != None

    def get_pidginbodycore(self, event_id_otx: tuple[int, str]) -> PidginBodyCore:
        return self.pidginbodycores.get(event_id_otx)

    def eval_pidginbodyrow(self, x_pidginbodyrow: PidginBodyRow):
        pidginbodycore_key = (x_pidginbodyrow.event_id, x_pidginbodyrow.otx_str)
        if self.pidginbodycore_exists(pidginbodycore_key):
            pidginbodycore_obj = self.get_pidginbodycore(pidginbodycore_key)
            pidginbodycore_obj.add_inx_str(x_pidginbodyrow.inx_str)
        else:
            pidginbodycore_obj = create_pidginbodycore(
                face_id=x_pidginbodyrow.face_id,
                event_id=x_pidginbodyrow.event_id,
                otx_str=x_pidginbodyrow.otx_str,
                inx_str=x_pidginbodyrow.inx_str,
            )
            self.pidginbodycores[pidginbodycore_key] = pidginbodycore_obj


def pidginbodybook_shop() -> PidginBodyBook:
    return PidginBodyBook(pidginbodycores={})
