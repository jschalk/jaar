from src.f00_instrument.file import save_file
from src.f00_instrument.pandas_tool import save_dataframe_to_csv
from src.f01_road.road import default_road_delimiter_if_none, create_road
from src.f04_gift.atom_config import (
    acct_id_str,
    base_str,
    road_str,
    type_AcctID_str,
    type_GroupID_str,
)
from src.f08_brick.brick import open_brick_csv
from src.f09_filter.bridge import bridgeunit_shop
from src.f09_filter.filter import filter_face_dir_files
from src.f09_filter.examples.filter_env import (
    env_dir_setup_cleanup,
    get_test_faces_dir,
)
from src.f09_filter.examples.example_bridges import (
    get_casa_maison_bridgeunit_set_by_explicit_label_map,
    get_casa_maison_road_src_dt,
    get_casa_maison_road_dst_dt,
    get_clean_roadunit_bridgekind,
    get_swim_groupid_bridgekind,
    get_suita_acctid_bridgekind,
    get_suita_acctid_src_dt,
    get_suita_acctid_dst_dt,
    get_sue_bridgeunit,
)
from os.path import exists as os_path_exists
from pandas import DataFrame


def test_filter_face_dir_files_CreatesFilteredFiles_Scenario0_SingleFile(
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
    sue_dir = f"{get_test_faces_dir()}/{sue_src}"
    bridge_filename = "bridge.json"
    bridgeunit_file_path = f"{sue_dir}/{bridge_filename}"
    print(f"{sue_dir=}")
    save_file(sue_dir, bridge_filename, sue_bridgeunit.get_json())
    sue_src_dt = get_suita_acctid_src_dt()
    sue_dst_dt = get_suita_acctid_dst_dt()
    src_dir = f"{sue_dir}/src"
    dst_dir = f"{sue_dir}/dst"

    example_filename = "appt_id_example.csv"
    src_file_path = f"{src_dir}/{example_filename}"
    dst_file_path = f"{dst_dir}/{example_filename}"
    save_dataframe_to_csv(sue_src_dt, src_dir, example_filename)
    assert os_path_exists(bridgeunit_file_path)
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path) is False

    # WHEN
    filter_face_dir_files(sue_dir)

    # THEN
    assert os_path_exists(bridgeunit_file_path)
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path)
    gen_dst_dt = open_brick_csv(dst_dir, example_filename)
    assert gen_dst_dt.iloc[0][acct_id_str()] == zia_src
    assert gen_dst_dt.iloc[1][acct_id_str()] == sue_dst
    assert gen_dst_dt.to_csv() != sue_src_dt.to_csv()
    static_dst_dt = DataFrame(columns=[acct_id_str()])
    static_dst_dt.loc[0, acct_id_str()] = zia_src
    static_dst_dt.loc[1, acct_id_str()] = sue_dst
    static_dst_dt.loc[2, acct_id_str()] = bob_dst
    static_dst_dt.loc[3, acct_id_str()] = xio_dst
    assert gen_dst_dt.iloc[0][acct_id_str()] == static_dst_dt.iloc[0][acct_id_str()]
    assert gen_dst_dt.iloc[1][acct_id_str()] == static_dst_dt.iloc[1][acct_id_str()]
    assert gen_dst_dt.iloc[2][acct_id_str()] == static_dst_dt.iloc[2][acct_id_str()]
    assert gen_dst_dt.iloc[3][acct_id_str()] == static_dst_dt.iloc[3][acct_id_str()]
    print(f"{gen_dst_dt.to_csv(index=False)=}")
    gen_csv = gen_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
    sue_dst_csv = sue_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
    assert gen_csv == sue_dst_csv
    assert gen_dst_dt.to_csv() == static_dst_dt.to_csv()


# # save two dataframes to be filtered: two files in src, two files in dst
# def test_filter_face_dir_files_CreatesFilteredFiles_Scenario1_TwoFile(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     bob_src = "Bob"
#     sue_src = "Sue"
#     xio_src = "Xio"
#     zia_src = "Zia"
#     bob_dst = "Bobita"
#     sue_dst = "Suita"
#     xio_dst = "Xioita"
#     sue_bridgeunit = bridgeunit_shop(sue_src)
#     sue_bridgeunit.set_bridgekind(get_suita_acctid_bridgekind())
#     sue_dir = f"{get_test_faces_dir()}/{sue_src}"
#     bridge_filename = "bridge.json"
#     bridgeunit_file_path = f"{sue_dir}/{bridge_filename}"
#     print(f"{sue_dir=}")
#     save_file(sue_dir, bridge_filename, sue_bridgeunit.get_json())
#     sue_src_dt = get_suita_acctid_src_dt()
#     sue_dst_dt = get_clean_roadunit_bridgekind()
#     src_dir = f"{sue_dir}/src"
#     dst_dir = f"{sue_dir}/dst"

#     example1_filename = "appt_id_example1.csv"
#     example2_filename = "appt_id_example2.csv"
#     src1_file_path = f"{src_dir}/{example1_filename}"
#     src2_file_path = f"{src_dir}/{example2_filename}"
#     dst1_file_path = f"{dst_dir}/{example1_filename}"
#     dst2_file_path = f"{dst_dir}/{example2_filename}"

#     create_dir(src_dir)
#     sue_src_dt.to_csv(src_file_path, index=False)
#     assert os_path_exists(bridgeunit_file_path)
#     assert os_path_exists(src_file_path)
#     assert os_path_exists(dst_file_path) is False

#     # WHEN
#     filter_face_dir_files(sue_dir)

#     # THEN
#     assert os_path_exists(bridgeunit_file_path)
#     assert os_path_exists(src_file_path)
#     assert os_path_exists(dst_file_path)
#     gen_dst_dt = open_brick_csv(dst_dir, example_filename)
#     assert gen_dst_dt.iloc[0][acct_id_str()] == zia_src
#     assert gen_dst_dt.iloc[1][acct_id_str()] == sue_dst
#     assert gen_dst_dt.to_csv() != sue_src_dt.to_csv()
#     static_dst_dt = DataFrame(columns=[acct_id_str()])
#     static_dst_dt.loc[0, acct_id_str()] = zia_src
#     static_dst_dt.loc[1, acct_id_str()] = sue_dst
#     static_dst_dt.loc[2, acct_id_str()] = bob_dst
#     static_dst_dt.loc[3, acct_id_str()] = xio_dst
#     assert gen_dst_dt.iloc[0][acct_id_str()] == static_dst_dt.iloc[0][acct_id_str()]
#     assert gen_dst_dt.iloc[1][acct_id_str()] == static_dst_dt.iloc[1][acct_id_str()]
#     assert gen_dst_dt.iloc[2][acct_id_str()] == static_dst_dt.iloc[2][acct_id_str()]
#     assert gen_dst_dt.iloc[3][acct_id_str()] == static_dst_dt.iloc[3][acct_id_str()]
#     print(f"{gen_dst_dt.to_csv(index=False)=}")
#     gen_csv = gen_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
#     sue_dst_csv = sue_dst_dt.sort_values(acct_id_str()).to_csv(index=False)
#     assert gen_csv == sue_dst_csv
#     assert gen_dst_dt.to_csv() == static_dst_dt.to_csv()


# save two dataframes to be filtered: two files in src, two files in dst
def test_filter_face_dir_files_CreatesFilteredFiles_Scenario2_SingleFile_RoadUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    src_music45_str = "music45"
    dst_music87_str = "music87"
    casa_src_str = "casa"
    casa_dst_str = "maison"
    casa_src_road = create_road(src_music45_str, casa_src_str)
    casa_dst_road = create_road(dst_music87_str, casa_dst_str)
    clean_src_str = "clean"
    clean_dst_str = "propre"
    clean_src_road = create_road(casa_src_road, clean_src_str)
    clean_dst_road = create_road(casa_dst_road, clean_dst_str)
    sweep_str = "sweep"
    sweep_src_road = create_road(clean_src_road, sweep_str)
    sweep_dst_road = create_road(clean_dst_road, sweep_str)

    sue_bridgeunit = get_casa_maison_bridgeunit_set_by_explicit_label_map()
    sue_dir = f"{get_test_faces_dir()}/{sue_bridgeunit.face_id}"
    save_file(sue_dir, "bridge.json", sue_bridgeunit.get_json())
    sue_src_dt = get_casa_maison_road_src_dt()
    sue_dst_dt = get_casa_maison_road_dst_dt()
    src_dir = f"{sue_dir}/src"
    dst_dir = f"{sue_dir}/dst"

    example_filename = "road1_example.csv"
    src_file_path = f"{src_dir}/{example_filename}"
    dst_file_path = f"{dst_dir}/{example_filename}"
    save_dataframe_to_csv(sue_src_dt, src_dir, example_filename)
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path) is False

    # WHEN
    filter_face_dir_files(sue_dir)

    # THEN
    assert os_path_exists(src_file_path)
    assert os_path_exists(dst_file_path)
    print(f"{sue_src_dt=} \n")
    print(f"{sue_dst_dt=} \n")
    gen_dst_dt = open_brick_csv(dst_dir, example_filename)
    assert gen_dst_dt.iloc[0][base_str()] == dst_music87_str
    assert gen_dst_dt.iloc[1][base_str()] == casa_dst_road
    assert gen_dst_dt.to_csv() != sue_src_dt.to_csv()
    assert gen_dst_dt.iloc[0][base_str()] == sue_dst_dt.iloc[0][base_str()]
    assert gen_dst_dt.iloc[1][base_str()] == sue_dst_dt.iloc[1][base_str()]
    assert gen_dst_dt.iloc[2][base_str()] == sue_dst_dt.iloc[2][base_str()]
    assert gen_dst_dt.iloc[3][base_str()] == sue_dst_dt.iloc[3][base_str()]
    print(f"{gen_dst_dt.to_csv(index=False)=}")
    gen_csv = gen_dst_dt.sort_values(base_str()).to_csv(index=False)
    sue_dst_csv = sue_dst_dt.sort_values(base_str()).to_csv(index=False)
    assert gen_csv == sue_dst_csv
    assert gen_dst_dt.to_csv() == sue_dst_dt.to_csv()


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
