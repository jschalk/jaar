from src.f04_gift.atom_config import fiscal_id_str, owner_id_str, get_atom_config_args
from src.f09_brick.brick_config import get_brick_config_dict


def create_categorys_brick_format_dict() -> dict:
    brick_format_files_dict = {}
    x_count = 20
    for brick_category, category_dict in get_brick_config_dict().items():
        if category_dict.get("brick_type") == "budunit":
            brick_filename = f"brick_format_{x_count:05}_{brick_category}_v0_0_0.json"
            attributes_set = {fiscal_id_str(), owner_id_str()}
            args_dict = get_atom_config_args(brick_category)
            attributes_set.update(set(args_dict.keys()))

            brick_format = {"categorys": [brick_category], "attributes": attributes_set}
            brick_format_files_dict[brick_filename] = brick_format
            x_count += 1
    return brick_format_files_dict
