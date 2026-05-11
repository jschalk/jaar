from ch00_py.file_toolbox import create_path
from os import getcwd as os_getcwd


def get_excel_reader_config_path() -> str:
    "Returns path: ch17_brick/excel_reader.json"
    src_dir = create_path(os_getcwd(), "src")
    chapter_dir = create_path(src_dir, "ch17_brick")
    return create_path(chapter_dir, "excel_reader.json")
