from src.f4_gift.atom_config import (
    get_atom_config_dict,
    fiscal_id_str,
    owner_id_str,
    column_order_str,
    nesting_order_str,
    get_atom_config_args,
)
from src.f8_brick.brick import atom_categorys_str, attributes_str, sort_order_str


def create_categorys_brick_format_dict() -> dict:
    atom_config_dict = get_atom_config_dict()
    x_dict = {}
    x_count = 20
    for x_atom_category in atom_config_dict.keys():
        brick_filename = f"brick_format_{x_count:05}_{x_atom_category}_v0_0_0.json"
        attributes_dict = {
            fiscal_id_str(): {column_order_str(): 0, sort_order_str(): 0},
            owner_id_str(): {column_order_str(): 1, sort_order_str(): 1},
        }
        args_dict = get_atom_config_args(x_atom_category)
        for x_arg, arg_dict in args_dict.items():
            x_column_order = arg_dict.get(column_order_str())
            x_column_order += 2
            brick_dict = {column_order_str(): x_column_order}
            x_nesting_order = arg_dict.get(nesting_order_str())
            if x_nesting_order is not None:
                x_nesting_order += 2
                brick_dict[sort_order_str()] = x_nesting_order
            attributes_dict[x_arg] = brick_dict

        brick_format = {
            atom_categorys_str(): [x_atom_category],
            attributes_str(): attributes_dict,
        }
        x_dict[brick_filename] = brick_format
        x_count += 1

    return x_dict
