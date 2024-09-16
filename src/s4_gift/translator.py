from src.s0_instrument.python_tool import get_empty_dict_if_none
from src.s1_road.jaar_config import get_fiscal_id_if_None
from src.s1_road.road import FiscalID, AcctID, default_road_delimiter_if_none
from src.s4_gift.atom_config import acct_id_str
from src.s4_gift.atom import AtomUnit
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class Translator:
    in_fiscal_id: FiscalID = None
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


def translator_shop(in_fiscal_id: FiscalID = None):
    in_fiscal_id = get_fiscal_id_if_None(in_fiscal_id)
    return Translator(
        in_fiscal_id=in_fiscal_id,
        in_acct_ids=get_empty_dict_if_none(None),
        in_road_delimiter=default_road_delimiter_if_none(),
    )
