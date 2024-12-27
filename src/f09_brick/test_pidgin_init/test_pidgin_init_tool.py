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
    get_slash_acctmap,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_idea,
    get_pidgin_core_attrs_are_none_acctmap,
)
from src.f09_brick.pidgin_toolbox import (
    get_map_acct_dt_columns,
    get_map_group_dt_columns,
    get_map_idea_dt_columns,
    get_map_road_dt_columns,
    create_map_acct_dt,
    create_map_group_dt,
    create_map_idea_dt,
    create_map_road_dt,
    create_map_idea_dt,
    save_all_csvs_from_pidginunit,
    _load_acctmap_from_csv,
    _load_groupmap_from_csv,
    _load_ideamap_from_csv,
    _load_roadmap_from_csv,
    _save_map_idea_csv,
    create_dir_valid_empty_pidginunit,
    init_pidginunit_from_dir,
)
from src.f09_brick.pandas_tool import (
    get_ordered_csv,
    get_brick_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_map_acct_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_acct_dt_columns()
    assert len(get_map_acct_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_acct_id",
        "inx_acct_id",
    ]
    assert get_map_acct_dt_columns() == static_list
    assert set(get_map_acct_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_group_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_group_dt_columns()
    assert len(get_map_group_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_group_id",
        "inx_group_id",
    ]
    assert get_map_group_dt_columns() == static_list
    assert set(get_map_group_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_idea_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_idea_dt_columns()
    assert len(get_map_idea_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_idea",
        "inx_idea",
    ]
    assert get_map_idea_dt_columns() == static_list
    assert set(get_map_idea_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_road_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_road_dt_columns()
    assert len(get_map_road_dt_columns()) == 7
    static_list = [
        face_id_str(),
        event_id_str(),
        otx_wall_str(),
        inx_wall_str(),
        unknown_word_str(),
        "otx_road",
        "inx_road",
    ]
    assert get_map_road_dt_columns() == static_list
    assert set(get_map_road_dt_columns()).issubset(set(sorting_columns()))


def test_create_map_road_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    casa_mapunit = casa_pidginunit.get_roadmap()

    # WHEN
    casa_dataframe = create_map_road_dt(casa_mapunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_map_road_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_map_road_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(f"{casa_csv=}")
    print(f"{get_ordered_csv(get_casa_maison_road_otx2inx_dt())=}")
    assert casa_csv == get_ordered_csv(get_casa_maison_road_otx2inx_dt())


def test_create_map_idea_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_idea()
    casa_mapunit = casa_pidginunit.get_ideamap()

    # WHEN
    casa_dataframe = create_map_idea_dt(casa_mapunit)

    # THEN
    # print(f"{get_map_idea_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_map_idea_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_idea_csv = get_ordered_csv(get_casa_maison_idea_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_idea_csv=}")
    assert casa_csv == ex_idea_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    group_filename = "group.csv"
    idea_filename = "idea.csv"
    road_filename = "road.csv"
    acct_csv_path = f"{map_dir}/{acct_filename}"
    group_csv_path = f"{map_dir}/{group_filename}"
    idea_csv_path = f"{map_dir}/{idea_filename}"
    road_csv_path = f"{map_dir}/{road_filename}"
    assert os_path_exists(acct_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(idea_csv_path) is False
    assert os_path_exists(road_csv_path) is False
    assert len(get_dir_file_strs(map_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(acct_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(idea_csv_path)
    assert os_path_exists(road_csv_path)
    assert len(get_dir_file_strs(map_dir)) == 4


def test_load_acctmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    acct_csv_path = f"{map_dir}/{acct_filename}"
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(acct_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctmap = empty_pidginunit.get_mapunit(type_AcctID_str())
    sue_acctmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctmap=}")
    assert len(sue_acctmap.otx2inx) == 0

    # WHEN
    sue_acctmap = _load_acctmap_from_csv(map_dir, sue_acctmap)

    # THEN
    assert len(sue_acctmap.otx2inx) == 3
    ex_acctmap = sue_pidginunit.get_mapunit(type_AcctID_str())
    assert ex_acctmap == sue_acctmap


def test_load_acctmap_from_csv_DoesNothinWhenFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    map_dir = get_example_face_dir()
    acct_filename = "acct.csv"
    acct_csv_path = f"{map_dir}/{acct_filename}"
    assert os_path_exists(acct_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_acctmap = empty_pidginunit.get_mapunit(type_AcctID_str())
    sue_acctmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_acctmap=}")
    assert len(sue_acctmap.otx2inx) == 0

    # WHEN
    sue_acctmap = _load_acctmap_from_csv(map_dir, sue_acctmap)

    # THEN
    assert len(sue_acctmap.otx2inx) == 0


def test_load_groupmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    group_filename = "group.csv"
    group_csv_path = f"{map_dir}/{group_filename}"
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(group_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_groupmap = empty_pidginunit.get_mapunit(type_GroupID_str())
    sue_groupmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_groupmap=}")
    assert len(sue_groupmap.otx2inx) == 0

    # WHEN
    sue_groupmap = _load_groupmap_from_csv(map_dir, sue_groupmap)

    # THEN
    assert len(sue_groupmap.otx2inx) == 2
    ex_groupmap = sue_pidginunit.get_mapunit(type_GroupID_str())
    assert ex_groupmap == sue_groupmap


def test_load_groupmap_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    group_filename = "group.csv"
    group_csv_path = f"{map_dir}/{group_filename}"
    assert os_path_exists(group_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_groupmap = empty_pidginunit.get_mapunit(type_GroupID_str())
    sue_groupmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_groupmap=}")
    assert len(sue_groupmap.otx2inx) == 0

    # WHEN
    sue_groupmap = _load_groupmap_from_csv(map_dir, sue_groupmap)

    # THEN
    assert len(sue_groupmap.otx2inx) == 0


def test_load_ideamap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    idea_filename = "idea.csv"
    idea_csv_path = f"{map_dir}/{idea_filename}"
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(idea_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_ideamap = empty_pidginunit.get_mapunit(type_IdeaUnit_str())
    sue_ideamap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_ideamap=}")
    assert len(sue_ideamap.otx2inx) == 0

    # WHEN
    sue_ideamap = _load_ideamap_from_csv(map_dir, sue_ideamap)

    # THEN
    assert len(sue_ideamap.otx2inx) == 2
    ex_ideamap = sue_pidginunit.get_mapunit(type_IdeaUnit_str())
    assert ex_ideamap == sue_ideamap


def test_load_ideamap_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    idea_filename = "idea.csv"
    idea_csv_path = f"{map_dir}/{idea_filename}"
    assert os_path_exists(idea_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_ideamap = empty_pidginunit.get_mapunit(type_IdeaUnit_str())
    sue_ideamap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_ideamap=}")
    assert len(sue_ideamap.otx2inx) == 0

    # WHEN
    sue_ideamap = _load_ideamap_from_csv(map_dir, sue_ideamap)

    # THEN
    assert len(sue_ideamap.otx2inx) == 0


def test_load_roadmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = f"{map_dir}/{road_filename}"
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(road_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadmap = empty_pidginunit.get_mapunit(type_RoadUnit_str())
    sue_roadmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_roadmap=}")
    assert len(sue_roadmap.otx2inx) == 0

    # WHEN
    sue_roadmap = _load_roadmap_from_csv(map_dir, sue_roadmap)

    # THEN
    assert len(sue_roadmap.otx2inx) == 2
    ex_roadmap = sue_pidginunit.get_mapunit(type_RoadUnit_str())
    assert ex_roadmap.event_id == sue_roadmap.event_id
    assert ex_roadmap.face_id == sue_roadmap.face_id
    assert ex_roadmap.otx2inx == sue_roadmap.otx2inx
    assert ex_roadmap.ideamap != sue_roadmap.ideamap


def test_load_roadmap_from_csv_DoesNothingWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = f"{map_dir}/{road_filename}"
    assert os_path_exists(road_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadmap = empty_pidginunit.get_mapunit(type_RoadUnit_str())
    sue_roadmap.face_id = "Sue"
    print(f"{empty_pidginunit=} {sue_roadmap=}")
    assert len(sue_roadmap.otx2inx) == 0

    # WHEN
    sue_roadmap = _load_roadmap_from_csv(map_dir, sue_roadmap)

    # THEN
    assert len(sue_roadmap.otx2inx) == 0


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
    sue_pidginunit.set_acctmap(get_slash_acctmap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # # THEN
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    gen_mapunit = gen_pidginunit.get_mapunit(type_AcctID_str())
    assert gen_mapunit.unknown_word == x_unknown_word
    assert gen_mapunit.otx_wall == slash_otx_wall
    assert gen_mapunit.inx_wall == colon_inx_wall


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
    sue_pidginunit.set_acctmap(get_slash_acctmap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # THEN
    assert gen_pidginunit.face_id == sue_str
    assert gen_pidginunit.event_id == event7
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_wall == slash_otx_wall
    assert gen_pidginunit.inx_wall == colon_inx_wall
    gen_mapunit = gen_pidginunit.get_mapunit(type_AcctID_str())
    assert gen_mapunit.unknown_word == x_unknown_word
    assert gen_mapunit.otx_wall == slash_otx_wall
    assert gen_mapunit.inx_wall == colon_inx_wall


def test_init_pidginunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = init_pidginunit_from_dir(map_dir)

    # THEN
    assert gen_pidginunit
    assert len(gen_pidginunit.acctmap.otx2inx) == 3

    assert len(sue_pidginunit.acctmap.otx2inx) == 3
    assert gen_pidginunit.acctmap == sue_pidginunit.acctmap
    assert gen_pidginunit.groupmap == sue_pidginunit.groupmap
    assert gen_pidginunit.ideamap == sue_pidginunit.ideamap
    assert gen_pidginunit.roadmap.ideamap == sue_pidginunit.roadmap.ideamap
    assert gen_pidginunit.roadmap == sue_pidginunit.roadmap
    assert gen_pidginunit == sue_pidginunit
