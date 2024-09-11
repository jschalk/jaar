from src._instrument.python_tool import get_empty_dict_if_none
from src._road.jaar_config import get_tribe_id_if_None
from src._road.road import TribeID, AcctID, default_road_delimiter_if_none
from src.change.atom_config import acct_id_str
from src.change.atom import AtomUnit
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class Translator:
    in_tribe_id: TribeID = None
    in_acct_ids: dict[AcctID, AcctID] = None
    in_road_delimiter: str = None

    def set_acct_id(self, in_acct_id: AcctID, out_acct_id: AcctID):
        self.in_acct_ids[out_acct_id] = in_acct_id

    def out_acct_id_exists(self, out_acct_id: AcctID) -> bool:
        return self.in_acct_ids.get(out_acct_id) is not None

    def get_in_acct_id(self, out_acct_id: AcctID) -> AcctID:
        if self.out_acct_id_exists(out_acct_id):
            return self.in_acct_ids.get(out_acct_id)
        return out_acct_id

    def translate_acct_id(self, out_atomunit: AtomUnit) -> AtomUnit:
        in_atomunit = copy_deepcopy(out_atomunit)
        out_acct_id = in_atomunit.get_value(acct_id_str())
        in_acct_id = self.get_in_acct_id(out_acct_id)
        if in_acct_id != out_acct_id:
            in_atomunit.set_arg(acct_id_str(), in_acct_id)
        return in_atomunit


def translator_shop(in_tribe_id: TribeID = None):
    in_tribe_id = get_tribe_id_if_None(in_tribe_id)
    return Translator(
        in_tribe_id=in_tribe_id,
        in_acct_ids=get_empty_dict_if_none(None),
        in_road_delimiter=default_road_delimiter_if_none(),
    )
