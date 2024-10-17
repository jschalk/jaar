from src.f00_instrument.file import save_file, dir_files
from src.f04_gift.atom_config import (
    acct_id_str,
    road_str,
    type_AcctID_str,
    type_GroupID_str,
)
from src.f08_brick.brick import open_brick_csv
from src.f09_filter.bridge import bridgeunit_shop
from src.f09_filter.filter import filter_files_from_src_dir_to_dst_dir
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_filters_dir,
)
from src.f09_filter.examples.example_bridges import (
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
    get_suita_acctid_src_dt,
    get_suita_acctid_dst_dt,
)
from os.path import exists as os_path_exists
from pandas import DataFrame


# save two dataframes to be filtered: two files in src, two files in dst
def test_filter_files_from_src_dir_to_dst_dir_CreatesFilteredFiles_Scenario0_SingleFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_src = "Bob"
    sue_src = "Sue"
    xio_src = "Xio"
    zia_src = "Zia"
    bob_dst = "Bobita"
    sue_dst = "Suita"
    xio_dst = "Xioita"
    sue_bridgeunit = bridgeunit_shop(sue_src)
    sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())
    bridge_dir = f"{get_test_filters_dir()}/bridge"
    save_file(bridge_dir, f"{sue_src}.json", sue_bridgeunit.get_json())
    sue_src_dt = get_suita_acctid_src_dt()
    sue_dst_dt = get_suita_acctid_dst_dt()
    src_dir = f"{get_test_filters_dir()}/src"
    dst_dir = f"{get_test_filters_dir()}/dst"

    save_file(src_dir, f"{sue_src}.json", "save to create dir")
    save_file(dst_dir, f"{sue_src}.json", "save to create dir")
    bridgeunit_file_path = f"{bridge_dir}/{sue_src}.json"
    src_file_path = f"{src_dir}/{sue_src}.csv"
    dst_file_path = f"{dst_dir}/{sue_dst}.csv"
    sue_src_dt.to_csv(src_file_path, index=False)
    assert os_path_exists(bridgeunit_file_path)
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path) is False

    # WHEN
    filter_files_from_src_dir_to_dst_dir(src_dir, dst_dir, bridge_dir)

    # THEN
    assert os_path_exists(bridgeunit_file_path)
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path)
    gen_dst_dt = open_brick_csv(dst_dir, f"{sue_dst}.csv")
    assert gen_dst_dt.iloc[0][acct_id_str()] == zia_src
    assert gen_dst_dt.iloc[1][acct_id_str()] == sue_dst
    assert gen_dst_dt.to_csv() != sue_src_dt.to_csv()
    example_dst_dt = DataFrame(columns=[acct_id_str()])
    example_dst_dt.loc[0, acct_id_str()] = zia_src
    example_dst_dt.loc[1, acct_id_str()] = sue_dst
    example_dst_dt.loc[2, acct_id_str()] = bob_dst
    example_dst_dt.loc[3, acct_id_str()] = xio_dst
    assert gen_dst_dt.iloc[0][acct_id_str()] == example_dst_dt.iloc[0][acct_id_str()]
    assert gen_dst_dt.iloc[1][acct_id_str()] == example_dst_dt.iloc[1][acct_id_str()]
    assert gen_dst_dt.iloc[2][acct_id_str()] == example_dst_dt.iloc[2][acct_id_str()]
    assert gen_dst_dt.iloc[3][acct_id_str()] == example_dst_dt.iloc[3][acct_id_str()]
    print(f"{gen_dst_dt.to_csv(index=False)=}")
    gen_csv = gen_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
    sue_dst_csv = sue_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
    assert gen_csv == sue_dst_csv
    assert gen_dst_dt.to_csv() == example_dst_dt.to_csv()


# def test_BridgeUnit_get_dict_ReturnsObj_Scenario0():
#     # ESTABLISH
#     sue_str = "Sue"
#     sue_bridgeunit = bridgeunit_shop(sue_str)

#     # WHEN
#     sue_dict = sue_bridgeunit.get_dict()

#     # THEN
#     assert sue_dict
#     assert sue_dict.get("face_id") == sue_str
#     assert sue_dict.get("src_road_delimiter") == default_road_delimiter_if_none()
#     assert sue_dict.get("dst_road_delimiter") == default_road_delimiter_if_none()
#     assert sue_dict.get("unknown_word") == default_unknown_word()
#     assert sue_dict.get("bridgekinds")
#     x_bridgekinds = sue_dict.get("bridgekinds")
#     assert len(x_bridgekinds) == 3
#     assert set(x_bridgekinds.keys()) == {
#         type_AcctID_str(),
#         type_GroupID_str(),
#         road_str(),
#     }
#     acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
#     group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
#     road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
#     assert x_bridgekinds.get(type_AcctID_str()) == acct_id_bridgekind.get_dict()
#     assert x_bridgekinds.get(type_GroupID_str()) == group_id_bridgekind.get_dict()
#     assert x_bridgekinds.get(road_str()) == road_bridgekind.get_dict()


# def test_BridgeUnit_get_dict_ReturnsObj_Scenario1():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     slash_src_road_delimiter = "/"
#     colon_dst_road_delimiter = ":"
#     sue_bridgeunit = bridgeunit_shop(
#         sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
#     )
#     sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

#     # WHEN
#     sue_dict = sue_bridgeunit.get_dict()

#     # THEN
#     assert sue_dict.get("face_id") == sue_str
#     assert sue_dict.get("src_road_delimiter") == slash_src_road_delimiter
#     assert sue_dict.get("dst_road_delimiter") == colon_dst_road_delimiter
#     assert sue_dict.get("unknown_word") == x_unknown_word
#     assert sue_dict.get("bridgekinds")
#     x_bridgekinds = sue_dict.get("bridgekinds")
#     assert len(x_bridgekinds) == 3
#     acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
#     group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
#     road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
#     assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
#     assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
#     assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


# def test_BridgeUnit_get_json_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     sue_bridgeunit = bridgeunit_shop(sue_str)
#     sue_bridgeunit.set_bridgekind(get_clean_roadunit_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_swim_groupid_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())

#     # WHEN
#     sue_json = sue_bridgeunit.get_json()

#     # THEN
#     assert sue_json.find("bridgekinds") == 5
#     assert sue_json.find("src_road_delimiter") == 164


# def test_get_bridgeunit_from_dict_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     slash_src_road_delimiter = "/"
#     colon_dst_road_delimiter = ":"
#     sue_bridgeunit = bridgeunit_shop(
#         sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
#     )
#     sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

#     # WHEN
#     gen_bridgeunit = get_bridgeunit_from_dict(sue_bridgeunit.get_dict())

#     # THEN
#     assert gen_bridgeunit
#     assert gen_bridgeunit.face_id == sue_str
#     assert gen_bridgeunit.src_road_delimiter == slash_src_road_delimiter
#     assert gen_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter
#     assert gen_bridgeunit.unknown_word == x_unknown_word
#     x_bridgekinds = gen_bridgeunit.bridgekinds
#     assert len(x_bridgekinds) == 3
#     acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
#     group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
#     road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
#     assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
#     assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
#     assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()


# def test_get_bridgeunit_from_json_ReturnsObj():
#     # ESTABLISH
#     sue_str = "Sue"
#     x_unknown_word = "UnknownAcctId"
#     slash_src_road_delimiter = "/"
#     colon_dst_road_delimiter = ":"
#     sue_bridgeunit = bridgeunit_shop(
#         sue_str, slash_src_road_delimiter, colon_dst_road_delimiter, x_unknown_word
#     )
#     sue_bridgeunit.set_bridgekind(get_slash_roadunit_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_groupid_bridgekind())
#     sue_bridgeunit.set_bridgekind(get_slash_acctid_bridgekind())

#     # WHEN
#     gen_bridgeunit = get_bridgeunit_from_json(sue_bridgeunit.get_json())

#     # THEN
#     assert gen_bridgeunit
#     assert gen_bridgeunit.face_id == sue_str
#     assert gen_bridgeunit.src_road_delimiter == slash_src_road_delimiter
#     assert gen_bridgeunit.dst_road_delimiter == colon_dst_road_delimiter
#     assert gen_bridgeunit.unknown_word == x_unknown_word
#     x_bridgekinds = gen_bridgeunit.bridgekinds
#     assert len(x_bridgekinds) == 3
#     acct_id_bridgekind = sue_bridgeunit.get_bridgekind(type_AcctID_str())
#     group_id_bridgekind = sue_bridgeunit.get_bridgekind(type_GroupID_str())
#     road_bridgekind = sue_bridgeunit.get_bridgekind(road_str())
#     assert acct_id_bridgekind.get_dict() == get_slash_acctid_bridgekind().get_dict()
#     assert group_id_bridgekind.get_dict() == get_slash_groupid_bridgekind().get_dict()
#     assert road_bridgekind.get_dict() == get_slash_roadunit_bridgekind().get_dict()
