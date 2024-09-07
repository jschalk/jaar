# from src._instrument.python import x_is_json
from src._road.jaar_config import get_test_real_id
from src._road.road import default_road_delimiter_if_none
from src.bud.bud_tool import bud_acctunit_text
from src.gift.atom_config import atom_insert, acct_id_str
from src.gift.atom import atomunit_shop
from src.gift.translator import Translator, translator_shop

# from src.gift.gift import giftunit_shop, get_init_gift_id_if_None
# from src.gift.examples.example_atoms import get_atom_example_ideaunit_sports
# from src.gift.examples.example_changes import get_changeunit_sue_example
from copy import deepcopy as copy_deepcopy


def test_Translator_Exists():
    # ESTABLISH / WHEN
    x_translator = Translator()

    # THEN
    assert x_translator.in_real_id is None
    assert x_translator.in_acct_ids is None
    assert x_translator.in_road_delimiter is None


def test_translator_shop_WithOutParametersReturnsObj():
    # ESTABLISH / WHEN
    music_translator = translator_shop()

    # THEN
    assert music_translator.in_real_id == get_test_real_id()
    assert music_translator.in_acct_ids == {}
    assert music_translator.in_road_delimiter == default_road_delimiter_if_none()


def test_translator_shop_WithParametersReturnsObj():
    # ESTABLISH
    music_text = "Music89"

    # WHEN
    music_translator = translator_shop(music_text)
    assert music_translator.in_real_id == music_text
    assert music_translator.in_acct_ids == {}


def test_Translator_set_acct_id_SetsAttr():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    assert music_translator.in_acct_ids == {}

    # WHEN
    music_translator.set_acct_id(sue_text, susan_text)

    # THEN
    assert music_translator.in_acct_ids == {susan_text: sue_text}


def test_Translator_out_acct_id_exists_ReturnsObj():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    assert music_translator.out_acct_id_exists(susan_text) is False

    # WHEN
    music_translator.set_acct_id(sue_text, susan_text)

    # THEN
    assert music_translator.out_acct_id_exists(susan_text)


def test_Translator_get_in_acct_id_ReturnsObj_Equal():
    # ESTABLISH
    music_translator = translator_shop()
    yao_text = "Yao"

    # WHEN / THEN
    assert yao_text == music_translator.get_in_acct_id(yao_text)


def test_Translator_get_in_acct_id_ReturnsObj_NotEqual():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    music_translator.set_acct_id(sue_text, susan_text)

    # WHEN / THEN
    assert sue_text == music_translator.get_in_acct_id(susan_text)


def test_Translator_translate_acct_id_ReturnsObjWithNoChanges():
    # ESTABLISH
    yao_text = "Yao"
    x_category = bud_acctunit_text()
    credit_belief_text = "credit_belief"
    acctunit_atom = atomunit_shop(x_category, atom_insert())
    acctunit_atom.set_required_arg(acct_id_str(), yao_text)
    acctunit_atom.set_optional_arg(credit_belief_text, 51)

    old_atomunit = copy_deepcopy(acctunit_atom)
    music_translator = translator_shop()
    assert acctunit_atom.get_value(acct_id_str()) == yao_text
    assert acctunit_atom.get_value(credit_belief_text) == 51

    # WHEN
    translated_atom = music_translator.translate_acct_id(acctunit_atom)

    # THEN
    assert acctunit_atom.get_value(acct_id_str()) == yao_text
    assert acctunit_atom.get_value(credit_belief_text) == 51
    assert translated_atom == old_atomunit


def test_Translator_translate_acct_id_ReturnsObjWithChange_acct_id():
    # ESTABLISH
    susan_text = "Susan"
    x_category = bud_acctunit_text()
    credit_belief_text = "credit_belief"
    acctunit_atom = atomunit_shop(x_category, atom_insert())
    acctunit_atom.set_required_arg(acct_id_str(), susan_text)
    acctunit_atom.set_optional_arg(credit_belief_text, 51)

    sue_text = "Sue"
    music_translator = translator_shop()
    music_translator.set_acct_id(sue_text, susan_text)
    assert acctunit_atom.get_value(acct_id_str()) == susan_text
    assert acctunit_atom.get_value(credit_belief_text) == 51

    # WHEN
    translated_atom = music_translator.translate_acct_id(acctunit_atom)

    # THEN
    assert translated_atom.get_value(acct_id_str()) != susan_text
    assert translated_atom.get_value(acct_id_str()) == sue_text
    assert translated_atom.get_value(credit_belief_text) == 51
