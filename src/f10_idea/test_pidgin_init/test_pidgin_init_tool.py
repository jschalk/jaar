from src.f00_data_toolboxs.file_toolbox import get_dir_file_strs, create_path
from src.f04_pack.atom_config import (
    type_NameUnit_str,
    type_TitleUnit_str,
    type_RoadUnit_str,
    type_LabelUnit_str,
    road_str,
    face_name_str,
    event_int_str,
    type_NameUnit_str,
    type_LabelUnit_str,
)
from src.f09_pidgin.pidgin_config import (
    otx_bridge_str,
    inx_bridge_str,
    unknown_word_str,
)
from src.f09_pidgin.pidgin import pidginunit_shop
from src.f09_pidgin.examples.pidgin_env import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.f09_pidgin.examples.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_pidginunit_set_by_title,
    get_casa_maison_road_otx2inx_dt,
    get_casa_maison_title_dt,
    get_slash_namemap,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_title,
    get_pidgin_core_attrs_are_none_namemap,
)
from src.f10_idea.pidgin_toolbox import (
    get_map_name_dt_columns,
    get_map_label_dt_columns,
    get_map_title_dt_columns,
    get_map_road_dt_columns,
    create_map_name_dt,
    create_map_label_dt,
    create_map_title_dt,
    create_map_road_dt,
    create_map_title_dt,
    save_all_csvs_from_pidginunit,
    _load_namemap_from_csv,
    _load_labelmap_from_csv,
    _load_titlemap_from_csv,
    _load_roadmap_from_csv,
    _save_map_title_csv,
    create_dir_valid_empty_pidginunit,
    init_pidginunit_from_dir,
)
from src.f10_idea.idea_db_tool import (
    get_ordered_csv,
    get_idea_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_map_name_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_name_dt_columns()
    assert len(get_map_name_dt_columns()) == 7
    static_list = [
        face_name_str(),
        event_int_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
        "otx_name",
        "inx_name",
    ]
    assert get_map_name_dt_columns() == static_list
    assert set(get_map_name_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_label_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_label_dt_columns()
    assert len(get_map_label_dt_columns()) == 7
    static_list = [
        face_name_str(),
        event_int_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
        "otx_label",
        "inx_label",
    ]
    assert get_map_label_dt_columns() == static_list
    assert set(get_map_label_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_title_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_title_dt_columns()
    assert len(get_map_title_dt_columns()) == 7
    static_list = [
        face_name_str(),
        event_int_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_word_str(),
        "otx_title",
        "inx_title",
    ]
    assert get_map_title_dt_columns() == static_list
    assert set(get_map_title_dt_columns()).issubset(set(sorting_columns()))


def test_get_map_road_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_map_road_dt_columns()
    assert len(get_map_road_dt_columns()) == 7
    static_list = [
        face_name_str(),
        event_int_str(),
        otx_bridge_str(),
        inx_bridge_str(),
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


def test_create_map_title_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_title()
    casa_mapunit = casa_pidginunit.get_titlemap()

    # WHEN
    casa_dataframe = create_map_title_dt(casa_mapunit)

    # THEN
    # print(f"{get_map_title_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_map_title_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_title_csv = get_ordered_csv(get_casa_maison_title_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_title_csv=}")
    assert casa_csv == ex_title_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    label_filename = "label.csv"
    title_filename = "title.csv"
    road_filename = "road.csv"
    name_csv_path = create_path(map_dir, name_filename)
    group_csv_path = create_path(map_dir, label_filename)
    title_csv_path = create_path(map_dir, title_filename)
    road_csv_path = create_path(map_dir, road_filename)
    assert os_path_exists(name_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(title_csv_path) is False
    assert os_path_exists(road_csv_path) is False
    assert len(get_dir_file_strs(map_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(name_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(title_csv_path)
    assert os_path_exists(road_csv_path)
    assert len(get_dir_file_strs(map_dir)) == 4


def test_load_namemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(name_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_namemap = empty_pidginunit.get_mapunit(type_NameUnit_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 3
    ex_namemap = sue_pidginunit.get_mapunit(type_NameUnit_str())
    assert ex_namemap == sue_namemap


def test_load_namemap_from_csv_DoesNotChangeWhenFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    assert os_path_exists(name_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_namemap = empty_pidginunit.get_mapunit(type_NameUnit_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 0


def test_load_labelmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    group_csv_path = create_path(map_dir, label_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(group_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_labelmap = empty_pidginunit.get_mapunit(type_LabelUnit_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 2
    ex_labelmap = sue_pidginunit.get_mapunit(type_LabelUnit_str())
    assert ex_labelmap == sue_labelmap


def test_load_labelmap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    group_csv_path = create_path(map_dir, label_filename)
    assert os_path_exists(group_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_labelmap = empty_pidginunit.get_mapunit(type_LabelUnit_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 0


def test_load_titlemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    title_csv_path = create_path(map_dir, title_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(title_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_titlemap = empty_pidginunit.get_mapunit(type_TitleUnit_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 2
    ex_titlemap = sue_pidginunit.get_mapunit(type_TitleUnit_str())
    assert ex_titlemap == sue_titlemap


def test_load_titlemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    title_csv_path = create_path(map_dir, title_filename)
    assert os_path_exists(title_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_titlemap = empty_pidginunit.get_mapunit(type_TitleUnit_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 0


def test_load_roadmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = create_path(map_dir, road_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(road_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadmap = empty_pidginunit.get_mapunit(type_RoadUnit_str())
    sue_roadmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_roadmap=}")
    assert len(sue_roadmap.otx2inx) == 0

    # WHEN
    sue_roadmap = _load_roadmap_from_csv(map_dir, sue_roadmap)

    # THEN
    assert len(sue_roadmap.otx2inx) == 2
    ex_roadmap = sue_pidginunit.get_mapunit(type_RoadUnit_str())
    assert ex_roadmap.event_int == sue_roadmap.event_int
    assert ex_roadmap.face_name == sue_roadmap.face_name
    assert ex_roadmap.otx2inx == sue_roadmap.otx2inx
    assert ex_roadmap.titlemap != sue_roadmap.titlemap


def test_load_roadmap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    road_filename = "road.csv"
    road_csv_path = create_path(map_dir, road_filename)
    assert os_path_exists(road_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_roadmap = empty_pidginunit.get_mapunit(type_RoadUnit_str())
    sue_roadmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_roadmap=}")
    assert len(sue_roadmap.otx2inx) == 0

    # WHEN
    sue_roadmap = _load_roadmap_from_csv(map_dir, sue_roadmap)

    # THEN
    assert len(sue_roadmap.otx2inx) == 0


def test_create_dir_valid_empty_pidginunit_Sets_otx_bridge_inx_bridge(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        face_name=sue_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # # THEN
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    gen_mapunit = gen_pidginunit.get_mapunit(type_NameUnit_str())
    assert gen_mapunit.unknown_word == x_unknown_word
    assert gen_mapunit.otx_bridge == slash_otx_bridge
    assert gen_mapunit.inx_bridge == colon_inx_bridge


def test_create_dir_valid_empty_pidginunit_Returns_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_word = "UnknownWord"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    event7 = 7
    sue_pidginunit = pidginunit_shop(
        face_name=sue_str,
        event_int=event7,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_word=x_unknown_word,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # THEN
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == event7
    assert gen_pidginunit.unknown_word == x_unknown_word
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    gen_mapunit = gen_pidginunit.get_mapunit(type_NameUnit_str())
    assert gen_mapunit.unknown_word == x_unknown_word
    assert gen_mapunit.otx_bridge == slash_otx_bridge
    assert gen_mapunit.inx_bridge == colon_inx_bridge


def test_init_pidginunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = init_pidginunit_from_dir(map_dir)

    # THEN
    assert gen_pidginunit
    assert len(gen_pidginunit.namemap.otx2inx) == 3

    assert len(sue_pidginunit.namemap.otx2inx) == 3
    assert gen_pidginunit.namemap == sue_pidginunit.namemap
    assert gen_pidginunit.labelmap == sue_pidginunit.labelmap
    assert gen_pidginunit.titlemap == sue_pidginunit.titlemap
    assert gen_pidginunit.roadmap.titlemap == sue_pidginunit.roadmap.titlemap
    assert gen_pidginunit.roadmap == sue_pidginunit.roadmap
    assert gen_pidginunit == sue_pidginunit
