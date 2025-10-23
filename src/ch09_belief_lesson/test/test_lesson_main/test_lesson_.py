from pytest import raises as pytest_raises
from src.ch01_py.dict_toolbox import get_json_from_dict
from src.ch03_voice.voice import voiceunit_shop
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_default_first_label
from src.ch08_belief_atom.atom_main import beliefatom_shop
from src.ch09_belief_lesson._ref.ch09_semantic_types import (
    FaceName,
    default_knot_if_None,
)
from src.ch09_belief_lesson.delta import beliefdelta_shop
from src.ch09_belief_lesson.lesson_main import (
    LessonUnit,
    get_init_lesson_id_if_None,
    get_lessonunit_from_dict,
    init_lesson_id,
    lessonunit_shop,
)
from src.ch09_belief_lesson.test._util.ch09_examples import (
    get_atom_example_planunit_sports,
    get_beliefdelta_sue_example,
)
from src.ref.keywords import Ch09Keywords as kw


def test_FaceName_Exists():
    # ESTABLISH / WHEN / THEN
    assert FaceName() == ""
    assert FaceName("cookie") == "cookie"


def test_init_lesson_id_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert init_lesson_id() == 0


def test_get_init_lesson_id_if_None_ReturnsObj():
    # ESTABLISH / WHEN / THEN
    assert get_init_lesson_id_if_None() == init_lesson_id()
    assert get_init_lesson_id_if_None(None) == init_lesson_id()
    assert get_init_lesson_id_if_None(1) == 1


def test_LessonUnit_Exists():
    # ESTABLISH / WHEN
    x_lessonunit = LessonUnit()

    # THEN
    assert not x_lessonunit.face_name
    assert not x_lessonunit.moment_label
    assert not x_lessonunit.belief_name
    assert not x_lessonunit._lesson_id
    assert not x_lessonunit._beliefdelta
    assert not x_lessonunit._delta_start
    assert not x_lessonunit.lessons_dir
    assert not x_lessonunit.atoms_dir
    assert not x_lessonunit.spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"

    # WHEN
    bob_lessonunit = lessonunit_shop(belief_name=bob_str)

    # THEN
    assert not bob_lessonunit.face_name
    assert bob_lessonunit.moment_label == get_default_first_label()
    assert bob_lessonunit.belief_name == bob_str
    assert bob_lessonunit._lesson_id == 0
    assert bob_lessonunit._beliefdelta == beliefdelta_shop()
    assert bob_lessonunit._delta_start == 0
    assert not bob_lessonunit.lessons_dir
    assert not bob_lessonunit.atoms_dir
    assert not bob_lessonunit.spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithNonEmptyArgs():
    # ESTABLISH
    bob_str = "Bob"
    bob_lesson_id = 13
    sue_str = "Sue"
    bob_beliefdelta = get_beliefdelta_sue_example()
    bob_delta_start = 6
    bob_lessons_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"
    amy45_str = "amy45"
    amy45_e5_spark_num = 5

    # WHEN
    bob_lessonunit = lessonunit_shop(
        face_name=sue_str,
        belief_name=bob_str,
        moment_label=amy45_str,
        _lesson_id=bob_lesson_id,
        _beliefdelta=bob_beliefdelta,
        _delta_start=bob_delta_start,
        lessons_dir=bob_lessons_dir,
        atoms_dir=bob_atoms_dir,
        spark_num=amy45_e5_spark_num,
    )

    # THEN
    assert bob_lessonunit.face_name == sue_str
    assert bob_lessonunit.belief_name == bob_str
    assert bob_lessonunit.moment_label == amy45_str
    assert bob_lessonunit._lesson_id == bob_lesson_id
    assert bob_lessonunit._beliefdelta == bob_beliefdelta
    assert bob_lessonunit._delta_start == bob_delta_start
    assert bob_lessonunit.lessons_dir == bob_lessons_dir
    assert bob_lessonunit.atoms_dir == bob_atoms_dir
    assert bob_lessonunit.spark_num == amy45_e5_spark_num


def test_lessonunit_shop_ReturnsObjEstablishWithSomeArgs_v1():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"

    # WHEN
    bob_lessonunit = lessonunit_shop(belief_name=bob_str, face_name=yao_str)

    # THEN
    assert bob_lessonunit.belief_name == bob_str
    assert bob_lessonunit.face_name == yao_str


def test_LessonUnit_set_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(belief_name=bob_str)
    sue_str = "Sue"
    assert bob_lessonunit.face_name is None
    assert bob_lessonunit.face_name != sue_str

    # WHEN
    bob_lessonunit.set_face(sue_str)

    # THEN
    assert bob_lessonunit.face_name == sue_str


def test_LessonUnit_del_face_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(belief_name=bob_str)
    yao_str = "Yao"
    bob_lessonunit.set_face(yao_str)
    assert bob_lessonunit.face_name == yao_str

    # WHEN
    bob_lessonunit.del_face()

    # THEN
    assert bob_lessonunit.face_name != yao_str
    assert bob_lessonunit.face_name is None


def test_LessonUnit_set_beliefdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(belief_name=bob_str)
    assert bob_lessonunit._beliefdelta == beliefdelta_shop()

    # WHEN
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    bob_lessonunit.set_beliefdelta(x_beliefdelta)

    # THEN
    assert bob_lessonunit._beliefdelta == x_beliefdelta


def test_LessonUnit_set_delta_start_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(bob_str)
    assert bob_lessonunit._delta_start == 0

    # WHEN
    x_delta_start = 11
    bob_lessonunit.set_delta_start(x_delta_start)

    # THEN
    assert bob_lessonunit._delta_start == x_delta_start


def test_LessonUnit_beliefatom_exists_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    x_beliefdelta = beliefdelta_shop()
    bob_lessonunit = lessonunit_shop(belief_name=bob_str)
    bob_lessonunit.set_beliefdelta(x_beliefdelta)

    # WHEN
    sports_beliefatom = get_atom_example_planunit_sports()

    # THEN
    assert bob_lessonunit.beliefatom_exists(sports_beliefatom) is False

    # WHEN
    x_beliefdelta.set_beliefatom(sports_beliefatom)
    bob_lessonunit.set_beliefdelta(x_beliefdelta)

    # THEN
    assert bob_lessonunit.beliefatom_exists(sports_beliefatom)


def test_LessonUnit_del_beliefdelta_SetsAttribute():
    # ESTABLISH
    bob_str = "Bob"
    x_beliefdelta = beliefdelta_shop()
    x_beliefdelta.set_beliefatom(get_atom_example_planunit_sports())
    bob_lessonunit = lessonunit_shop(belief_name=bob_str, _beliefdelta=x_beliefdelta)
    assert bob_lessonunit._beliefdelta != beliefdelta_shop()
    assert bob_lessonunit._beliefdelta == x_beliefdelta

    # WHEN
    bob_lessonunit.del_beliefdelta()

    # THEN
    assert bob_lessonunit._beliefdelta == beliefdelta_shop()


def test_LessonUnit_get_step_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_label=amy45_str, belief_name=bob_str, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(sue_str)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

    # THEN
    assert x_dict.get(kw.moment_label) is not None
    assert x_dict.get(kw.moment_label) == amy45_str
    assert x_dict.get(kw.belief_name) is not None
    assert x_dict.get(kw.belief_name) == bob_str
    assert x_dict.get(kw.face_name) is not None
    assert x_dict.get(kw.face_name) == sue_str
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == amy45_e5_int

    delta_str = "delta"
    assert x_dict.get(delta_str) is not None
    assert x_dict.get(delta_str) == beliefdelta_shop().get_ordered_beliefatoms()
    assert x_dict.get(delta_str) == {}


def test_LessonUnit_get_step_dict_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_lessonunit = lessonunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    x_dict = bob_lessonunit.get_step_dict()

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


def test_LessonUnit_get_step_dict_ReturnsObj_delta_start():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(
        bob_str, _beliefdelta=sue_beliefdelta, _delta_start=x_delta_start
    )

    # WHEN
    step_dict = bob_lessonunit.get_step_dict()

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


def test_LessonUnit_get_serializable_dict_ReturnsObj_Simple():
    # ESTABLISH
    bob_str = "Bob"
    sue_str = "Sue"
    amy45_str = "amy45"
    amy45_e5_int = 5
    bob_lessonunit = lessonunit_shop(
        moment_label=amy45_str, belief_name=bob_str, spark_num=amy45_e5_int
    )
    bob_lessonunit.set_face(sue_str)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_dict()

    # THEN
    assert total_dict.get(kw.moment_label) is not None
    assert total_dict.get(kw.moment_label) == amy45_str
    assert total_dict.get(kw.belief_name) is not None
    assert total_dict.get(kw.belief_name) == bob_str
    assert total_dict.get(kw.face_name) is not None
    assert total_dict.get(kw.face_name) == sue_str
    assert total_dict.get(kw.spark_num) is not None
    assert total_dict.get(kw.spark_num) == amy45_e5_int
    delta_str = "delta"
    assert total_dict.get(delta_str) == {}


def test_LessonUnit_get_serializable_dict_ReturnsObj_Scenario0_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_lessonunit = lessonunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    total_dict = bob_lessonunit.get_serializable_dict()

    # THEN
    print(f"{total_dict=}")
    delta_str = "delta"
    assert total_dict.get(delta_str) is not None
    assert total_dict.get(delta_str) == sue_beliefdelta.get_ordered_dict()


def test_LessonUnit_get_serializable_dict_ReturnsObj_Scenario1_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_lessonunit = lessonunit_shop(bob_str, _beliefdelta=sue_beliefdelta)

    # WHEN
    generated_dict = bob_lessonunit.get_serializable_dict()

    # THEN
    assert generated_dict
    print("generated_json")
    print(generated_dict)
    expected_json = """{
  "belief_name": "Bob", 
  "delta": {
    "0": {
      "crud": "DELETE", 
      "dimen": "belief_voiceunit", 
      "jkeys": {"voice_name": "Sue"}, 
      "jvalues": {}
    }, 
    "1": {
      "crud": "UPDATE", 
      "dimen": "beliefunit", 
      "jkeys": {}, 
      "jvalues": {"credor_respect": 77}
    }
  }, 
  "face_name": null, 
  "moment_label": "YY", 
  "spark_num": null
}"""
    assert get_json_from_dict(generated_dict) == expected_json


def test_get_lessonunit_from_dict_ReturnsObj_WithBeliefDeltaPopulated():
    # ESTABLISH
    bob_str = "Bob"
    sue_beliefdelta = get_beliefdelta_sue_example()
    bob_lessonunit = lessonunit_shop(
        bob_str, _beliefdelta=sue_beliefdelta, spark_num=778
    )

    # WHEN
    generated_bob_lessonunit = get_lessonunit_from_dict(
        bob_lessonunit.get_serializable_dict()
    )

    # THEN
    assert generated_bob_lessonunit
    assert generated_bob_lessonunit.face_name == bob_lessonunit.face_name
    assert generated_bob_lessonunit.spark_num == bob_lessonunit.spark_num
    assert generated_bob_lessonunit.moment_label == bob_lessonunit.moment_label
    assert generated_bob_lessonunit._beliefdelta == bob_lessonunit._beliefdelta
    assert generated_bob_lessonunit == bob_lessonunit


def test_LessonUnit_get_delta_atom_numbers_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(bob_str)
    bob_lessonunit.set_beliefdelta(sue_beliefdelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(yao_str)
    x_dict = bob_lessonunit.get_step_dict()

    # WHEN
    x_delta_atom_numbers = bob_lessonunit.get_delta_atom_numbers(x_dict)
    # THEN
    assert x_delta_atom_numbers == [x_delta_start, x_delta_start + 1]


def test_LessonUnit_get_deltametric_dict_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    yao_str = "Yao"
    spark5_int = 5550
    sue_beliefdelta = get_beliefdelta_sue_example()
    x_delta_start = 7
    bob_lessonunit = lessonunit_shop(bob_str)
    bob_lessonunit.set_beliefdelta(sue_beliefdelta)
    bob_lessonunit.set_delta_start(x_delta_start)
    bob_lessonunit.set_face(yao_str)
    bob_lessonunit.spark_num = spark5_int

    # WHEN
    x_dict = bob_lessonunit.get_deltametric_dict()

    # THEN
    assert x_dict.get(kw.belief_name) is not None
    assert x_dict.get(kw.belief_name) == bob_str
    assert x_dict.get(kw.face_name) is not None
    assert x_dict.get(kw.face_name) == yao_str
    assert x_dict.get(kw.spark_num) is not None
    assert x_dict.get(kw.spark_num) == spark5_int

    delta_atom_numbers_str = "delta_atom_numbers"
    assert x_dict.get(delta_atom_numbers_str) is not None
    assert x_dict.get(delta_atom_numbers_str) == [7, 8]

    delta_min_str = "delta_min"
    assert x_dict.get(delta_min_str) is None
    delta_max_str = "delta_max"
    assert x_dict.get(delta_max_str) is None


def test_LessonUnit_add_p_beliefatom_Sets_BeliefUnit_voiceunits():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(bob_str)
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen
    print(f"{bob_voiceunit.to_dict()=}")
    bob_required_dict = {kw.voice_name: bob_voiceunit.to_dict().get(kw.voice_name)}
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit._beliefdelta.beliefatoms == {}

    # WHEN
    bob_lessonunit.add_p_beliefatom(
        dimen=kw.belief_voiceunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit._beliefdelta.beliefatoms) == 1
    assert (
        bob_lessonunit._beliefdelta.beliefatoms.get(kw.INSERT)
        .get(kw.belief_voiceunit)
        .get(bob_str)
        is not None
    )


def test_LessonUnit_get_edited_belief_ReturnsObj_BeliefUnit_insert_voice():
    # ESTABLISH
    sue_str = "Sue"
    sue_lessonunit = lessonunit_shop(sue_str)

    before_sue_beliefunit = beliefunit_shop(sue_str)
    yao_str = "Yao"
    zia_str = "Zia"
    before_sue_beliefunit.add_voiceunit(yao_str)
    assert before_sue_beliefunit.voice_exists(yao_str)
    assert before_sue_beliefunit.voice_exists(zia_str) is False
    dimen = kw.belief_voiceunit
    x_beliefatom = beliefatom_shop(dimen, kw.INSERT)
    x_beliefatom.set_jkey(kw.voice_name, zia_str)
    x_voice_cred_lumen = 55
    x_voice_debt_lumen = 66
    x_beliefatom.set_jvalue("voice_cred_lumen", x_voice_cred_lumen)
    x_beliefatom.set_jvalue("voice_debt_lumen", x_voice_debt_lumen)
    sue_lessonunit._beliefdelta.set_beliefatom(x_beliefatom)
    print(f"{sue_lessonunit._beliefdelta.beliefatoms.keys()=}")

    # WHEN
    after_sue_beliefunit = sue_lessonunit.get_lesson_edited_belief(
        before_sue_beliefunit
    )

    # THEN
    yao_voiceunit = after_sue_beliefunit.get_voice(yao_str)
    zia_voiceunit = after_sue_beliefunit.get_voice(zia_str)
    assert yao_voiceunit is not None
    assert zia_voiceunit is not None
    assert zia_voiceunit.voice_cred_lumen == x_voice_cred_lumen
    assert zia_voiceunit.voice_debt_lumen == x_voice_debt_lumen


def test_LessonUnit_get_edited_belief_RaisesErrorWhenlessonAttrsAndBeliefAttrsAreNotTheSame():
    # ESTABLISH
    yao_str = "Yao"
    xia_str = "Xia"
    amy23_str = "amy23"
    bob_lessonunit = lessonunit_shop(yao_str, xia_str, moment_label=amy23_str)
    sue_str = "Sue"
    amy45_str = "amy45"
    before_sue_beliefunit = beliefunit_shop(sue_str, moment_label=amy45_str)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_lessonunit.get_lesson_edited_belief(before_sue_beliefunit)
    assert str(excinfo.value) == "lesson belief conflict amy23 != amy45 or Yao != Sue"


def test_LessonUnit_is_empty_ReturnsObj():
    # ESTABLISH
    bob_str = "Bob"
    bob_lessonunit = lessonunit_shop(bob_str)
    bob_voice_cred_lumen = 55
    bob_voice_debt_lumen = 66
    bob_voiceunit = voiceunit_shop(bob_str, bob_voice_cred_lumen, bob_voice_debt_lumen)
    cw_str = kw.voice_cred_lumen
    dw_str = kw.voice_debt_lumen
    print(f"{bob_voiceunit.to_dict()=}")
    bob_required_dict = {kw.voice_name: bob_voiceunit.to_dict().get(kw.voice_name)}
    bob_optional_dict = {cw_str: bob_voiceunit.to_dict().get(cw_str)}
    bob_optional_dict[dw_str] = bob_voiceunit.to_dict().get(dw_str)
    print(f"{bob_required_dict=}")
    assert bob_lessonunit._beliefdelta.beliefatoms == {}
    assert bob_lessonunit.is_empty()

    # WHEN
    bob_lessonunit.add_p_beliefatom(
        dimen=kw.belief_voiceunit,
        crud_str=kw.INSERT,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )

    # THEN
    assert len(bob_lessonunit._beliefdelta.beliefatoms) == 1
    assert bob_lessonunit.is_empty() is False

    # WHEN
    bob_lessonunit._beliefdelta.beliefatoms = {}

    # THEN
    assert bob_lessonunit.is_empty()

    # Test for UPDATE_str operation
    bob_lessonunit_update = lessonunit_shop(bob_str)
    bob_lessonunit_update.add_p_beliefatom(
        dimen=kw.belief_voiceunit,
        crud_str=kw.UPDATE,
        jkeys=bob_required_dict,
        jvalues=bob_optional_dict,
    )
    assert len(bob_lessonunit_update._beliefdelta.beliefatoms) == 1
    assert bob_lessonunit_update.is_empty() is False

    # Test for DELETE_str operation
    bob_lessonunit_delete = lessonunit_shop(bob_str)
    bob_lessonunit_delete.add_p_beliefatom(
        dimen=kw.belief_voiceunit,
        crud_str=kw.DELETE,
        jkeys=bob_required_dict,
        jvalues={},
    )
    assert len(bob_lessonunit_delete._beliefdelta.beliefatoms) == 1
    assert bob_lessonunit_delete.is_empty() is False
