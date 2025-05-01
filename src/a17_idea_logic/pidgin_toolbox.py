from src.a00_data_toolbox.file_toolbox import save_file, get_dir_file_strs, create_path
from src.a16_pidgin_logic.pidgin import (
    PidginUnit,
    pidginunit_shop,
    NameMap,
    LabelMap,
    TagMap,
    RoadMap,
)
from src.a17_idea_logic.idea_db_tool import get_ordered_csv, open_csv
from pandas import DataFrame
from os.path import exists as os_path_exists


def get_pidgin_name_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_name",
        "inx_name",
    ]


def get_pidgin_label_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]


def get_pidgin_tag_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_tag",
        "inx_tag",
    ]


def get_pidgin_road_dt_columns() -> list[str]:
    return [
        "event_int",
        "face_name",
        "otx_bridge",
        "inx_bridge",
        "unknown_word",
        "otx_road",
        "inx_road",
    ]


def create_pidgin_name_dt(x_map: NameMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_name": otx_value,
            "inx_name": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_name_dt_columns())


def create_pidgin_label_dt(x_map: LabelMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_label_dt_columns())


def create_pidgin_tag_dt(x_map: TagMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_tag": otx_value,
            "inx_tag": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_tag_dt_columns())


def create_pidgin_road_dt(x_map: RoadMap) -> DataFrame:
    x_rows_list = [
        {
            "event_int": x_map.event_int,
            "face_name": x_map.face_name,
            "otx_bridge": x_map.otx_bridge,
            "inx_bridge": x_map.inx_bridge,
            "unknown_word": x_map.unknown_word,
            "otx_road": otx_value,
            "inx_road": inx_value,
        }
        for otx_value, inx_value in x_map.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_pidgin_road_dt_columns())


def save_all_csvs_from_pidginunit(x_dir: str, x_pidginunit: PidginUnit):
    _save_pidgin_name_csv(x_dir, x_pidginunit.namemap)
    _save_pidgin_label_csv(x_dir, x_pidginunit.labelmap)
    _save_pidgin_tag_csv(x_dir, x_pidginunit.tagmap)
    _save_pidgin_road_csv(x_dir, x_pidginunit.roadmap)


def _save_pidgin_name_csv(x_dir: str, namemap: NameMap):
    x_dt = create_pidgin_name_dt(namemap)
    save_file(x_dir, "name.csv", get_ordered_csv(x_dt))


def _save_pidgin_label_csv(x_dir: str, labelmap: LabelMap):
    x_dt = create_pidgin_label_dt(labelmap)
    save_file(x_dir, "label.csv", get_ordered_csv(x_dt))


def _save_pidgin_tag_csv(x_dir: str, tagmap: TagMap):
    x_dt = create_pidgin_tag_dt(tagmap)
    save_file(x_dir, "tag.csv", get_ordered_csv(x_dt))


def _save_pidgin_road_csv(x_dir: str, roadmap: RoadMap):
    x_dt = create_pidgin_road_dt(roadmap)
    save_file(x_dir, "road.csv", get_ordered_csv(x_dt))


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


def _load_labelmap_from_csv(x_dir, x_labelmap: LabelMap) -> LabelMap:
    label_filename = "label.csv"
    if os_path_exists(create_path(x_dir, label_filename)):
        otx2inx_dt = open_csv(x_dir, label_filename)
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_label")
            inx_value = table_row.get("inx_label")
            if x_labelmap.otx2inx_exists(otx_value, inx_value) is False:
                x_labelmap.set_otx2inx(otx_value, inx_value)
    return x_labelmap


def _load_tagmap_from_csv(x_dir, x_tagmap: TagMap) -> TagMap:
    tag_filename = "tag.csv"
    if os_path_exists(create_path(x_dir, tag_filename)):
        otx2inx_dt = open_csv(x_dir, "tag.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_tag")
            inx_value = table_row.get("inx_tag")
            if x_tagmap.otx2inx_exists(otx_value, inx_value) is False:
                x_tagmap.set_otx2inx(otx_value, inx_value)
    return x_tagmap


def _load_roadmap_from_csv(x_dir, x_roadmap: RoadMap) -> RoadMap:
    road_filename = "road.csv"
    if os_path_exists(create_path(x_dir, road_filename)):
        otx2inx_dt = open_csv(x_dir, "road.csv")
        for table_row in otx2inx_dt.to_dict("records"):
            otx_value = table_row.get("otx_road")
            inx_value = table_row.get("inx_road")
            if x_roadmap.otx2inx_exists(otx_value, inx_value) is False:
                x_roadmap.set_otx2inx(otx_value, inx_value)
    return x_roadmap


def create_dir_valid_empty_pidginunit(x_dir: str) -> PidginUnit:
    face_name_set = set()
    event_int_set = set()
    unknown_word_set = set()
    otx_bridge_set = set()
    inx_bridge_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_name_set.update(x_dt.face_name.unique())
        event_int_set.update(x_dt.event_int.unique())
        unknown_word_set.update(x_dt.unknown_word.unique())
        otx_bridge_set.update(x_dt.otx_bridge.unique())
        inx_bridge_set.update(x_dt.inx_bridge.unique())

    if len(face_name_set) == 1:
        face_name = face_name_set.pop()
    if len(event_int_set) == 1:
        event_int = event_int_set.pop()
    if len(unknown_word_set) == 1:
        unknown_word = unknown_word_set.pop()
    if len(otx_bridge_set) == 1:
        otx_bridge = otx_bridge_set.pop()
    if len(inx_bridge_set) == 1:
        inx_bridge = inx_bridge_set.pop()

    return pidginunit_shop(
        face_name=face_name,
        event_int=event_int,
        otx_bridge=otx_bridge,
        inx_bridge=inx_bridge,
        unknown_word=unknown_word,
    )


def init_pidginunit_from_dir(x_dir: str) -> PidginUnit:
    x_pidginunit = create_dir_valid_empty_pidginunit(x_dir)
    _load_namemap_from_csv(x_dir, x_pidginunit.namemap)
    _load_labelmap_from_csv(x_dir, x_pidginunit.labelmap)
    _load_tagmap_from_csv(x_dir, x_pidginunit.tagmap)
    _load_roadmap_from_csv(x_dir, x_pidginunit.roadmap)
    x_pidginunit.roadmap.tagmap = x_pidginunit.tagmap
    return x_pidginunit
