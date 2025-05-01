from src.a00_data_toolbox.file_toolbox import create_path, count_dirs_files, save_file
from src.a02_finance_logic._utils.strs_a02 import (
    owner_name_str,
    fisc_tag_str,
    deal_time_str,
    quota_str,
    celldepth_str,
)
from src.a06_bud_logic._utils.str_a06 import face_name_str, event_int_str, acct_name_str
from src.a12_hub_tools.hub_path import (
    create_fisc_json_path,
    create_job_path,
    create_gut_path,
    create_deal_acct_mandate_ledger_path as deal_mandate,
    create_fisc_ote1_csv_path,
)
from src.a15_fisc_logic._utils.str_a15 import cumlative_minute_str, hour_tag_str
from src.a16_pidgin_logic._utils.str_a16 import otx_name_str, inx_name_str
from src.a17_idea_logic._utils.str_a17 import brick_agg_str, brick_raw_str
from src.a17_idea_logic.idea_db_tool import upsert_sheet, sheet_exists
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame
from os.path import exists as os_path_exists


def test_WorldUnit_mud_to_stances_Scenario0_DeletesPreviousFiles(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    print(f"{fizz_world.worlds_dir=}")
    mstr_dir = fizz_world._fisc_mstr_dir
    fiscs_dir = create_path(mstr_dir, "fiscs")
    testing2_filename = "testing2.txt"
    testing3_filename = "testing3.txt"
    save_file(fizz_world.worlds_dir, testing2_filename, "")
    save_file(fiscs_dir, testing3_filename, "")
    testing2_path = create_path(fizz_world.worlds_dir, testing2_filename)
    testing3_path = create_path(fiscs_dir, testing3_filename)
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path)
    print(f"{testing3_path=}")
    assert count_dirs_files(fizz_world.worlds_dir) == 9

    # WHEN
    fizz_world.mud_to_stances(store_tracing_files=True)

    # THEN
    assert os_path_exists(testing2_path)
    assert os_path_exists(testing3_path) is False
    assert count_dirs_files(fizz_world.worlds_dir) == 23


# def test_WorldUnit_mud_to_stances_Scenario1_CreatesFiles(env_dir_setup_cleanup):
#     # ESTABLISH:
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str, worlds_dir())
#     # delete_dir(fizz_world.worlds_dir)
#     sue_str = "Sue"
#     sue_inx = "Suzy"
#     event3 = 3
#     ex_filename = "fizzbuzz.xlsx"
#     mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
#     br00113_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_tag_str(),
#         owner_name_str(),
#         acct_name_str(),
#         otx_name_str(),
#         inx_name_str(),
#     ]
#     a23_str = "accord23"
#     br00113_str = "br00113"
#     br00113row0 = [
#         sue_str,
#         event3,
#         a23_str,
#         sue_str,
#         sue_str,
#         sue_str,
#         sue_inx,
#     ]
#     br00113_df = DataFrame([br00113row0], columns=br00113_columns)
#     br00113_ex0_str = f"example0_{br00113_str}"
#     upsert_sheet(mud_file_path, br00113_ex0_str, br00113_df)
#     br00113_xlsx = f"{br00113_str}.xlsx"
#     brick_events_xlsx = "brick_events.xlsx"
#     pidname_xlsx = "pidname.xlsx"
#     fisunit_xlsx = "fisunit.xlsx"
#     budunit_xlsx = "budunit.xlsx"
#     budacct_xlsx = "budacct.xlsx"
#     brick_events_xlsx = "brick_events.xlsx"
#     assert not sheet_exists(br00113_xlsx, sheet_name="brick_raw")
#     assert not sheet_exists(br00113_xlsx, sheet_name="brick_agg")
#     assert not sheet_exists(brick_events_xlsx, sheet_name="agg")
#     assert not sheet_exists(brick_events_xlsx, sheet_name="valid")
#     assert not sheet_exists(br00113_xlsx, sheet_name="brick_valid")
#     assert not sheet_exists(pidname_xlsx, sheet_name="sound_raw")
#     assert not sheet_exists(pidname_xlsx, sheet_name="sound_agg")
#     assert not sheet_exists(pidname_xlsx, sheet_name="sound_valid")
#     assert not sheet_exists(fisunit_xlsx, sheet_name="sound_raw")
#     assert not sheet_exists(fisunit_xlsx, sheet_name="sound_agg")
#     assert not sheet_exists(fisunit_xlsx, sheet_name="sound_valid")
#     assert not sheet_exists(budunit_xlsx, sheet_name="sound_raw")
#     assert not sheet_exists(budunit_xlsx, sheet_name="sound_agg")
#     assert not sheet_exists(budunit_xlsx, sheet_name="sound_valid")
#     assert not sheet_exists(budacct_xlsx, sheet_name="sound_raw")
#     assert not sheet_exists(budacct_xlsx, sheet_name="sound_agg")
#     assert not sheet_exists(budacct_xlsx, sheet_name="sound_valid")
#     event1_sound_budunit_path = "events/1/sound_budunit.csv"
#     event1_sound_budacct_path = "events/1/sound_budacct.csv"
#     event1_pidgin_json_path = "events/1/pidgin.json"
#     event1_inherited_pidgin_json_path = "events/1/inherited_pidgin.json"
#     event1_voice_budunit_path = "events/1/voice_budunit.csv"
#     event1_voice_budacct_path = "events/1/voice_budacct.csv"
#     assert not os_path_exists(event1_sound_budunit_path)
#     assert not os_path_exists(event1_sound_budacct_path)
#     assert not os_path_exists(event1_pidgin_json_path)
#     assert not os_path_exists(event1_inherited_pidgin_json_path)
#     assert not os_path_exists(event1_voice_budunit_path)
#     assert not os_path_exists(event1_voice_budacct_path)
#     assert not sheet_exists(fisunit_xlsx, sheet_name="voice_raw")
#     assert not sheet_exists(fisunit_xlsx, sheet_name="voice_agg")
#     assert not sheet_exists(fisunit_xlsx, sheet_name="voice_valid")
#     assert not sheet_exists(budunit_xlsx, sheet_name="voice_raw")
#     assert not sheet_exists(budunit_xlsx, sheet_name="voice_agg")
#     assert not sheet_exists(budunit_xlsx, sheet_name="voice_valid")
#     assert not sheet_exists(budacct_xlsx, sheet_name="voice_raw")
#     assert not sheet_exists(budacct_xlsx, sheet_name="voice_agg")
#     assert not sheet_exists(budacct_xlsx, sheet_name="voice_valid")

#     # WHEN
#     fizz_world.mud_to_stances(store_tracing_files=True)

#     # THEN
#     assert sheet_exists(br00113_xlsx, sheet="brick_raw")
#     assert sheet_exists(br00113_xlsx, sheet="brick_agg")
#     assert sheet_exists(brick_events_xlsx, sheet="agg")
#     assert sheet_exists(brick_events_xlsx, sheet="valid")
#     assert sheet_exists(br00113_xlsx, sheet="brick_valid")
#     assert sheet_exists(pidname_xlsx, sheet="sound_raw")
#     assert sheet_exists(pidname_xlsx, sheet="sound_agg")
#     assert sheet_exists(pidname_xlsx, sheet="sound_valid")
#     assert sheet_exists(fisunit_xlsx, sheet="sound_raw")
#     assert sheet_exists(fisunit_xlsx, sheet="sound_agg")
#     assert sheet_exists(fisunit_xlsx, sheet="sound_valid")
#     assert sheet_exists(budunit_xlsx, sheet="sound_raw")
#     assert sheet_exists(budunit_xlsx, sheet="sound_agg")
#     assert sheet_exists(budunit_xlsx, sheet="sound_valid")
#     assert sheet_exists(budacct_xlsx, sheet="sound_raw")
#     assert sheet_exists(budacct_xlsx, sheet="sound_agg")
#     assert sheet_exists(budacct_xlsx, sheet="sound_valid")
#     assert os_path_exists(event1_sound_budunit_path)
#     assert os_path_exists(event1_sound_budacct_path)
#     assert os_path_exists(event1_pidgin_json_path)
#     assert os_path_exists(event1_inherited_pidgin_json_path)
#     assert os_path_exists(event1_voice_budunit_path)
#     assert os_path_exists(event1_voice_budacct_path)
#     assert sheet_exists(fisunit_xlsx, sheet="voice_raw")
#     assert sheet_exists(fisunit_xlsx, sheet="voice_agg")
#     assert sheet_exists(fisunit_xlsx, sheet="voice_valid")
#     assert sheet_exists(budunit_xlsx, sheet="voice_raw")
#     assert sheet_exists(budunit_xlsx, sheet="voice_agg")
#     assert sheet_exists(budunit_xlsx, sheet="voice_valid")
#     assert sheet_exists(budacct_xlsx, sheet="voice_raw")
#     assert sheet_exists(budacct_xlsx, sheet="voice_agg")
#     assert sheet_exists(budacct_xlsx, sheet="voice_valid")

#     # In mud directory 1 excel sheet
#     # sheet1: idea format: "event_int,face_name,fisc_tag,owner_name,acct_name,otx_name,inx_name": (idea_format_00113_acct_map1_v0_0_0)
#     # sue_str,event3,a23_str,sue_str,sue_str,sue_str,sue_inx

#     # THEN asserts:
#     # file br00113.xlsx, sheet="brick_raw" == one row file_dir, file_name, sheet_name,event_int,face_name,fisc_tag,owner_name,acct_name,otx_name,inx_name
#     # file br00113.xlsx, sheet="brick_agg" == event_int,face_name,fisc_tag,owner_name,acct_name,otx_name,inx_name,error_message
#     # file brick_events.xlsx, sheet="agg" == event_int,face_name,error_message
#     # file brick_events.xlsx, sheet="valid" == event_int,face_name
#     # file br00113.xlsx, sheet="brick_valid" == event_int,face_name,fisc_tag,owner_name,acct_name,otx_name,inx_name

#     # file pidname.xlsx, sheet="sound_raw" ==  idea_number,event_int,face_name,otx_name,inx_name
#     # file pidname.xlsx, sheet="sound_agg" == event_int,face_name,otx_name,inx_name,error_message
#     # file pidname.xlsx, sheet="sound_valid" == event_int,face_name,otx_name,inx_name

#     # file fisunit.xlsx, sheet="sound_raw" == idea_number,event_int,face_name,fisc_tag,...
#     # file fisunit.xlsx, sheet="sound_agg" == event_int,face_name,fisc_tag,...,error_message
#     # file fisunit.xlsx, sheet="sound_valid" == event_int,face_name,fisc_tag,...
#     # file budunit.xlsx, sheet="sound_raw" == idea_number,event_int,face_name,fisc_tag,owner_name,...
#     # file budunit.xlsx, sheet="sound_agg" == event_int,face_name,fisc_tag,owner_name,...,error_message
#     # file budunit.xlsx, sheet="sound_valid" == event_int,face_name,fisc_tag,owner_name,...
#     # file budacct.xlsx, sheet="sound_raw" == idea_number,event_int,face_name,fisc_tag,...
#     # file budacct.xlsx, sheet="sound_agg" == event_int,face_name,fisc_tag,...,error_message
#     # file budacct.xlsx, sheet="sound_valid" == event_int,face_name,fisc_tag,...

#     # file fisunit.xlsx, sheet="voice_raw" == idea_number,event_int,face_name,fisc_tag,...
#     # file fisunit.xlsx, sheet="voice_agg" == event_int,face_name,fisc_tag,...,error_message
#     # file fisunit.xlsx, sheet="voice_valid" == event_int,face_name,fisc_tag,...
#     # file budunit.xlsx, sheet="voice_raw" == idea_number,event_int,face_name,fisc_tag,owner_name,...
#     # file budunit.xlsx, sheet="voice_agg" == event_int,face_name,fisc_tag,owner_name,...,error_message
#     # file budunit.xlsx, sheet="voice_valid" == event_int,face_name,fisc_tag,owner_name,...
#     # file budacct.xlsx, sheet="voice_raw" == idea_number,event_int,face_name,fisc_tag,...
#     # file budacct.xlsx, sheet="voice_agg" == event_int,face_name,fisc_tag,...,error_message
#     # file budacct.xlsx, sheet="sound_valid" == event_int,face_name,fisc_tag,...

#     # events_dir/event_int/ sound_dimen.csv =
#     # events_dir/event3/ sound_budunit.csv =
#     # events_dir/event3/ sound_budacct.csv =
#     # events_dir/event3/ event_pidgin.csv =
#     # events_dir/event3/ event_inherited_pidgin.json =
#     # events_dir/event3/ voice_budunit.csv =
#     # events_dir/event3/ voice_budacct.csv =


def test_WorldUnit_mud_to_stances_Scenario2_CreatesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    # delete_dir(fizz_world.worlds_dir)
    sue_str = "Sue"
    event1 = 1
    event2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    br00003_columns = [
        event_int_str(),
        face_name_str(),
        cumlative_minute_str(),
        fisc_tag_str(),
        hour_tag_str(),
    ]
    br00001_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        deal_time_str(),
        quota_str(),
        celldepth_str(),
    ]
    accord23_str = "accord23"
    tp37 = 37
    sue_quota = 235
    sue_celldepth = 3
    br1row0 = [event2, sue_str, accord23_str, sue_str, tp37, sue_quota, sue_celldepth]
    br00001_1df = DataFrame([br1row0], columns=br00001_columns)
    br00001_ex0_str = "example0_br00001"
    upsert_sheet(mud_file_path, br00001_ex0_str, br00001_1df)

    br3row0 = [event1, sue_str, minute_360, accord23_str, hour6am]
    br3row1 = [event1, sue_str, minute_420, accord23_str, hour7am]
    br3row2 = [event2, sue_str, minute_420, accord23_str, hour7am]
    br00003_1df = DataFrame([br3row0, br3row1], columns=br00003_columns)
    br00003_3df = DataFrame([br3row1, br3row0, br3row2], columns=br00003_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex3_str = "example3_br00003"
    upsert_sheet(mud_file_path, br00003_ex1_str, br00003_1df)
    upsert_sheet(mud_file_path, br00003_ex3_str, br00003_3df)
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
    mstr_dir = fizz_world._fisc_mstr_dir
    wrong_a23_fisc_dir = create_path(mstr_dir, accord23_str)
    assert os_path_exists(wrong_a23_fisc_dir) is False
    brick_file_path = create_path(fizz_world._brick_dir, "br00003.xlsx")
    a23_json_path = create_fisc_json_path(mstr_dir, accord23_str)
    a23_sue_gut_path = create_gut_path(mstr_dir, accord23_str, sue_str)
    a23_sue_job_path = create_job_path(mstr_dir, accord23_str, sue_str)
    sue37_mandate_path = deal_mandate(mstr_dir, accord23_str, sue_str, tp37)
    assert os_path_exists(mud_file_path)
    assert not os_path_exists(brick_file_path)
    assert not os_path_exists(a23_json_path)
    assert not os_path_exists(a23_sue_gut_path)
    assert not os_path_exists(a23_sue_job_path)
    assert not os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fizz_world.worlds_dir) == 7

    # WHEN
    fizz_world.mud_to_stances(store_tracing_files=True)

    # THEN
    assert os_path_exists(wrong_a23_fisc_dir) is False
    assert os_path_exists(mud_file_path)
    assert os_path_exists(brick_file_path)
    assert sheet_exists(brick_file_path, brick_raw_str())
    assert os_path_exists(brick_file_path)
    assert os_path_exists(a23_json_path)
    assert os_path_exists(a23_sue_gut_path)
    assert os_path_exists(a23_sue_job_path)
    assert os_path_exists(sue37_mandate_path)
    assert count_dirs_files(fizz_world.worlds_dir) == 81


def test_WorldUnit_mud_to_stances_Senario2_WhenNoFiscIdeas_ote1_IsStillCreated(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event2 = 2
    ex_filename = "fizzbuzz.xlsx"
    mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
    accord23_str = "accord23"
    br00011_columns = [
        event_int_str(),
        face_name_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    br00011_rows = [[event2, sue_str, accord23_str, sue_str, sue_str]]
    br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
    upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
    fisc_mstr = fizz_world._fisc_mstr_dir
    a23_ote1_csv_path = create_fisc_ote1_csv_path(fisc_mstr, accord23_str)
    assert os_path_exists(a23_ote1_csv_path) is False

    # WHEN
    fizz_world.mud_to_stances()

    # THEN
    assert os_path_exists(a23_ote1_csv_path)


# def test_WorldUnit_mud_to_stances_CreatesBrickFiles(env_dir_setup_cleanup):
#     # ESTABLISH
#     fizz_str = "fizz"
#     fizz_world = worldunit_shop(fizz_str, worlds_dir())
#     delete_dir(fizz_world.worlds_dir)
#     sue_str = "Sue"
#     event1 = 1
#     event2 = 2
#     minute_360 = 360
#     minute_420 = 420
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     mud_file_path = create_path(fizz_world._mud_dir, ex_filename)
#     br00003_columns = [
#         face_name_str(),
#         event_int_str(),
#         cumlative_minute_str(),
#         fisc_tag_str(),
#         hour_tag_str(),
#     ]
#     accord23_str = "accord23"
#     row1 = [event1, sue_str,  minute_360, accord23_str, hour6am]
#     row2 = [event1, sue_str,  minute_420, accord23_str, hour7am]
#     row3 = [event2, sue_str,  minute_420, accord23_str, hour7am]
#     df1 = DataFrame([row1, row2], columns=br00003_columns)
#     df3 = DataFrame([row2, row1, row3], columns=br00003_columns)
#     br00003_ex1_str = "example1_br00003"
#     br00003_ex3_str = "example3_br00003"
#     upsert_sheet(mud_file_path, br00003_ex1_str, df1)
#     upsert_sheet(mud_file_path, br00003_ex3_str, df3)
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         "fisc_tag",
#         "owner_name",
#         "acct_name",
#     ]
#     br00011_rows = [[event2, sue_str,  accord23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(mud_file_path, "br00011_ex3", br00011_df)
#     mstr_dir = fizz_world._mstr_dir
#     fiscs_dir = create_path(mstr_dir, "fiscs")
#     a23_json_path = create_fisc_json_path(mstr_dir, accord23_str)
#     a23_sue_gut_path = create_gut_path(fiscs_dir, accord23_str, sue_str)
#     a23_sue_job_path = create_job_path(fiscs_dir, accord23_str, sue_str)
#     assert os_path_exists(mud_file_path)
#     assert os_path_exists(a23_json_path) is False
#     assert os_path_exists(a23_sue_gut_path) is False
#     assert os_path_exists(a23_sue_job_path) is False

#     # WHEN
#     fizz_world.mud_to_stances()

#     # THEN
#     brick_file_path = create_path(fizz_world._brick_dir, "br00003.xlsx")
#     assert os_path_exists(mud_file_path)
#     assert os_path_exists(brick_file_path)
#     assert os_path_exists(a23_json_path)
#     assert os_path_exists(a23_sue_gut_path)
#     assert os_path_exists(a23_sue_job_path)
