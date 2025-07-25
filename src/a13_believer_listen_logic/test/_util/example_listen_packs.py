from src.a09_pack_logic.pack import PackUnit, packunit_shop
from src.a13_believer_listen_logic.test._util.example_listen_atoms import (
    get_atom_example_factunit_knee,
    get_atom_example_planunit_ball,
    get_atom_example_planunit_knee,
    get_atom_example_planunit_sports,
)


def yao_sue_packunit() -> PackUnit:
    return packunit_shop(believer_name="Yao", _pack_id=37, face_name="Sue")


def get_sue_packunit() -> PackUnit:
    return packunit_shop(believer_name="Sue", _pack_id=37, face_name="Yao")


def sue_1believeratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(believer_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_sports())
    return x_packunit


def sue_2believeratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(believer_name="Sue", _pack_id=53, face_name="Yao")
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_knee())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_sports())
    return x_packunit


def sue_3believeratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(believer_name="Sue", _pack_id=37, face_name="Yao")
    x_packunit._believerdelta.set_believeratom(get_atom_example_factunit_knee())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_ball())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_knee())
    return x_packunit


def sue_4believeratoms_packunit() -> PackUnit:
    x_packunit = packunit_shop(believer_name="Sue", _pack_id=47, face_name="Yao")
    x_packunit._believerdelta.set_believeratom(get_atom_example_factunit_knee())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_ball())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_knee())
    x_packunit._believerdelta.set_believeratom(get_atom_example_planunit_sports())
    return x_packunit
