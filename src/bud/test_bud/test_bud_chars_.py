from src.bud.char import charunit_shop
from src.bud.lobby import awardlink_shop
from src.bud.bud import budunit_shop
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_BudUnit_set_charunit_SetObjCorrectly():
    # ESTABLISH
    yao_text = "Yao"
    yao_charunit = charunit_shop(yao_text)
    yao_charunit.add_lobbyship(yao_text)
    deepcopy_yao_charunit = copy_deepcopy(yao_charunit)
    slash_text = "/"
    bob_bud = budunit_shop("Bob", _road_delimiter=slash_text)

    # WHEN
    bob_bud.set_charunit(yao_charunit)

    # THEN
    assert bob_bud._chars.get(yao_text)._road_delimiter == slash_text
    x_chars = {yao_charunit.char_id: deepcopy_yao_charunit}
    assert bob_bud._chars != x_chars
    deepcopy_yao_charunit._road_delimiter = bob_bud._road_delimiter
    assert bob_bud._chars == x_chars


def test_BudUnit_set_char_DoesNotSet_char_id_lobbyship():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_bud.set_charunit(charunit_shop(zia_text), auto_set_lobbyship=False)

    # THEN
    assert yao_bud.get_char(zia_text).get_lobbyship(zia_text) is None


def test_BudUnit_set_char_DoesSet_char_id_lobbyship():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"

    # WHEN
    yao_bud.set_charunit(charunit_shop(zia_text))

    # THEN
    zia_zia_lobbyship = yao_bud.get_char(zia_text).get_lobbyship(zia_text)
    assert zia_zia_lobbyship is not None
    assert zia_zia_lobbyship.credor_weight == 1
    assert zia_zia_lobbyship.debtor_weight == 1


def test_BudUnit_set_char_DoesNotOverRide_char_id_lobbyship():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    ohio_text = ",Ohio"
    zia_ohio_credor_w = 33
    zia_ohio_debtor_w = 44
    zia_charunit = charunit_shop(zia_text)
    zia_charunit.add_lobbyship(ohio_text, zia_ohio_credor_w, zia_ohio_debtor_w)

    # WHEN
    yao_bud.set_charunit(zia_charunit)

    # THEN
    zia_ohio_lobbyship = yao_bud.get_char(zia_text).get_lobbyship(ohio_text)
    assert zia_ohio_lobbyship is not None
    assert zia_ohio_lobbyship.credor_weight == zia_ohio_credor_w
    assert zia_ohio_lobbyship.debtor_weight == zia_ohio_debtor_w
    zia_zia_lobbyship = yao_bud.get_char(zia_text).get_lobbyship(zia_text)
    assert zia_zia_lobbyship is None


def test_BudUnit_set_char_CorrectlySets_chars_lobbyships():
    # ESTABLISH
    x_bit = 5
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    assert len(yao_bud._chars) == 0
    assert len(yao_bud.get_lobby_ids_dict()) == 0

    # WHEN
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"
    yao_bud.set_charunit(charunit_shop(zia_text))
    yao_bud.set_charunit(charunit_shop(sue_text))
    yao_bud.set_charunit(charunit_shop(xio_text))

    # THEN
    assert yao_bud._chars.get(zia_text)._bit == x_bit
    assert len(yao_bud._chars) == 3
    assert len(yao_bud.get_lobby_ids_dict()) == 3

    # WHEN
    zia_lobby = zia_text
    sue_lobby = sue_text
    xio_lobby = xio_text
    yao_bud._idearoot.set_awardlink(awardlink_shop(zia_lobby, give_weight=10))
    yao_bud._idearoot.set_awardlink(awardlink_shop(sue_lobby, give_weight=10))
    yao_bud._idearoot.set_awardlink(awardlink_shop(xio_lobby, give_weight=10))
    assert len(yao_bud._idearoot._awardlinks) == 3


def test_BudUnit_add_charunit_CorrectlySets_chars():
    # ESTABLISH
    x_bit = 6
    yao_bud = budunit_shop("Yao", _bit=x_bit)
    zia_text = "Zia"
    sue_text = "Sue"
    xio_text = "Xio"

    # WHEN
    yao_bud.add_charunit(zia_text, credor_weight=13, debtor_weight=8)
    yao_bud.add_charunit(sue_text, debtor_weight=5)
    yao_bud.add_charunit(xio_text, credor_weight=17)

    # THEN
    assert len(yao_bud._chars) == 3
    assert len(yao_bud.get_lobby_ids_dict()) == 3
    assert yao_bud._chars.get(xio_text).credor_weight == 17
    assert yao_bud._chars.get(sue_text).debtor_weight == 5
    assert yao_bud._chars.get(xio_text)._bit == x_bit


def test_BudUnit_char_exists_ReturnsObj():
    # ESTABLISH
    bob_bud = budunit_shop("Bob")
    yao_text = "Yao"

    # WHEN / THEN
    assert bob_bud.char_exists(yao_text) is False

    # ESTABLISH
    bob_bud.add_charunit(yao_text)

    # WHEN / THEN
    assert bob_bud.char_exists(yao_text)


def test_BudUnit_set_char_Creates_lobbyship():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    before_zia_credor = 7
    before_zia_debtor = 17
    yao_bud.add_charunit(zia_text, before_zia_credor, before_zia_debtor)
    zia_charunit = yao_bud.get_char(zia_text)
    zia_lobbyship = zia_charunit.get_lobbyship(zia_text)
    assert zia_lobbyship.credor_weight != before_zia_credor
    assert zia_lobbyship.debtor_weight != before_zia_debtor
    assert zia_lobbyship.credor_weight == 1
    assert zia_lobbyship.debtor_weight == 1

    # WHEN
    after_zia_credor = 11
    after_zia_debtor = 13
    yao_bud.set_charunit(charunit_shop(zia_text, after_zia_credor, after_zia_debtor))

    # THEN
    assert zia_lobbyship.credor_weight != after_zia_credor
    assert zia_lobbyship.debtor_weight != after_zia_debtor
    assert zia_lobbyship.credor_weight == 1
    assert zia_lobbyship.debtor_weight == 1


def test_BudUnit_edit_char_RaiseExceptionWhenCharDoesNotExist():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    zia_credor_weight = 55

    # WHEN
    with pytest_raises(Exception) as excinfo:
        yao_bud.edit_charunit(zia_text, credor_weight=zia_credor_weight)
    assert str(excinfo.value) == f"CharUnit '{zia_text}' does not exist."


def test_BudUnit_edit_char_CorrectlyUpdatesObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    old_zia_credor_weight = 55
    old_zia_debtor_weight = 66
    yao_bud.set_charunit(
        charunit_shop(
            zia_text,
            old_zia_credor_weight,
            old_zia_debtor_weight,
        )
    )
    zia_charunit = yao_bud.get_char(zia_text)
    assert zia_charunit.credor_weight == old_zia_credor_weight
    assert zia_charunit.debtor_weight == old_zia_debtor_weight

    # WHEN
    new_zia_credor_weight = 22
    new_zia_debtor_weight = 33
    yao_bud.edit_charunit(
        char_id=zia_text,
        credor_weight=new_zia_credor_weight,
        debtor_weight=new_zia_debtor_weight,
    )

    # THEN
    assert zia_charunit.credor_weight == new_zia_credor_weight
    assert zia_charunit.debtor_weight == new_zia_debtor_weight


def test_BudUnit_get_char_ReturnsCorrectObj():
    # ESTABLISH
    yao_bud = budunit_shop("Yao")
    zia_text = "Zia"
    sue_text = "Sue"
    yao_bud.add_charunit(zia_text)
    yao_bud.add_charunit(sue_text)

    # WHEN
    zia_char = yao_bud.get_char(zia_text)
    sue_char = yao_bud.get_char(sue_text)

    # THEN
    assert zia_char == yao_bud._chars.get(zia_text)
    assert sue_char == yao_bud._chars.get(sue_text)
