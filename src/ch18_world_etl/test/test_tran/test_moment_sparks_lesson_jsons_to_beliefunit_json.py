from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import create_path, open_json, save_json
from src.ch07_belief_logic.belief_main import beliefunit_shop, get_beliefunit_from_dict
from src.ch10_lesson.lesson_main import get_lessonunit_from_dict, lessonunit_shop
from src.ch11_bud._ref.ch11_path import (
    create_belief_spark_dir_path,
    create_spark_all_lesson_path,
    create_spark_expressed_lesson_path,
)
from src.ch18_world_etl.test._util.ch18_env import (
    env_dir_setup_cleanup,
    get_chapter_temp_dir,
)
from src.ch18_world_etl.transformers import (
    etl_spark_lesson_json_to_spark_inherited_beliefunits,
)
from src.ref.keywords import Ch18Keywords as kw


def test_etl_spark_lesson_json_to_spark_inherited_beliefunits_SetsFiles_belief_json(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    a23_bob_e3_dir = create_belief_spark_dir_path(
        moment_mstr_dir, a23_str, bob_inx, spark3
    )
    a23_bob_e7_dir = create_belief_spark_dir_path(
        moment_mstr_dir, a23_str, bob_inx, spark7
    )
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, None, a23_str, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, None, a23_str, spark_num=spark7)
    blrpern_dimen = kw.belief_voiceunit
    bob_jkeys = {kw.voice_name: bob_inx}
    bob_jvalues = {kw.voice_cred_lumen: credit77, kw.voice_debt_lumen: None}
    yao_jkeys = {kw.voice_name: yao_inx}
    yao_jvalues = {kw.voice_cred_lumen: credit44, kw.voice_debt_lumen: None}
    a23_bob_e3_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.voice_name: sue_inx}
    sue_jvalues = {kw.voice_cred_lumen: credit88, kw.voice_debt_lumen: None}
    a23_bob_e7_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    e3_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark3
    )
    e7_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark7
    )
    save_json(e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_dict())
    save_json(e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_dict())
    assert os_path_exists(e3_all_lesson_path)
    assert os_path_exists(e7_all_lesson_path)
    belief_filename = "belief.json"
    e3_belief_path = create_path(a23_bob_e3_dir, belief_filename)
    e7_belief_path = create_path(a23_bob_e7_dir, belief_filename)
    assert os_path_exists(e3_belief_path) is False
    assert os_path_exists(e7_belief_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_beliefunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_belief_path)
    assert os_path_exists(e7_belief_path)
    expected_e3_bob_belief = beliefunit_shop(bob_inx, a23_str)
    expected_e7_bob_belief = beliefunit_shop(bob_inx, a23_str)
    expected_e3_bob_belief.add_voiceunit(bob_inx, credit77)
    expected_e3_bob_belief.add_voiceunit(yao_inx, credit44)
    expected_e7_bob_belief.add_voiceunit(bob_inx, credit77)
    expected_e7_bob_belief.add_voiceunit(sue_inx, credit88)
    expected_e7_bob_belief.add_voiceunit(yao_inx, credit44)
    generated_e3_belief = get_beliefunit_from_dict(open_json(e3_belief_path))
    generated_e7_belief = get_beliefunit_from_dict(open_json(e7_belief_path))
    assert generated_e3_belief.voices == expected_e3_bob_belief.voices
    assert generated_e3_belief == expected_e3_bob_belief
    assert generated_e3_belief.to_dict() == expected_e3_bob_belief.to_dict()
    assert generated_e7_belief.voices == expected_e7_bob_belief.voices
    assert generated_e7_belief.to_dict() == expected_e7_bob_belief.to_dict()


def test_etl_spark_lesson_json_to_spark_inherited_beliefunits_SetsFiles_expressed_lesson(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    yao_inx = "Yaoe"
    xia_inx = "Xia"
    spark3 = 3
    spark7 = 7
    credit44 = 44
    credit77 = 77
    credit88 = 88
    a23_str = "amy23"
    moment_mstr_dir = get_chapter_temp_dir()
    a23_bob_e3_lesson = lessonunit_shop(bob_inx, xia_inx, a23_str, spark_num=spark3)
    a23_bob_e7_lesson = lessonunit_shop(bob_inx, xia_inx, a23_str, spark_num=spark7)
    blrpern_dimen = kw.belief_voiceunit
    bob_jkeys = {kw.voice_name: bob_inx}
    bob_jvalues = {kw.voice_cred_lumen: credit77}
    yao_jkeys = {kw.voice_name: yao_inx}
    yao_jvalues = {kw.voice_cred_lumen: credit44}
    a23_bob_e3_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e3_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, yao_jkeys, yao_jvalues)
    sue_jkeys = {kw.voice_name: sue_inx}
    sue_jvalues = {kw.voice_cred_lumen: credit88}
    a23_bob_e7_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, bob_jkeys, bob_jvalues)
    a23_bob_e7_lesson.add_p_beliefatom(blrpern_dimen, kw.INSERT, sue_jkeys, sue_jvalues)
    a23_bob_e3_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark3
    )
    a23_bob_e7_all_lesson_path = create_spark_all_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark7
    )
    save_json(
        a23_bob_e3_all_lesson_path, None, a23_bob_e3_lesson.get_serializable_dict()
    )
    save_json(
        a23_bob_e7_all_lesson_path, None, a23_bob_e7_lesson.get_serializable_dict()
    )
    e3_expressed_lesson_path = create_spark_expressed_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark3
    )
    e7_expressed_lesson_path = create_spark_expressed_lesson_path(
        moment_mstr_dir, a23_str, bob_inx, spark7
    )
    assert os_path_exists(a23_bob_e3_all_lesson_path)
    assert os_path_exists(a23_bob_e7_all_lesson_path)
    assert os_path_exists(e3_expressed_lesson_path) is False
    assert os_path_exists(e7_expressed_lesson_path) is False

    # WHEN
    etl_spark_lesson_json_to_spark_inherited_beliefunits(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_expressed_lesson_path)
    assert os_path_exists(e7_expressed_lesson_path)
    gen_e3_express_lesson = get_lessonunit_from_dict(
        open_json(e3_expressed_lesson_path)
    )
    gen_e7_express_lesson = get_lessonunit_from_dict(
        open_json(e7_expressed_lesson_path)
    )
    expected_e3_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, a23_str, spark_num=spark3
    )
    expected_e7_bob_lesson = lessonunit_shop(
        bob_inx, xia_inx, a23_str, spark_num=spark7
    )
    expected_e3_bob_lesson.add_p_beliefatom(
        blrpern_dimen, kw.INSERT, bob_jkeys, bob_jvalues
    )
    expected_e3_bob_lesson.add_p_beliefatom(
        blrpern_dimen, kw.INSERT, yao_jkeys, yao_jvalues
    )
    expected_e7_bob_lesson.add_p_beliefatom(
        blrpern_dimen, kw.INSERT, sue_jkeys, sue_jvalues
    )
    assert expected_e3_bob_lesson == a23_bob_e3_lesson
    assert expected_e7_bob_lesson._beliefdelta != a23_bob_e7_lesson._beliefdelta
    assert expected_e7_bob_lesson != a23_bob_e7_lesson
    # expected_e3_bob_lesson.add_p_beliefatom()
    # expected_e3_bob_lesson.add_p_beliefatom()
    # expected_e7_bob_lesson.add_p_beliefatom()
    # expected_e7_bob_lesson.add_p_beliefatom()
    # expected_e7_bob_lesson.add_p_beliefatom()
    assert gen_e3_express_lesson == expected_e3_bob_lesson
    gen_e7_express_delta = gen_e7_express_lesson._beliefdelta
    expected_e7_delta = expected_e7_bob_lesson._beliefdelta
    assert gen_e7_express_delta.beliefatoms == expected_e7_delta.beliefatoms
    assert gen_e7_express_lesson._beliefdelta == expected_e7_bob_lesson._beliefdelta
    assert gen_e7_express_lesson == expected_e7_bob_lesson
