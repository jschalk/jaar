from src.a00_data_toolbox.file_toolbox import create_path
from src.a02_finance_logic._utils.strs_a02 import owner_name_str, fisc_tag_str
from src.a06_bud_logic._utils.str_a06 import face_name_str, acct_name_str, event_int_str
from src.a16_pidgin_logic.pidgin_config import (
    inx_bridge_str,
    otx_bridge_str,
    inx_name_str,
    otx_name_str,
    inx_tag_str,
    otx_tag_str,
    inx_road_str,
    otx_road_str,
    inx_label_str,
    otx_label_str,
    unknown_word_str,
)
from src.a17_idea_logic.idea_db_tool import (
    upsert_sheet,
    sheet_exists,
    _get_pidgen_idea_format_filenames,
    yell_agg_str,
)
from src.a18_etl_toolbox.tran_path import create_yell_pidgin_path
from src.a18_etl_toolbox.pidgin_agg import PidginPrimeColumns
from src.a19_world_logic.world import worldunit_shop
from src.a19_world_logic._utils.env_a19 import (
    get_module_temp_dir as worlds_dir,
    env_dir_setup_cleanup,
)
from pandas import DataFrame, read_excel as pandas_read_excel
from os.path import exists as os_path_exists


def test_get_pidgen_idea_format_filenames_ReturnsObj():
    # ESTABLISH / WHEN
    pidgen_idea_filenames = _get_pidgen_idea_format_filenames()

    # THEN
    print(f"need examples for {pidgen_idea_filenames=}")
    assert pidgen_idea_filenames == {
        "br00042.xlsx",
        "br00043.xlsx",
        "br00044.xlsx",
        "br00045.xlsx",
        "br00113.xlsx",
        "br00115.xlsx",
        "br00116.xlsx",
        "br00117.xlsx",
    }


def test_WorldUnit_yell_agg_df_to_yell_pidgin_raw_df_CreatesFile(env_dir_setup_cleanup):
    # ESTABLISH
    fizz_world = worldunit_shop("fizz", worlds_dir())
    bob_str = "Bob"
    sue_str = "Sue"
    yao_str = "Yao"
    yao_inx = "Yaoito"
    bob_inx = "Bobito"
    rdx = ":"
    ukx = "Unknown"
    m_str = "accord23"
    event1 = 1
    event2 = 2
    event5 = 5
    br00113_file_path = create_path(fizz_world._yell_dir, "br00113.xlsx")
    br00113_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_name_str(),
        inx_name_str(),
    ]
    br00043_file_path = create_path(fizz_world._yell_dir, "br00043.xlsx")
    br00043_columns = [
        face_name_str(),
        event_int_str(),
        otx_name_str(),
        inx_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00113_rows = [sue0, sue1]
    br00113_df = DataFrame(br00113_rows, columns=br00113_columns)
    upsert_sheet(br00113_file_path, yell_agg_str(), br00113_df)
    br00043_df = [sue2, sue3, yao1]
    br00043_df = DataFrame(br00043_df, columns=br00043_columns)
    upsert_sheet(br00043_file_path, yell_agg_str(), br00043_df)
    pidgin_path = create_yell_pidgin_path(fizz_world._yell_dir)

    br00115_file_path = create_path(fizz_world._yell_dir, "br00115.xlsx")
    br00115_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_label_str(),
        inx_label_str(),
    ]
    br00042_file_path = create_path(fizz_world._yell_dir, "br00042.xlsx")
    br00042_columns = [
        face_name_str(),
        event_int_str(),
        otx_label_str(),
        inx_label_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00115_rows = [sue0, sue1]
    br00115_df = DataFrame(br00115_rows, columns=br00115_columns)
    upsert_sheet(br00115_file_path, yell_agg_str(), br00115_df)
    b40_rows = [sue2, sue3, yao1]
    br00042_df = DataFrame(b40_rows, columns=br00042_columns)
    upsert_sheet(br00042_file_path, yell_agg_str(), br00042_df)

    br00116_file_path = create_path(fizz_world._yell_dir, "br00116.xlsx")
    br00116_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_tag_str(),
        inx_tag_str(),
    ]
    br00044_file_path = create_path(fizz_world._yell_dir, "br00044.xlsx")
    br00044_columns = [
        face_name_str(),
        event_int_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    br00116_rows = [sue0, sue1]
    br00116_df = DataFrame(br00116_rows, columns=br00116_columns)
    upsert_sheet(br00116_file_path, yell_agg_str(), br00116_df)
    br00044_rows = [sue2, sue3, yao1]
    br00044_df = DataFrame(br00044_rows, columns=br00044_columns)
    upsert_sheet(br00044_file_path, yell_agg_str(), br00044_df)

    br00117_file_path = create_path(fizz_world._yell_dir, "br00117.xlsx")
    br00117_columns = [
        face_name_str(),
        event_int_str(),
        fisc_tag_str(),
        owner_name_str(),
        acct_name_str(),
        otx_road_str(),
        inx_road_str(),
    ]
    br00045_file_path = create_path(fizz_world._yell_dir, "br00045.xlsx")
    br00045_columns = [
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    sue0 = [sue_str, event1, m_str, bob_str, yao_str, yao_str, yao_inx]
    sue1 = [sue_str, event1, m_str, bob_str, bob_str, bob_str, bob_inx]
    sue2 = [sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    sue3 = [sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    yao1 = [yao_str, event1, yao_str, yao_inx, rdx, rdx, ukx]
    b117_rows = [sue0, sue1]
    br00117_df = DataFrame(b117_rows, columns=br00117_columns)
    upsert_sheet(br00117_file_path, yell_agg_str(), br00117_df)
    br00045_rows = [sue2, sue3, yao1]
    br00045_df = DataFrame(br00045_rows, columns=br00045_columns)
    upsert_sheet(br00045_file_path, yell_agg_str(), br00045_df)

    fizz_world._events = {event2: sue_str, event5: sue_str}
    assert os_path_exists(pidgin_path) is False

    # WHEN
    fizz_world.yell_agg_df_to_yell_pidgin_raw_df()

    # THEN
    assert os_path_exists(pidgin_path)
    label_raw_str = "label_raw"
    name_raw_str = "name_raw"
    tag_raw_str = "tag_raw"
    road_raw_str = "road_raw"
    assert sheet_exists(pidgin_path, name_raw_str)
    assert sheet_exists(pidgin_path, label_raw_str)
    assert sheet_exists(pidgin_path, tag_raw_str)
    assert sheet_exists(pidgin_path, road_raw_str)

    gen_label_df = pandas_read_excel(pidgin_path, sheet_name=label_raw_str)
    gen_name_df = pandas_read_excel(pidgin_path, sheet_name=name_raw_str)
    gen_tag_df = pandas_read_excel(pidgin_path, sheet_name=tag_raw_str)
    gen_road_df = pandas_read_excel(pidgin_path, sheet_name=road_raw_str)

    label_file_columns = PidginPrimeColumns().pidgin_label_raw_columns
    assert list(gen_label_df.columns) == label_file_columns
    assert len(gen_label_df) == 2
    b3 = "br00115"
    b4 = "br00042"
    e1_label3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_label4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_label_rows = [e1_label3, e1_label4]
    e1_label_df = DataFrame(e1_label_rows, columns=label_file_columns)
    assert len(gen_label_df) == len(e1_label_df)
    print(f"{gen_label_df.to_csv()=}")
    print(f" {e1_label_df.to_csv()=}")
    assert gen_label_df.to_csv(index=False) == e1_label_df.to_csv(index=False)

    name_raw_columns = PidginPrimeColumns().pidgin_name_raw_columns
    assert list(gen_name_df.columns) == name_raw_columns
    assert len(gen_name_df) == 2
    b3 = "br00113"
    b4 = "br00043"
    e1_name3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_name4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_name_rows = [e1_name3, e1_name4]
    e1_name_df = DataFrame(e1_name_rows, columns=name_raw_columns)
    assert len(gen_name_df) == len(e1_name_df)
    print(f"{gen_name_df.to_csv()=}")
    print(f" {e1_name_df.to_csv()=}")
    assert gen_name_df.to_csv(index=False) == e1_name_df.to_csv(index=False)

    tag_file_columns = [
        "idea_number",
        face_name_str(),
        event_int_str(),
        otx_tag_str(),
        inx_tag_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_tag_df.columns) == tag_file_columns
    assert len(gen_tag_df) == 2
    b3 = "br00116"
    b4 = "br00044"
    e1_tag3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_tag4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_tag_rows = [e1_tag3, e1_tag4]
    e1_tag_df = DataFrame(e1_tag_rows, columns=tag_file_columns)
    assert len(gen_tag_df) == len(e1_tag_df)
    print(f"{gen_tag_df.to_csv()=}")
    print(f" {e1_tag_df.to_csv()=}")
    assert gen_tag_df.to_csv(index=False) == e1_tag_df.to_csv(index=False)

    road_file_columns = [
        "idea_number",
        face_name_str(),
        event_int_str(),
        otx_road_str(),
        inx_road_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
    ]
    assert list(gen_road_df.columns) == road_file_columns
    assert len(gen_road_df) == 2
    b3 = "br00117"
    b4 = "br00045"
    e1_road3 = [b4, sue_str, event2, sue_str, sue_str, rdx, rdx, ukx]
    e1_road4 = [b4, sue_str, event5, bob_str, bob_inx, rdx, rdx, ukx]
    e1_road_rows = [e1_road3, e1_road4]
    e1_road_df = DataFrame(e1_road_rows, columns=road_file_columns)
    assert len(gen_road_df) == len(e1_road_df)
    print(f"{gen_road_df.to_csv()=}")
    print(f" {e1_road_df.to_csv()=}")
    assert gen_road_df.to_csv(index=False) == e1_road_df.to_csv(index=False)
