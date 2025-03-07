from src.f04_gift.gift import giftunit_shop, GiftUnit
from src.f05_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_name="Yao", _gift_id=37, face_name="Sue")


def get_sue_giftunit() -> GiftUnit:
    return giftunit_shop(owner_name="Sue", _gift_id=37, face_name="Yao")


def sue_1atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_name="Sue", _gift_id=53, face_name="Yao")
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit


def sue_2atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_name="Sue", _gift_id=53, face_name="Yao")
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_knee())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit


def sue_3atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_name="Sue", _gift_id=37, face_name="Yao")
    x_giftunit._buddelta.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_ball())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_knee())
    return x_giftunit


def sue_4atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(owner_name="Sue", _gift_id=47, face_name="Yao")
    x_giftunit._buddelta.set_atomunit(get_atom_example_factunit_knee())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_ball())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_knee())
    x_giftunit._buddelta.set_atomunit(get_atom_example_itemunit_sports())
    return x_giftunit
