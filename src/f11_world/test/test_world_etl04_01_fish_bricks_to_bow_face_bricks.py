from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import event_id_str
from src.f09_brick.pandas_tool import (
    get_sheet_names,
    upsert_sheet,
    fish_valid_str,
    sheet_exists,
)
from src.f11_world.world import worldunit_shop
from src.f11_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, read_excel as pandas_read_excel


def test_WorldUnit_fish_bricks_to_bow_face_bricks_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    brick_columns = [
        face_id_str(),
        event_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, event3, music23_str, hour6am, minute_360]
    row2 = [sue_str, event3, music23_str, hour7am, minute_420]
    br00003_fish_agg_df = DataFrame([row1, row2], columns=brick_columns)
    br00003_agg_file_path = create_path(fizz_world._fish_dir, "br00003.xlsx")
    upsert_sheet(br00003_agg_file_path, fish_valid_str(), br00003_fish_agg_df)
    assert sheet_exists(br00003_agg_file_path, fish_valid_str())
    sue_dir = create_path(fizz_world._faces_bow_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, "br00003.xlsx")
    assert sheet_exists(sue_br00003_filepath, fish_valid_str()) is False

    # WHEN
    fizz_world.fish_bricks_to_bow_face_bricks()

    # THEN
    assert sheet_exists(sue_br00003_filepath, fish_valid_str())
    assert get_sheet_names(sue_br00003_filepath) == [fish_valid_str()]
    sue_br3_agg_df = pandas_read_excel(
        br00003_agg_file_path, sheet_name=fish_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")

    assert len(sue_br3_agg_df.columns) == len(br00003_fish_agg_df.columns)
    assert list(sue_br3_agg_df.columns) == list(br00003_fish_agg_df.columns)
    assert len(sue_br3_agg_df) > 0
    assert len(sue_br3_agg_df) == len(br00003_fish_agg_df)
    assert len(sue_br3_agg_df) == 2
    assert sue_br3_agg_df.to_csv() == br00003_fish_agg_df.to_csv()


# def test_WorldUnit_fish_staging_to_fish_agg_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz")
#     sue_str = "Sue"
#     event3 = 3
#     event7 = 7
#     minute_360 = 360
#     minute_420 = 420
#     minute_480 = 480
#     hour6am = "6am"
#     hour7am = "7am"
#     ex_file_name = "fizzbuzz.xlsx"
#     ocean_file_path = create_path(fizz_world._ocean_dir, ex_file_name)
#     brick_columns = [
#         face_id_str(),
#         event_id_str(),
#         fiscal_id_str(),
#         hour_label_str(),
#         cumlative_minute_str(),
#     ]
#     music23_str = "music23"
#     row1 = [sue_str, event3, music23_str, hour6am, minute_360]
#     row2 = [sue_str, event3, music23_str, hour7am, minute_420]
#     row3 = [sue_str, event3, music23_str, hour7am, minute_480]
#     row4 = [sue_str, event7, music23_str, hour7am, minute_480]
#     df1 = DataFrame([row1, row2, row3, row4], columns=brick_columns)
#     upsert_sheet(ocean_file_path, "example1_br00003", df1)
#     fizz_world.ocean_to_fish_staging()
#     br00003_agg_file_path = create_path(fizz_world._fish_dir, "br00003.xlsx")
#     fish_df = pandas_read_excel(br00003_agg_file_path, sheet_name=fish_staging_str())
#     assert len(fish_df) == 4
#     assert sheet_exists(br00003_agg_file_path, fish_valid_str()) is False

#     # WHEN
#     fizz_world.fish_staging_to_fish_agg()

#     # THEN
#     assert sheet_exists(br00003_agg_file_path, fish_valid_str())
#     gen_br00003_agg_df = pandas_read_excel(
#         br00003_agg_file_path, sheet_name=fish_valid_str()
#     )
#     ex_otx_df = DataFrame([row1, row4], columns=brick_columns)
#     # print(f"{gen_otx_df.columns=}")
#     print("gen_br00003_agg_df")
#     print(f"{gen_br00003_agg_df}")
#     assert len(gen_br00003_agg_df.columns) == len(ex_otx_df.columns)
#     assert list(gen_br00003_agg_df.columns) == list(ex_otx_df.columns)
#     assert len(gen_br00003_agg_df) > 0
#     assert len(gen_br00003_agg_df) == len(ex_otx_df)
#     assert len(gen_br00003_agg_df) == 2
#     assert gen_br00003_agg_df.to_csv() == ex_otx_df.to_csv()
#     assert get_sheet_names(br00003_agg_file_path) == [fish_staging_str(), fish_valid_str()]

#     assert 1 == 2
