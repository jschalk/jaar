from src.a00_data_toolboxs.file_toolbox import create_path
from src.a02_finance_toolboxs.deal import fisc_title_str
from src.a08_bud_atom_logic.atom_config import face_name_str, event_int_str
from src.a15_fisc_logic.fisc_config import cumlative_minute_str, hour_title_str
from src.a16_pidgin_logic.pidgin_config import (
    inx_bridge_str,
    inx_name_str,
    otx_bridge_str,
    otx_name_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import (
    get_sheet_names,
    upsert_sheet,
    cart_valid_str,
    sheet_exists,
)
from src.a18_etl_toolbox.transformers import etl_cart_ideas_to_otz_face_ideas
from src.a18_etl_toolbox.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_cart_ideas_to_otz_face_ideas_CreatesFaceIdeaSheets_Scenario0_SingleFaceName(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    row1 = [sue_str, event3, accord23_str, hour6am, minute_360]
    row2 = [sue_str, event3, accord23_str, hour7am, minute_420]
    br00003_cart_agg_df = DataFrame([row1, row2], columns=idea_columns)
    x_etl_dir = get_test_etl_dir()
    x_cart_dir = create_path(x_etl_dir, "cart")
    x_faces_otz_dir = create_path(x_etl_dir, "faces_otz")
    br00003_filename = "br00003.xlsx"
    br00003_agg_file_path = create_path(x_cart_dir, br00003_filename)
    upsert_sheet(br00003_agg_file_path, cart_valid_str(), br00003_cart_agg_df)
    assert sheet_exists(br00003_agg_file_path, cart_valid_str())
    sue_dir = create_path(x_faces_otz_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, br00003_filename)
    assert sheet_exists(sue_br00003_filepath, cart_valid_str()) is False

    # WHEN
    etl_cart_ideas_to_otz_face_ideas(x_cart_dir, x_faces_otz_dir)

    # THEN
    assert sheet_exists(sue_br00003_filepath, cart_valid_str())
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
    assert get_sheet_names(sue_br00003_filepath) == [cart_valid_str()]


def test_etl_cart_ideas_to_otz_face_ideas_CreatesFaceIdeaSheets_Scenario1_MultpleFaceNames(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    zia_str = "Zia"
    event3 = 3
    event7 = 7
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    idea_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    sue1 = [sue_str, event3, accord23_str, hour6am, minute_360]
    sue2 = [sue_str, event3, accord23_str, hour7am, minute_420]
    zia3 = [zia_str, event7, accord23_str, hour7am, minute_420]
    br00003_cart_agg_df = DataFrame([sue1, sue2, zia3], columns=idea_columns)
    x_etl_dir = get_test_etl_dir()
    x_cart_dir = create_path(x_etl_dir, "cart")
    x_faces_otz_dir = create_path(x_etl_dir, "faces_otz")
    br00003_filename = "br00003.xlsx"
    br00003_agg_file_path = create_path(x_cart_dir, br00003_filename)
    upsert_sheet(br00003_agg_file_path, cart_valid_str(), br00003_cart_agg_df)
    sue_dir = create_path(x_faces_otz_dir, sue_str)
    zia_dir = create_path(x_faces_otz_dir, zia_str)
    sue_br00003_filepath = create_path(sue_dir, br00003_filename)
    zia_br00003_filepath = create_path(zia_dir, br00003_filename)
    assert sheet_exists(sue_br00003_filepath, cart_valid_str()) is False
    assert sheet_exists(zia_br00003_filepath, cart_valid_str()) is False

    # WHEN
    etl_cart_ideas_to_otz_face_ideas(x_cart_dir, x_faces_otz_dir)

    # THEN
    assert sheet_exists(sue_br00003_filepath, cart_valid_str())
    assert sheet_exists(zia_br00003_filepath, cart_valid_str())
    assert get_sheet_names(sue_br00003_filepath) == [cart_valid_str()]
    assert get_sheet_names(zia_br00003_filepath) == [cart_valid_str()]
    sue_br3_agg_df = pandas_read_excel(
        sue_br00003_filepath, sheet_name=cart_valid_str()
    )
    zia_br3_agg_df = pandas_read_excel(
        zia_br00003_filepath, sheet_name=cart_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")
    print(f"{zia_br3_agg_df.columns=}")
    example_sue_df = DataFrame([sue1, sue2], columns=idea_columns)
    example_zia_df = DataFrame([zia3], columns=idea_columns)
    pandas_assert_frame_equal(sue_br3_agg_df, example_sue_df)
    pandas_assert_frame_equal(zia_br3_agg_df, example_zia_df)


def test_etl_cart_ideas_to_otz_face_ideas_Scenario2_PidginDimenIdeasAreNotLoaded(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    event3 = 3
    minute_360 = 360
    minute_420 = 420
    hour6am = "6am"
    hour7am = "7am"
    br00003_columns = [
        face_name_str(),
        event_int_str(),
        fisc_title_str(),
        hour_title_str(),
        cumlative_minute_str(),
    ]
    accord23_str = "accord23"
    sue3_0 = [sue_str, event3, accord23_str, hour6am, minute_360]
    sue3_1 = [sue_str, event3, accord23_str, hour7am, minute_420]
    br00003_cart_agg_df = DataFrame([sue3_0, sue3_1], columns=br00003_columns)

    br00043_columns = [
        face_name_str(),
        event_int_str(),
        inx_bridge_str(),
        inx_name_str(),
        otx_bridge_str(),
        otx_name_str(),
        unknown_word_str(),
    ]
    sue43_0 = [sue_str, event3, ":", "Bob", ":", "Bobby", "Unknown"]
    sue43_1 = [sue_str, event3, ":", "Bob", ":", "Bobby", "Unknown"]
    br00043_cart_agg_df = DataFrame([sue43_0, sue43_1], columns=br00043_columns)

    x_etl_dir = get_test_etl_dir()
    x_cart_dir = create_path(x_etl_dir, "cart")
    x_faces_otz_dir = create_path(x_etl_dir, "faces_otz")
    br00003_filename = "br00003.xlsx"
    br00043_filename = "br00043.xlsx"
    br00003_agg_file_path = create_path(x_cart_dir, br00003_filename)
    br00043_agg_file_path = create_path(x_cart_dir, br00043_filename)
    upsert_sheet(br00003_agg_file_path, cart_valid_str(), br00003_cart_agg_df)
    upsert_sheet(br00043_agg_file_path, cart_valid_str(), br00043_cart_agg_df)
    assert sheet_exists(br00003_agg_file_path, cart_valid_str())
    assert sheet_exists(br00043_agg_file_path, cart_valid_str())

    sue_dir = create_path(x_faces_otz_dir, sue_str)
    sue_br00003_filepath = create_path(sue_dir, br00003_filename)
    sue_br00043_filepath = create_path(sue_dir, br00043_filename)
    assert sheet_exists(sue_br00003_filepath, cart_valid_str()) is False
    assert sheet_exists(sue_br00043_filepath, cart_valid_str()) is False

    # WHEN
    etl_cart_ideas_to_otz_face_ideas(x_cart_dir, x_faces_otz_dir)

    # THEN
    assert sheet_exists(sue_br00003_filepath, cart_valid_str())
    assert sheet_exists(sue_br00043_filepath, cart_valid_str()) is False
    sue_br3_agg_df = pandas_read_excel(
        sue_br00003_filepath, sheet_name=cart_valid_str()
    )
    print(f"{sue_br3_agg_df.columns=}")
    example_sue_df = DataFrame([sue3_0, sue3_1], columns=br00003_columns)
    pandas_assert_frame_equal(sue_br3_agg_df, example_sue_df)
