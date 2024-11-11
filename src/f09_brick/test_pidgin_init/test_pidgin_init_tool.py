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
    get_casa_maison_pidginunit_set_by_otx_to_inx,
    get_casa_maison_pidginunit_set_by_explicit_label,
    get_casa_maison_road_otx_to_inx_dt,
    get_casa_maison_road_explicit_label_dt,
    get_slash_acctid_bridgeunit,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_explicit_label,
)
from src.f09_brick.pidgin_toolbox import (
    get_otx_to_inx_dt_columns,
    get_explicit_label_columns,
    create_otx_to_inx_dt,
    create_explicit_label_dt,
    save_all_csvs_from_pidginunit,
    _load_otx_to_inx_from_csv,
    _load_explicit_label_from_csv,
    _save_explicit_label_csv,
    create_dir_valid_pidginunit,
    init_pidginunit_from_dir,
)
from src.f09_brick.pandas_tool import (
    get_ordered_csv,
    get_brick_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_otx_to_inx_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_otx_to_inx_dt_columns()
    assert len(get_otx_to_inx_dt_columns()) == 7
    static_list = [
        face_id_str(),
        "obj_class",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
    ]
    assert get_otx_to_inx_dt_columns() == static_list
    assert set(get_otx_to_inx_dt_columns()).issubset(set(sorting_columns()))


def test_create_otx_to_inx_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx_to_inx()
    casa_bridgeunit = casa_pidginunit.get_bridgeunit(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_otx_to_inx_dt(casa_bridgeunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_otx_to_inx_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx_to_inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx_to_inx_dt())


def test_get_explicit_label_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_explicit_label_columns()
    assert len(get_explicit_label_columns()) == 7
    static_list = [
        face_id_str(),
        "obj_class",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]
    assert get_explicit_label_columns() == static_list
    assert set(get_explicit_label_columns()).issubset(set(sorting_columns()))


def test_create_explicit_label_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_explicit_label()
    casa_bridgeunit = casa_pidginunit.get_bridgeunit(type_RoadUnit_str())

    # WHEN
    casa_dataframe = create_explicit_label_dt(casa_bridgeunit)

    # THEN
    # print(f"{get_explicit_label_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_explicit_label_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_explicit_csv = get_ordered_csv(get_casa_maison_road_explicit_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_explicit_csv=}")
    assert casa_csv == ex_explicit_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_test_faces_dir()
    acctid_otx_to_inx_filename = f"{type_AcctID_str()}_otx_to_inx.csv"
    acctid_explicit_label_filename = f"{type_AcctID_str()}_explicit_label.csv"
    groupid_otx_to_inx_filename = f"{type_GroupID_str()}_otx_to_inx.csv"
    groupid_explicit_label_filename = f"{type_GroupID_str()}_explicit_label.csv"
    road_otx_to_inx_filename = f"{road_str()}_otx_to_inx.csv"
    road_explicit_label_filename = f"{road_str()}_explicit_label.csv"
    acctid_otx_to_inx_csv_path = f"{bridge_dir}/{acctid_otx_to_inx_filename}"
    acctid_explicit_label_csv_path = f"{bridge_dir}/{acctid_explicit_label_filename}"
    groupid_otx_to_inx_csv_path = f"{bridge_dir}/{groupid_otx_to_inx_filename}"
    groupid_explicit_label_csv_path = f"{bridge_dir}/{groupid_explicit_label_filename}"
    road_otx_to_inx_csv_path = f"{bridge_dir}/{road_otx_to_inx_filename}"
    road_explicit_label_csv_path = f"{bridge_dir}/{road_explicit_label_filename}"
    assert os_path_exists(acctid_otx_to_inx_csv_path) is False
    assert os_path_exists(acctid_explicit_label_csv_path) is False
    assert os_path_exists(groupid_otx_to_inx_csv_path) is False
    assert os_path_exists(groupid_explicit_label_csv_path) is False
    assert os_path_exists(road_otx_to_inx_csv_path) is False
    assert os_path_exists(road_explicit_label_csv_path) is False
    assert len(get_dir_file_strs(bridge_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    assert os_path_exists(acctid_explicit_label_csv_path)
    assert os_path_exists(groupid_otx_to_inx_csv_path)
    assert os_path_exists(groupid_explicit_label_csv_path)
    assert os_path_exists(road_otx_to_inx_csv_path)
    assert os_path_exists(road_explicit_label_csv_path)
    assert len(get_dir_file_strs(bridge_dir)) == 6


def test_load_otx_to_inx_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_test_faces_dir()
    acctid_filename = f"{type_AcctID_str()}_otx_to_inx.csv"
    acctid_otx_to_inx_csv_path = f"{bridge_dir}/{acctid_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctid_bridgeunit = empty_pidginunit.get_bridgeunit(type_AcctID_str())
    sue_acctid_bridgeunit.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctid_bridgeunit=}")
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 0

    # WHEN
    sue_acctid_bridgeunit = _load_otx_to_inx_from_csv(bridge_dir, sue_acctid_bridgeunit)

    # THEN
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 3
    ex_acctid_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert ex_acctid_bridgeunit == sue_acctid_bridgeunit


def test_load_explicit_label_map_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_casa_maison_pidginunit_set_by_explicit_label()
    before_road_bridgeunit = sue_pidginunit.get_bridgeunit(road_str())
    print(f"{before_road_bridgeunit.explicit_label=}")
    bridge_dir = get_test_faces_dir()
    road_filename = f"{road_str()}_explicit_label.csv"
    road_otx_to_inx_csv_path = f"{bridge_dir}/{road_filename}"
    _save_explicit_label_csv(bridge_dir, before_road_bridgeunit, road_str())
    assert os_path_exists(road_otx_to_inx_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    empty_road_bridgeunit = empty_pidginunit.get_bridgeunit(road_str())
    empty_road_bridgeunit.face_id = "Sue"
    print(f"{empty_pidginunit=} {empty_road_bridgeunit=}")
    assert len(empty_road_bridgeunit.explicit_label) == 0

    # WHEN
    gen_bridgeunit = _load_explicit_label_from_csv(bridge_dir, empty_road_bridgeunit)

    # THEN
    assert len(gen_bridgeunit.explicit_label) == 3
    assert gen_bridgeunit == before_road_bridgeunit
    assert gen_bridgeunit == empty_road_bridgeunit


def test_create_dir_valid_pidginunit_Sets_otx_road_delimiter_inx_road_delimiter(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_pidginunit = pidginunit_shop(
        x_face_id=sue_str,
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_bridgeunit(get_slash_acctid_bridgeunit())
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_pidginunit(bridge_dir)

    # # THEN
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_pidginunit.inx_road_delimiter == colon_inx_road_delimiter
    gen_bridgeunit = gen_pidginunit.get_bridgeunit(type_AcctID_str())
    assert gen_bridgeunit.unknown_word == x_unknown_word
    assert gen_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter


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
    assert len(gen_acctid_bridgeunit.otx_to_inx) == 3

    sue_acctid_bridgeunit = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 3
    assert gen_acctid_bridgeunit == sue_acctid_bridgeunit
    assert gen_pidginunit == sue_pidginunit
