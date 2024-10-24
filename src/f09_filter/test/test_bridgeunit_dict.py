from src.f00_instrument.file import dir_files
from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f09_filter.bridge import (
    bridgeunit_shop,
    default_unknown_word,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
    save_all_csvs_from_bridgeunit,
    _load_otx_to_inx_from_csv,
    _load_explicit_label_from_csv,
    _save_explicit_label_csv,
    create_dir_valid_bridgeunit,
    init_bridgeunit_from_dir,
)
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f09_filter.examples.example_bridges import (
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
    get_slash_roadunit_bridgekind,
    get_slash_groupid_bridgekind,
    get_slash_acctid_bridgekind,
    get_sue_bridgeunit,
    get_casa_maison_bridgeunit_set_by_explicit_label,
)
from os.path import exists as os_path_exists


def test_BridgeUnit_get_dict_ReturnsObj_Scenario0():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("inx_road_delimiter") == default_road_delimiter_if_none()
    assert sue_dict.get("unknown_word") == default_unknown_word()
    assert sue_dict.get("bridgekinds")
    x_bridgekinds = sue_dict.get("bridgekinds")
    assert len(x_bridgekinds) == 3
    assert set(x_bridgekinds.keys()) == {
        type_AcctID_str(),
        type_GroupID_str(),
        road_str(),
    }
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert x_bridgekinds.get(type_AcctID_str()) == acct_id_bridgekind.get_dict()
    assert x_bridgekinds.get(type_GroupID_str()) == group_id_bridgekind.get_dict()
    assert x_bridgekinds.get(road_str()) == road_bridgekind.get_dict()


def test_BridgeUnit_get_dict_ReturnsObj_Scenario1():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_otx_road_delimiter, colon_inx_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    sue_dict = sue_bridgeunit.get_dict()

    # THEN
    assert sue_dict.get("face_id") == sue_str
    assert sue_dict.get("otx_road_delimiter") == slash_otx_road_delimiter
    assert sue_dict.get("inx_road_delimiter") == colon_inx_road_delimiter
    assert sue_dict.get("unknown_word") == x_unknown_word
    assert sue_dict.get("bridgekinds")
    x_bridgekinds = sue_dict.get("bridgekinds")
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


def test_BridgeUnit_get_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    sue_bridgeunit = bridgeunit_shop(sue_str)
    sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())

    # WHEN
    sue_json = sue_bridgeunit.get_json()

    # THEN
    assert sue_json.find("bridgekinds") == 5
    assert sue_json.find("otx_road_delimiter") == 129


def test_get_bridgeunit_from_dict_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_otx_road_delimiter, colon_inx_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_dict(sue_bridgeunit.get_dict())

    # THEN
    assert gen_bridgeunit
    assert gen_bridgeunit.face_id == sue_str
    assert gen_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_bridgeunit.unknown_word == x_unknown_word
    x_bridgekinds = gen_bridgeunit.bridgekinds
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


def test_get_bridgeunit_from_json_ReturnsObj():
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        sue_str, slash_otx_road_delimiter, colon_inx_road_delimiter, x_unknown_word
    )
    sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

    # WHEN
    gen_bridgeunit = get_bridgeunit_from_json(sue_bridgeunit.get_json())

    # THEN
    assert gen_bridgeunit
    assert gen_bridgeunit.face_id == sue_str
    assert gen_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    assert gen_bridgeunit.unknown_word == x_unknown_word
    x_bridgekinds = gen_bridgeunit.bridgekinds
    assert len(x_bridgekinds) == 3
    acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
    road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
    assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
    assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


def test_save_all_csvs_from_bridgeunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_bridgeunit = get_sue_bridgeunit()
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
    assert len(dir_files(bridge_dir)) == 0

    # WHEN
    save_all_csvs_from_bridgeunit(bridge_dir, sue_bridgeunit)

    # THEN
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    assert os_path_exists(acctid_explicit_label_csv_path)
    assert os_path_exists(groupid_otx_to_inx_csv_path)
    assert os_path_exists(groupid_explicit_label_csv_path)
    assert os_path_exists(road_otx_to_inx_csv_path)
    assert os_path_exists(road_explicit_label_csv_path)
    assert len(dir_files(bridge_dir)) == 6


def test_load_otx_to_inx_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_bridgeunit = get_sue_bridgeunit()
    bridge_dir = get_test_faces_dir()
    acctid_filename = f"{type_AcctID_str()}_otx_to_inx.csv"
    acctid_otx_to_inx_csv_path = f"{bridge_dir}/{acctid_filename}"
    save_all_csvs_from_bridgeunit(bridge_dir, sue_bridgeunit)
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    empty_bridgeunit = bridgeunit_shop("Sue")
    sue_acctid_bridgekind = empty_bridgeunit.get_bridgekind(type_AcctID_str())
    sue_acctid_bridgekind.face_id = "Sue"
    print(f"{empty_bridgeunit=} {sue_acctid_bridgekind=}")
    assert len(sue_acctid_bridgekind.otx_to_inx) == 0

    # WHEN
    sue_acctid_bridgekind = _load_otx_to_inx_from_csv(bridge_dir, sue_acctid_bridgekind)

    # THEN
    assert len(sue_acctid_bridgekind.otx_to_inx) == 3
    ex_acctid_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    assert ex_acctid_bridgekind == sue_acctid_bridgekind


def test_load_explicit_label_map_from_csv_SetsAttr(env_dir_setup_cleanup):
    # ESTABLISH
    sue_bridgeunit = get_casa_maison_bridgeunit_set_by_explicit_label()
    before_road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
    print(f"{before_road_bridgekind.explicit_label=}")
    bridge_dir = get_test_faces_dir()
    road_filename = f"{road_str()}_explicit_label.csv"
    road_otx_to_inx_csv_path = f"{bridge_dir}/{road_filename}"
    _save_explicit_label_csv(bridge_dir, before_road_bridgekind, road_str())
    assert os_path_exists(road_otx_to_inx_csv_path)
    empty_bridgeunit = bridgeunit_shop("Sue")
    empty_road_bridgekind = empty_bridgeunit.get_bridgekind(road_str())
    empty_road_bridgekind.face_id = "Sue"
    print(f"{empty_bridgeunit=} {empty_road_bridgekind=}")
    assert len(empty_road_bridgekind.explicit_label) == 0

    # WHEN
    gen_bridgekind = _load_explicit_label_from_csv(bridge_dir, empty_road_bridgekind)

    # THEN
    assert len(gen_bridgekind.explicit_label) == 3
    assert gen_bridgekind == before_road_bridgekind
    assert gen_bridgekind == empty_road_bridgekind


def test_create_dir_valid_bridgeunit_Sets_otx_road_delimiter_inx_road_delimiter(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownAcctId"
    slash_otx_road_delimiter = "/"
    colon_inx_road_delimiter = ":"
    sue_bridgeunit = bridgeunit_shop(
        x_face_id=sue_str,
        x_otx_road_delimiter=slash_otx_road_delimiter,
        x_inx_road_delimiter=colon_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
    )
    sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_bridgeunit(bridge_dir, sue_bridgeunit)

    # WHEN
    gen_bridgeunit = create_dir_valid_bridgeunit(bridge_dir)

    # # THEN
    assert gen_bridgeunit.unknown_word == x_unknown_word
    assert gen_bridgeunit.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgeunit.inx_road_delimiter == colon_inx_road_delimiter
    gen_bridgekind = gen_bridgeunit.get_bridgekind(type_AcctID_str())
    assert gen_bridgekind.unknown_word == x_unknown_word
    assert gen_bridgekind.otx_road_delimiter == slash_otx_road_delimiter
    assert gen_bridgekind.inx_road_delimiter == colon_inx_road_delimiter


def test_init_bridgeunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_bridgeunit = get_sue_bridgeunit()
    bridge_dir = get_test_faces_dir()
    save_all_csvs_from_bridgeunit(bridge_dir, sue_bridgeunit)

    # WHEN
    gen_bridgeunit = init_bridgeunit_from_dir(bridge_dir)

    # THEN
    assert gen_bridgeunit
    gen_acctid_bridgekind = gen_bridgeunit.get_bridgekind(type_AcctID_str())
    assert len(gen_acctid_bridgekind.otx_to_inx) == 3

    sue_acctid_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
    assert len(sue_acctid_bridgekind.otx_to_inx) == 3
    assert gen_acctid_bridgekind == sue_acctid_bridgekind
    assert gen_bridgeunit == sue_bridgeunit
