from os.path import exists as os_path_exists
from src.ch01_data_toolbox.file_toolbox import create_path, get_dir_file_strs
from src.ch16_lire_logic.lire_main import lireunit_shop
from src.ch16_lire_logic.test._util.example_lires import (
    get_casa_maison_label_dt,
    get_casa_maison_lireunit_set_by_label,
    get_casa_maison_lireunit_set_by_otx2inx,
    get_casa_maison_rope_otx2inx_dt,
    get_lire_core_attrs_are_none_namemap,
    get_slash_namemap,
    get_sue_lireunit,
)
from src.ch17_idea_logic._ref.ch17_keywords import (
    LabelTerm_str,
    NameTerm_str,
    RopeTerm_str,
    TitleTerm_str,
    event_int_str,
    face_name_str,
    inx_knot_str,
    otx_knot_str,
    unknown_str_str,
)
from src.ch17_idea_logic.idea_db_tool import (
    get_idea_elements_sort_order as sorting_columns,
    get_ordered_csv,
)
from src.ch17_idea_logic.lire_toolbox import (
    _load_labelmap_from_csv,
    _load_namemap_from_csv,
    _load_ropemap_from_csv,
    _load_titlemap_from_csv,
    _save_lire_label_csv,
    create_dir_valid_empty_lireunit,
    create_lire_label_dt,
    create_lire_name_dt,
    create_lire_rope_dt,
    create_lire_title_dt,
    get_lire_label_dt_columns,
    get_lire_name_dt_columns,
    get_lire_rope_dt_columns,
    get_lire_title_dt_columns,
    init_lireunit_from_dir,
    save_all_csvs_from_lireunit,
)
from src.ch17_idea_logic.test._util.ch17_env import (
    env_dir_setup_cleanup,
    idea_moments_dir as get_example_face_dir,
)


def test_get_lire_name_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_lire_name_dt_columns()
    assert len(get_lire_name_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_knot_str(),
        inx_knot_str(),
        unknown_str_str(),
        "otx_name",
        "inx_name",
    ]
    assert get_lire_name_dt_columns() == static_list
    assert set(get_lire_name_dt_columns()).issubset(set(sorting_columns()))


def test_get_lire_title_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_lire_title_dt_columns()
    assert len(get_lire_title_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_knot_str(),
        inx_knot_str(),
        unknown_str_str(),
        "otx_title",
        "inx_title",
    ]
    assert get_lire_title_dt_columns() == static_list
    assert set(get_lire_title_dt_columns()).issubset(set(sorting_columns()))


def test_get_lire_label_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_lire_label_dt_columns()
    assert len(get_lire_label_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_knot_str(),
        inx_knot_str(),
        unknown_str_str(),
        "otx_label",
        "inx_label",
    ]
    assert get_lire_label_dt_columns() == static_list
    assert set(get_lire_label_dt_columns()).issubset(set(sorting_columns()))


def test_get_lire_rope_dt_columns_ReturnsObj():
    # ESTABLISH / WHEN /THEN
    assert get_lire_rope_dt_columns()
    assert len(get_lire_rope_dt_columns()) == 7
    static_list = [
        event_int_str(),
        face_name_str(),
        otx_knot_str(),
        inx_knot_str(),
        unknown_str_str(),
        "otx_rope",
        "inx_rope",
    ]
    assert get_lire_rope_dt_columns() == static_list
    assert set(get_lire_rope_dt_columns()).issubset(set(sorting_columns()))


def test_create_lire_rope_dt_ReturnsObj():
    # ESTABLISH
    casa_lireunit = get_casa_maison_lireunit_set_by_otx2inx()
    casa_mapunit = casa_lireunit.get_ropemap()

    # WHEN
    casa_dataframe = create_lire_rope_dt(casa_mapunit)
    print(f"{casa_dataframe=}")

    # THEN
    assert list(casa_dataframe.columns) == get_lire_rope_dt_columns()
    assert len(casa_dataframe) == 4
    casa_csv = get_ordered_csv(casa_dataframe)
    print(f"{get_lire_rope_dt_columns()=}")
    print(f"{casa_dataframe.columns=}")
    print(casa_csv)
    print(get_ordered_csv(get_casa_maison_rope_otx2inx_dt()))
    assert casa_csv == get_ordered_csv(get_casa_maison_rope_otx2inx_dt())


def test_create_lire_label_dt_ReturnsObj():
    # ESTABLISH
    casa_lireunit = get_casa_maison_lireunit_set_by_label()
    casa_mapunit = casa_lireunit.get_labelmap()

    # WHEN
    casa_dataframe = create_lire_label_dt(casa_mapunit)

    # THEN
    # print(f"{get_lire_label_dt_columns()=}")
    # print(f"    {list(casa_dataframe.columns)=}")
    # print("")
    # print(f"{casa_dataframe=}")
    assert list(casa_dataframe.columns) == get_lire_label_dt_columns()
    assert len(casa_dataframe) == 3
    casa_csv = get_ordered_csv(casa_dataframe)
    ex_label_csv = get_ordered_csv(get_casa_maison_label_dt())
    print(f"       {casa_csv=}")
    print(f"{ex_label_csv=}")
    assert casa_csv == ex_label_csv


def test_save_all_csvs_from_lireunit_SavesFiles(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    title_filename = "title.csv"
    label_filename = "label.csv"
    rope_filename = "rope.csv"
    name_csv_path = create_path(map_dir, name_filename)
    group_csv_path = create_path(map_dir, title_filename)
    label_csv_path = create_path(map_dir, label_filename)
    rope_csv_path = create_path(map_dir, rope_filename)
    assert os_path_exists(name_csv_path) is False
    assert os_path_exists(group_csv_path) is False
    assert os_path_exists(label_csv_path) is False
    assert os_path_exists(rope_csv_path) is False
    assert len(get_dir_file_strs(map_dir)) == 0

    # WHEN
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)

    # THEN
    assert os_path_exists(name_csv_path)
    assert os_path_exists(group_csv_path)
    assert os_path_exists(label_csv_path)
    assert os_path_exists(rope_csv_path)
    assert len(get_dir_file_strs(map_dir)) == 4


def test_load_namemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)
    assert os_path_exists(name_csv_path)
    empty_lireunit = lireunit_shop("Sue")
    sue_namemap = empty_lireunit.get_mapunit(NameTerm_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 3
    ex_namemap = sue_lireunit.get_mapunit(NameTerm_str())
    assert ex_namemap == sue_namemap


def test_load_namemap_from_csv_DoesNotChangeWhenFileDoesNotExist(env_dir_setup_cleanup):
    # ESTABLISH
    map_dir = get_example_face_dir()
    name_filename = "name.csv"
    name_csv_path = create_path(map_dir, name_filename)
    assert os_path_exists(name_csv_path) is False
    empty_lireunit = lireunit_shop("Sue")
    sue_namemap = empty_lireunit.get_mapunit(NameTerm_str())
    sue_namemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_namemap=}")
    assert len(sue_namemap.otx2inx) == 0

    # WHEN
    sue_namemap = _load_namemap_from_csv(map_dir, sue_namemap)

    # THEN
    assert len(sue_namemap.otx2inx) == 0


def test_load_titlemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)
    assert os_path_exists(group_csv_path)
    empty_lireunit = lireunit_shop("Sue")
    sue_titlemap = empty_lireunit.get_mapunit(TitleTerm_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 2
    ex_titlemap = sue_lireunit.get_mapunit(TitleTerm_str())
    assert ex_titlemap == sue_titlemap


def test_load_titlemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    title_filename = "title.csv"
    group_csv_path = create_path(map_dir, title_filename)
    assert os_path_exists(group_csv_path) is False
    empty_lireunit = lireunit_shop("Sue")
    sue_titlemap = empty_lireunit.get_mapunit(TitleTerm_str())
    sue_titlemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_titlemap=}")
    assert len(sue_titlemap.otx2inx) == 0

    # WHEN
    sue_titlemap = _load_titlemap_from_csv(map_dir, sue_titlemap)

    # THEN
    assert len(sue_titlemap.otx2inx) == 0


def test_load_labelmap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)
    assert os_path_exists(label_csv_path)
    empty_lireunit = lireunit_shop("Sue")
    sue_labelmap = empty_lireunit.get_mapunit(LabelTerm_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 2
    ex_labelmap = sue_lireunit.get_mapunit(LabelTerm_str())
    assert ex_labelmap == sue_labelmap


def test_load_labelmap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    label_filename = "label.csv"
    label_csv_path = create_path(map_dir, label_filename)
    assert os_path_exists(label_csv_path) is False
    empty_lireunit = lireunit_shop("Sue")
    sue_labelmap = empty_lireunit.get_mapunit(LabelTerm_str())
    sue_labelmap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_labelmap=}")
    assert len(sue_labelmap.otx2inx) == 0

    # WHEN
    sue_labelmap = _load_labelmap_from_csv(map_dir, sue_labelmap)

    # THEN
    assert len(sue_labelmap.otx2inx) == 0


def test_load_ropemap_from_csv_SetsAttrWhenFileExists(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    rope_filename = "rope.csv"
    rope_csv_path = create_path(map_dir, rope_filename)
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)
    assert os_path_exists(rope_csv_path)
    empty_lireunit = lireunit_shop("Sue")
    sue_ropemap = empty_lireunit.get_mapunit(RopeTerm_str())
    sue_ropemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_ropemap=}")
    assert len(sue_ropemap.otx2inx) == 0

    # WHEN
    sue_ropemap = _load_ropemap_from_csv(map_dir, sue_ropemap)

    # THEN
    assert len(sue_ropemap.otx2inx) == 2
    ex_ropemap = sue_lireunit.get_mapunit(RopeTerm_str())
    assert ex_ropemap.event_int == sue_ropemap.event_int
    assert ex_ropemap.face_name == sue_ropemap.face_name
    assert ex_ropemap.otx2inx == sue_ropemap.otx2inx
    assert ex_ropemap.labelmap != sue_ropemap.labelmap


def test_load_ropemap_from_csv_DoesNotChangeWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    map_dir = get_example_face_dir()
    rope_filename = "rope.csv"
    rope_csv_path = create_path(map_dir, rope_filename)
    assert os_path_exists(rope_csv_path) is False
    empty_lireunit = lireunit_shop("Sue")
    sue_ropemap = empty_lireunit.get_mapunit(RopeTerm_str())
    sue_ropemap.face_name = "Sue"
    print(f"{empty_lireunit=} {sue_ropemap=}")
    assert len(sue_ropemap.otx2inx) == 0

    # WHEN
    sue_ropemap = _load_ropemap_from_csv(map_dir, sue_ropemap)

    # THEN
    assert len(sue_ropemap.otx2inx) == 0


def test_create_dir_valid_empty_lireunit_Sets_otx_knot_inx_knot(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    sue_lireunit = lireunit_shop(
        face_name=sue_str,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_lireunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)

    # WHEN
    gen_lireunit = create_dir_valid_empty_lireunit(map_dir)

    # # THEN
    assert gen_lireunit.unknown_str == x_unknown_str
    assert gen_lireunit.otx_knot == slash_otx_knot
    assert gen_lireunit.inx_knot == colon_inx_knot
    gen_mapunit = gen_lireunit.get_mapunit(NameTerm_str())
    assert gen_mapunit.unknown_str == x_unknown_str
    assert gen_mapunit.otx_knot == slash_otx_knot
    assert gen_mapunit.inx_knot == colon_inx_knot


def test_create_dir_valid_empty_lireunit_Returns_event_int(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    sue_str = "Sue"
    x_unknown_str = "UnknownTerm"
    slash_otx_knot = "/"
    colon_inx_knot = ":"
    event7 = 7
    sue_lireunit = lireunit_shop(
        face_name=sue_str,
        event_int=event7,
        otx_knot=slash_otx_knot,
        inx_knot=colon_inx_knot,
        unknown_str=x_unknown_str,
    )
    sue_lireunit.set_namemap(get_slash_namemap())
    map_dir = get_example_face_dir()
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)

    # WHEN
    gen_lireunit = create_dir_valid_empty_lireunit(map_dir)

    # THEN
    assert gen_lireunit.face_name == sue_str
    assert gen_lireunit.event_int == event7
    assert gen_lireunit.unknown_str == x_unknown_str
    assert gen_lireunit.otx_knot == slash_otx_knot
    assert gen_lireunit.inx_knot == colon_inx_knot
    gen_mapunit = gen_lireunit.get_mapunit(NameTerm_str())
    assert gen_mapunit.unknown_str == x_unknown_str
    assert gen_mapunit.otx_knot == slash_otx_knot
    assert gen_mapunit.inx_knot == colon_inx_knot


def test_init_lireunit_from_dir_ReturnsObj(env_dir_setup_cleanup):
    # ESTABLISH
    sue_lireunit = get_sue_lireunit()
    map_dir = get_example_face_dir()
    save_all_csvs_from_lireunit(map_dir, sue_lireunit)

    # WHEN
    gen_lireunit = init_lireunit_from_dir(map_dir)

    # THEN
    assert gen_lireunit
    assert len(gen_lireunit.namemap.otx2inx) == 3

    assert len(sue_lireunit.namemap.otx2inx) == 3
    assert gen_lireunit.namemap == sue_lireunit.namemap
    assert gen_lireunit.titlemap == sue_lireunit.titlemap
    assert gen_lireunit.labelmap == sue_lireunit.labelmap
    assert gen_lireunit.ropemap.labelmap == sue_lireunit.ropemap.labelmap
    assert gen_lireunit.ropemap == sue_lireunit.ropemap
    assert gen_lireunit == sue_lireunit
