from src.a00_data_toolbox.file_toolbox import save_file, create_path
from src.a01_word_logic.road import create_road
from src.a08_bud_atom_logic.atom_config import acct_name_str, base_str
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a16_pidgin_logic.pidgin_config import pidgin_filename
from src.a16_pidgin_logic._utils.env_a16 import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.a16_pidgin_logic._utils.example_pidgins import (
    get_casa_maison_pidginunit_set_by_tag,
    get_casa_maison_road_otx_dt,
    get_casa_maison_road_inx_dt,
    get_clean_roadmap,
    get_swim_labelmap,
    get_suita_namemap,
    get_suita_acct_name_otx_dt,
    get_suita_acct_name_inx_dt,
    get_sue_pidginunit,
)
from src.a17_idea_logic.idea_db_tool import (
    save_dataframe_to_csv,
    open_csv,
    move_otx_csvs_to_pidgin_inx,
    _get_pidgen_idea_format_filenames,
    _get_fisc_idea_format_filenames,
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
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_dir = create_path(get_example_face_dir(), sue_otx)
    pidginunit_file_path = create_path(sue_dir, pidgin_filename())
    print(f"{sue_dir=}")
    save_file(sue_dir, pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_suita_acct_name_otx_dt()
    sue_inx_dt = get_suita_acct_name_inx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    example_filename = "acct_name_example.csv"
    otx_file_path = create_path(otz_dir, example_filename)
    inx_file_path = create_path(inz_dir, example_filename)
    save_dataframe_to_csv(sue_otx_dt, otz_dir, example_filename)
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    gen_inx_dt = open_csv(inz_dir, example_filename)
    assert gen_inx_dt.iloc[0][acct_name_str()] == bob_inx
    assert gen_inx_dt.iloc[3][acct_name_str()] == zia_otx
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    static_inx_dt = DataFrame(columns=[acct_name_str()])
    static_inx_dt.loc[0, acct_name_str()] = bob_inx
    static_inx_dt.loc[1, acct_name_str()] = sue_inx
    static_inx_dt.loc[2, acct_name_str()] = xio_inx
    static_inx_dt.loc[3, acct_name_str()] = zia_otx
    assert gen_inx_dt.iloc[0][acct_name_str()] == static_inx_dt.iloc[0][acct_name_str()]
    assert gen_inx_dt.iloc[1][acct_name_str()] == static_inx_dt.iloc[1][acct_name_str()]
    assert gen_inx_dt.iloc[2][acct_name_str()] == static_inx_dt.iloc[2][acct_name_str()]
    assert gen_inx_dt.iloc[3][acct_name_str()] == static_inx_dt.iloc[3][acct_name_str()]
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(acct_name_str()).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(acct_name_str()).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == static_inx_dt.to_csv()


# save two dataframes to be pidgined: two files in otx, two files in inx
def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario1_SingleFile_RoadUnit(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    otx_accord45_str = "accord45"
    inx_accord87_str = "accord87"
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_road = create_road(otx_accord45_str, casa_otx_str)
    casa_inx_road = create_road(inx_accord87_str, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_road = create_road(casa_otx_road, clean_otx_str)
    clean_inx_road = create_road(casa_inx_road, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_road = create_road(clean_otx_road, sweep_str)
    sweep_inx_road = create_road(clean_inx_road, sweep_str)

    sue_pidginunit = get_casa_maison_pidginunit_set_by_tag()
    sue_dir = create_path(get_example_face_dir(), sue_pidginunit.face_name)
    save_file(sue_dir, pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_casa_maison_road_otx_dt()
    sue_inx_dt = get_casa_maison_road_inx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    example_filename = "road1_example.csv"
    otx_file_path = create_path(otz_dir, example_filename)
    inx_file_path = create_path(inz_dir, example_filename)
    save_dataframe_to_csv(sue_otx_dt, otz_dir, example_filename)
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(otx_file_path)
    assert os_path_exists(inx_file_path)
    print(f"{sue_otx_dt=} \n")
    print(f"{sue_inx_dt=} \n")
    gen_inx_dt = open_csv(inz_dir, example_filename)
    assert gen_inx_dt.iloc[0][base_str()] == inx_accord87_str
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
    sue_pidginunit = get_casa_maison_pidginunit_set_by_tag()
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_dir = create_path(get_example_face_dir(), sue_pidginunit.face_name)
    pidginunit_file_path = create_path(sue_dir, pidgin_filename())
    print(f"{sue_dir=}")
    save_file(sue_dir, pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_suita_acct_name_otx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    acct_name_filename = "acct_name_example.csv"
    acct_name_otx_file_path = create_path(otz_dir, acct_name_filename)
    acct_name_inx_file_path = create_path(inz_dir, acct_name_filename)
    road1_otx_dt = get_casa_maison_road_otx_dt()
    road1_filename = "road1_example.csv"
    road1_otx_file_path = create_path(otz_dir, road1_filename)
    road1_inx_file_path = create_path(inz_dir, road1_filename)
    save_dataframe_to_csv(road1_otx_dt, otz_dir, road1_filename)
    save_dataframe_to_csv(sue_otx_dt, otz_dir, acct_name_filename)
    assert os_path_exists(road1_otx_file_path)
    assert os_path_exists(road1_inx_file_path) is False
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(acct_name_otx_file_path)
    assert os_path_exists(acct_name_inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(road1_otx_file_path)
    assert os_path_exists(road1_inx_file_path)
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(acct_name_otx_file_path)
    assert os_path_exists(acct_name_inx_file_path)
    acct_inx_dt = open_csv(inz_dir, acct_name_filename)
    gen_csv = acct_inx_dt.sort_values(acct_name_str()).to_csv(index=False)
    sue_inx_dt = get_suita_acct_name_inx_dt()
    assert gen_csv == sue_inx_dt.sort_values(acct_name_str()).to_csv(index=False)

    gen_road1_inx_dt = open_csv(inz_dir, road1_filename)
    road1_inx_dt = get_casa_maison_road_inx_dt()
    assert gen_road1_inx_dt.to_csv() == road1_inx_dt.to_csv()


def test_get_pidgen_idea_format_filenames_ReturnsObj():
    # ESTABLISH
    br00003_filename = "br00003.xlsx"
    br00042_filename = "br00042.xlsx"
    br00043_filename = "br00043.xlsx"
    br00044_filename = "br00044.xlsx"

    # WHEN
    x_pidgen_idea_filenames = _get_pidgen_idea_format_filenames()

    # THEN
    print(f"{x_pidgen_idea_filenames=}")
    assert br00003_filename not in x_pidgen_idea_filenames
    assert br00042_filename in x_pidgen_idea_filenames
    assert br00043_filename in x_pidgen_idea_filenames
    assert br00044_filename in x_pidgen_idea_filenames
    assert len(x_pidgen_idea_filenames) == 8


def test_get_fisc_idea_format_filenames_ReturnsObj():
    # ESTABLISH
    br00000_filename = "br00000.xlsx"
    br00001_filename = "br00001.xlsx"
    br00002_filename = "br00002.xlsx"
    br00003_filename = "br00003.xlsx"
    br00004_filename = "br00004.xlsx"
    br00005_filename = "br00005.xlsx"
    br00042_filename = "br00042.xlsx"

    # WHEN
    x_pidgen_idea_filenames = _get_fisc_idea_format_filenames()

    # THEN
    print(f"{x_pidgen_idea_filenames=}")
    assert br00000_filename in x_pidgen_idea_filenames
    assert br00001_filename in x_pidgen_idea_filenames
    assert br00002_filename in x_pidgen_idea_filenames
    assert br00003_filename in x_pidgen_idea_filenames
    assert br00004_filename in x_pidgen_idea_filenames
    assert br00005_filename in x_pidgen_idea_filenames
    assert br00042_filename not in x_pidgen_idea_filenames
    assert len(x_pidgen_idea_filenames) == 6
