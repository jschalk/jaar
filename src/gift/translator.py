from src._instrument.python import get_empty_dict_if_none
from src._road.jaar_config import get_test_real_id
from src._road.road import RealID, CharID, default_road_delimiter_if_none
from src.gift.atom import AtomUnit
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class Translator:
    in_real_id: RealID = None
    in_char_ids: dict[CharID, CharID] = None
    in_road_delimiter: str = None

    def set_char_id(self, in_char_id: CharID, out_char_id: CharID):
        self.in_char_ids[out_char_id] = in_char_id

    def out_char_id_exists(self, out_char_id: CharID) -> bool:
        return self.in_char_ids.get(out_char_id) != None

    def get_in_char_id(self, out_char_id: CharID) -> CharID:
        if self.out_char_id_exists(out_char_id):
            return self.in_char_ids.get(out_char_id)
        return out_char_id

    def translate_char_id(self, out_atomunit: AtomUnit) -> AtomUnit:
        in_atomunit = copy_deepcopy(out_atomunit)
        char_id_text = "char_id"
        out_char_id = in_atomunit.get_value(char_id_text)
        in_char_id = self.get_in_char_id(out_char_id)
        if in_char_id != out_char_id:
            in_atomunit.set_arg(char_id_text, in_char_id)
        return in_atomunit


def translator_shop(in_real_id: RealID = None):
    if in_real_id is None:
        in_real_id = get_test_real_id()
    return Translator(
        in_real_id=in_real_id,
        in_char_ids=get_empty_dict_if_none(None),
        in_road_delimiter=default_road_delimiter_if_none(),
    )
