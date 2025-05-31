from os.path import exists as os_path_exists
from pandas import DataFrame
from src.a00_data_toolbox.file_toolbox import create_path, get_dir_file_strs, save_file
from src.a16_pidgin_logic.pidgin import (
    LabelMap,
    NameMap,
    PidginUnit,
    TitleMap,
    WayMap,
    pidginunit_shop,
)
from src.a17_idea_logic.idea_db_tool import get_ordered_csv, open_csv


def get_pidgin_name_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_str",
        "otx_name",
        "inx_name",
    ]


def get_pidgin_title_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_str",
        "otx_title",
        "inx_title",
    ]


def get_pidgin_label_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_str",
        "otx_label",
        "inx_label",
    ]


def get_pidgin_way_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_str",
        "otx_way",
        "inx_way",
    ]


def create_pidgin_name_dt(x_map: NameMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_str": x_map.unknown_str,
            "otx_name": otx_value,
            "inx_name": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_name_dt_columns())


def create_pidgin_title_dt(x_map: TitleMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_str": x_map.unknown_str,
            "otx_title": otx_value,
            "inx_title": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_title_dt_columns())


def create_pidgin_label_dt(x_map: LabelMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_str": x_map.unknown_str,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_label_dt_columns())


def create_pidgin_way_dt(x_map: WayMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_str": x_map.unknown_str,
            "otx_way": otx_value,
            "inx_way": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_way_dt_columns())


def save_all_csvs_from_pidginunit(x_dir: str, x_pidginunit: PidginUnit):
    _save_pidgin_name_csv(x_dir, x_pidginunit.namemap)
    _save_pidgin_title_csv(x_dir, x_pidginunit.titlemap)
    _save_pidgin_label_csv(x_dir, x_pidginunit.labelmap)
    _save_pidgin_way_csv(x_dir, x_pidginunit.waymap)


def _save_pidgin_name_csv(x_dir: str, namemap: NameMap):
    x_dt = create_pidgin_name_dt(namemap)
    save_file(x_dir, "name.csv", get_ordered_csv(x_dt))


def _save_pidgin_title_csv(x_dir: str, titlemap: TitleMap):
    x_dt = create_pidgin_title_dt(titlemap)
    save_file(x_dir, "title.csv", get_ordered_csv(x_dt))


def _save_pidgin_label_csv(x_dir: str, labelmap: LabelMap):
    x_dt = create_pidgin_label_dt(labelmap)
    save_file(x_dir, "label.csv", get_ordered_csv(x_dt))


def _save_pidgin_way_csv(x_dir: str, waymap: WayMap):
    x_dt = create_pidgin_way_dt(waymap)
    save_file(x_dir, "way.csv", get_ordered_csv(x_dt))


def _load_namemap_from_csv(x_dir, x_namemap: NameMap) -> NameMap:
    name_filename = "name.csv"
    if os_path_exists(create_path(x_dir, name_filename)):
        otx2inx_dt = open_csv(x_dir, name_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_name")
            inx_value = table_row.get("inx_name")
            if x_namemap.otx2inx_exists(otx_value, inx_value) is False:
                x_namemap.set_otx2inx(otx_value, inx_value)
    return x_namemap


def _load_titlemap_from_csv(x_dir, x_titlemap: TitleMap) -> TitleMap:
    title_filename = "title.csv"
    if os_path_exists(create_path(x_dir, title_filename)):
        otx2inx_dt = open_csv(x_dir, title_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_title")
            inx_value = table_row.get("inx_title")
            if x_titlemap.otx2inx_exists(otx_value, inx_value) is False:
                x_titlemap.set_otx2inx(otx_value, inx_value)
    return x_titlemap


def _load_labelmap_from_csv(x_dir, x_labelmap: LabelMap) -> LabelMap:
    label_filename = "label.csv"
    if os_path_exists(create_path(x_dir, label_filename)):
        otx2inx_dt = open_csv(x_dir, "label.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_label")
            inx_value = table_row.get("inx_label")
            if x_labelmap.otx2inx_exists(otx_value, inx_value) is False:
                x_labelmap.set_otx2inx(otx_value, inx_value)
    return x_labelmap


def _load_waymap_from_csv(x_dir, x_waymap: WayMap) -> WayMap:
    way_filename = "way.csv"
    if os_path_exists(create_path(x_dir, way_filename)):
        otx2inx_dt = open_csv(x_dir, "way.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_way")
            inx_value = table_row.get("inx_way")
            if x_waymap.otx2inx_exists(otx_value, inx_value) is False:
                x_waymap.set_otx2inx(otx_value, inx_value)
    return x_waymap


def create_dir_valid_empty_pidginunit(x_dir: str) -> PidginUnit:
    face_name_set = set()
    event_int_set = set()
    unknown_str_set = set()
    otx_bridge_set = set()
    inx_bridge_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_name_set.update(x_dt.face_name.unique())
        event_int_set.update(x_dt.event_int.unique())
        unknown_str_set.update(x_dt.unknown_str.unique())
        otx_bridge_set.update(x_dt.otx_bridge.unique())
        inx_bridge_set.update(x_dt.inx_bridge.unique())

    if len(face_name_set) == 1:
        face_name = face_name_set.pop()
    if len(event_int_set) == 1:
        event_int = event_int_set.pop()
    if len(unknown_str_set) == 1:
        unknown_str = unknown_str_set.pop()
    if len(otx_bridge_set) == 1:
        otx_bridge = otx_bridge_set.pop()
    if len(inx_bridge_set) == 1:
        inx_bridge = inx_bridge_set.pop()

    return pidginunit_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_str=unknown_str,
    )


def init_pidginunit_from_dir(x_dir: str) -> PidginUnit:
    x_pidginunit = create_dir_valid_empty_pidginunit(x_dir)
    _load_namemap_from_csv(x_dir, x_pidginunit.namemap)
    _load_titlemap_from_csv(x_dir, x_pidginunit.titlemap)
    _load_labelmap_from_csv(x_dir, x_pidginunit.labelmap)
    _load_waymap_from_csv(x_dir, x_pidginunit.waymap)
    x_pidginunit.waymap.labelmap = x_pidginunit.labelmap
    return x_pidginunit
