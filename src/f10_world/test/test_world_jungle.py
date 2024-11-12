from src.f00_instrument.file import create_file_path, create_dir
from src.f04_gift.atom_config import face_id_str, fiscal_id_str
from src.f07_fiscal.fiscal_config import cumlative_minute_str, hour_label_str
from src.f08_pidgin.pidgin_config import (
    eon_id_str,
    inx_road_delimiter_str,
    otx_road_delimiter_str,
    inx_word_str,
    otx_word_str,
    unknown_word_str,
    inx_label_str,
    otx_label_str,
)
from src.f09_brick.pandas_tool import _get_pidgen_brick_format_filenames
from src.f10_world.world import worldunit_shop, WorldUnit
from src.f10_world.world_tool import get_all_brick_dataframes
from src.f10_world.examples.world_env import get_test_worlds_dir, env_dir_setup_cleanup
from pandas import DataFrame, ExcelWriter, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_WorldUnit_jungle_to_zoo_CreatesZooFiles(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    eon_1 = 1
    eon_2 = 2
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_file_path(fizz_world._jungle_dir, ex_file_name)
    zoo_file_path = create_file_path(fizz_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
        hour_label_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, eon_1, minute_360, music23_str, hour6am]
    row2 = [sue_str, eon_1, minute_420, music23_str, hour7am]
    row3 = [sue_str, eon_2, minute_420, music23_str, hour7am]
    incomplete_brick_columns = [
        face_id_str(),
        eon_id_str(),
        cumlative_minute_str(),
        fiscal_id_str(),
    ]
    incom_row1 = [sue_str, eon_1, minute_360, music23_str]
    incom_row2 = [sue_str, eon_1, minute_420, music23_str]

    df1 = DataFrame([row1, row2], columns=brick_columns)
    df2 = DataFrame([incom_row1, incom_row2], columns=incomplete_brick_columns)
    df3 = DataFrame([row2, row1, row3], columns=brick_columns)
    br00003_ex1_str = "example1_br00003"
    br00003_ex2_str = "example2_br00003"
    br00003_ex3_str = "example3_br00003"
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name=br00003_ex1_str, index=False)
        df2.to_excel(writer, sheet_name=br00003_ex2_str, index=False)
        df3.to_excel(writer, sheet_name=br00003_ex3_str, index=False)
    assert os_path_exists(zoo_file_path) is False

    # WHEN
    fizz_world.jungle_to_zoo()

    # THEN
    print(f"{zoo_file_path=}")
    assert os_path_exists(zoo_file_path)
    x_df = pandas_read_excel(zoo_file_path, sheet_name="zoo")
    assert set(brick_columns).issubset(set(x_df.columns))
    file_dir_str = "file_dir"
    file_name_str = "file_name"
    sheet_name_str = "sheet_name"
    assert file_dir_str in set(x_df.columns)
    assert file_name_str in set(x_df.columns)
    assert sheet_name_str in set(x_df.columns)
    assert len(x_df) == 5


def test_WorldUnit_zoo_to_otx_CreatesOtxSheets_Scenario0_GroupByWorks(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_str = "fizz"
    fizz_world = worldunit_shop(fizz_str)
    sue_str = "Sue"
    eon_1 = 1
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_file_path(fizz_world._jungle_dir, ex_file_name)
    zoo_file_path = create_file_path(fizz_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, eon_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, eon_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, eon_1, music23_str, hour7am, minute_420]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
    fizz_world.jungle_to_zoo()
    zoo_df = pandas_read_excel(zoo_file_path, sheet_name="zoo")
    assert len(zoo_df) == 3

    # WHEN
    fizz_world.zoo_to_otx()

    # THEN
    gen_otx_df = pandas_read_excel(zoo_file_path, sheet_name="otx")
    ex_otx_df = DataFrame([row1, row2], columns=brick_columns)
    print(f"{gen_otx_df.columns=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 2
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()


def test_WorldUnit_zoo_to_otx_CreatesOtxSheets_Scenario1_GroupByOnlyNonConflictingRecords(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz")
    sue_str = "Sue"
    eon_1 = 1
    minute_360 = 360
    minute_420 = 420
    minute_480 = 480
    hour6am = "6am"
    hour7am = "7am"
    ex_file_name = "fizzbuzz.xlsx"
    jungle_file_path = create_file_path(fizz_world._jungle_dir, ex_file_name)
    zoo_file_path = create_file_path(fizz_world._zoo_dir, "br00003.xlsx")
    brick_columns = [
        face_id_str(),
        eon_id_str(),
        fiscal_id_str(),
        hour_label_str(),
        cumlative_minute_str(),
    ]
    music23_str = "music23"
    row1 = [sue_str, eon_1, music23_str, hour6am, minute_360]
    row2 = [sue_str, eon_1, music23_str, hour7am, minute_420]
    row3 = [sue_str, eon_1, music23_str, hour7am, minute_480]
    df1 = DataFrame([row1, row2, row3], columns=brick_columns)
    with ExcelWriter(jungle_file_path) as writer:
        df1.to_excel(writer, sheet_name="example1_br00003")
    fizz_world.jungle_to_zoo()
    zoo_df = pandas_read_excel(zoo_file_path, sheet_name="zoo")
    assert len(zoo_df) == 3

    # WHEN
    fizz_world.zoo_to_otx()

    # THEN
    gen_otx_df = pandas_read_excel(zoo_file_path, sheet_name="otx")
    ex_otx_df = DataFrame([row1], columns=brick_columns)
    # print(f"{gen_otx_df.columns=}")
    print(f"{gen_otx_df=}")
    assert len(ex_otx_df.columns) == len(gen_otx_df.columns)
    assert list(ex_otx_df.columns) == list(gen_otx_df.columns)
    assert len(gen_otx_df) > 0
    assert len(ex_otx_df) == len(gen_otx_df)
    assert len(gen_otx_df) == 1
    assert ex_otx_df.to_csv() == gen_otx_df.to_csv()


# def test_WorldUnit_otx_to_pidgen_ref_CreatesPidgenSheets_Scenario0(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     pidgen_brick_filenames = _get_pidgen_brick_format_filenames()
#     print(f"need examples for {pidgen_brick_filenames=}")
#     br00040_xlsx_file = "br00040.xlsx"
#     br00041_xlsx_file = "br00041.xlsx"
#     assert pidgen_brick_filenames == {br00040_xlsx_file, br00041_xlsx_file}

#     fizz_world = worldunit_shop("fizz")
#     sue_str = "Sue"
#     yao_str = "Yao"
#     eon_1 = 1
#     hour6am = "6am"
#     hour7am = "7am"
#     vetday = "veterns day"
#     armday = "armistice day"
#     slash_str = "/"
#     colon_str = ":"
#     x_unknown = "unknownSue"
#     br00040_file_path = create_file_path(fizz_world._zoo_dir, br00040_file_path)
#     br00041_file_path = create_file_path(fizz_world._zoo_dir, br00041_file_path)
#     br00040_columns = [
#         eon_id_str(),
#         face_id_str(),
#         inx_road_delimiter_str(),
#         inx_word_str(),
#         otx_road_delimiter_str(),
#         otx_word_str(),
#         unknown_word_str(),
#     ]
#     br00041_columns = [
#         face_id_str(),
#         eon_id_str(),
#         inx_label_str(),
#         inx_road_delimiter_str(),
#         otx_label_str(),
#         otx_road_delimiter_str(),
#         unknown_word_str(),
#     ]
#     row1 = [sue_str, eon_1, hour6am, slash_str, hour6am, colon_str, x_unknown]
#     row2 = [sue_str, eon_1, hour7am, slash_str, hour7am, colon_str, x_unknown]
#     row3 = [sue_str, eon_1, hour7am, slash_str, hour7am, colon_str, x_unknown]
#     row4 = [yao_str, eon_1, hour7am, slash_str, hour7am, colon_str, x_unknown]
#     row5 = [sue_str, eon_1, armday, slash_str, vetday, colon_str, x_unknown]
#     br00040_df = DataFrame([row1, row2, row3], columns=br00040_columns)
#     br00041_df = DataFrame([row4, row5], columns=br00041_columns)
#     with ExcelWriter(br00040_file_path) as writer:
#         br00040_df.to_excel(writer, sheet_name="otx")
#     with ExcelWriter(br00041_file_path) as writer:
#         br00041_df.to_excel(writer, sheet_name="otx")
#     face_file_path = create_file_path(fizz_world._zoo_dir, "faces.xlsx")
#     assert os_path_exists(face_file_path) is None

#     # WHEN
#     fizz_world.otx_to_pidgen_ref()

#     # THEN
#     assert os_path_exists(face_file_path)
#     otx_str = "bridge_otx_to_inx"
#     exp_str = "bridge_explicit_label"
#     gen_bridge_otx_to_inx_df = pandas_read_excel(face_file_path, sheet_name=otx_str)
#     gen_bridge_explicit_label_df = pandas_read_excel(face_file_path, sheet_name=exp_str)
#     # print(f"{gen_otx_df.columns=}")
#     ex1_faces_df = DataFrame([row1, row2, row3], columns=br00040_columns)
#     br00041_df = DataFrame([row4, row5], columns=br00041_columns)
#     assert len(gen_faces_df.columns) == len(ex1_faces_df.columns)
#     assert list(gen_faces_df.columns) == list(ex1_faces_df.columns)
#     assert len(gen_faces_df) > 0
#     assert len(gen_faces_df) == len(ex1_faces_df)
#     assert len(gen_faces_df) == 1
#     assert gen_faces_df.to_csv() == ex1_faces_df.to_csv()
