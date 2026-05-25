from ch00_py.file_toolbox import create_path, open_json
from ch13_time._ref.ch13_semantic_types import LabelTerm


def get_custom_epoch_config(epoch_label: LabelTerm) -> dict:
    x_filename = f"epoch_config_{epoch_label}.json"
    file_path = create_path("src", "ch13_time", "epoch_configs", x_filename)
    return open_json(file_path)


def get_five_config() -> dict:
    return get_custom_epoch_config("five")


def get_creg_config() -> dict:
    return get_custom_epoch_config("creg")


def get_squirt_config() -> dict:
    return get_custom_epoch_config("squirt")


def get_lizzy9_config() -> dict:
    return get_custom_epoch_config("lizzy9")
