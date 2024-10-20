from src.f01_road.road import default_road_delimiter_if_none
from src.f04_gift.atom_config import road_str, type_AcctID_str, type_GroupID_str
from src.f09_filter.bridge import (
    bridgeunit_shop,
    default_unknown_word,
    get_bridgeunit_from_dict,
    get_bridgeunit_from_json,
    save_all_bridgeunit_files,
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


def test_save_all_bridgeunit_files_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_bridgeunit = get_sue_bridgeunit()
    bridge_dir = get_test_faces_dir()
    acctid_otx_to_inx_filename = f"{type_AcctID_str()}_otx_to_inx_dt.csv"
    acctid_explicit_label_filename = f"{type_AcctID_str()}_explicit_label.csv"
    groupid_otx_to_inx_filename = f"{type_GroupID_str()}_otx_to_inx_dt.csv"
    groupid_explicit_label_filename = f"{type_GroupID_str()}_explicit_label.csv"
    road_otx_to_inx_filename = f"{road_str()}_otx_to_inx_dt.csv"
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

    # WHEN
    save_all_bridgeunit_files(bridge_dir, sue_bridgeunit)

    # THEN
    assert os_path_exists(acctid_otx_to_inx_csv_path)
    assert os_path_exists(acctid_explicit_label_csv_path)
    assert os_path_exists(groupid_otx_to_inx_csv_path)
    assert os_path_exists(groupid_explicit_label_csv_path)
    assert os_path_exists(road_otx_to_inx_csv_path)
    assert os_path_exists(road_explicit_label_csv_path)
