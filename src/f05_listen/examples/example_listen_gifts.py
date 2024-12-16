from src.f04_gift.gift import giftunit_shop, GiftUnit
from src.f05_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_id="Yao", _gift_id=37, face_id="Sue")


def get_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_id="Sue", _gift_id=37, face_id="Yao")


def sue_1atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=53, face_id="Yao")
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit


def sue_2atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=53, face_id="Yao")
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_knee())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit


def sue_3atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=37, face_id="Yao")
    x_giftunit._deltaunit.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_ball())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_knee())
    return x_giftunit


def sue_4atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_id="Sue", _gift_id=47, face_id="Yao")
    x_giftunit._deltaunit.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_ball())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_knee())
    x_giftunit._deltaunit.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit
