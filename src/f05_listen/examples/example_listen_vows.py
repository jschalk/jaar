from src.f04_vow.vow import vowunit_shop, vowUnit
from src.f05_listen.examples.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_itemunit_ball,
    get_atom_example_itemunit_knee,
    get_atom_example_itemunit_sports,
)


def yao_sue_vowunit() -> vowUnit:
    return vowunit_shop(owner_name="Yao", _vow_id=37, face_name="Sue")


def get_sue_vowunit() -> vowUnit:
    return vowunit_shop(owner_name="Sue", _vow_id=37, face_name="Yao")


def sue_1budatoms_vowunit() -> vowUnit:
    x_vowunit = vowunit_shop(owner_name="Sue", _vow_id=53, face_name="Yao")
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_vowunit


def sue_2budatoms_vowunit() -> vowUnit:
    x_vowunit = vowunit_shop(owner_name="Sue", _vow_id=53, face_name="Yao")
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_vowunit


def sue_3budatoms_vowunit() -> vowUnit:
    x_vowunit = vowunit_shop(owner_name="Sue", _vow_id=37, face_name="Yao")
    x_vowunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    return x_vowunit


def sue_4budatoms_vowunit() -> vowUnit:
    x_vowunit = vowunit_shop(owner_name="Sue", _vow_id=47, face_name="Yao")
    x_vowunit._buddelta.set_budatom(get_atom_example_factunit_knee())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_ball())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_knee())
    x_vowunit._buddelta.set_budatom(get_atom_example_itemunit_sports())
    return x_vowunit
