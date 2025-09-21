from os.path import exists as os_path_exists
from pandas import DataFrame, read_excel as pandas_read_excel
from pandas.testing import assert_frame_equal
from shutil import copy2 as shutil_copy2
from src.a00_data_toolbox.file_toolbox import create_path, set_dir
from src.ch17_idea_logic.idea_db_tool import get_sheet_names, upsert_sheet
from src.ch18_etl_toolbox.ch18_path import (
    create_stance0001_path,
    create_stances_dir_path,
)
from src.ch20_world_logic._ref.ch20_terms import (
    belief_name_str,
    event_int_str,
    face_name_str,
    moment_label_str,
    voice_name_str,
)
from src.ch20_world_logic.test._util.ch20_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir as worlds_dir,
)
from src.ch20_world_logic.world import worldunit_shop


def test_WorldUnit_create_stances_Senario0_EmptyWorld_CreatesFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    fay_world.sheets_input_to_clarity_mstr()
    fay_stance0001_path = create_stance0001_path(fay_world.output_dir)
    assert os_path_exists(fay_stance0001_path) is False

    # WHEN
    fay_world.create_stances(prettify_excel_bool=False)

    # THEN
    assert os_path_exists(fay_stance0001_path)


def test_WorldUnit_create_stances_Senario1_Add_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    sue_str = "Sue"
    event2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    amy23_str = "amy23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        voice_name_str(),
    ]
    br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    fay_world.sheets_input_to_clarity_mstr()
    fay_stance0001_path = create_stance0001_path(fay_world.output_dir)
    assert os_path_exists(fay_stance0001_path) is False

    # WHEN
    fay_world.create_stances(prettify_excel_bool=False)

    # THEN
    assert os_path_exists(fay_stance0001_path)
    print(get_sheet_names(fay_stance0001_path))
    br00021_sheet_df = pandas_read_excel(fay_stance0001_path, "br00021")
    print(f"{br00021_sheet_df=}")
    assert br00021_sheet_df.iloc[0]["face_name"] == "Fay"


def test_WorldUnit_create_stances_Senario2_CreatedStanceCanBeIdeasForOtherWorldUnit(
    env_dir_setup_cleanup,
):
    # sourcery skip: no-loop-in-tests
    # ESTABLISH
    fay_str = "Fay"
    fay_output_dir = create_path(worlds_dir(), "Fay_output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), fay_output_dir)
    sue_str = "Sue"
    event2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    amy23_str = "amy23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        voice_name_str(),
    ]
    br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    fay_world.sheets_input_to_clarity_mstr()
    fay_stance0001_path = create_stance0001_path(fay_world.output_dir)
    fay_world.create_stances()
    bob_output_dir = create_path(worlds_dir(), "Bob_output")
    bob_world = worldunit_shop("Bob", worlds_dir(), bob_output_dir)
    bob_input_st0001_path = create_path(bob_world._moment_mstr_dir, "Bob_input.xlsx")
    set_dir(create_stances_dir_path(bob_world._moment_mstr_dir))
    shutil_copy2(fay_stance0001_path, dst=bob_input_st0001_path)
    # print(f" {pandas_read_excel(fay_stance0001_path)=}")
    # print(f"{pandas_read_excel(bob_input_st0001_path)=}")
    print(f"{bob_input_st0001_path=}")
    print(f"{get_sheet_names(bob_input_st0001_path)=}")
    bob_world.sheets_input_to_clarity_mstr()
    bob_stance0001_path = create_stance0001_path(bob_world.output_dir)
    assert os_path_exists(bob_stance0001_path) is False

    # WHEN
    bob_world.create_stances(prettify_excel_bool=False)

    # THEN
    assert os_path_exists(bob_stance0001_path)
    print(f"{get_sheet_names(bob_stance0001_path)=}")
    for sheetname in get_sheet_names(bob_stance0001_path):
        print(f"comparing {sheetname=}...")
        fay_sheet_df = pandas_read_excel(fay_stance0001_path, sheetname)
        bob_sheet_df = pandas_read_excel(fay_stance0001_path, sheetname)
        # if sheetname == "br00021":
        #     print(f"{fay_sheet_df=}")
        #     print(f"{bob_sheet_df=}")
        assert_frame_equal(fay_sheet_df, bob_sheet_df)


def test_WorldUnit_create_stances_Senario3_Create_calendar_markdown(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    output_dir = create_path(worlds_dir(), "output")
    fay_world = worldunit_shop(fay_str, worlds_dir(), output_dir)
    sue_str = "Sue"
    event2 = 2
    ex_filename = "Faybob.xlsx"
    input_file_path = create_path(fay_world._input_dir, ex_filename)
    a23_str = "amy23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        moment_label_str(),
        belief_name_str(),
        voice_name_str(),
    ]
    br00011_rows = [[event2, sue_str, a23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
    fay_world.sheets_input_to_clarity_mstr()

    a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
    print(f"      {a23_calendar_md_path=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    fay_world.create_stances(prettify_excel_bool=False)

    # THEN
    assert os_path_exists(a23_calendar_md_path)


# def test_WorldUnit_sheets_input_to_clarity_CreatesFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     fay_str = "Fay"
#     fay_world = worldunit_shop(fay_str, worlds_dir())
#     # delete_dir(fay_world.worlds_dir)
#     sue_str = "Sue"
#     event1 = 1
#     event2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "Faybob.xlsx"
#     input_file_path = create_path(fay_world._input_dir, ex_filename)
#     br00003_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumulative_minute_str(),
#         moment_label_str(),
#         hour_label_str(),
#     ]
#     br00001_columns = [
#         face_name_str(),
#         event_int_str(),
#         moment_label_str(),
#         belief_name_str(),
#         bud_time(),
#         quota_str(),
#         celldepth_str(),
#     ]
#     amy23_str = "amy23"
#     tp37 = 37
#     sue_quota = 235
#     sue_celldepth = 3
#     br1row0 = [event2, sue_str, amy23_str, sue_str, tp37, sue_quota, sue_celldepth]
#     br00001_1df = DataFrame([br1row0], columns=br00001_columns)
#     br00001_ex0_str = "example0_br00001"
#     upsert_sheet(input_file_path, br00001_ex0_str, br00001_1df)

#     br3row0 = [event1, sue_str,  minute_360, amy23_str, hour6am]
#     br3row1 = [event1, sue_str,  minute_420, amy23_str, hour7am]
#     br3row2 = [event2, sue_str, minute_420, amy23_str, hour7am]
#     br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
#     br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(input_file_path, br00003_ex1_str, br00003_1df)
#     upsert_sheet(input_file_path, br00003_ex3_str, br00003_3df)
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         moment_label_str(),
#         belief_name_str(),
#         voice_name_str(),
#     ]
#     br00011_rows = [[event2, sue_str, amy23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
#     mstr_dir = fay_world._moment_mstr_dir
#     wrong_a23_moment_dir = create_path(mstr_dir, amy23_str)
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     a23_json_path = create_moment_json_path(mstr_dir, amy23_str)
#     a23_sue_gut_path = create_gut_path(mstr_dir, amy23_str, sue_str)
#     a23_sue_job_path = create_job_path(mstr_dir, amy23_str, sue_str)
#     sue37_mandate_path = bud_mandate(mstr_dir, amy23_str, sue_str, tp37)
#     assert os_path_exists(input_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_gut_path) is False
#     assert os_path_exists(a23_sue_job_path) is False
#     assert os_path_exists(sue37_mandate_path) is False
#     assert count_dirs_files(fay_world.worlds_dir) == 7

#     # WHEN
#     fay_world.sheets_input_to_clarity_mstr()

#     # THEN
#     assert os_path_exists(wrong_a23_moment_dir) is False
#     brick_file_path = create_path(fay_world._brick_dir, "br00003.xlsx")
#     assert os_path_exists(input_file_path)
#     assert os_path_exists(brick_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_gut_path)
#     assert os_path_exists(a23_sue_job_path)
#     assert os_path_exists(sue37_mandate_path)
#     assert count_dirs_files(fay_world.worlds_dir) == 91
