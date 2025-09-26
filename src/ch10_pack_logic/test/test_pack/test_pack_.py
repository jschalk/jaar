from pytest import raises as pytest_raises
from src.ch01_data_toolbox.dict_toolbox import x_is_json
from src.ch04_group_logic.voice import voiceunit_shop
from src.ch06_plan_logic.plan import get_default_moment_label
from src.ch07_belief_logic.belief_main import beliefunit_shop
from src.ch09_belief_atom_logic.atom_main import beliefatom_shop
from src.ch10_pack_logic._ref.ch10_keywords import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
    belief_name_str,
    belief_voiceunit_str,
    event_int_str,
    face_name_str,
    moment_label_str,
    voice_cred_points_str,
    voice_debt_points_str,
    voice_name_str,
)
from src.ch10_pack_logic._ref.ch10_semantic_types import FaceName, default_knot_if_None
from src.ch10_pack_logic.delta import beliefdelta_shop
from src.ch10_pack_logic.pack import (
    PackUnit,
    get_init_pack_id_if_None,
    get_packunit_from_json,
    init_pack_id,
    packunit_shop,
)
from src.ch10_pack_logic.test._util.ch10_examples import (
    get_atom_example_planunit_sports,
    get_beliefdelta_sue_example,
)


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"
    assert not FaceName(f"cookie{default_knot_if_None()}").is_name()


def test_init_pack_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_pack_id() == 0


def test_get_init_pack_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_pack_id_if_None() == init_pack_id()
    assert get_init_pack_id_if_None(None) == init_pack_id()
    assert get_init_pack_id_if_None(1) == 1


def test_PackUnit_Exists():
    # ESTABLISH / WHEN
    x_packunit = PackUnit()

    # THEN
    assert not x_packunit.face_name
    assert not x_packunit.moment_label
    assert not x_packunit.belief_name
    assert not x_packunit._pack_id
    assert not x_packunit._beliefdelta
    assert not x_packunit._delta_start
    assert not x_packunit._packs_dir
    assert not x_packunit._atoms_dir
    assert not x_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_packunit = packunit_shop(belief_name=bob_str)

    # THEN
    assert not bob_packunit.face_name
    assert bob_packunit.moment_label == get_default_moment_label()
    assert bob_packunit.belief_name == bob_str
    assert bob_packunit._pack_id == 0
    assert bob_packunit._beliefdelta == beliefdelta_shop()
    assert bob_packunit._delta_start == 0
    assert not bob_packunit._packs_dir
    assert not bob_packunit._atoms_dir
    assert not bob_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_pack_id = 13
    sue_str = "Sue"
    bob_beliefdelta = get_beliefdelta_sue_example()
    bob_delta_start = 6
    bob_packs_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    amy45_str = "amy45"
    amy45_e5_event_int = 5

    # WHEN
    bob_packunit = packunit_shop(
        face_name=sue_str,
        belief_name=bob_str,
        moment_label=amy45_str,
        _pack_id=bob_pack_id,
        _beliefdelta=bob_beliefdelta,
        _delta_start=bob_delta_start,
        _packs_dir=bob_packs_dir,
        _atoms_dir=bob_atoms_dir,
        event_int=amy45_e5_event_int,
    )

    # THEN
    assert bob_packunit.face_name == sue_str
    assert bob_packunit.belief_name == bob_str
    assert bob_packunit.moment_label == amy45_str
    assert bob_packunit._pack_id == bob_pack_id
    assert bob_packunit._beliefdelta == bob_beliefdelta
    assert bob_packunit._delta_start == bob_delta_start
    assert bob_packunit._packs_dir == bob_packs_dir
    assert bob_packunit._atoms_dir == bob_atoms_dir
    assert bob_packunit.event_int == amy45_e5_event_int


def test_packunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_packunit = packunit_shop(belief_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_packunit.belief_name == bob_str
    assert bob_packunit.face_name == yao_str


def test_PackUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(belief_name=bob_str)
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
    bob_packunit = packunit_shop(belief_name=bob_str)
    yao_str = "Yao"
    bob_packunit.set_face(yao_str)
    assert bob_packunit.face_name == yao_str

    # WHEN
    bob_packunit.del_face()

    # THEN
    assert bob_packunit.face_name != yao_str
    assert bob_packunit.face_name is None


def test_PackUnit_set_beliefdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(belief_name=bob_str)
    assert bob_packunit._beliefdelta == beliefdelta_shop()

    # WHEN
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    bob_packunit.set_beliefdelta(x_beliefdelta)

    # THEN
    assert bob_packunit._beliefdelta == x_beliefdelta


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


def test_PackUnit_beliefatom_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_beliefdelta = beliefdelta_shop()
    bob_packunit = packunit_shop(belief_name=bob_str)
    bob_packunit.set_beliefdelta(x_beliefdelta)

    # WHEN
    sports_beliefatom = get_atom_example_planunit_sports()

    # THEN
    assert bob_packunit.beliefatom_exists(sports_beliefatom) is False

    # WHEN
    x_beliefdelta.set_beliefatom(sports_beliefatom)
    bob_packunit.set_beliefdelta(x_beliefdelta)

    # THEN
    assert bob_packunit.beliefatom_exists(sports_beliefatom)


def test_PackUnit_del_beliefdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    bob_packunit = packunit_shop(belief_name=bob_str, _beliefdelta=x_beliefdelta)
    assert bob_packunit._beliefdelta != beliefdelta_shop()
    assert bob_packunit._beliefdelta == x_beliefdelta

    # WHEN
    bob_packunit.del_beliefdelta()

    # THEN
    assert bob_packunit._beliefdelta == beliefdelta_shop()


def test_PackUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_packunit = packunit_shop(
        moment_label=amy45_str, belief_name=bob_str, event_int=amy45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    assert x_dict.get(moment_label_str()) is not None
    assert x_dict.get(moment_label_str()) == amy45_str
    assert x_dict.get(belief_name_str()) is not None
    assert x_dict.get(belief_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == sue_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == amy45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == beliefdelta_shop().get_ordered_beliefatoms()
    assert x_dict.get(delta_str) == {}


def test_PackUnit_get_step_dict_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_beliefdelta.get_ordered_beliefatoms()
    sue_beliefatoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_beliefdelta.get_sorted_beliefatoms())=}")
    print(f"{sue_beliefatoms_dict.keys()=}")
    # print(f"{sue_beliefatoms_dict.get(0)=}")
    assert sue_beliefatoms_dict.get(2) is None
    assert sue_beliefatoms_dict.get(0) is not None
    assert sue_beliefatoms_dict.get(1) is not None


def test_PackUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(
        bob_str, _beliefdelta=sue_beliefdelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_beliefdelta.get_ordered_beliefatoms(
        x_delta_start
    )
    sue_beliefatoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_beliefdelta.get_sorted_beliefatoms())=}")
    print(f"{sue_beliefatoms_dict.keys()=}")
    # print(f"{sue_beliefatoms_dict.get(0)=}")
    assert sue_beliefatoms_dict.get(x_delta_start + 2) is None
    assert sue_beliefatoms_dict.get(x_delta_start + 0) is not None
    assert sue_beliefatoms_dict.get(x_delta_start + 1) is not None


def test_PackUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_packunit = packunit_shop(
        moment_label=amy45_str, belief_name=bob_str, event_int=amy45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    assert total_dict.get(moment_label_str()) is not None
    assert total_dict.get(moment_label_str()) == amy45_str
    assert total_dict.get(belief_name_str()) is not None
    assert total_dict.get(belief_name_str()) == bob_str
    assert total_dict.get(face_name_str()) is not None
    assert total_dict.get(face_name_str()) == sue_str
    assert total_dict.get(event_int_str()) is not None
    assert total_dict.get(event_int_str()) == amy45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_PackUnit_get_serializable_dict_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_beliefdelta.get_ordered_dict()


def test_PackUnit_get_json_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    generated_json = bob_packunit.get_json()

    # THEN
    assert generated_json
    print(f"{generated_json=}")
    expected_json = """{
  "belief_name": "Bob",
  "delta": {
    "0": {
      "crud": "DELETE",
      "dimen": "belief_voiceunit",
      "jkeys": {
        "voice_name": "Sue"
      },
      "jvalues": {}
    },
    "1": {
      "crud": "UPDATE",
      "dimen": "beliefunit",
      "jkeys": {},
      "jvalues": {
        "credor_respect": 77
      }
    }
  },
  "event_int": null,
  "face_name": null,
  "moment_label": "ZZ"
}"""
    assert generated_json == expected_json


def test_get_packunit_from_json_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _beliefdelta=sue_beliefdelta, event_int=778)

    # WHEN
    generated_bob_packunit = get_packunit_from_json(bob_packunit.get_json())

    # THEN
    assert generated_bob_packunit
    assert generated_bob_packunit.face_name == bob_packunit.face_name
    assert generated_bob_packunit.event_int == bob_packunit.event_int
    assert generated_bob_packunit.moment_label == bob_packunit.moment_label
    assert generated_bob_packunit._beliefdelta == bob_packunit._beliefdelta
    assert generated_bob_packunit == bob_packunit


def test_PackUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_beliefdelta(sue_beliefdelta)
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
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_beliefdelta(sue_beliefdelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(yao_str)
    bob_packunit.event_int = event5_int

    # WHEN
    x_dict = bob_packunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(belief_name_str()) is not None
    assert x_dict.get(belief_name_str()) == bob_str
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
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_beliefdelta(sue_beliefdelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(sue_str)
    bob_packunit.set_face(yao_str)

    # WHEN
    delta_json = bob_packunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)


def test_PackUnit_add_beliefatom_Sets_BeliefUnit_voiceunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_voice_cred_points = 55
    bob_voice_debt_points = 66
    bob_voiceunit = voiceunit_shop(
        bob_str, bob_voice_cred_points, bob_voice_debt_points
    )
    cw_str = voice_cred_points_str()
    dw_str = voice_debt_points_str()
    print(f"{bob_voiceunit.to_dict()=}")
    bob_required_dict = {
        voice_name_str(): bob_voiceunit.to_dict().get(voice_name_str())
    }
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._beliefdelta.beliefatoms == {}

    # WHEN
    bob_packunit.add_beliefatom(
        dimen=belief_voiceunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._beliefdelta.beliefatoms) == 1
    assert (
        bob_packunit._beliefdelta.beliefatoms.get(INSERT_str())
        .get(belief_voiceunit_str())
        .get(bob_str)
        is not None
    )


def test_PackUnit_get_edited_belief_ReturnsObj_BeliefUnit_insert_voice():
    # ESTABLISH
    sue_str = "Sue"
    sue_packunit = packunit_shop(sue_str)

    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    assert before_sue_beliefunit.voice_exists(yao_str)
    assert before_sue_beliefunit.voice_exists(zia_str) is False
    dimen = belief_voiceunit_str()
    x_beliefatom = beliefatom_shop(dimen, INSERT_str())
    x_beliefatom.set_jkey(voice_name_str(), zia_str)
    x_voice_cred_points = 55
    x_voice_debt_points = 66
    x_beliefatom.set_jvalue("voice_cred_points", x_voice_cred_points)
    x_beliefatom.set_jvalue("voice_debt_points", x_voice_debt_points)
    sue_packunit._beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{sue_packunit._beliefdelta.beliefatoms.keys()=}")

    # WHEN
    after_sue_beliefunit = sue_packunit.get_pack_edited_belief(before_sue_beliefunit)

    # THEN
    yao_voiceunit = after_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = after_sue_beliefunit.get_voice(zia_str)
    assert yao_voiceunit is not None
    assert zia_voiceunit is not None
    assert zia_voiceunit.voice_cred_points == x_voice_cred_points
    assert zia_voiceunit.voice_debt_points == x_voice_debt_points


def test_PackUnit_get_edited_belief_RaisesErrorWhenpackAttrsAndBeliefAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    amy23_str = "amy23"
    bob_packunit = packunit_shop(yao_str, xia_str, moment_label=amy23_str)
    sue_str = "Sue"
    amy45_str = "amy45"
    before_sue_beliefunit = beliefunit_shop(sue_str, moment_label=amy45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_packunit.get_pack_edited_belief(before_sue_beliefunit)
    assert str(excinfo.value) == "pack belief conflict amy23 != amy45 or Yao != Sue"


def test_PackUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_voice_cred_points = 55
    bob_voice_debt_points = 66
    bob_voiceunit = voiceunit_shop(
        bob_str, bob_voice_cred_points, bob_voice_debt_points
    )
    cw_str = voice_cred_points_str()
    dw_str = voice_debt_points_str()
    print(f"{bob_voiceunit.to_dict()=}")
    bob_required_dict = {
        voice_name_str(): bob_voiceunit.to_dict().get(voice_name_str())
    }
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._beliefdelta.beliefatoms == {}
    assert bob_packunit.is_empty()

    # WHEN
    bob_packunit.add_beliefatom(
        dimen=belief_voiceunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._beliefdelta.beliefatoms) == 1
    assert bob_packunit.is_empty() is False

    # WHEN
    bob_packunit._beliefdelta.beliefatoms = {}

    # THEN
    assert bob_packunit.is_empty()

    # Test for UPDATE_str operation
    bob_packunit_update = packunit_shop(bob_str)
    bob_packunit_update.add_beliefatom(
        dimen=belief_voiceunit_str(),
        crud_str=UPDATE_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_packunit_update._beliefdelta.beliefatoms) == 1
    assert bob_packunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_packunit_delete = packunit_shop(bob_str)
    bob_packunit_delete.add_beliefatom(
        dimen=belief_voiceunit_str(),
        crud_str=DELETE_str(),
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_packunit_delete._beliefdelta.beliefatoms) == 1
    assert bob_packunit_delete.is_empty() is False
