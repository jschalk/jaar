from src.f00_instrument.file import save_file
from src.f01_road.road import create_road
from src.f04_gift.atom_config import acct_id_str, base_str
from src.f09_brick.pandas_tool import save_dataframe_to_csv, open_csv
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f09_brick.pandas_tool import (
    move_otx_csvs_to_pidgin_inx,
    _get_pidgen_brick_format_filenames,
)
from src.f08_pidgin.examples.pidgin_env import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_nub_label,
    get_casa_maison_road_otx_dt,
    get_casa_maison_road_inx_dt,
    get_clean_roadbridge,
    get_swim_groupbridge,
    get_suita_acctbridge,
    get_suita_acctid_otx_dt,
    get_suita_acctid_inx_dt,
    get_sue_pidginunit,
)
from os.path import exists as os_path_exists
from pandas import DataFrame


def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario0_SingleFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bob_otx = "Bob"
    sue_otx = "Sue"
    xio_otx = "Xio"
    zia_otx = "Zia"
    bob_inx = "Bobita"
    sue_inx = "Suita"
    xio_inx = "Xioita"
    sue_pidginunit = pidginunit_shop(sue_otx)
    sue_pidginunit.set_acctbridge(get_suita_acctbridge())
    sue_dir = f"{get_example_face_dir()}/{sue_otx}"
    pidgin_filename = "pidgin.json"
    pidginunit_file_path = f"{sue_dir}/{pidgin_filename}"
    print(f"{sue_dir=}")
    save_file(sue_dir, pidgin_filename, sue_pidginunit.get_json())
    sue_otx_dt = get_suita_acctid_otx_dt()
    sue_inx_dt = get_suita_acctid_inx_dt()
    otx_dir = f"{sue_dir}/otx"
    inx_dir = f"{sue_dir}/inx"

    example_filename = "acct_id_example.csv"
    otx_file_path = f"{otx_dir}/{example_filename}"
    inx_file_path = f"{inx_dir}/{example_filename}"
    save_dataframe_to_csv(sue_otx_dt, otx_dir, example_filename)
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    gen_inx_dt = open_csv(inx_dir, example_filename)
    assert gen_inx_dt.iloc[0][acct_id_str()] == bob_inx
    assert gen_inx_dt.iloc[3][acct_id_str()] == zia_otx
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    static_inx_dt = DataFrame(columns=[acct_id_str()])
    static_inx_dt.loc[0, acct_id_str()] = bob_inx
    static_inx_dt.loc[1, acct_id_str()] = sue_inx
    static_inx_dt.loc[2, acct_id_str()] = xio_inx
    static_inx_dt.loc[3, acct_id_str()] = zia_otx
    assert gen_inx_dt.iloc[0][acct_id_str()] == static_inx_dt.iloc[0][acct_id_str()]
    assert gen_inx_dt.iloc[1][acct_id_str()] == static_inx_dt.iloc[1][acct_id_str()]
    assert gen_inx_dt.iloc[2][acct_id_str()] == static_inx_dt.iloc[2][acct_id_str()]
    assert gen_inx_dt.iloc[3][acct_id_str()] == static_inx_dt.iloc[3][acct_id_str()]
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(acct_id_str()).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(acct_id_str()).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == static_inx_dt.to_csv()


# save two dataframes to be pidgined: two files in otx, two files in inx
def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario1_SingleFile_RoadUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    otx_music45_str = "music45"
    inx_music87_str = "music87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_music45_str, casa_otx_str)
    casa_inx_road = create_road(inx_music87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)

    sue_pidginunit = get_casa_maison_pidginunit_set_by_nub_label()
    sue_dir = f"{get_example_face_dir()}/{sue_pidginunit.face_id}"
    save_file(sue_dir, "pidgin.json", sue_pidginunit.get_json())
    sue_otx_dt = get_casa_maison_road_otx_dt()
    sue_inx_dt = get_casa_maison_road_inx_dt()
    otx_dir = f"{sue_dir}/otx"
    inx_dir = f"{sue_dir}/inx"

    example_filename = "road1_example.csv"
    otx_file_path = f"{otx_dir}/{example_filename}"
    inx_file_path = f"{inx_dir}/{example_filename}"
    save_dataframe_to_csv(sue_otx_dt, otx_dir, example_filename)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    print(f"{sue_otx_dt=} \n")
    print(f"{sue_inx_dt=} \n")
    gen_inx_dt = open_csv(inx_dir, example_filename)
    assert gen_inx_dt.iloc[0][base_str()] == inx_music87_str
    assert gen_inx_dt.iloc[1][base_str()] == casa_inx_road
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    assert gen_inx_dt.iloc[0][base_str()] == sue_inx_dt.iloc[0][base_str()]
    assert gen_inx_dt.iloc[1][base_str()] == sue_inx_dt.iloc[1][base_str()]
    assert gen_inx_dt.iloc[2][base_str()] == sue_inx_dt.iloc[2][base_str()]
    assert gen_inx_dt.iloc[3][base_str()] == sue_inx_dt.iloc[3][base_str()]
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(base_str()).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(base_str()).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == sue_inx_dt.to_csv()


# save two dataframes to be pidgined: two files in otx, two files in inx
def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario2_TwoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_pidginunit = get_casa_maison_pidginunit_set_by_nub_label()
    sue_pidginunit.set_acctbridge(get_suita_acctbridge())
    sue_dir = f"{get_example_face_dir()}/{sue_pidginunit.face_id}"
    pidgin_filename = "pidgin.json"
    pidginunit_file_path = f"{sue_dir}/{pidgin_filename}"
    print(f"{sue_dir=}")
    save_file(sue_dir, pidgin_filename, sue_pidginunit.get_json())
    sue_otx_dt = get_suita_acctid_otx_dt()
    otx_dir = f"{sue_dir}/otx"
    inx_dir = f"{sue_dir}/inx"

    acct_id_filename = "acct_id_example.csv"
    acct_id_otx_file_path = f"{otx_dir}/{acct_id_filename}"
    acct_id_inx_file_path = f"{inx_dir}/{acct_id_filename}"
    road1_otx_dt = get_casa_maison_road_otx_dt()
    road1_filename = "road1_example.csv"
    road1_otx_file_path = f"{otx_dir}/{road1_filename}"
    road1_inx_file_path = f"{inx_dir}/{road1_filename}"
    save_dataframe_to_csv(road1_otx_dt, otx_dir, road1_filename)
    save_dataframe_to_csv(sue_otx_dt, otx_dir, acct_id_filename)
    assert os_path_exists(road1_otx_file_path)
    assert os_path_exists(road1_inx_file_path) is False
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(acct_id_otx_file_path)
    assert os_path_exists(acct_id_inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(road1_otx_file_path)
    assert os_path_exists(road1_inx_file_path)
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(acct_id_otx_file_path)
    assert os_path_exists(acct_id_inx_file_path)
    acct_inx_dt = open_csv(inx_dir, acct_id_filename)
    gen_csv = acct_inx_dt.sort_values(acct_id_str()).to_csv(index=False)
    sue_inx_dt = get_suita_acctid_inx_dt()
    assert gen_csv == sue_inx_dt.sort_values(acct_id_str()).to_csv(index=False)

    gen_road1_inx_dt = open_csv(inx_dir, road1_filename)
    road1_inx_dt = get_casa_maison_road_inx_dt()
    assert gen_road1_inx_dt.to_csv() == road1_inx_dt.to_csv()


def test_get_pidgen_brick_format_filenames_ReturnsObj():
    # ESTABLISH
    br00003_file_name = "br00003.xlsx"
    br00041_file_name = "br00041.xlsx"
    br00042_file_name = "br00042.xlsx"
    br00044_file_name = "br00044.xlsx"

    # WHEN
    x_pidgen_brick_filenames = _get_pidgen_brick_format_filenames()

    # THEN
    print(f"{x_pidgen_brick_filenames=}")
    assert br00003_file_name not in x_pidgen_brick_filenames
    assert br00041_file_name in x_pidgen_brick_filenames
    assert br00042_file_name in x_pidgen_brick_filenames
    assert br00044_file_name in x_pidgen_brick_filenames
    assert len(x_pidgen_brick_filenames) == 10


# def test_get_pidgen_brick_format_filenames_ReturnsObj():
#     # ESTABLISH
#     env_dir = get_example_face_dir()
#     br00003_file_name = "br00003.xlsx"
#     br00040_file_name = "br00040.xlsx"
#     br00041_file_name = "br00041.xlsx"
#     br00042_file_name = "br00042.xlsx"
#     save_file(env_dir, br00003_file_name, "")
#     save_file(env_dir, br00040_file_name, "")
#     save_file(env_dir, br00041_file_name, "")
#     save_file(env_dir, br00042_file_name, "")

#     # WHEN
#     x_pidgen_brick_filenames = _get_pidgen_brick_format_filenames()

#     # THEN
#     print(f"{x_pidgen_brick_filenames=}")
#     assert br00003_file_name not in x_pidgen_brick_filenames
#     assert br00040_file_name in x_pidgen_brick_filenames
#     assert br00041_file_name in x_pidgen_brick_filenames
#     assert br00042_file_name not in x_pidgen_brick_filenames
#     assert len(x_pidgen_brick_filenames) == 2
