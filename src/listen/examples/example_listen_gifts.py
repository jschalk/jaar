from src.gift.gift import giftunit_shop, GiftUnit
from src.listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_sports,
)


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_id="Yao", _gift_id=37, _face_id="Sue")


def get_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_id="Sue", _gift_id=37, _face_id="Yao")


def sue_1atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=53, _face_id="Yao")
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_sports())
    return x_giftunit


def sue_2atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=53, _face_id="Yao")
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_knee())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_sports())
    return x_giftunit


def sue_3atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=37, _face_id="Yao")
    x_giftunit._changeunit.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_ball())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_knee())
    return x_giftunit


def sue_4atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=47, _face_id="Yao")
    x_giftunit._changeunit.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_ball())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_knee())
    x_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_sports())
    return x_giftunit
