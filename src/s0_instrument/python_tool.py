from json import loads as json_loads, dumps as json_dumps
from copy import deepcopy as copy_deepcopy
from plotly.graph_objects import Figure as plotly_Figure
from csv import reader as csv_reader, writer as csv_writer
from io import StringIO as io_StringIO


def get_empty_dict_if_none(x_dict: dict) -> dict:
    return {} if x_dict is None else x_dict


def get_empty_set_if_none(x_set: set) -> set:
    return set() if x_set is None else x_set


def get_1_if_None(x_obj):
    return 1 if x_obj is None else x_obj


def get_0_if_None(x_obj=None):
    return 0 if x_obj is None else x_obj


def get_empty_list_if_None(x_obj=None):
    return [] if x_obj is None else x_obj


def get_False_if_None(x_obj=None):
    return False if x_obj is None else x_obj


def get_positive_int(x_obj: any = None):
    try:
        x_int = int(x_obj)
    except Exception:
        x_int = 0
    return max(x_int, 0)


def add_dict_if_missing(x_dict: dict, x_keylist: list[any]):
    for x_key in x_keylist:
        if x_dict.get(x_key) is None:
            x_dict[x_key] = {}
        x_dict = x_dict.get(x_key)


def place_obj_in_dict(x_dict: dict, x_keylist: list[any], x_obj: any):
    x_keylist = copy_deepcopy(x_keylist)
    last_key = x_keylist.pop(-1)
    add_dict_if_missing(x_dict, x_keylist=x_keylist)
    last_dict = x_dict
    for x_key in x_keylist:
        last_dict = last_dict[x_key]
    last_dict[last_key] = x_obj


def x_is_json(x_json: str) -> bool:
    try:
        get_dict_from_json(x_json)
    except ValueError as e:
        return False
    return True


class NestedValueException(Exception):
    pass


def get_nested_value(
    x_dict: dict, x_keylist: list, if_missing_return_None: bool = False
) -> any:
    if not if_missing_return_None:
        return _sub_get_nested_value(x_dict, x_keylist)
    try:
        return _sub_get_nested_value(x_dict, x_keylist)
    except Exception:
        return None


def _sub_get_nested_value(x_dict: dict, x_keylist: list) -> any:
    last_key = x_keylist.pop(-1)
    temp_dict = x_dict
    x_count = 0
    for x_key in x_keylist:
        if temp_dict.get(x_key) is None:
            raise NestedValueException(f"'{x_key}' failed at level {x_count}.")
        x_count += 1
        temp_dict = temp_dict.get(x_key)

    if temp_dict.get(last_key) is None:
        raise NestedValueException(f"'{last_key}' failed at level {x_count}.")
    return temp_dict[last_key]


def get_all_nondictionary_objs(x_dict: dict) -> dict[str : list[any]]:
    level1_keys = x_dict.keys()
    z_dict = {}
    for level1_key in level1_keys:
        z_dict[level1_key] = []
        level1_list = z_dict.get(level1_key)
        eval_items = list(x_dict.get(level1_key).values())
        while eval_items != []:
            eval_item = eval_items.pop(0)
            if type(eval_item) == type({}):
                eval_items.extend(eval_item.values())
            else:
                level1_list.append(eval_item)
    return z_dict


def get_json_from_dict(dict_x: dict) -> str:
    return json_dumps(obj=dict_x)


def get_dict_from_json(x_json: str) -> dict[str,]:
    return json_loads(x_json)


def extract_csv_headers(x_csv: str, delimiter: str = None) -> tuple[list[str], str]:
    x_reader = csv_reader(x_csv.splitlines(), delimiter=",")

    title_row = None
    si = io_StringIO()
    new_csv_writer = csv_writer(si, delimiter=",")
    for x_count, row in enumerate(x_reader):
        if x_count == 0:
            title_row = row
        else:
            new_csv_writer.writerow(row)
    headers_list = []
    if title_row is None:
        return headers_list
    headers_list.extend(title_row[column_num] for column_num in range(len(title_row)))
    x_csv = si.getvalue()
    y_csv = x_csv.replace("\r", "")
    return headers_list, y_csv


def add_headers_to_csv(
    headers_list: list[str], headersless_csv: str, delimiter: str = None
) -> str:
    if delimiter is None:
        delimiter = ","
    header_str = delimiter.join(str(header) for header in headers_list)
    return f"{header_str}\n{headersless_csv}"


def get_csv_column1_column2_metrics(
    headerless_csv: str, delimiter: str = None
) -> dict[str, dict[str, int]]:
    y_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        column2_count = get_nested_value(y_dict, [row[0], row[1]], True)
        if not column2_count:
            column2_count = 1
        else:
            column2_count += 1
        place_obj_in_dict(y_dict, [row[0], row[1]], column2_count)
    return y_dict


def create_l2nested_csv_dict(
    headerless_csv: str, delimiter: str = None
) -> dict[str, dict[str, str]]:
    io_dict = {}
    x_reader = csv_reader(headerless_csv.splitlines(), delimiter=",")
    for row in x_reader:
        fiscal_owner_io = (
            get_nested_value(io_dict, [row[0], row[1]], True) or io_StringIO()
        )
        new_csv_writer = csv_writer(fiscal_owner_io, delimiter=",")
        new_csv_writer.writerow(row)
        place_obj_in_dict(io_dict, [row[0], row[1]], fiscal_owner_io)

    x_dict = {}
    for fiscal_id, owner_id_dict in io_dict.items():
        for owner_id, io_function in owner_id_dict.items():
            fiscal_owner_csv = io_function.getvalue()
            fiscal_owner_csv = fiscal_owner_csv.replace("\r", "")
            place_obj_in_dict(x_dict, [fiscal_id, owner_id], fiscal_owner_csv)

    return x_dict


def create_sorted_concatenated_str(y_list: list[str]) -> str:
    x_list = sorted(y_list)
    x_str = "".join(f",{x_header}" for x_header in x_list)
    return x_str[1:]


def get_positional_dict(x_list: list[str]) -> dict[str, int]:
    return {x_element: x_count for x_count, x_element in enumerate(x_list)}


def conditional_fig_show(fig: plotly_Figure, graphics_bool: bool):
    if graphics_bool:
        fig.show()


def add_simp_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str, x_color=None):
    if x_color is None:
        x_color = "LightSeaGreen"
    line_dict = dict(color=x_color, width=4)
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_direc_rect(fig: plotly_Figure, x0, y0, x1, y1, display_str):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0, y1, display_str)


def add_rect_str(fig, x0, y0, text):
    x_margin = 0.2
    fig.add_annotation(
        x=x0 + x_margin, y=y0 - x_margin, text=text, showarrow=False, align="left"
    )


def add_keep__rect(
    fig: plotly_Figure, x0, y0, x1, y1, text1=None, text2=None, text3=None, text4=None
):
    line_dict = dict(color="LightSeaGreen", width=2, dash="dot")
    fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1, line=line_dict)
    add_rect_str(fig, x0 + 0.5, y1, text1)
    add_rect_str(fig, x0 + 0.5, y1 - 0.2, text2)
    add_rect_str(fig, x0 + 0.5, y1 - 0.4, text3)
    add_rect_str(fig, x0 + 0.5, y1 - 0.6, text4)


def add_2_curve(fig: plotly_Figure, path: str, color: str):
    fig.add_shape(dict(type="path", path=path, line_color=color))


def add_rect_arrow(fig: plotly_Figure, x0, y0, ax0, ay0, color=None):
    if color is None:
        color = "black"
    fig.add_annotation(
        x=x0,  # arrows' head
        y=y0,  # arrows' head
        ax=ax0,  # arrows' tail
        ay=ay0,  # arrows' tail
        xref="x",
        yref="y",
        axref="x",
        ayref="y",
        text="",  # arrow only
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=3,
        arrowcolor=color,
    )
