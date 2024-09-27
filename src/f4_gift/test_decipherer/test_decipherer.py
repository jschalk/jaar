# from src.f0_instrument.python import x_is_json
from src.f1_road.jaar_config import get_test_fiscal_id
from src.f1_road.road import default_road_delimiter_if_none
from src.f2_bud.bud_tool import bud_acctunit_str
from src.f4_gift.atom_config import atom_insert, acct_id_str
from src.f4_gift.atom import atomunit_shop
from src.f4_gift.decipherer import Decipherer, decipherer_shop

# from src.f4_gift.gift import giftunit_shop, get_init_gift_id_if_None
# from src.f4_gift.examples.example_atoms import get_atom_example_ideaunit_sports
# from src.f4_gift.examples.example_deltas import get_deltaunit_sue_example
from copy import deepcopy as copy_deepcopy


def test_Decipherer_Exists():
    # ESTABLISH / WHEN
    x_decipherer = Decipherer()

    # THEN
    assert x_decipherer.in_fiscal_id is None
    assert x_decipherer.in_acct_ids is None
    assert x_decipherer.in_road_delimiter is None


def test_decipherer_shop_WithOutParametersReturnsObj():
    # ESTABLISH / WHEN
    music_decipherer = decipherer_shop()

    # THEN
    assert music_decipherer.in_fiscal_id == get_test_fiscal_id()
    assert music_decipherer.in_acct_ids == {}
    assert music_decipherer.in_road_delimiter == default_road_delimiter_if_none()


def test_decipherer_shop_WithParametersReturnsObj():
    # ESTABLISH
    music_str = "Music89"

    # WHEN
    music_decipherer = decipherer_shop(music_str)
    assert music_decipherer.in_fiscal_id == music_str
    assert music_decipherer.in_acct_ids == {}


def test_Decipherer_set_acct_id_SetsAttr():
    # ESTABLISH
    sue_str = "Sue"
    susan_str = "Susan"
    music_decipherer = decipherer_shop()
    assert music_decipherer.in_acct_ids == {}

    # WHEN
    music_decipherer.set_acct_id(sue_str, susan_str)

    # THEN
    assert music_decipherer.in_acct_ids == {susan_str: sue_str}


def test_Decipherer_out_acct_id_exists_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    susan_str = "Susan"
    music_decipherer = decipherer_shop()
    assert music_decipherer.out_acct_id_exists(susan_str) is False

    # WHEN
    music_decipherer.set_acct_id(sue_str, susan_str)

    # THEN
    assert music_decipherer.out_acct_id_exists(susan_str)


def test_Decipherer_get_in_acct_id_ReturnsObj_Equal():
    # ESTABLISH
    music_decipherer = decipherer_shop()
    yao_str = "Yao"

    # WHEN / THEN
    assert yao_str == music_decipherer.get_in_acct_id(yao_str)


def test_Decipherer_get_in_acct_id_ReturnsObj_NotEqual():
    # ESTABLISH
    sue_str = "Sue"
    susan_str = "Susan"
    music_decipherer = decipherer_shop()
    music_decipherer.set_acct_id(sue_str, susan_str)

    # WHEN / THEN
    assert sue_str == music_decipherer.get_in_acct_id(susan_str)


def test_Decipherer_decipher_acct_id_ReturnsObjWithNoDeltas():
    # ESTABLISH
    yao_str = "Yao"
    x_category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    acctunit_atom = atomunit_shop(x_category, atom_insert())
    acctunit_atom.set_required_arg(acct_id_str(), yao_str)
    acctunit_atom.set_optional_arg(credit_belief_str, 51)

    old_atomunit = copy_deepcopy(acctunit_atom)
    music_decipherer = decipherer_shop()
    assert acctunit_atom.get_value(acct_id_str()) == yao_str
    assert acctunit_atom.get_value(credit_belief_str) == 51

    # WHEN
    deciphered_atom = music_decipherer.decipher_acct_id(acctunit_atom)

    # THEN
    assert acctunit_atom.get_value(acct_id_str()) == yao_str
    assert acctunit_atom.get_value(credit_belief_str) == 51
    assert deciphered_atom == old_atomunit


def test_Decipherer_decipher_acct_id_ReturnsObjWithDelta_acct_id():
    # ESTABLISH
    susan_str = "Susan"
    x_category = bud_acctunit_str()
    credit_belief_str = "credit_belief"
    acctunit_atom = atomunit_shop(x_category, atom_insert())
    acctunit_atom.set_required_arg(acct_id_str(), susan_str)
    acctunit_atom.set_optional_arg(credit_belief_str, 51)

    sue_str = "Sue"
    music_decipherer = decipherer_shop()
    music_decipherer.set_acct_id(sue_str, susan_str)
    assert acctunit_atom.get_value(acct_id_str()) == susan_str
    assert acctunit_atom.get_value(credit_belief_str) == 51

    # WHEN
    deciphered_atom = music_decipherer.decipher_acct_id(acctunit_atom)

    # THEN
    assert deciphered_atom.get_value(acct_id_str()) != susan_str
    assert deciphered_atom.get_value(acct_id_str()) == sue_str
    assert deciphered_atom.get_value(credit_belief_str) == 51
