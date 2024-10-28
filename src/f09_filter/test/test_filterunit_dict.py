from src.f00_instrument.file import get_dir_file_strs
from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f09_filter.filter import (
    filterunit_shop,
    default_unknown_word,
    get_filterunit_from_dict,
    get_filterunit_from_json,
    save_all_csvs_from_filterunit,
    _load_otx_to_inx_from_csv,
    _load_explicit_label_from_csv,
    _save_explicit_label_csv,
    create_dir_valid_filterunit,
    init_filterunit_from_dir,
)
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f09_filter.examples.example_filters import (
    get_clean_roadunit_bridgeunit,
    get_swim_groupid_bridgeunit,
    get_suita_acctid_bridgeunit,
    get_slash_roadunit_bridgeunit,
    get_slash_groupid_bridgeunit,
    get_slash_acctid_bridgeunit,
    get_sue_filterunit,
    get_casa_maison_filterunit_set_by_explicit_label,
)
from os.path import exists as os_path_exists


def test_FilterUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str)

    # WHEN
    sue_dict = sue_filterunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("time_id") == sue_filterunit.time_id
    assert sue_dict.get("otx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("inx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    assert set(x_bridgeunits.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert x_bridgeunits.get(type_AcctID_str()) == acct_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(type_GroupID_str()) == group_id_bridgeunit.get_dict()
    assert x_bridgeunits.get(road_str()) == road_bridgeunit.get_dict()


def test_FilterUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str, 0, slash_otx_road_delimiter, colon_inx_road_delimiter, x_unknown_word
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    sue_dict = sue_filterunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_road_delimiter") == slash_otx_road_delimiter
    assert sue_dict.get("inx_road_delimiter") == colon_inx_road_delimiter
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("bridgeunits")
    x_bridgeunits = sue_dict.get("bridgeunits")
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_FilterUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_filterunit = filterunit_shop(sue_str)
    sue_filterunit.set_bridgeunit(get_clean_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_swim_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_suita_acctid_bridgeunit())

    # WHEN
    sue_json = sue_filterunit.get_json()

    # THEN
    assert sue_json.find("bridgeunits") == 5
    assert sue_json.find("otx_road_delimiter") == 129


def test_get_filterunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_time_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str,
        sue_time_id,
        slash_otx_road_delimiter,
        colon_inx_road_delimiter,
        x_unknown_word,
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_filterunit = get_filterunit_from_dict(sue_filterunit.get_dict())

    # THEN
    assert gen_filterunit
    assert gen_filterunit.face_id == sue_str
    assert gen_filterunit.time_id == sue_time_id
    assert gen_filterunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_filterunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_filterunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_filterunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_get_filterunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_time_id = 77
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        sue_str,
        sue_time_id,
        slash_otx_road_delimiter,
        colon_inx_road_delimiter,
        x_unknown_word,
    )
    sue_filterunit.set_bridgeunit(get_slash_roadunit_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_groupid_bridgeunit())
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())

    # WHEN
    gen_filterunit = get_filterunit_from_json(sue_filterunit.get_json())

    # THEN
    assert gen_filterunit
    assert gen_filterunit.face_id == sue_str
    assert gen_filterunit.time_id == sue_time_id
    assert gen_filterunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_filterunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_filterunit.unknown_word == x_unknown_word
    x_bridgeunits = gen_filterunit.bridgeunits
    assert len(x_bridgeunits) == 3
    acct_id_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    group_id_bridgeunit = sue_filterunit.get_bridgeunit(type_GroupID_str())
    road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    assert acct_id_bridgeunit.get_dict() == get_slash_acctid_bridgeunit().get_dict()
    assert group_id_bridgeunit.get_dict() == get_slash_groupid_bridgeunit().get_dict()
    assert road_bridgeunit.get_dict() == get_slash_roadunit_bridgeunit().get_dict()


def test_save_all_csvs_from_filterunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_filterunit = get_sue_filterunit()
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
    save_all_csvs_from_filterunit(bridge_dir, sue_filterunit)

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
    sue_filterunit = get_sue_filterunit()
    bridge_dir = get_test_faces_dir()
    acctid_filename = f"{type_AcctID_str()}_otx_to_inx.csv"
    acctid_otx_to_inx_csv_path = f"{bridge_dir}/{acctid_filename}"
    save_all_csvs_from_filterunit(bridge_dir, sue_filterunit)
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    empty_filterunit = filterunit_shop("Sue")
    sue_acctid_bridgeunit = empty_filterunit.get_bridgeunit(type_AcctID_str())
    sue_acctid_bridgeunit.face_id = "Sue"
    print(f"{empty_filterunit=} {sue_acctid_bridgeunit=}")
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 0

    # WHEN
    sue_acctid_bridgeunit = _load_otx_to_inx_from_csv(bridge_dir, sue_acctid_bridgeunit)

    # THEN
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 3
    ex_acctid_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    assert ex_acctid_bridgeunit == sue_acctid_bridgeunit


def test_load_explicit_label_map_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_filterunit = get_casa_maison_filterunit_set_by_explicit_label()
    before_road_bridgeunit = sue_filterunit.get_bridgeunit(road_str())
    print(f"{before_road_bridgeunit.explicit_label=}")
    bridge_dir = get_test_faces_dir()
    road_filename = f"{road_str()}_explicit_label.csv"
    road_otx_to_inx_csv_path = f"{bridge_dir}/{road_filename}"
    _save_explicit_label_csv(bridge_dir, before_road_bridgeunit, road_str())
    assert os_path_exists(road_otx_to_inx_csv_path)
    empty_filterunit = filterunit_shop("Sue")
    empty_road_bridgeunit = empty_filterunit.get_bridgeunit(road_str())
    empty_road_bridgeunit.face_id = "Sue"
    print(f"{empty_filterunit=} {empty_road_bridgeunit=}")
    assert len(empty_road_bridgeunit.explicit_label) == 0

    # WHEN
    gen_bridgeunit = _load_explicit_label_from_csv(bridge_dir, empty_road_bridgeunit)

    # THEN
    assert len(gen_bridgeunit.explicit_label) == 3
    assert gen_bridgeunit == before_road_bridgeunit
    assert gen_bridgeunit == empty_road_bridgeunit


def test_create_dir_valid_filterunit_Sets_otx_road_delimiter_inx_road_delimiter(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_filterunit = filterunit_shop(
        x_face_id=sue_str,
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
    )
    sue_filterunit.set_bridgeunit(get_slash_acctid_bridgeunit())
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_filterunit(bridge_dir, sue_filterunit)

    # WHEN
    gen_filterunit = create_dir_valid_filterunit(bridge_dir)

    # # THEN
    assert gen_filterunit.unknown_word == x_unknown_word
    assert gen_filterunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_filterunit.inx_road_delimiter == colon_inx_road_delimiter
    gen_bridgeunit = gen_filterunit.get_bridgeunit(type_AcctID_str())
    assert gen_bridgeunit.unknown_word == x_unknown_word
    assert gen_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter


def test_init_filterunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_filterunit = get_sue_filterunit()
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_filterunit(bridge_dir, sue_filterunit)

    # WHEN
    gen_filterunit = init_filterunit_from_dir(bridge_dir)

    # THEN
    assert gen_filterunit
    gen_acctid_bridgeunit = gen_filterunit.get_bridgeunit(type_AcctID_str())
    assert len(gen_acctid_bridgeunit.otx_to_inx) == 3

    sue_acctid_bridgeunit = sue_filterunit.get_bridgeunit(type_AcctID_str())
    assert len(sue_acctid_bridgeunit.otx_to_inx) == 3
    assert gen_acctid_bridgeunit == sue_acctid_bridgeunit
    assert gen_filterunit == sue_filterunit
