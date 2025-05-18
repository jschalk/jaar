from src.a00_data_toolbox.file_toolbox import get_dir_file_strs, create_path
from src.a06_bud_logic._utils.str_a06 import (
    type_NameStr_str,
    type_LabelStr_str,
    type_WayStr_str,
    type_TitleStr_str,
    concept_way_str,
    face_name_str,
    event_int_str,
    type_NameStr_str,
    type_TitleStr_str,
)
from src.a16_pidgin_logic._utils.str_a16 import (
    otx_bridge_str,
    inx_bridge_str,
    unknown_term_str,
)
from src.a16_pidgin_logic.pidgin import pidginunit_shop
from src.a16_pidgin_logic._utils.env_a16 import (
    env_dir_setup_cleanup,
    get_example_face_dir,
)
from src.a16_pidgin_logic._utils.example_pidgins import (
    get_casa_maison_pidginunit_set_by_otx2inx,
    get_casa_maison_pidginunit_set_by_label,
    get_casa_maison_way_otx2inx_dt,
    get_casa_maison_label_dt,
    get_slash_namemap,
    get_sue_pidginunit,
    get_casa_maison_pidginunit_set_by_label,
    get_pidgin_core_attrs_are_none_namemap,
)
from src.a17_idea_logic.pidgin_toolbox import (
    get_pidgin_name_dt_columns,
    get_pidgin_title_dt_columns,
    get_pidgin_label_dt_columns,
    get_pidgin_way_dt_columns,
    create_pidgin_name_dt,
    create_pidgin_title_dt,
    create_pidgin_label_dt,
    create_pidgin_way_dt,
    create_pidgin_label_dt,
    save_all_csvs_from_pidginunit,
    _load_namemap_from_csv,
    _load_titlemap_from_csv,
    _load_labelmap_from_csv,
    _load_waymap_from_csv,
    _save_pidgin_label_csv,
    create_dir_valid_empty_pidginunit,
    init_pidginunit_from_dir,
)
from src.a17_idea_logic.idea_db_tool import (
    get_ordered_csv,
    get_idea_elements_sort_order as sorting_columns,
)
from os.path import exists as os_path_exists


def test_get_pidgin_name_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_pidgin_name_dt_columns()
    assert len(get_pidgin_name_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
        "otx_name",
        "inx_name",
    ]
    assert get_pidgin_name_dt_columns() == static_list
    assert set(get_pidgin_name_dt_columns()).issubset(set(sorting_columns()))


def test_get_pidgin_title_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_pidgin_title_dt_columns()
    assert len(get_pidgin_title_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
        "otx_title",
        "inx_title",
    ]
    assert get_pidgin_title_dt_columns() == static_list
    assert set(get_pidgin_title_dt_columns()).issubset(set(sorting_columns()))


def test_get_pidgin_label_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_pidgin_label_dt_columns()
    assert len(get_pidgin_label_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
        "otx_label",
        "inx_label",
    ]
    assert get_pidgin_label_dt_columns() == static_list
    assert set(get_pidgin_label_dt_columns()).issubset(set(sorting_columns()))


def test_get_pidgin_way_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_pidgin_way_dt_columns()
    assert len(get_pidgin_way_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_bridge_str(),
        inx_bridge_str(),
        unknown_term_str(),
        "otx_way",
        "inx_way",
    ]
    assert get_pidgin_way_dt_columns() == static_list
    assert set(get_pidgin_way_dt_columns()).issubset(set(sorting_columns()))


def test_create_pidgin_way_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_otx2inx()
    casa_mapunit = casa_pidginunit.get_waymap()

    # WHEN
    casa_dataframe = create_pidgin_way_dt(casa_mapunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_pidgin_way_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_pidgin_way_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(casa_csv)
    print(get_ordered_csv(get_casa_maison_way_otx2inx_dt()))
    assert casa_csv == get_ordered_csv(get_casa_maison_way_otx2inx_dt())


def test_create_pidgin_label_dt_ReturnsObj():
    # ESTABLISH
    casa_pidginunit = get_casa_maison_pidginunit_set_by_label()
    casa_mapunit = casa_pidginunit.get_labelmap()

    # WHEN
    casa_dataframe = create_pidgin_label_dt(casa_mapunit)

    # THEN
    # print(f"{get_pidgin_label_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_pidgin_label_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_label_csv = get_ordered_csv(get_casa_maison_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_label_csv=}")
    assert casa_csv == ex_label_csv


def test_save_all_csvs_from_pidginunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    title_filename = "title.csv"
    label_filename = "label.csv"
    way_filename = "way.csv"
    name_csv_path = create_path(map_dir, name_filename)
    group_csv_path = create_path(map_dir, title_filename)
    label_csv_path = create_path(map_dir, label_filename)
    way_csv_path = create_path(map_dir, way_filename)
    assert os_path_exists(name_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(label_csv_path) is False
    assert os_path_exists(way_csv_path) is False
    assert len(get_dir_file_strs(map_dir)) == 0

    # WHEN
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # THEN
    assert os_path_exists(name_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(label_csv_path)
    assert os_path_exists(way_csv_path)
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
    sue_namemap = empty_pidginunit.get_mapunit(type_NameStr_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 3
    ex_namemap = sue_pidginunit.get_mapunit(type_NameStr_str())
    assert ex_namemap == sue_namemap


def test_load_namemap_from_csv_DoesNotChangeWhenFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    assert os_path_exists(name_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_namemap = empty_pidginunit.get_mapunit(type_NameStr_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 0


def test_load_titlemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(group_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_titlemap = empty_pidginunit.get_mapunit(type_TitleStr_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 2
    ex_titlemap = sue_pidginunit.get_mapunit(type_TitleStr_str())
    assert ex_titlemap == sue_titlemap


def test_load_titlemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    assert os_path_exists(group_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_titlemap = empty_pidginunit.get_mapunit(type_TitleStr_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 0


def test_load_labelmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(label_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_labelmap = empty_pidginunit.get_mapunit(type_LabelStr_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 2
    ex_labelmap = sue_pidginunit.get_mapunit(type_LabelStr_str())
    assert ex_labelmap == sue_labelmap


def test_load_labelmap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    assert os_path_exists(label_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_labelmap = empty_pidginunit.get_mapunit(type_LabelStr_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 0


def test_load_waymap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_pidginunit = get_sue_pidginunit()
    map_dir = get_example_face_dir()
    way_filename = "way.csv"
    way_csv_path = create_path(map_dir, way_filename)
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)
    assert os_path_exists(way_csv_path)
    empty_pidginunit = pidginunit_shop("Sue")
    sue_waymap = empty_pidginunit.get_mapunit(type_WayStr_str())
    sue_waymap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_waymap=}")
    assert len(sue_waymap.otx2inx) == 0

    # WHEN
    sue_waymap = _load_waymap_from_csv(map_dir, sue_waymap)

    # THEN
    assert len(sue_waymap.otx2inx) == 2
    ex_waymap = sue_pidginunit.get_mapunit(type_WayStr_str())
    assert ex_waymap.event_int == sue_waymap.event_int
    assert ex_waymap.face_name == sue_waymap.face_name
    assert ex_waymap.otx2inx == sue_waymap.otx2inx
    assert ex_waymap.labelmap != sue_waymap.labelmap


def test_load_waymap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    way_filename = "way.csv"
    way_csv_path = create_path(map_dir, way_filename)
    assert os_path_exists(way_csv_path) is False
    empty_pidginunit = pidginunit_shop("Sue")
    sue_waymap = empty_pidginunit.get_mapunit(type_WayStr_str())
    sue_waymap.face_name = "Sue"
    print(f"{empty_pidginunit=} {sue_waymap=}")
    assert len(sue_waymap.otx2inx) == 0

    # WHEN
    sue_waymap = _load_waymap_from_csv(map_dir, sue_waymap)

    # THEN
    assert len(sue_waymap.otx2inx) == 0


def test_create_dir_valid_empty_pidginunit_Sets_otx_bridge_inx_bridge(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    sue_pidginunit = pidginunit_shop(
        face_name=sue_str,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # # THEN
    assert gen_pidginunit.unknown_term == x_unknown_term
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    gen_mapunit = gen_pidginunit.get_mapunit(type_NameStr_str())
    assert gen_mapunit.unknown_term == x_unknown_term
    assert gen_mapunit.otx_bridge == slash_otx_bridge
    assert gen_mapunit.inx_bridge == colon_inx_bridge


def test_create_dir_valid_empty_pidginunit_Returns_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_term = "UnknownTerm"
    slash_otx_bridge = "/"
    colon_inx_bridge = ":"
    event7 = 7
    sue_pidginunit = pidginunit_shop(
        face_name=sue_str,
        event_int=event7,
        otx_bridge=slash_otx_bridge,
        inx_bridge=colon_inx_bridge,
        unknown_term=x_unknown_term,
    )
    sue_pidginunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_pidginunit(map_dir, sue_pidginunit)

    # WHEN
    gen_pidginunit = create_dir_valid_empty_pidginunit(map_dir)

    # THEN
    assert gen_pidginunit.face_name == sue_str
    assert gen_pidginunit.event_int == event7
    assert gen_pidginunit.unknown_term == x_unknown_term
    assert gen_pidginunit.otx_bridge == slash_otx_bridge
    assert gen_pidginunit.inx_bridge == colon_inx_bridge
    gen_mapunit = gen_pidginunit.get_mapunit(type_NameStr_str())
    assert gen_mapunit.unknown_term == x_unknown_term
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
    assert gen_pidginunit.titlemap == sue_pidginunit.titlemap
    assert gen_pidginunit.labelmap == sue_pidginunit.labelmap
    assert gen_pidginunit.waymap.labelmap == sue_pidginunit.waymap.labelmap
    assert gen_pidginunit.waymap == sue_pidginunit.waymap
    assert gen_pidginunit == sue_pidginunit
