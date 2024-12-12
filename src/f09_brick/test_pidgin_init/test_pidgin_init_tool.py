from src.f00_instrument.file import get_dir_file_strs
from src.f04_gift.atom_config import (
    type_AcctID_str,
    type_IdeaUnit_str,
    type_RoadUnit_str,
    type_GroupID_str,
    road_str,
    face_id_str,
    type_AcctID_str,
    type_GroupID_str,
)
from src.f08_pidgin.pidgin_config import (
    event_id_str,
    otx_wall_str,
    inx_wall_str,
    unknown_word_str,
)
from src.f08_pidgin.pidgin import pidginunit_shop
from src.f08_pidgin.examples.pidgin_env import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.f08_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_pidginunit_set_by_idea,
    get_casa_maison_road_otx2inx_dt,
    get_casa_maison_idea_dt,
    get_slash_acctbridge,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_idea,
    get_pidgin_core_attrs_are_none_acctbridge,
)
from src.f09_brick.pidgin_toolbox import (
    get_bridge_acct_dt_columns,
    get_bridge_group_dt_columns,
    get_bridge_idea_dt_columns,
    get_bridge_road_dt_columns,
    create_bridge_acct_dt,
    create_bridge_group_dt,
    create_bridge_idea_dt,
    create_bridge_road_dt,
    create_bridge_idea_dt,
    save_all_csvs_from_pidginunit,
    _load_acctbridge_from_csv,
    _load_groupbridge_from_csv,
    _load_ideabridge_from_csv,
    _load_roadbridge_from_csv,
    _save_bridge_idea_csv,
    create_dir_valid_empty_pidginunit,
    init_pidginunit_from_dir,
)
from src.f09_brick.pandas_tool import (
    get_ordered_csv,
    get_brick_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_bridge_acct_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_acct_dt_columns()
    assert len(get_bridge_acct_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_acct_id",
        "inx_acct_id",
    ]
    assert get_bridge_acct_dt_columns() == static_list
    assert set(get_bridge_acct_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_group_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_group_dt_columns()
    assert len(get_bridge_group_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_group_id",
        "inx_group_id",
    ]
    assert get_bridge_group_dt_columns() == static_list
    assert set(get_bridge_group_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_idea_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_idea_dt_columns()
    assert len(get_bridge_idea_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_idea",
        "inx_idea",
    ]
    assert get_bridge_idea_dt_columns() == static_list
    assert set(get_bridge_idea_dt_columns()).issubset(set(sorting_columns()))


def test_get_bridge_road_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_bridge_road_dt_columns()
    assert len(get_bridge_road_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_road",
        "inx_road",
    ]
    assert get_bridge_road_dt_columns() == static_list
    assert set(get_bridge_road_dt_columns()).issubset(set(sorting_columns()))


def test_create_bridge_road_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    casa_bridgeunit = casa_pidginunit.get_roadbridge()

    # WHEN
    casa_dataframe = create_bridge_road_dt(casa_bridgeunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_bridge_road_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_bridge_road_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx2inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx2inx_dt())


def test_create_bridge_idea_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_idea()
    casa_bridgeunit = casa_pidginunit.get_ideabridge()

    # WHEN
    casa_dataframe = create_bridge_idea_dt(casa_bridgeunit)

    # THEN
    # print(f"{get_bridge_idea_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_bridge_idea_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_idea_csv = get_ordered_csv(get_casa_maison_idea_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_idea_csv=}")
    assert casa_csv == ex_idea_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    group_filename = "group.csv"
    idea_filename = "idea.csv"
    road_filename = "road.csv"
    acct_csv_path = f"{bridge_dir}/{acct_filename}"
    group_csv_path = f"{bridge_dir}/{group_filename}"
    idea_csv_path = f"{bridge_dir}/{idea_filename}"
    road_csv_path = f"{bridge_dir}/{road_filename}"
    assert os_path_exists(acct_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(idea_csv_path) is False
    assert os_path_exists(road_csv_path) is False
    assert len(get_dir_file_strs(bridge_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(acct_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(idea_csv_path)
    assert os_path_exists(road_csv_path)
    assert len(get_dir_file_strs(bridge_dir)) == 4


def test_load_acctbridge_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    acct_csv_path = f"{bridge_dir}/{acct_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(acct_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctbridge = empty_pidginunit.get_bridgeunit(type_AcctID_str())
    sue_acctbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctbridge=}")
    assert len(sue_acctbridge.otx2inx) == 0

    # WHEN
    sue_acctbridge = _load_acctbridge_from_csv(bridge_dir, sue_acctbridge)

    # THEN
    assert len(sue_acctbridge.otx2inx) == 3
    ex_acctbridge = sue_pidginunit.get_bridgeunit(type_AcctID_str())
    assert ex_acctbridge == sue_acctbridge


def test_load_acctbridge_from_csv_DoesNothinWhenFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    bridge_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    acct_csv_path = f"{bridge_dir}/{acct_filename}"
    assert os_path_exists(acct_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctbridge = empty_pidginunit.get_bridgeunit(type_AcctID_str())
    sue_acctbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctbridge=}")
    assert len(sue_acctbridge.otx2inx) == 0

    # WHEN
    sue_acctbridge = _load_acctbridge_from_csv(bridge_dir, sue_acctbridge)

    # THEN
    assert len(sue_acctbridge.otx2inx) == 0


def test_load_groupbridge_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    group_filename = "group.csv"
    group_csv_path = f"{bridge_dir}/{group_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(group_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_groupbridge = empty_pidginunit.get_bridgeunit(type_GroupID_str())
    sue_groupbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_groupbridge=}")
    assert len(sue_groupbridge.otx2inx) == 0

    # WHEN
    sue_groupbridge = _load_groupbridge_from_csv(bridge_dir, sue_groupbridge)

    # THEN
    assert len(sue_groupbridge.otx2inx) == 2
    ex_groupbridge = sue_pidginunit.get_bridgeunit(type_GroupID_str())
    assert ex_groupbridge == sue_groupbridge


def test_load_groupbridge_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bridge_dir = get_example_face_dir()
    group_filename = "group.csv"
    group_csv_path = f"{bridge_dir}/{group_filename}"
    assert os_path_exists(group_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_groupbridge = empty_pidginunit.get_bridgeunit(type_GroupID_str())
    sue_groupbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_groupbridge=}")
    assert len(sue_groupbridge.otx2inx) == 0

    # WHEN
    sue_groupbridge = _load_groupbridge_from_csv(bridge_dir, sue_groupbridge)

    # THEN
    assert len(sue_groupbridge.otx2inx) == 0


def test_load_ideabridge_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    idea_filename = "idea.csv"
    idea_csv_path = f"{bridge_dir}/{idea_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(idea_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_ideabridge = empty_pidginunit.get_bridgeunit(type_IdeaUnit_str())
    sue_ideabridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_ideabridge=}")
    assert len(sue_ideabridge.otx2inx) == 0

    # WHEN
    sue_ideabridge = _load_ideabridge_from_csv(bridge_dir, sue_ideabridge)

    # THEN
    assert len(sue_ideabridge.otx2inx) == 2
    ex_ideabridge = sue_pidginunit.get_bridgeunit(type_IdeaUnit_str())
    assert ex_ideabridge == sue_ideabridge


def test_load_ideabridge_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bridge_dir = get_example_face_dir()
    idea_filename = "idea.csv"
    idea_csv_path = f"{bridge_dir}/{idea_filename}"
    assert os_path_exists(idea_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_ideabridge = empty_pidginunit.get_bridgeunit(type_IdeaUnit_str())
    sue_ideabridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_ideabridge=}")
    assert len(sue_ideabridge.otx2inx) == 0

    # WHEN
    sue_ideabridge = _load_ideabridge_from_csv(bridge_dir, sue_ideabridge)

    # THEN
    assert len(sue_ideabridge.otx2inx) == 0


def test_load_roadbridge_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    bridge_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = f"{bridge_dir}/{road_filename}"
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)
    assert os_path_exists(road_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadbridge = empty_pidginunit.get_bridgeunit(type_RoadUnit_str())
    sue_roadbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_roadbridge=}")
    assert len(sue_roadbridge.otx2inx) == 0

    # WHEN
    sue_roadbridge = _load_roadbridge_from_csv(bridge_dir, sue_roadbridge)

    # THEN
    assert len(sue_roadbridge.otx2inx) == 2
    ex_roadbridge = sue_pidginunit.get_bridgeunit(type_RoadUnit_str())
    assert ex_roadbridge.event_id == sue_roadbridge.event_id
    assert ex_roadbridge.face_id == sue_roadbridge.face_id
    assert ex_roadbridge.otx2inx == sue_roadbridge.otx2inx
    assert ex_roadbridge.ideabridge != sue_roadbridge.ideabridge


def test_load_roadbridge_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    bridge_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = f"{bridge_dir}/{road_filename}"
    assert os_path_exists(road_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadbridge = empty_pidginunit.get_bridgeunit(type_RoadUnit_str())
    sue_roadbridge.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_roadbridge=}")
    assert len(sue_roadbridge.otx2inx) == 0

    # WHEN
    sue_roadbridge = _load_roadbridge_from_csv(bridge_dir, sue_roadbridge)

    # THEN
    assert len(sue_roadbridge.otx2inx) == 0


def test_create_dir_valid_empty_pidginunit_Sets_otx_wall_inx_wall(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    sue_pidginunit = pidginunit_shop(
        face_id=sue_str,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
        unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())
    bridge_dir = get_example_face_dir()
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


def test_create_dir_valid_empty_pidginunit_Returns_event_id(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    slash_otx_wall = "/"
    colon_inx_wall = ":"
    event7 = 7
    sue_pidginunit = pidginunit_shop(
        face_id=sue_str,
        event_id=event7,
        otx_wall=slash_otx_wall,
        inx_wall=colon_inx_wall,
        unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_acctbridge(get_slash_acctbridge())
    bridge_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(bridge_dir)

    # THEN
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == event7
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
    bridge_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(bridge_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = init_pidginunit_from_dir(bridge_dir)

    # THEN
    assert gen_pidginunit
    assert len(gen_pidginunit.acctbridge.otx2inx) == 3

    assert len(sue_pidginunit.acctbridge.otx2inx) == 3
    assert gen_pidginunit.acctbridge == sue_pidginunit.acctbridge
    assert gen_pidginunit.groupbridge == sue_pidginunit.groupbridge
    assert gen_pidginunit.ideabridge == sue_pidginunit.ideabridge
    assert gen_pidginunit.roadbridge.ideabridge == sue_pidginunit.roadbridge.ideabridge
    assert gen_pidginunit.roadbridge == sue_pidginunit.roadbridge
    assert gen_pidginunit == sue_pidginunit
