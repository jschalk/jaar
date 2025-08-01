from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a03_group_logic.partner import partnerunit_shop
from src.a05_plan_logic.plan import get_default_belief_label
from src.a06_believer_logic.believer_main import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import (
    believer_partnerunit_str,
    partner_cred_points_str,
    partner_debt_points_str,
    partner_name_str,
)
from src.a08_believer_atom_logic.atom_main import believeratom_shop
from src.a08_believer_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import believerdelta_shop
from src.a09_pack_logic.pack import (
    PackUnit,
    get_init_pack_id_if_None,
    get_packunit_from_json,
    init_pack_id,
    packunit_shop,
)
from src.a09_pack_logic.test._util.a09_str import (
    belief_label_str,
    believer_name_str,
    event_int_str,
    face_name_str,
)
from src.a09_pack_logic.test._util.example_atoms import get_atom_example_planunit_sports
from src.a09_pack_logic.test._util.example_deltas import get_believerdelta_sue_example


def test_init_pack_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_pack_id() == 0


def test_get_init_pack_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_pack_id_if_None() == init_pack_id()
    assert get_init_pack_id_if_None(None) == init_pack_id()
    assert get_init_pack_id_if_None(1) == 1


def test_PackUnit_exists():
    # ESTABLISH / WHEN
    x_packunit = PackUnit()

    # THEN
    assert not x_packunit.face_name
    assert not x_packunit.belief_label
    assert not x_packunit.believer_name
    assert not x_packunit._pack_id
    assert not x_packunit._believerdelta
    assert not x_packunit._delta_start
    assert not x_packunit._packs_dir
    assert not x_packunit._atoms_dir
    assert not x_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_packunit = packunit_shop(believer_name=bob_str)

    # THEN
    assert not bob_packunit.face_name
    assert bob_packunit.belief_label == get_default_belief_label()
    assert bob_packunit.believer_name == bob_str
    assert bob_packunit._pack_id == 0
    assert bob_packunit._believerdelta == believerdelta_shop()
    assert bob_packunit._delta_start == 0
    assert not bob_packunit._packs_dir
    assert not bob_packunit._atoms_dir
    assert not bob_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_pack_id = 13
    sue_str = "Sue"
    bob_believerdelta = get_believerdelta_sue_example()
    bob_delta_start = 6
    bob_packs_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    amy45_str = "amy45"
    amy45_e5_event_int = 5

    # WHEN
    bob_packunit = packunit_shop(
        face_name=sue_str,
        believer_name=bob_str,
        belief_label=amy45_str,
        _pack_id=bob_pack_id,
        _believerdelta=bob_believerdelta,
        _delta_start=bob_delta_start,
        _packs_dir=bob_packs_dir,
        _atoms_dir=bob_atoms_dir,
        event_int=amy45_e5_event_int,
    )

    # THEN
    assert bob_packunit.face_name == sue_str
    assert bob_packunit.believer_name == bob_str
    assert bob_packunit.belief_label == amy45_str
    assert bob_packunit._pack_id == bob_pack_id
    assert bob_packunit._believerdelta == bob_believerdelta
    assert bob_packunit._delta_start == bob_delta_start
    assert bob_packunit._packs_dir == bob_packs_dir
    assert bob_packunit._atoms_dir == bob_atoms_dir
    assert bob_packunit.event_int == amy45_e5_event_int


def test_packunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_packunit = packunit_shop(believer_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_packunit.believer_name == bob_str
    assert bob_packunit.face_name == yao_str


def test_PackUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(believer_name=bob_str)
    sue_str = "Sue"
    assert bob_packunit.face_name is None
    assert bob_packunit.face_name != sue_str

    # WHEN
    bob_packunit.set_face(sue_str)

    # THEN
    assert bob_packunit.face_name == sue_str


def test_PackUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(believer_name=bob_str)
    yao_str = "Yao"
    bob_packunit.set_face(yao_str)
    assert bob_packunit.face_name == yao_str

    # WHEN
    bob_packunit.del_face()

    # THEN
    assert bob_packunit.face_name != yao_str
    assert bob_packunit.face_name is None


def test_PackUnit_set_believerdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(believer_name=bob_str)
    assert bob_packunit._believerdelta == believerdelta_shop()

    # WHEN
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(get_atom_example_planunit_sports())
    bob_packunit.set_believerdelta(x_believerdelta)

    # THEN
    assert bob_packunit._believerdelta == x_believerdelta


def test_PackUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    assert bob_packunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_packunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_packunit._delta_start == x_delta_start


def test_PackUnit_believeratom_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_believerdelta = believerdelta_shop()
    bob_packunit = packunit_shop(believer_name=bob_str)
    bob_packunit.set_believerdelta(x_believerdelta)

    # WHEN
    sports_believeratom = get_atom_example_planunit_sports()

    # THEN
    assert bob_packunit.believeratom_exists(sports_believeratom) is False

    # WHEN
    x_believerdelta.set_believeratom(sports_believeratom)
    bob_packunit.set_believerdelta(x_believerdelta)

    # THEN
    assert bob_packunit.believeratom_exists(sports_believeratom)


def test_PackUnit_del_believerdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_believerdelta = believerdelta_shop()
    x_believerdelta.set_believeratom(get_atom_example_planunit_sports())
    bob_packunit = packunit_shop(believer_name=bob_str, _believerdelta=x_believerdelta)
    assert bob_packunit._believerdelta != believerdelta_shop()
    assert bob_packunit._believerdelta == x_believerdelta

    # WHEN
    bob_packunit.del_believerdelta()

    # THEN
    assert bob_packunit._believerdelta == believerdelta_shop()


def test_PackUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_packunit = packunit_shop(
        belief_label=amy45_str, believer_name=bob_str, event_int=amy45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    assert x_dict.get(belief_label_str()) is not None
    assert x_dict.get(belief_label_str()) == amy45_str
    assert x_dict.get(believer_name_str()) is not None
    assert x_dict.get(believer_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == sue_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == amy45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == believerdelta_shop().get_ordered_believeratoms()
    assert x_dict.get(delta_str) == {}


def test_PackUnit_get_step_dict_ReturnsObj_WithBelieverDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_believerdelta = get_believerdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _believerdelta=sue_believerdelta)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_believerdelta.get_ordered_believeratoms()
    sue_believeratoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_believerdelta.get_sorted_believeratoms())=}")
    print(f"{sue_believeratoms_dict.keys()=}")
    # print(f"{sue_believeratoms_dict.get(0)=}")
    assert sue_believeratoms_dict.get(2) is None
    assert sue_believeratoms_dict.get(0) is not None
    assert sue_believeratoms_dict.get(1) is not None


def test_PackUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_believerdelta = get_believerdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(
        bob_str, _believerdelta=sue_believerdelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_believerdelta.get_ordered_believeratoms(
        x_delta_start
    )
    sue_believeratoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_believerdelta.get_sorted_believeratoms())=}")
    print(f"{sue_believeratoms_dict.keys()=}")
    # print(f"{sue_believeratoms_dict.get(0)=}")
    assert sue_believeratoms_dict.get(x_delta_start + 2) is None
    assert sue_believeratoms_dict.get(x_delta_start + 0) is not None
    assert sue_believeratoms_dict.get(x_delta_start + 1) is not None


def test_PackUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_packunit = packunit_shop(
        belief_label=amy45_str, believer_name=bob_str, event_int=amy45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    assert total_dict.get(belief_label_str()) is not None
    assert total_dict.get(belief_label_str()) == amy45_str
    assert total_dict.get(believer_name_str()) is not None
    assert total_dict.get(believer_name_str()) == bob_str
    assert total_dict.get(face_name_str()) is not None
    assert total_dict.get(face_name_str()) == sue_str
    assert total_dict.get(event_int_str()) is not None
    assert total_dict.get(event_int_str()) == amy45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_PackUnit_get_serializable_dict_ReturnsObj_WithBelieverDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_believerdelta = get_believerdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _believerdelta=sue_believerdelta)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_believerdelta.get_ordered_dict()


def test_PackUnit_get_json_ReturnsObj_WithBelieverDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_believerdelta = get_believerdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _believerdelta=sue_believerdelta)

    # WHEN
    generated_json = bob_packunit.get_json()

    # THEN
    assert generated_json
    print(f"{generated_json=}")
    expected_json = """{
  "belief_label": "ZZ",
  "believer_name": "Bob",
  "delta": {
    "0": {
      "crud": "DELETE",
      "dimen": "believer_partnerunit",
      "jkeys": {
        "partner_name": "Sue"
      },
      "jvalues": {}
    },
    "1": {
      "crud": "UPDATE",
      "dimen": "believerunit",
      "jkeys": {},
      "jvalues": {
        "credor_respect": 77
      }
    }
  },
  "event_int": null,
  "face_name": null
}"""
    assert generated_json == expected_json


def test_get_packunit_from_json_ReturnsObj_WithBelieverDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_believerdelta = get_believerdelta_sue_example()
    bob_packunit = packunit_shop(
        bob_str, _believerdelta=sue_believerdelta, event_int=778
    )

    # WHEN
    generated_bob_packunit = get_packunit_from_json(bob_packunit.get_json())

    # THEN
    assert generated_bob_packunit
    assert generated_bob_packunit.face_name == bob_packunit.face_name
    assert generated_bob_packunit.event_int == bob_packunit.event_int
    assert generated_bob_packunit.belief_label == bob_packunit.belief_label
    assert generated_bob_packunit._believerdelta == bob_packunit._believerdelta
    assert generated_bob_packunit == bob_packunit


def test_PackUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_believerdelta = get_believerdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_believerdelta(sue_believerdelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(yao_str)
    x_dict = bob_packunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_packunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_PackUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    event5_int = 5550
    sue_believerdelta = get_believerdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_believerdelta(sue_believerdelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(yao_str)
    bob_packunit.event_int = event5_int

    # WHEN
    x_dict = bob_packunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(believer_name_str()) is not None
    assert x_dict.get(believer_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == yao_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == event5_int

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_PackUnit_get_deltametric_json_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    sue_believerdelta = get_believerdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_believerdelta(sue_believerdelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(sue_str)
    bob_packunit.set_face(yao_str)

    # WHEN
    delta_json = bob_packunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)


def test_PackUnit_add_believeratom_CorrectlySets_BelieverUnit_partnerunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    print(f"{bob_partnerunit.get_dict()=}")
    bob_required_dict = {
        partner_name_str(): bob_partnerunit.get_dict().get(partner_name_str())
    }
    bob_optional_dict = {cw_str: bob_partnerunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._believerdelta.believeratoms == {}

    # WHEN
    bob_packunit.add_believeratom(
        dimen=believer_partnerunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._believerdelta.believeratoms) == 1
    assert (
        bob_packunit._believerdelta.believeratoms.get(INSERT_str())
        .get(believer_partnerunit_str())
        .get(bob_str)
        is not None
    )


def test_PackUnit_get_edited_believer_ReturnsObj_BelieverUnit_insert_partner():
    # ESTABLISH
    sue_str = "Sue"
    sue_packunit = packunit_shop(sue_str)

    before_sue_believerunit = believerunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_believerunit.add_partnerunit(yao_str)
    assert before_sue_believerunit.partner_exists(yao_str)
    assert before_sue_believerunit.partner_exists(zia_str) is False
    dimen = believer_partnerunit_str()
    x_believeratom = believeratom_shop(dimen, INSERT_str())
    x_believeratom.set_jkey(partner_name_str(), zia_str)
    x_partner_cred_points = 55
    x_partner_debt_points = 66
    x_believeratom.set_jvalue("partner_cred_points", x_partner_cred_points)
    x_believeratom.set_jvalue("partner_debt_points", x_partner_debt_points)
    sue_packunit._believerdelta.set_believeratom(x_believeratom)
    print(f"{sue_packunit._believerdelta.believeratoms.keys()=}")

    # WHEN
    after_sue_believerunit = sue_packunit.get_edited_believer(before_sue_believerunit)

    # THEN
    yao_partnerunit = after_sue_believerunit.get_partner(yao_str)
    zia_partnerunit = after_sue_believerunit.get_partner(zia_str)
    assert yao_partnerunit is not None
    assert zia_partnerunit is not None
    assert zia_partnerunit.partner_cred_points == x_partner_cred_points
    assert zia_partnerunit.partner_debt_points == x_partner_debt_points


def test_PackUnit_get_edited_believer_RaisesErrorWhenpackAttrsAndBelieverAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    amy23_str = "amy23"
    bob_packunit = packunit_shop(yao_str, xia_str, belief_label=amy23_str)
    sue_str = "Sue"
    amy45_str = "amy45"
    before_sue_believerunit = believerunit_shop(sue_str, belief_label=amy45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_packunit.get_edited_believer(before_sue_believerunit)
    assert str(excinfo.value) == "pack believer conflict amy23 != amy45 or Yao != Sue"


def test_PackUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_partner_cred_points = 55
    bob_partner_debt_points = 66
    bob_partnerunit = partnerunit_shop(
        bob_str, bob_partner_cred_points, bob_partner_debt_points
    )
    cw_str = partner_cred_points_str()
    dw_str = partner_debt_points_str()
    print(f"{bob_partnerunit.get_dict()=}")
    bob_required_dict = {
        partner_name_str(): bob_partnerunit.get_dict().get(partner_name_str())
    }
    bob_optional_dict = {cw_str: bob_partnerunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_partnerunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._believerdelta.believeratoms == {}
    assert bob_packunit.is_empty()

    # WHEN
    bob_packunit.add_believeratom(
        dimen=believer_partnerunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._believerdelta.believeratoms) == 1
    assert bob_packunit.is_empty() is False

    # WHEN
    bob_packunit._believerdelta.believeratoms = {}

    # THEN
    assert bob_packunit.is_empty()

    # Test for UPDATE_str operation
    bob_packunit_update = packunit_shop(bob_str)
    bob_packunit_update.add_believeratom(
        dimen=believer_partnerunit_str(),
        crud_str=UPDATE_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_packunit_update._believerdelta.believeratoms) == 1
    assert bob_packunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_packunit_delete = packunit_shop(bob_str)
    bob_packunit_delete.add_believeratom(
        dimen=believer_partnerunit_str(),
        crud_str=DELETE_str(),
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_packunit_delete._believerdelta.believeratoms) == 1
    assert bob_packunit_delete.is_empty() is False
