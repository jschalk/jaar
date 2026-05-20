from ch00_py.file_toolbox import create_path


def get_excel_reader_config_path() -> str:
    "Returns path: ch17_brick/excel_reader.json"
    chapter_dir = create_path("src", "ch17_brick")
    return create_path(chapter_dir, "excel_reader.json")
