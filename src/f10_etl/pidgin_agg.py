from src.f00_instrument.dict_toolbox import get_empty_set_if_None
from src.f09_brick.pandas_tool import if_nan_return_None
from dataclasses import dataclass


@dataclass
class PidginHeartRow:
    face_id: str
    event_id: int
    otx_bridge: str
    inx_bridge: str
    unknown_word: str


@dataclass
class PidginHeartUnit:
    face_id: str = None
    event_id: int = None
    otx_bridges: set[str] = None
    inx_bridges: set[str] = None
    unknown_words: set[str] = None

    def add_otx_bridge(self, otx_bridge: str):
        otx_bridge = if_nan_return_None(otx_bridge)

        if None in self.otx_bridges and otx_bridge != None:
            self.otx_bridges.remove(None)

        if otx_bridge is None and self.otx_bridges == set():
            self.otx_bridges.add(otx_bridge)
        elif otx_bridge != None:
            self.otx_bridges.add(otx_bridge)

    def add_inx_bridge(self, inx_bridge: str):
        inx_bridge = if_nan_return_None(inx_bridge)

        if None in self.inx_bridges and inx_bridge != None:
            self.inx_bridges.remove(None)

        if inx_bridge is None and self.inx_bridges == set():
            self.inx_bridges.add(inx_bridge)
        elif inx_bridge != None:
            self.inx_bridges.add(inx_bridge)

    def add_unknown_word(self, unknown_word: str):
        unknown_word = if_nan_return_None(unknown_word)

        if None in self.unknown_words and unknown_word != None:
            self.unknown_words.remove(None)

        if unknown_word is None and self.unknown_words == set():
            self.unknown_words.add(unknown_word)
        elif unknown_word != None:
            self.unknown_words.add(unknown_word)

    def is_valid(self) -> bool:
        return (
            len(self.otx_bridges) == 1
            and len(self.inx_bridges) == 1
            and len(self.unknown_words) == 1
        )

    def get_valid_pidginheartrow(self) -> PidginHeartRow:
        if self.is_valid():
            return PidginHeartRow(
                face_id=self.face_id,
                event_id=self.event_id,
                otx_bridge=min(self.otx_bridges),
                inx_bridge=min(self.inx_bridges),
                unknown_word=min(self.unknown_words),
            )


def pidginheartunit_shop(
    face_id: str,
    event_id: int,
    otx_bridges: set[str] = None,
    inx_bridges: set[str] = None,
    unknown_words: set[str] = None,
) -> PidginHeartUnit:
    return PidginHeartUnit(
        face_id,
        event_id,
        get_empty_set_if_None(otx_bridges),
        get_empty_set_if_None(inx_bridges),
        get_empty_set_if_None(unknown_words),
    )


def create_pidginheartunit(
    face_id: str, event_id: int, otx_bridge: str, inx_bridge: str, unknown_word: str
) -> PidginHeartUnit:
    x_pidginheartunit = pidginheartunit_shop(face_id, event_id)
    print(f"{otx_bridge=} {type(otx_bridge)=}")
    print(f"{inx_bridge=} {type(inx_bridge)=}")
    print(f"{unknown_word=} {type(unknown_word)=}")
    x_pidginheartunit.add_otx_bridge(otx_bridge)
    x_pidginheartunit.add_inx_bridge(inx_bridge)
    x_pidginheartunit.add_unknown_word(unknown_word)
    return x_pidginheartunit


@dataclass
class PidginHeartBook:
    pidginheartunits: dict[int, PidginHeartUnit] = None

    def _overwrite_pidginheartunit(self, x_pidginheartunit: PidginHeartUnit):
        self.pidginheartunits[x_pidginheartunit.event_id] = x_pidginheartunit

    def pidginheartunit_exists(self, event_id: int):
        return self.pidginheartunits.get(event_id) != None

    def get_pidginheartunit(self, event_id: int) -> PidginHeartUnit:
        return self.pidginheartunits.get(event_id)

    def eval_pidginheartrow(self, x_pidginheartrow: PidginHeartRow):
        if self.pidginheartunit_exists(x_pidginheartrow.event_id):
            pidginheartunit_obj = self.get_pidginheartunit(x_pidginheartrow.event_id)
            pidginheartunit_obj.add_otx_bridge(x_pidginheartrow.otx_bridge)
            pidginheartunit_obj.add_inx_bridge(x_pidginheartrow.inx_bridge)
            pidginheartunit_obj.add_unknown_word(x_pidginheartrow.unknown_word)
        else:
            pidginheartunit_obj = create_pidginheartunit(
                face_id=x_pidginheartrow.face_id,
                event_id=x_pidginheartrow.event_id,
                otx_bridge=x_pidginheartrow.otx_bridge,
                inx_bridge=x_pidginheartrow.inx_bridge,
                unknown_word=x_pidginheartrow.unknown_word,
            )
            self.pidginheartunits[x_pidginheartrow.event_id] = pidginheartunit_obj

    def add_pidginheartrow(
        self,
        face_id: str,
        event_id: int,
        otx_bridge: str,
        inx_bridge: str,
        unknown_word: str,
    ):
        x_pidginheartrow = PidginHeartRow(
            face_id, event_id, otx_bridge, inx_bridge, unknown_word
        )
        self.eval_pidginheartrow(x_pidginheartrow)

    def event_id_is_valid(self, event_id: int) -> bool:
        if self.pidginheartunit_exists(event_id) is False:
            return False
        return self.get_pidginheartunit(event_id).is_valid()


def pidginheartbook_shop() -> PidginHeartBook:
    return PidginHeartBook(pidginheartunits={})


@dataclass
class PidginBodyRow:
    face_id: str
    event_id: int
    otx_str: str
    inx_str: str


@dataclass
class PidginBodyUnit:
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


def pidginbodyunit_shop(
    face_id: str,
    event_id: int,
    otx_str: str,
    inx_strs: set[str] = None,
) -> PidginBodyUnit:
    return PidginBodyUnit(face_id, event_id, otx_str, get_empty_set_if_None(inx_strs))


def create_pidginbodyunit(
    face_id: str, event_id: int, otx_str: str, inx_str: str
) -> PidginBodyUnit:
    x_pidginbodyunit = pidginbodyunit_shop(face_id, event_id, otx_str)
    x_pidginbodyunit.add_inx_str(inx_str)
    return x_pidginbodyunit


@dataclass
class PidginBodyBook:
    pidginheartbook: PidginHeartBook = None
    pidginbodyunits: dict[tuple[int, str], PidginBodyUnit] = None

    def get_valid_pidginbodylists(
        self,
    ) -> list[list[str, int, str, str, str, str, str]]:
        x_list = []
        for x_pidginbodyunit in self.pidginbodyunits.values():
            if x_pidginbodyunit.is_valid():
                x_pidginheartunit = self.pidginheartbook.get_pidginheartunit(
                    x_pidginbodyunit.event_id
                )
                x_pidginheartrow = x_pidginheartunit.get_valid_pidginheartrow()

                x_pidginbodylist = [
                    x_pidginbodyunit.face_id,
                    x_pidginbodyunit.event_id,
                    x_pidginbodyunit.otx_str,
                    min(x_pidginbodyunit.inx_strs),
                    x_pidginheartrow.otx_bridge,
                    x_pidginheartrow.inx_bridge,
                    x_pidginheartrow.unknown_word,
                ]
                x_list.append(x_pidginbodylist)
        return x_list

    def _overwrite_pidginbodyunit(self, x_pidginbodyunit: PidginBodyUnit):
        x_key = (x_pidginbodyunit.event_id, x_pidginbodyunit.otx_str)
        self.pidginbodyunits[x_key] = x_pidginbodyunit

    def pidginbodyunit_exists(self, event_id: int, otx_str: str):
        return self.pidginbodyunits.get((event_id, otx_str)) != None

    def get_pidginbodyunit(self, event_id: int, otx_str: str) -> PidginBodyUnit:
        return self.pidginbodyunits.get((event_id, otx_str))

    def eval_pidginbodyrow(self, x_pidginbodyrow: PidginBodyRow):
        x_event_id = x_pidginbodyrow.event_id
        x_otx_str = x_pidginbodyrow.otx_str
        if self.heart_is_valid(x_event_id):
            if self.pidginbodyunit_exists(x_event_id, x_otx_str):
                pidginbodyunit_obj = self.get_pidginbodyunit(x_event_id, x_otx_str)
                pidginbodyunit_obj.add_inx_str(x_pidginbodyrow.inx_str)
            else:
                pidginbodyunit_obj = create_pidginbodyunit(
                    face_id=x_pidginbodyrow.face_id,
                    event_id=x_pidginbodyrow.event_id,
                    otx_str=x_pidginbodyrow.otx_str,
                    inx_str=x_pidginbodyrow.inx_str,
                )
                pidginbodyunit_key = (x_event_id, x_otx_str)
                self.pidginbodyunits[pidginbodyunit_key] = pidginbodyunit_obj

    def add_pidginheartrow(
        self,
        face_id: str,
        event_id: int,
        otx_bridge: str,
        inx_bridge: str,
        unknown_word: str,
    ):
        self.pidginheartbook.add_pidginheartrow(
            face_id, event_id, otx_bridge, inx_bridge, unknown_word
        )

    def heart_is_valid(self, event_id: int) -> bool:
        return self.pidginheartbook.event_id_is_valid(event_id)

    def body_is_valid(self, event_id: int, otx_str: str) -> bool:
        if self.pidginbodyunit_exists(event_id, otx_str):
            return self.get_pidginbodyunit(event_id, otx_str).is_valid()
        return False


def pidginbodybook_shop(pidginheartbook: PidginHeartBook = None) -> PidginBodyBook:
    if pidginheartbook is None:
        pidginheartbook = pidginheartbook_shop()
    return PidginBodyBook(pidginheartbook=pidginheartbook, pidginbodyunits={})
