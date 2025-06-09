from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a13_plan_listen_logic._test_util.example_listen_atoms import (
    get_atom_example_conceptunit_ball,
    get_atom_example_conceptunit_knee,
    get_atom_example_conceptunit_sports,
    get_atom_example_factunit_knee,
)


def yao_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Yao", _pack_id=37, face_name="Sue")


def get_sue_packunit() -> PackUnit:
    return packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")


def sue_1planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_2planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit


def sue_3planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_ball())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    return x_packunit


def sue_4planatoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(owner_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._plandelta.set_planatom(get_atom_example_factunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_ball())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_knee())
    x_packunit._plandelta.set_planatom(get_atom_example_conceptunit_sports())
    return x_packunit
