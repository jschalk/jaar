from src.f00_instrument.file import save_file, get_dir_file_strs
from src.f08_pidgin.pidgin import PidginUnit, BridgeUnit, pidginunit_shop
from src.f09_brick.pandas_tool import get_ordered_csv, open_csv
from pandas import DataFrame


def get_otx2inx_dt_columns() -> list[str]:
    return [
        "face_id",
        "jaar_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_word",
        "inx_word",
    ]


def get_nub_label_columns() -> list[str]:
    return [
        "face_id",
        "jaar_type",
        "otx_road_delimiter",
        "inx_road_delimiter",
        "unknown_word",
        "otx_label",
        "inx_label",
    ]


def create_otx2inx_dt(x_bridgeunit: BridgeUnit) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridgeunit.face_id,
            "jaar_type": x_bridgeunit.jaar_type,
            "otx_road_delimiter": x_bridgeunit.otx_road_delimiter,
            "inx_road_delimiter": x_bridgeunit.inx_road_delimiter,
            "unknown_word": x_bridgeunit.unknown_word,
            "otx_word": otx_value,
            "inx_word": inx_value,
        }
        for otx_value, inx_value in x_bridgeunit.otx2inx.items()
    ]
    return DataFrame(x_rows_list, columns=get_otx2inx_dt_columns())


def create_nub_label_dt(x_bridgeunit: BridgeUnit) -> DataFrame:
    x_rows_list = [
        {
            "face_id": x_bridgeunit.face_id,
            "jaar_type": x_bridgeunit.jaar_type,
            "otx_road_delimiter": x_bridgeunit.otx_road_delimiter,
            "inx_road_delimiter": x_bridgeunit.inx_road_delimiter,
            "unknown_word": x_bridgeunit.unknown_word,
            "otx_label": otx_value,
            "inx_label": inx_value,
        }
        for otx_value, inx_value in x_bridgeunit.nub_label.items()
    ]
    return DataFrame(x_rows_list, columns=get_nub_label_columns())


def save_all_csvs_from_pidginunit(x_dir: str, x_pidginunit: PidginUnit):
    for x_key, x_bridgeunit in x_pidginunit.bridgeunits.items():
        _save_otx2inx_csv(x_dir, x_bridgeunit, x_key)
        _save_nub_label_csv(x_dir, x_bridgeunit, x_key)


def _save_otx2inx_csv(x_dir: str, x_bridgeunit: BridgeUnit, x_filename: str):
    x_otx2inx_dt = create_otx2inx_dt(x_bridgeunit)
    x_otx2inx_csv = get_ordered_csv(x_otx2inx_dt)
    x_otx2inx_filename = f"{x_filename}_otx2inx.csv"
    save_file(x_dir, x_otx2inx_filename, x_otx2inx_csv)


def _save_nub_label_csv(x_dir, x_bridgeunit, x_key):
    x_nub_label_dt = create_nub_label_dt(x_bridgeunit)
    x_nub_label_csv = get_ordered_csv(x_nub_label_dt)
    x_nub_label_filename = f"{x_key}_nub_label.csv"
    save_file(x_dir, x_nub_label_filename, x_nub_label_csv)


def _load_otx2inx_from_csv(x_dir, x_bridgeunit: BridgeUnit) -> BridgeUnit:
    file_key = x_bridgeunit.jaar_type
    if x_bridgeunit.jaar_type in {"RoadNode", "RoadUnit"}:
        file_key = "road"
    otx2inx_filename = f"{file_key}_otx2inx.csv"
    otx2inx_dt = open_csv(x_dir, otx2inx_filename)
    for table_row in otx2inx_dt.to_dict("records"):
        otx_word_value = table_row.get("otx_word")
        inx_word_value = table_row.get("inx_word")
        if x_bridgeunit.otx2inx_exists(otx_word_value, inx_word_value) is False:
            x_bridgeunit.set_otx2inx(otx_word_value, inx_word_value)
    return x_bridgeunit


def _load_nub_label_from_csv(x_dir, x_bridgeunit: BridgeUnit) -> BridgeUnit:
    file_key = x_bridgeunit.jaar_type
    if x_bridgeunit.jaar_type in {"RoadNode", "RoadUnit"}:
        file_key = "road"
    nub_label_filename = f"{file_key}_nub_label.csv"
    nub_label_dt = open_csv(x_dir, nub_label_filename)
    for table_row in nub_label_dt.to_dict("records"):
        otx_word_value = table_row.get("otx_label")
        inx_word_value = table_row.get("inx_label")
        if x_bridgeunit.nub_label_exists(otx_word_value, inx_word_value) is False:
            x_bridgeunit.set_nub_label(otx_word_value, inx_word_value)
    return x_bridgeunit


def create_dir_valid_empty_pidginunit(x_dir: str) -> PidginUnit:
    face_id_set = set()
    unknown_word_set = set()
    otx_road_delimiter_set = set()
    inx_road_delimiter_set = set()
    for x_filename in get_dir_file_strs(x_dir).keys():
        x_dt = open_csv(x_dir, x_filename)
        face_id_set.update(x_dt.face_id.unique())
        unknown_word_set.update(x_dt.unknown_word.unique())
        otx_road_delimiter_set.update(x_dt.otx_road_delimiter.unique())
        inx_road_delimiter_set.update(x_dt.inx_road_delimiter.unique())

    if len(face_id_set) == 1:
        x_face_id = face_id_set.pop()
    if len(unknown_word_set) == 1:
        x_unknown_word = unknown_word_set.pop()
    if len(otx_road_delimiter_set) == 1:
        x_otx_road_delimiter = otx_road_delimiter_set.pop()
    if len(inx_road_delimiter_set) == 1:
        x_inx_road_delimiter = inx_road_delimiter_set.pop()

    # if (
    #     face_id_set != set()
    #     or unknown_word_set != set()
    #     or otx_road_delimiter_set != set()
    #     or inx_road_delimiter_set != set()
    # ):
    #     raise Exception(
    #         f"{face_id_set=} {unknown_word_set=}  {otx_road_delimiter_set=} {inx_road_delimiter_set=}"
    #     )

    return pidginunit_shop(
        x_face_id=x_face_id,
        x_otx_road_delimiter=x_otx_road_delimiter,
        x_inx_road_delimiter=x_inx_road_delimiter,
        x_unknown_word=x_unknown_word,
    )


def init_pidginunit_from_dir(x_dir: str) -> PidginUnit:
    x_pidginunit = create_dir_valid_empty_pidginunit(x_dir)
    for x_bridgeunit in x_pidginunit.bridgeunits.values():
        _load_otx2inx_from_csv(x_dir, x_bridgeunit)
        _load_nub_label_from_csv(x_dir, x_bridgeunit)
    return x_pidginunit
