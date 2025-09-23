from os.path import exists as os_path_exists
from pandas import DataFrame
from src.ch01_data_toolbox.file_toolbox import create_path, save_file
from src.ch02_rope_logic.rope import create_rope, to_rope
from src.ch16_pidgin_logic.pidgin_config import get_pidgin_filename
from src.ch16_pidgin_logic.pidgin_main import pidginunit_shop
from src.ch16_pidgin_logic.test._util.example_pidgins import (
    get_casa_maison_pidginunit_set_by_label,
    get_casa_maison_rope_inx_dt,
    get_casa_maison_rope_otx_dt,
    get_clean_ropemap,
    get_sue_pidginunit,
    get_suita_namemap,
    get_suita_voice_name_inx_dt,
    get_suita_voice_name_otx_dt,
    get_swim_titlemap,
)
from src.ch17_idea_logic._ref.ch17_keywords import reason_context_str, voice_name_str
from src.ch17_idea_logic.idea_db_tool import (
    _get_pidgen_idea_format_filenames,
    move_otx_csvs_to_pidgin_inx,
    open_csv,
    save_dataframe_to_csv,
)
from src.ch17_idea_logic.test._util.ch17_env import (
    env_dir_setup_cleanup,
    idea_moments_dir as get_example_face_dir,
)


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
    pidginunit_file_path = create_path(sue_dir, get_pidgin_filename())
    print(f"{sue_dir=}")
    save_file(sue_dir, get_pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_suita_voice_name_otx_dt()
    sue_inx_dt = get_suita_voice_name_inx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    example_filename = "voice_name_example.csv"
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
    assert gen_inx_dt.iloc[0][voice_name_str()] == bob_inx
    assert gen_inx_dt.iloc[3][voice_name_str()] == zia_otx
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    static_inx_dt = DataFrame(columns=[voice_name_str()])
    static_inx_dt.loc[0, voice_name_str()] = bob_inx
    static_inx_dt.loc[1, voice_name_str()] = sue_inx
    static_inx_dt.loc[2, voice_name_str()] = xio_inx
    static_inx_dt.loc[3, voice_name_str()] = zia_otx
    assert (
        gen_inx_dt.iloc[0][voice_name_str()] == static_inx_dt.iloc[0][voice_name_str()]
    )
    assert (
        gen_inx_dt.iloc[1][voice_name_str()] == static_inx_dt.iloc[1][voice_name_str()]
    )
    assert (
        gen_inx_dt.iloc[2][voice_name_str()] == static_inx_dt.iloc[2][voice_name_str()]
    )
    assert (
        gen_inx_dt.iloc[3][voice_name_str()] == static_inx_dt.iloc[3][voice_name_str()]
    )
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(voice_name_str()).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(voice_name_str()).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == static_inx_dt.to_csv()


# save two dataframes to be pidgined: two files in otx, two files in inx
def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario1_SingleFile_RopePointer(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    otx_amy45_str = "amy45"
    inx_amy87_str = "amy87"
    otx_amy45_rope = to_rope(otx_amy45_str)
    inx_amy87_rope = to_rope(inx_amy87_str)
    casa_otx_str = "casa"
    casa_inx_str = "maison"
    casa_otx_rope = create_rope(otx_amy45_rope, casa_otx_str)
    casa_inx_rope = create_rope(inx_amy87_rope, casa_inx_str)
    clean_otx_str = "clean"
    clean_inx_str = "propre"
    clean_otx_rope = create_rope(casa_otx_rope, clean_otx_str)
    clean_inx_rope = create_rope(casa_inx_rope, clean_inx_str)
    sweep_str = "sweep"
    sweep_otx_rope = create_rope(clean_otx_rope, sweep_str)
    sweep_inx_rope = create_rope(clean_inx_rope, sweep_str)

    sue_pidginunit = get_casa_maison_pidginunit_set_by_label()
    sue_dir = create_path(get_example_face_dir(), sue_pidginunit.face_name)
    save_file(sue_dir, get_pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_casa_maison_rope_otx_dt()
    sue_inx_dt = get_casa_maison_rope_inx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    example_filename = "rope1_example.csv"
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
    assert gen_inx_dt.iloc[0][reason_context_str()] == inx_amy87_rope
    assert gen_inx_dt.iloc[1][reason_context_str()] == casa_inx_rope
    assert gen_inx_dt.to_csv() != sue_otx_dt.to_csv()
    assert (
        gen_inx_dt.iloc[0][reason_context_str()]
        == sue_inx_dt.iloc[0][reason_context_str()]
    )
    assert (
        gen_inx_dt.iloc[1][reason_context_str()]
        == sue_inx_dt.iloc[1][reason_context_str()]
    )
    assert (
        gen_inx_dt.iloc[2][reason_context_str()]
        == sue_inx_dt.iloc[2][reason_context_str()]
    )
    assert (
        gen_inx_dt.iloc[3][reason_context_str()]
        == sue_inx_dt.iloc[3][reason_context_str()]
    )
    print(f"{gen_inx_dt.to_csv(index=False)=}")
    gen_csv = gen_inx_dt.sort_values(reason_context_str()).to_csv(index=False)
    sue_inx_csv = sue_inx_dt.sort_values(reason_context_str()).to_csv(index=False)
    assert gen_csv == sue_inx_csv
    assert gen_inx_dt.to_csv() == sue_inx_dt.to_csv()


# save two dataframes to be pidgined: two files in otx, two files in inx
def test_move_otx_csvs_to_pidgin_inx_CreatesPidginedFiles_Scenario2_TwoFile(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_pidginunit = get_casa_maison_pidginunit_set_by_label()
    sue_pidginunit.set_namemap(get_suita_namemap())
    sue_dir = create_path(get_example_face_dir(), sue_pidginunit.face_name)
    pidginunit_file_path = create_path(sue_dir, get_pidgin_filename())
    print(f"{sue_dir=}")
    save_file(sue_dir, get_pidgin_filename(), sue_pidginunit.get_json())
    sue_otx_dt = get_suita_voice_name_otx_dt()
    otz_dir = create_path(sue_dir, "otz")
    inz_dir = create_path(sue_dir, "inz")

    voice_name_filename = "voice_name_example.csv"
    voice_name_otx_file_path = create_path(otz_dir, voice_name_filename)
    voice_name_inx_file_path = create_path(inz_dir, voice_name_filename)
    rope1_otx_dt = get_casa_maison_rope_otx_dt()
    rope1_filename = "rope1_example.csv"
    rope1_otx_file_path = create_path(otz_dir, rope1_filename)
    rope1_inx_file_path = create_path(inz_dir, rope1_filename)
    save_dataframe_to_csv(rope1_otx_dt, otz_dir, rope1_filename)
    save_dataframe_to_csv(sue_otx_dt, otz_dir, voice_name_filename)
    assert os_path_exists(rope1_otx_file_path)
    assert os_path_exists(rope1_inx_file_path) is False
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(voice_name_otx_file_path)
    assert os_path_exists(voice_name_inx_file_path) is False

    # WHEN
    move_otx_csvs_to_pidgin_inx(sue_dir)

    # THEN
    assert os_path_exists(rope1_otx_file_path)
    assert os_path_exists(rope1_inx_file_path)
    assert os_path_exists(pidginunit_file_path)
    assert os_path_exists(voice_name_otx_file_path)
    assert os_path_exists(voice_name_inx_file_path)
    voice_inx_dt = open_csv(inz_dir, voice_name_filename)
    gen_csv = voice_inx_dt.sort_values(voice_name_str()).to_csv(index=False)
    sue_inx_dt = get_suita_voice_name_inx_dt()
    assert gen_csv == sue_inx_dt.sort_values(voice_name_str()).to_csv(index=False)

    gen_rope1_inx_dt = open_csv(inz_dir, rope1_filename)
    rope1_inx_dt = get_casa_maison_rope_inx_dt()
    assert gen_rope1_inx_dt.to_csv() == rope1_inx_dt.to_csv()


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
