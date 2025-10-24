from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import open_file, open_json, save_file
from src.ch09_belief_lesson.lesson_main import get_lessonunit_from_dict, lessonunit_shop
from src.ch12_bud._ref.ch12_path import (
    create_belief_spark_dir_path as belief_spark_dir,
    create_spark_all_lesson_path as all_lesson_path,
)
from src.ch18_world_etl.test._util.ch18_env import get_temp_dir, temp_dir_setup
from src.ch18_world_etl.tran_sqlstrs import create_prime_tablename
from src.ch18_world_etl.transformers import etl_spark_belief_csvs_to_lesson_json
from src.ref.keywords import Ch18Keywords as kw


def test_etl_spark_belief_csvs_to_lesson_json_CreatesFiles_Scenario0_IgnoresCSV_beliefunit(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    spark3 = 3
    a23_str = "amy23"
    put_agg_tablename = create_prime_tablename(kw.beliefunit, "h", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = get_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, spark3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, spark7)
    a23_bob_e3_dir = belief_spark_dir(moment_mstr_dir, a23_str, bob_inx, spark3)
    e3_put_csv = f"""{kw.spark_num},{kw.face_name},moment_label,belief_name,credor_respect,debtor_respect,fund_pool,max_tree_traverse,tally,fund_grain,mana_grain,respect_grain
{spark3},{sue_inx},{a23_str},{bob_inx},,,,,,,,
"""
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    e3_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_str, bob_inx, spark3)
    assert os_path_exists(e3_all_lesson_path) is False

    # WHEN
    etl_spark_belief_csvs_to_lesson_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_lesson_path)
    expected_e3_lesson = lessonunit_shop(bob_inx, None, a23_str, spark_num=spark3)
    e3_lessonunit = get_lessonunit_from_dict(open_json(e3_all_lesson_path))
    assert e3_lessonunit.spark_num == expected_e3_lesson.spark_num
    expected_beliefdelta = expected_e3_lesson._beliefdelta
    generated_e3_beliefdelta = e3_lessonunit._beliefdelta
    assert generated_e3_beliefdelta.beliefatoms == expected_beliefdelta.beliefatoms
    assert e3_lessonunit._beliefdelta == expected_e3_lesson._beliefdelta
    assert e3_lessonunit == expected_e3_lesson


def test_etl_spark_belief_csvs_to_lesson_json_CreatesFiles_Scenario1(
    temp_dir_setup,
):
    # ESTABLISH
    sue_inx = "Suzy"
    bob_inx = "Bobby"
    spark3 = 3
    spark7 = 7
    credit77 = 77
    credit88 = 88
    debt_empty = ""
    a23_str = "amy23"
    blfvoce_str = kw.belief_voiceunit
    put_agg_tablename = create_prime_tablename(blfvoce_str, "h", "agg", "put")
    put_agg_csv_filename = f"{put_agg_tablename}.csv"
    moment_mstr_dir = get_temp_dir()
    # a23_bob_dir = create_path(a23_dir, bob_inx)
    # a23_bob_e3_dir = create_path(a23_bob_dir, spark3)
    # a23_bob_e7_dir = create_path(a23_bob_dir, spark7)
    a23_bob_e3_dir = belief_spark_dir(moment_mstr_dir, a23_str, bob_inx, spark3)
    a23_bob_e7_dir = belief_spark_dir(moment_mstr_dir, a23_str, bob_inx, spark7)
    e3_put_csv = f"""{kw.spark_num},{kw.face_name},{kw.moment_label},{kw.belief_name},{kw.voice_name},{kw.voice_cred_lumen},{kw.voice_debt_lumen}
{spark3},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
"""
    e7_put_csv = f"""{kw.spark_num},{kw.face_name},{kw.moment_label},{kw.belief_name},{kw.voice_name},{kw.voice_cred_lumen},{kw.voice_debt_lumen}
{spark7},{sue_inx},{a23_str},{bob_inx},{bob_inx},{credit77},{debt_empty}
{spark7},{sue_inx},{a23_str},{bob_inx},{sue_inx},{credit88},{debt_empty}
"""
    print(f"     {a23_bob_e3_dir=}  {put_agg_csv_filename}")
    print(f"     {a23_bob_e7_dir=}  {put_agg_csv_filename}")
    save_file(a23_bob_e3_dir, put_agg_csv_filename, e3_put_csv)
    save_file(a23_bob_e7_dir, put_agg_csv_filename, e7_put_csv)
    e3_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_str, bob_inx, spark3)
    e7_all_lesson_path = all_lesson_path(moment_mstr_dir, a23_str, bob_inx, spark7)
    print(f"   {e3_all_lesson_path=}")
    print(f"   {e7_all_lesson_path=}")
    assert os_path_exists(e3_all_lesson_path) is False
    assert os_path_exists(e7_all_lesson_path) is False

    # WHEN
    etl_spark_belief_csvs_to_lesson_json(moment_mstr_dir)

    # THEN
    assert os_path_exists(e3_all_lesson_path)
    assert os_path_exists(e7_all_lesson_path)
    # print(f"{open_file(e3_lesson_path)=}")
    # print(f"{open_file(e7_lesson_path)=}")
    # lessons_dir = create_path(fay_world._moment_mstr_dir, "lessons")
    # atoms_dir = create_path(fay_world._moment_mstr_dir, "atoms")
    # e3_lesson = lessonunit_shop(bob_inx, sue_inx, a23_str, lessons_dir, atoms_dir, spark3)
    # e7_lesson = lessonunit_shop(bob_inx, sue_inx, a23_str, lessons_dir, atoms_dir, spark7)
    expected_e3_lesson = lessonunit_shop(bob_inx, None, a23_str, spark_num=spark3)
    expected_e7_lesson = lessonunit_shop(bob_inx, None, a23_str, spark_num=spark7)
    blfvoce_dimen = kw.belief_voiceunit
    expected_e3_lesson._beliefdelta.add_beliefatom(
        blfvoce_dimen,
        kw.INSERT,
        jkeys={kw.voice_name: bob_inx},
        jvalues={kw.voice_cred_lumen: credit77, kw.voice_debt_lumen: None},
    )
    expected_e7_lesson._beliefdelta.add_beliefatom(
        blfvoce_dimen,
        kw.INSERT,
        jkeys={kw.voice_name: bob_inx},
        jvalues={kw.voice_cred_lumen: credit77, kw.voice_debt_lumen: None},
    )
    expected_e7_lesson._beliefdelta.add_beliefatom(
        blfvoce_dimen,
        kw.INSERT,
        jkeys={kw.voice_name: sue_inx},
        jvalues={kw.voice_cred_lumen: credit88, kw.voice_debt_lumen: None},
    )
    e3_lessonunit = get_lessonunit_from_dict(open_json(e3_all_lesson_path))
    e7_lessonunit = get_lessonunit_from_dict(open_json(e7_all_lesson_path))
    # print(f"{e7_lessonunit=}")
    assert e3_lessonunit.spark_num == expected_e3_lesson.spark_num
    expected_beliefdelta = expected_e3_lesson._beliefdelta
    generated_e3_beliefdelta = e3_lessonunit._beliefdelta
    assert generated_e3_beliefdelta.beliefatoms == expected_beliefdelta.beliefatoms
    assert e3_lessonunit._beliefdelta == expected_e3_lesson._beliefdelta
    assert e3_lessonunit == expected_e3_lesson
    e7_insert = e7_lessonunit._beliefdelta.beliefatoms.get("INSERT")
    expected_e7_insert = expected_e7_lesson._beliefdelta.beliefatoms.get("INSERT")
    # print(e7_insert.get("belief_voiceunit").keys())
    # print(expected_e7_insert.get("belief_voiceunit").keys())
    e7_blfvoce = e7_insert.get("belief_voiceunit")
    expected_e7_blfvoce = expected_e7_insert.get("belief_voiceunit")
    assert e7_blfvoce.keys() == expected_e7_blfvoce.keys()
    # print(f"{expected_e7_insert.keys()=}")
    assert e7_insert == expected_e7_insert
    assert e7_lessonunit._beliefdelta == expected_e7_lesson._beliefdelta
    assert e7_lessonunit == expected_e7_lesson
