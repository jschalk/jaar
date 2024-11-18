from src.f00_instrument.file import get_dir_file_strs
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_RoadNode_str,
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
    get_test_faces_dir,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_pidginunit_set_by_nub_label,
    get_casa_maison_road_otx2inx_dt,
    get_casa_maison_road_nub_label_dt,
    get_slash_acctid_bridgeunit,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_nub_label,
)
from src.f09_brick.pidgin_toolbox import (
    get_otx2inx_dt_columns,
    get_nub_label_columns,
    create_otx2inx_dt,
    create_nub_label_dt,
    save_all_csvs_from_pidginunit,
    _load_otx2inx_from_csv,
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


def test_get_otx2inx_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_otx2inx_dt_columns()
    assert len(get_otx2inx_dt_columns()) == 7
    static_list = [
        face_id_str(),
        "jaar_type",
        "otx_wall",
        "inx_wall",
        "unknown_word",
        "otx_word",
        "inx_word",
    ]
    assert get_otx2inx_dt_columns() == static_list
    assert set(get_otx2inx_dt_columns()).issubset(set(sorting_columns()))


def test_create_otx2inx_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    casa_bridgeunit = casa_pidginunit.get_bridgeunit(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_otx2inx_dt(casa_bridgeunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_otx2inx_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx2inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx2inx_dt())


def test_get_nub_label_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_nub_label_columns()
    assert len(get_nub_label_columns()) == 7
    static_list = [
        face_id_str(),
        "jaar_type",
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
    casa_bridgeunit = casa_pidginunit.get_bridgeunit(type_RoadUnit_str())

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
    bridge_dir = get_test_faces_dir()
    acctid_otx2inx_filename = f"{type_AcctID_str()}_otx2inx.csv"
    acctid_nub_label_filename = f"{type_AcctID_str()}_nub_label.csv"
    groupid_otx2inx_filename = f"{type_GroupID_str()}_otx2inx.csv"
    groupid_nub_label_filename = f"{type_GroupID_str()}_nub_label.csv"
    road_otx2inx_filename = f"{road_str()}_otx2inx.csv"
    road_nub_label_filename = f"{road_str()}_nub_label.csv"
    acctid_otx2inx_csv_path = f"{bridge_dir}/{acctid_otx2inx_filename}"
    acctid_nub_label_csv_path = f"{bridge_dir}/{acctid_nub_label_filename}"
    groupid_otx2inx_csv_path = f"{bridge_dir}/{groupid_otx2inx_filename}"
    groupid_nub_label_csv_path = f"{bridge_dir}/{groupid_nub_label_filename}"
    road_otx2inx_csv_path = f"{bridge_dir}/{road_otx2inx_filename}"
    road_nub_label_csv_path = f"{bridge_dir}/{road_nub_label_filename}"
    assert os_path_exists(acctid_otx2inx_csv_path) is False
    assert os_path_exists(acctid_nub_label_csv_path) is False
    assert os_path_exists(groupid_otx2inx_csv_path) is False
    assert os_path_exists(groupid_nub_label_csv_path) is False
    assert os_path_exists(road_otx2inx_csv_path) is False
    assert os_path_exists(road_nub_label_csv_path) is False
    assert len(get_dir_file_strs(bridge_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(acctid_otx2inx_csv_path)
    assert os_path_exists(acctid_nub_label_csv_path)
    assert os_path_exists(groupid_otx2inx_csv_path)
    assert os_path_exists(groupid_nub_label_csv_path)
    assert os_path_exists(road_otx2inx_csv_path)
    assert os_path_exists(road_nub_label_csv_path)
    assert len(get_dir_file_strs(bridge_dir)) == 6


def test_load_otx2inx_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_test_faces_dir()
    acctid_filename = f"{type_AcctID_str()}_otx2inx.csv"
    acctid_otx2inx_csv_path = f"{bridge_dir}/{acctid_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(acctid_otx2inx_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctid_bridgeunit = empty_pidginunit.get_bridgeunit(type_AcctID_str())
    sue_acctid_bridgeunit.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctid_bridgeunit=}")
    assert len(sue_acctid_bridgeunit.otx2inx) == 0

    # WHEN
    sue_acctid_bridgeunit = _load_otx2inx_from_csv(bridge_dir, sue_acctid_bridgeunit)

    # THEN
    assert len(sue_acctid_bridgeunit.otx2inx) == 3
    ex_acctid_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert ex_acctid_bridgeunit == sue_acctid_bridgeunit


def test_load_nub_label_map_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_casa_maison_pidginunit_set_by_nub_label()
    before_road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    print(f"{before_road_bridgeunit.nub_label=}")
    bridge_dir = get_test_faces_dir()
    road_filename = f"{road_str()}_nub_label.csv"
    road_otx2inx_csv_path = f"{bridge_dir}/{road_filename}"
    _save_nub_label_csv(bridge_dir, before_road_bridgeunit, road_str())
    assert os_path_exists(road_otx2inx_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    empty_road_bridgeunit = empty_pidginunit.get_bridgeunit(road_str())
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
    sue_pidginunit.set_bridgeunit(get_slash_acctid_bridgeunit())
    bridge_dir = get_test_faces_dir()
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
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = init_pidginunit_from_dir(bridge_dir)

    # THEN
    assert gen_pidginunit
    gen_acctid_bridgeunit = gen_pidginunit.get_bridgeunit(type_AcctID_str())
    assert len(gen_acctid_bridgeunit.otx2inx) == 3

    sue_acctid_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert len(sue_acctid_bridgeunit.otx2inx) == 3
    assert gen_acctid_bridgeunit == sue_acctid_bridgeunit
    assert gen_pidginunit == sue_pidginunit
