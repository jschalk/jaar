from src.f00_instrument.file import get_dir_file_strs
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_IdeaUnit_str,
    type_RoadUnit_str,
    type_GroupID_str,
    road_str,
    face_id_str,
    type_AcctID_str,
    type_GroupID_str,
)
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f08_pidgin.examples.pidgin_env import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_pidginunit_set_by_nub_label,
    get_casa_maison_road_otx2inx_dt,
    get_casa_maison_road_nub_label_dt,
    get_slash_acctbridge,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_nub_label,
)
from src.f09_brick.pidgin_toolbox import (
    get_bridge_acct_dt_columns,
    get_bridge_group_dt_columns,
    get_bridge_idea_dt_columns,
    get_bridge_road_dt_columns,
    get_nub_label_columns,
    create_bridge_acct_dt,
    create_bridge_group_dt,
    create_bridge_idea_dt,
    create_bridge_road_dt,
    create_nub_label_dt,
    save_all_csvs_from_pidginunit,
    _load_acctbridge_from_csv,
    _load_groupbridge_from_csv,
    _load_ideabridge_from_csv,
    _load_roadbridge_from_csv,
    _load_nub_label_from_csv,
    _save_nub_label_csv,
    create_dir_valid_empty_pidginunit,
    init_pidginunit_from_dir,
)
from src.f09_brick.pandas_tool import (
    get_ordered_csv,
    get_brick_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_bridge_acct_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_acct_dt_columns()
    assert len(get_bridge_acct_dt_columns()) == 6
    static_list = [
        face_id_str(),
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_acct_id",
        "inx_acct_id",
    ]
    assert get_bridge_acct_dt_columns() == static_list
    assert set(get_bridge_acct_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_group_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_group_dt_columns()
    assert len(get_bridge_group_dt_columns()) == 6
    static_list = [
        face_id_str(),
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_group_id",
        "inx_group_id",
    ]
    assert get_bridge_group_dt_columns() == static_list
    assert set(get_bridge_group_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_idea_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_idea_dt_columns()
    assert len(get_bridge_idea_dt_columns()) == 6
    static_list = [
        face_id_str(),
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_idea",
        "inx_idea",
    ]
    assert get_bridge_idea_dt_columns() == static_list
    assert set(get_bridge_idea_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_road_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_road_dt_columns()
    assert len(get_bridge_road_dt_columns()) == 6
    static_list = [
        face_id_str(),
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_road",
        "inx_road",
    ]
    assert get_bridge_road_dt_columns() == static_list
    assert set(get_bridge_road_dt_columns()).issubset(set(sorting_columns()))


def test_create_bridge_road_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    casa_bridgeunit = casa_pidginunit.get_roadbridge()

    # WHEN
    casa_dataframe = create_bridge_road_dt(casa_bridgeunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_bridge_road_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_bridge_road_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx2inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx2inx_dt())


def test_get_nub_label_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_nub_label_columns()
    assert len(get_nub_label_columns()) == 6
    static_list = [
        face_id_str(),
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]
    assert get_nub_label_columns() == static_list
    assert set(get_nub_label_columns()).issubset(set(sorting_columns()))


def test_create_nub_label_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_nub_label()
    casa_bridgeunit = casa_pidginunit.get_roadbridge()

    # WHEN
    casa_dataframe = create_nub_label_dt(casa_bridgeunit)

    # THEN
    # print(f"{get_nub_label_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_nub_label_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_nub_csv = get_ordered_csv(get_casa_maison_road_nub_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_nub_csv=}")
    assert casa_csv == ex_nub_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    group_filename = "group.csv"
    idea_filename = "idea.csv"
    road_filename = "road.csv"
    nub_label_filename = "nub_label.csv"
    acct_csv_path = f"{bridge_dir}/{acct_filename}"
    group_csv_path = f"{bridge_dir}/{group_filename}"
    idea_csv_path = f"{bridge_dir}/{idea_filename}"
    road_csv_path = f"{bridge_dir}/{road_filename}"
    nub_label_csv_path = f"{bridge_dir}/{nub_label_filename}"
    assert os_path_exists(acct_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(idea_csv_path) is False
    assert os_path_exists(road_csv_path) is False
    assert os_path_exists(nub_label_csv_path) is False
    assert len(get_dir_file_strs(bridge_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(acct_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(idea_csv_path)
    assert os_path_exists(road_csv_path)
    assert os_path_exists(nub_label_csv_path)
    assert len(get_dir_file_strs(bridge_dir)) == 5


def test_load_acctbridge_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    acct_csv_path = f"{bridge_dir}/{acct_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(acct_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctbridge = empty_pidginunit.get_bridgeunit(type_AcctID_str())
    sue_acctbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctbridge=}")
    assert len(sue_acctbridge.otx2inx) == 0

    # WHEN
    sue_acctbridge = _load_acctbridge_from_csv(bridge_dir, sue_acctbridge)

    # THEN
    assert len(sue_acctbridge.otx2inx) == 3
    ex_acctbridge = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert ex_acctbridge == sue_acctbridge


def test_load_groupbridge_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    group_filename = "group.csv"
    group_csv_path = f"{bridge_dir}/{group_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(group_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_groupbridge = empty_pidginunit.get_bridgeunit(type_GroupID_str())
    sue_groupbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_groupbridge=}")
    assert len(sue_groupbridge.otx2inx) == 0

    # WHEN
    sue_groupbridge = _load_groupbridge_from_csv(bridge_dir, sue_groupbridge)

    # THEN
    assert len(sue_groupbridge.otx2inx) == 2
    ex_groupbridge = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    assert ex_groupbridge == sue_groupbridge


def test_load_nub_label_map_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_casa_maison_pidginunit_set_by_nub_label()
    before_road_bridgeunit = sue_pidginunit.roadbridge
    print(f"{before_road_bridgeunit.nub_label=}")
    bridge_dir = get_example_face_dir()
    nub_filename = "nub_label.csv"
    nub_csv_path = f"{bridge_dir}/{nub_filename}"
    _save_nub_label_csv(bridge_dir, before_road_bridgeunit)
    assert os_path_exists(nub_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    empty_road_bridgeunit = empty_pidginunit.roadbridge
    empty_road_bridgeunit.face_id = "Sue"
    print(f"{empty_pidginunit=} {empty_road_bridgeunit=}")
    assert len(empty_road_bridgeunit.nub_label) == 0

    # WHEN
    gen_bridgeunit = _load_nub_label_from_csv(bridge_dir, empty_road_bridgeunit)

    # THEN
    assert len(gen_bridgeunit.nub_label) == 3
    assert gen_bridgeunit == before_road_bridgeunit
    assert gen_bridgeunit == empty_road_bridgeunit


def test_create_dir_valid_empty_pidginunit_Sets_otx_wall_inx_wall(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        x_face_id=sue_str,
        x_otx_wall=slash_otx_wall,
        x_inx_wall=colon_inx_wall,
        x_unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())
    bridge_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(bridge_dir)

    # # THEN
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    gen_bridgeunit = gen_pidginunit.get_bridgeunit(type_AcctID_str())
    assert gen_bridgeunit.unknown_word == x_unknown_word
    assert gen_bridgeunit.otx_wall == slash_otx_wall
    assert gen_bridgeunit.inx_wall == colon_inx_wall


def test_init_pidginunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = init_pidginunit_from_dir(bridge_dir)

    # THEN
    assert gen_pidginunit
    assert len(gen_pidginunit.acctbridge.otx2inx) == 3

    assert len(sue_pidginunit.acctbridge.otx2inx) == 3
    assert gen_pidginunit.acctbridge == sue_pidginunit.acctbridge
    assert gen_pidginunit.groupbridge == sue_pidginunit.groupbridge
    assert gen_pidginunit.ideabridge == sue_pidginunit.ideabridge
    assert gen_pidginunit.roadbridge == sue_pidginunit.roadbridge
    assert gen_pidginunit == sue_pidginunit
