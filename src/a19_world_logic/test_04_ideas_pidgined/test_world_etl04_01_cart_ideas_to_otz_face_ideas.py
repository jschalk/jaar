from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_tag_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_tag_str
from src.a17_idea_logic.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    cart_valid_str,
    sheet_exists,
)
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic.examples.world_env import (
    get_test_worlds_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_cart_ideas_to_otz_face_ideas_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str, worlds_dir())
    sue_str = "Sue"
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        hour_tag_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event3, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event3, accord23_str, hour7am, minute_420]
    br00003_cart_agg_df = DataFrame([row1, row2], columns=idea_columns)
    br00003_agg_file_path = create_path(fizz_world._cart_dir, "br00003.xlsx")
    upsert_sheet(br00003_agg_file_path, cart_valid_str(), br00003_cart_agg_df)
    assert sheet_exists(br00003_agg_file_path, cart_valid_str())
    sue_dir = create_path(fizz_world._syntax_otz_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, "br00003.xlsx")
    assert sheet_exists(sue_br00003_filepath, cart_valid_str()) is False

    # WHEN
    fizz_world.cart_ideas_to_otz_face_ideas()

    # THEN
    assert sheet_exists(sue_br00003_filepath, cart_valid_str())
    assert get_sheet_names(sue_br00003_filepath) == [cart_valid_str()]
    sue_br3_agg_df = pandas_read_excel(
        br00003_agg_file_path, sheet_name=cart_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")

    assert len(sue_br3_agg_df.columns) == len(br00003_cart_agg_df.columns)
    assert list(sue_br3_agg_df.columns) == list(br00003_cart_agg_df.columns)
    assert len(sue_br3_agg_df) > 0
    assert len(sue_br3_agg_df) == len(br00003_cart_agg_df)
    assert len(sue_br3_agg_df) == 2
    assert sue_br3_agg_df.to_csv() == br00003_cart_agg_df.to_csv()


# def test_WorldUnit_cart_staging_to_cart_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz", worlds_dir())
#     sue_str = "Sue"
#     event3 = 3
#     event7 = 7
#     minute_360 = 360
#     minute_420 = 420
#     minute_480 = 480
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_filename = "fizzbuzz.xlsx"
#     sound_file_path = create_path(fizz_world._sound_dir, ex_filename)
#     idea_columns = [
#         face_name_str(),
#         event_int_str(),
#         fisc_tag_str(),
#         hour_tag_str(),
#         cumlative_minute_str(),
#     ]
#     accord23_str = "accord23"
#     row1 = [sue_str, event3, accord23_str, hour6am, minute_360]
#     row2 = [sue_str, event3, accord23_str, hour7am, minute_420]
#     row3 = [sue_str, event3, accord23_str, hour7am, minute_480]
#     row4 = [sue_str, event7, accord23_str, hour7am, minute_480]
#     df1 = DataFrame([row1, row2, row3, row4], columns=idea_columns)
#     upsert_sheet(sound_file_path, "example1_br00003", df1)
#     fizz_world.sound_to_cart_staging()
#     br00003_agg_file_path = create_path(fizz_world._cart_dir, "br00003.xlsx")
#     cart_df = pandas_read_excel(br00003_agg_file_path, sheet_name=cart_staging_str())
#     assert len(cart_df) == 4
#     assert sheet_exists(br00003_agg_file_path, cart_valid_str()) is False

#     # WHEN
#     fizz_world.cart_staging_to_cart_agg()

#     # THEN
#     assert sheet_exists(br00003_agg_file_path, cart_valid_str())
#     gen_br00003_agg_df = pandas_read_excel(
#         br00003_agg_file_path, sheet_name=cart_valid_str()
#     )
#     ex_otx_df = DataFrame([row1, row4], columns=idea_columns)
#     # print(f"{gen_otx_df.columns=}")
#     print("gen_br00003_agg_df")
#     print(f"{gen_br00003_agg_df}")
#     assert len(gen_br00003_agg_df.columns) == len(ex_otx_df.columns)
#     assert list(gen_br00003_agg_df.columns) == list(ex_otx_df.columns)
#     assert len(gen_br00003_agg_df) > 0
#     assert len(gen_br00003_agg_df) == len(ex_otx_df)
#     assert len(gen_br00003_agg_df) == 2
#     assert gen_br00003_agg_df.to_csv() == ex_otx_df.to_csv()
#     assert get_sheet_names(br00003_agg_file_path) == [cart_staging_str(), cart_valid_str()]

#     assert 1 == 2
