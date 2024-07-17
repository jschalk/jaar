# from src._instrument.python import x_is_json
from src._road.jaar_config import get_test_real_id
from src._road.road import default_road_delimiter_if_none
from src.gift.atom import atomunit_shop, atom_update, atom_delete, atom_insert
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
    assert x_translator.in_char_ids is None
    assert x_translator.in_road_delimiter is None


def test_translator_shop_WithOutParametersReturnsObj():
    # ESTABLISH / WHEN
    music_translator = translator_shop()

    # THEN
    assert music_translator.in_real_id == get_test_real_id()
    assert music_translator.in_char_ids == {}
    assert music_translator.in_road_delimiter == default_road_delimiter_if_none()


def test_translator_shop_WithParametersReturnsObj():
    # ESTABLISH
    music_text = "Music89"

    # WHEN
    music_translator = translator_shop(music_text)
    assert music_translator.in_real_id == music_text
    assert music_translator.in_char_ids == {}


def test_Translator_set_char_id_SetsAttr():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    assert music_translator.in_char_ids == {}

    # WHEN
    music_translator.set_char_id(sue_text, susan_text)

    # THEN
    assert music_translator.in_char_ids == {susan_text: sue_text}


def test_Translator_out_char_id_exists_ReturnsObj():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    assert music_translator.out_char_id_exists(susan_text) == False

    # WHEN
    music_translator.set_char_id(sue_text, susan_text)

    # THEN
    assert music_translator.out_char_id_exists(susan_text)


def test_Translator_get_in_char_id_ReturnsObj_Equal():
    # ESTABLISH
    music_translator = translator_shop()
    yao_text = "Yao"

    # WHEN / THEN
    assert yao_text == music_translator.get_in_char_id(yao_text)


def test_Translator_get_in_char_id_ReturnsObj_NotEqual():
    # ESTABLISH
    sue_text = "Sue"
    susan_text = "Susan"
    music_translator = translator_shop()
    music_translator.set_char_id(sue_text, susan_text)

    # WHEN / THEN
    assert sue_text == music_translator.get_in_char_id(susan_text)


def test_Translator_translate_char_id_ReturnsObjWithNoChanges():
    # ESTABLISH
    yao_text = "Yao"
    x_category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    charunit_atom = atomunit_shop(x_category, atom_insert())
    charunit_atom.set_required_arg(char_id_text, yao_text)
    charunit_atom.set_optional_arg(credor_weight_text, 51)

    old_atomunit = copy_deepcopy(charunit_atom)
    music_translator = translator_shop()
    assert charunit_atom.get_value(char_id_text) == yao_text
    assert charunit_atom.get_value(credor_weight_text) == 51

    # WHEN
    translated_atom = music_translator.translate_char_id(charunit_atom)

    # THEN
    assert charunit_atom.get_value(char_id_text) == yao_text
    assert charunit_atom.get_value(credor_weight_text) == 51
    assert translated_atom == old_atomunit


def test_Translator_translate_char_id_ReturnsObjWithChange_char_id():
    # ESTABLISH
    susan_text = "Susan"
    x_category = "world_charunit"
    char_id_text = "char_id"
    credor_weight_text = "credor_weight"
    charunit_atom = atomunit_shop(x_category, atom_insert())
    charunit_atom.set_required_arg(char_id_text, susan_text)
    charunit_atom.set_optional_arg(credor_weight_text, 51)

    sue_text = "Sue"
    music_translator = translator_shop()
    music_translator.set_char_id(sue_text, susan_text)
    assert charunit_atom.get_value(char_id_text) == susan_text
    assert charunit_atom.get_value(credor_weight_text) == 51

    # WHEN
    translated_atom = music_translator.translate_char_id(charunit_atom)

    # THEN
    assert translated_atom.get_value(char_id_text) != susan_text
    assert translated_atom.get_value(char_id_text) == sue_text
    assert translated_atom.get_value(credor_weight_text) == 51
