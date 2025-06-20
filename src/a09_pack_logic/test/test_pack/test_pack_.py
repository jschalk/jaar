from pytest import raises as pytest_raises
from src.a00_data_toolbox.dict_toolbox import x_is_json
from src.a02_finance_logic.test._util.a02_str import owner_name_str, vow_label_str
from src.a03_group_logic.acct import acctunit_shop
from src.a05_concept_logic.concept import get_default_vow_label
from src.a06_plan_logic.plan import planunit_shop
from src.a06_plan_logic.test._util.a06_str import (
    acct_name_str,
    credit_score_str,
    debt_score_str,
    plan_acctunit_str,
)
from src.a08_plan_atom_logic.atom import planatom_shop
from src.a08_plan_atom_logic.test._util.a08_str import (
    DELETE_str,
    INSERT_str,
    UPDATE_str,
)
from src.a09_pack_logic.delta import plandelta_shop
from src.a09_pack_logic.pack import (
    PackUnit,
    get_init_pack_id_if_None,
    get_packunit_from_json,
    init_pack_id,
    packunit_shop,
)
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a09_pack_logic.test._util.example_atoms import (
    get_atom_example_conceptunit_sports,
)
from src.a09_pack_logic.test._util.example_deltas import get_plandelta_sue_example


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
    assert not x_packunit.vow_label
    assert not x_packunit.owner_name
    assert not x_packunit._pack_id
    assert not x_packunit._plandelta
    assert not x_packunit._delta_start
    assert not x_packunit._packs_dir
    assert not x_packunit._atoms_dir
    assert not x_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_packunit = packunit_shop(owner_name=bob_str)

    # THEN
    assert not bob_packunit.face_name
    assert bob_packunit.vow_label == get_default_vow_label()
    assert bob_packunit.owner_name == bob_str
    assert bob_packunit._pack_id == 0
    assert bob_packunit._plandelta == plandelta_shop()
    assert bob_packunit._delta_start == 0
    assert not bob_packunit._packs_dir
    assert not bob_packunit._atoms_dir
    assert not bob_packunit.event_int


def test_packunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_pack_id = 13
    sue_str = "Sue"
    bob_plandelta = get_plandelta_sue_example()
    bob_delta_start = 6
    bob_packs_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    accord45_str = "accord45"
    accord45_e5_event_int = 5

    # WHEN
    bob_packunit = packunit_shop(
        face_name=sue_str,
        owner_name=bob_str,
        vow_label=accord45_str,
        _pack_id=bob_pack_id,
        _plandelta=bob_plandelta,
        _delta_start=bob_delta_start,
        _packs_dir=bob_packs_dir,
        _atoms_dir=bob_atoms_dir,
        event_int=accord45_e5_event_int,
    )

    # THEN
    assert bob_packunit.face_name == sue_str
    assert bob_packunit.owner_name == bob_str
    assert bob_packunit.vow_label == accord45_str
    assert bob_packunit._pack_id == bob_pack_id
    assert bob_packunit._plandelta == bob_plandelta
    assert bob_packunit._delta_start == bob_delta_start
    assert bob_packunit._packs_dir == bob_packs_dir
    assert bob_packunit._atoms_dir == bob_atoms_dir
    assert bob_packunit.event_int == accord45_e5_event_int


def test_packunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_packunit = packunit_shop(owner_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_packunit.owner_name == bob_str
    assert bob_packunit.face_name == yao_str


def test_PackUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(owner_name=bob_str)
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
    bob_packunit = packunit_shop(owner_name=bob_str)
    yao_str = "Yao"
    bob_packunit.set_face(yao_str)
    assert bob_packunit.face_name == yao_str

    # WHEN
    bob_packunit.del_face()

    # THEN
    assert bob_packunit.face_name != yao_str
    assert bob_packunit.face_name is None


def test_PackUnit_set_plandelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(owner_name=bob_str)
    assert bob_packunit._plandelta == plandelta_shop()

    # WHEN
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(get_atom_example_conceptunit_sports())
    bob_packunit.set_plandelta(x_plandelta)

    # THEN
    assert bob_packunit._plandelta == x_plandelta


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


def test_PackUnit_planatom_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_plandelta = plandelta_shop()
    bob_packunit = packunit_shop(owner_name=bob_str)
    bob_packunit.set_plandelta(x_plandelta)

    # WHEN
    sports_planatom = get_atom_example_conceptunit_sports()

    # THEN
    assert bob_packunit.planatom_exists(sports_planatom) is False

    # WHEN
    x_plandelta.set_planatom(sports_planatom)
    bob_packunit.set_plandelta(x_plandelta)

    # THEN
    assert bob_packunit.planatom_exists(sports_planatom)


def test_PackUnit_del_plandelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_plandelta = plandelta_shop()
    x_plandelta.set_planatom(get_atom_example_conceptunit_sports())
    bob_packunit = packunit_shop(owner_name=bob_str, _plandelta=x_plandelta)
    assert bob_packunit._plandelta != plandelta_shop()
    assert bob_packunit._plandelta == x_plandelta

    # WHEN
    bob_packunit.del_plandelta()

    # THEN
    assert bob_packunit._plandelta == plandelta_shop()


def test_PackUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_packunit = packunit_shop(
        vow_label=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    assert x_dict.get(vow_label_str()) is not None
    assert x_dict.get(vow_label_str()) == accord45_str
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str
    assert x_dict.get(face_name_str()) is not None
    assert x_dict.get(face_name_str()) == sue_str
    assert x_dict.get(event_int_str()) is not None
    assert x_dict.get(event_int_str()) == accord45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == plandelta_shop().get_ordered_planatoms()
    assert x_dict.get(delta_str) == {}


def test_PackUnit_get_step_dict_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_plandelta = get_plandelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _plandelta=sue_plandelta)

    # WHEN
    x_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == sue_plandelta.get_ordered_planatoms()
    sue_planatoms_dict = x_dict.get(delta_str)
    print(f"{len(sue_plandelta.get_sorted_planatoms())=}")
    print(f"{sue_planatoms_dict.keys()=}")
    # print(f"{sue_planatoms_dict.get(0)=}")
    assert sue_planatoms_dict.get(2) is None
    assert sue_planatoms_dict.get(0) is not None
    assert sue_planatoms_dict.get(1) is not None


def test_PackUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(
        bob_str, _plandelta=sue_plandelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_packunit.get_step_dict()

    # THEN
    delta_str = "delta"
    assert step_dict.get(delta_str) is not None
    assert step_dict.get(delta_str) == sue_plandelta.get_ordered_planatoms(
        x_delta_start
    )
    sue_planatoms_dict = step_dict.get(delta_str)
    print(f"{len(sue_plandelta.get_sorted_planatoms())=}")
    print(f"{sue_planatoms_dict.keys()=}")
    # print(f"{sue_planatoms_dict.get(0)=}")
    assert sue_planatoms_dict.get(x_delta_start + 2) is None
    assert sue_planatoms_dict.get(x_delta_start + 0) is not None
    assert sue_planatoms_dict.get(x_delta_start + 1) is not None


def test_PackUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    accord45_str = "accord45"
    accord45_e5_int = 5
    bob_packunit = packunit_shop(
        vow_label=accord45_str, owner_name=bob_str, event_int=accord45_e5_int
    )
    bob_packunit.set_face(sue_str)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    assert total_dict.get(vow_label_str()) is not None
    assert total_dict.get(vow_label_str()) == accord45_str
    assert total_dict.get(owner_name_str()) is not None
    assert total_dict.get(owner_name_str()) == bob_str
    assert total_dict.get(face_name_str()) is not None
    assert total_dict.get(face_name_str()) == sue_str
    assert total_dict.get(event_int_str()) is not None
    assert total_dict.get(event_int_str()) == accord45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_PackUnit_get_serializable_dict_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_plandelta = get_plandelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _plandelta=sue_plandelta)

    # WHEN
    total_dict = bob_packunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_plandelta.get_ordered_dict()


def test_PackUnit_get_json_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_plandelta = get_plandelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _plandelta=sue_plandelta)

    # WHEN
    generated_json = bob_packunit.get_json()

    # THEN
    assert generated_json
    print(f"{generated_json=}")
    expected_json = """{
  "delta": {
    "0": {
      "crud": "DELETE",
      "dimen": "plan_acctunit",
      "jkeys": {
        "acct_name": "Sue"
      },
      "jvalues": {}
    },
    "1": {
      "crud": "UPDATE",
      "dimen": "planunit",
      "jkeys": {},
      "jvalues": {
        "credor_respect": 77
      }
    }
  },
  "event_int": null,
  "face_name": null,
  "owner_name": "Bob",
  "vow_label": "ZZ"
}"""
    assert generated_json == expected_json


def test_get_packunit_from_json_ReturnsObj_WithPlanDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_plandelta = get_plandelta_sue_example()
    bob_packunit = packunit_shop(bob_str, _plandelta=sue_plandelta, event_int=778)

    # WHEN
    generated_bob_packunit = get_packunit_from_json(bob_packunit.get_json())

    # THEN
    assert generated_bob_packunit
    assert generated_bob_packunit.face_name == bob_packunit.face_name
    assert generated_bob_packunit.event_int == bob_packunit.event_int
    assert generated_bob_packunit.vow_label == bob_packunit.vow_label
    assert generated_bob_packunit._plandelta == bob_packunit._plandelta
    assert generated_bob_packunit == bob_packunit


def test_PackUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_plandelta(sue_plandelta)
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
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_plandelta(sue_plandelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(yao_str)
    bob_packunit.event_int = event5_int

    # WHEN
    x_dict = bob_packunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(owner_name_str()) is not None
    assert x_dict.get(owner_name_str()) == bob_str
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
    sue_plandelta = get_plandelta_sue_example()
    x_delta_start = 7
    bob_packunit = packunit_shop(bob_str)
    bob_packunit.set_plandelta(sue_plandelta)
    bob_packunit.set_delta_start(x_delta_start)
    bob_packunit.set_face(sue_str)
    bob_packunit.set_face(yao_str)

    # WHEN
    delta_json = bob_packunit.get_deltametric_json()

    # THEN
    assert x_is_json(delta_json)


def test_PackUnit_add_planatom_CorrectlySets_PlanUnit_acctunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_credit_score = 55
    bob_debt_score = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_score, bob_debt_score)
    cw_str = credit_score_str()
    dw_str = debt_score_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._plandelta.planatoms == {}

    # WHEN
    bob_packunit.add_planatom(
        dimen=plan_acctunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._plandelta.planatoms) == 1
    assert (
        bob_packunit._plandelta.planatoms.get(INSERT_str())
        .get(plan_acctunit_str())
        .get(bob_str)
        is not None
    )


def test_PackUnit_get_edited_plan_ReturnsObj_PlanUnit_insert_acct():
    # ESTABLISH
    sue_str = "Sue"
    sue_packunit = packunit_shop(sue_str)

    before_sue_planunit = planunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_planunit.add_acctunit(yao_str)
    assert before_sue_planunit.acct_exists(yao_str)
    assert before_sue_planunit.acct_exists(zia_str) is False
    dimen = plan_acctunit_str()
    x_planatom = planatom_shop(dimen, INSERT_str())
    x_planatom.set_jkey(acct_name_str(), zia_str)
    x_credit_score = 55
    x_debt_score = 66
    x_planatom.set_jvalue("credit_score", x_credit_score)
    x_planatom.set_jvalue("debt_score", x_debt_score)
    sue_packunit._plandelta.set_planatom(x_planatom)
    print(f"{sue_packunit._plandelta.planatoms.keys()=}")

    # WHEN
    after_sue_planunit = sue_packunit.get_edited_plan(before_sue_planunit)

    # THEN
    yao_acctunit = after_sue_planunit.get_acct(yao_str)
    zia_acctunit = after_sue_planunit.get_acct(zia_str)
    assert yao_acctunit is not None
    assert zia_acctunit is not None
    assert zia_acctunit.credit_score == x_credit_score
    assert zia_acctunit.debt_score == x_debt_score


def test_PackUnit_get_edited_plan_RaisesErrorWhenpackAttrsAndPlanAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    accord23_str = "accord23"
    bob_packunit = packunit_shop(yao_str, xia_str, vow_label=accord23_str)
    sue_str = "Sue"
    accord45_str = "accord45"
    before_sue_planunit = planunit_shop(sue_str, vow_label=accord45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_packunit.get_edited_plan(before_sue_planunit)
    assert str(excinfo.value) == "pack plan conflict accord23 != accord45 or Yao != Sue"


def test_PackUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_packunit = packunit_shop(bob_str)
    bob_credit_score = 55
    bob_debt_score = 66
    bob_acctunit = acctunit_shop(bob_str, bob_credit_score, bob_debt_score)
    cw_str = credit_score_str()
    dw_str = debt_score_str()
    print(f"{bob_acctunit.get_dict()=}")
    bob_required_dict = {acct_name_str(): bob_acctunit.get_dict().get(acct_name_str())}
    bob_optional_dict = {cw_str: bob_acctunit.get_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_acctunit.get_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_packunit._plandelta.planatoms == {}
    assert bob_packunit.is_empty()

    # WHEN
    bob_packunit.add_planatom(
        dimen=plan_acctunit_str(),
        crud_str=INSERT_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_packunit._plandelta.planatoms) == 1
    assert bob_packunit.is_empty() is False

    # WHEN
    bob_packunit._plandelta.planatoms = {}

    # THEN
    assert bob_packunit.is_empty()

    # Test for UPDATE_str operation
    bob_packunit_update = packunit_shop(bob_str)
    bob_packunit_update.add_planatom(
        dimen=plan_acctunit_str(),
        crud_str=UPDATE_str(),
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_packunit_update._plandelta.planatoms) == 1
    assert bob_packunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_packunit_delete = packunit_shop(bob_str)
    bob_packunit_delete.add_planatom(
        dimen=plan_acctunit_str(),
        crud_str=DELETE_str(),
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_packunit_delete._plandelta.planatoms) == 1
    assert bob_packunit_delete.is_empty() is False
