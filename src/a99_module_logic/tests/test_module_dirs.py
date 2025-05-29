from src.a00_data_toolbox.file_toolbox import get_level1_dirs, create_path
from os.path import exists as os_path_exists
from ast import (
    parse as ast_parse,
    walk as ast_walk,
    ImportFrom as ast_ImportFrom,
)
from os.path import join as os_path_join
from os import walk as os_walk


def get_imports_from_file(file_path):
    """
    Parses a Python file and returns a list of lists.
    Each inner list contains:
    - The source module from a 'from ... import ...' statement
    - Followed by all imported objects from that module

    Example:
    [['math', 'sqrt', 'pi'], ['os.path', 'join']]

    :param file_path: Path to the Python (.py) file
    :return: List of lists: [module, imported_obj1, imported_obj2, ...]
    """
    imports = []

    with open(file_path, "r", encoding="utf-8") as file:
        node = ast_parse(file.read(), filename=file_path)

    for n in ast_walk(node):
        if isinstance(n, ast_ImportFrom) and n.module:
            import_entry = [n.module, [alias.name for alias in n.names]]
            imports.append(import_entry)

    return imports


def get_python_files_with_flag(directory, x_str=None):
    """
    Recursively finds .py files in a directory.
    If x_str is provided, only files with x_str in the filename are included.

    Returns a dictionary: {file_path: 1, ...}

    :param directory: Root directory to search
    :param x_str: Optional substring to filter filenames
    :return: Dictionary of matching file paths and the number 1
    """
    py_files = {}

    for root, _, files in os_walk(directory):
        for file in files:
            if file.endswith(".py") and (x_str is None or x_str in file):
                full_path = os_path_join(root, file)
                py_files[full_path] = get_imports_from_file(full_path)

    return py_files


def get_module_descs() -> dict[str, str]:
    src_dir = "src"
    module_descs = get_level1_dirs(src_dir)
    module_descs.pop(-1) == "a99_module_logic"
    return {
        module_desc: create_path(src_dir, module_desc) for module_desc in module_descs
    }


def test_ModuleDirectorysAreNumberedCorrectly():
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH

    # WHEN / THEN
    previous_module_number = -1
    for module_desc, module_dir in get_module_descs().items():
        module_number = int(module_desc[1:3])
        assert module_number == previous_module_number + 1
        # print(f"{module_desc=} {module_number=}")
        utils_dir = create_path(module_dir, "_test_util")
        assert os_path_exists(utils_dir)
        str_func_path = create_path(utils_dir, f"a{module_desc[1:3]}_str.py")
        assert os_path_exists(str_func_path)
        env_files = get_python_files_with_flag(utils_dir, "env")
        if len(env_files) > 0:
            print(f"{env_files=}")
            assert len(env_files) == 1
            env_filename = str(list(env_files.keys())[0])
            print(f"{env_filename=}")
            assert env_filename.endswith(f"a{module_desc[1:3]}_env.py")

        previous_module_number = module_number


def test_CheckAllPythonFileImportsAreInCorrectFormat():
    # sourcery skip: no-loop-in-tests
    # ESTABLISH / WHEN / THEN
    for module_desc, module_dir in get_module_descs().items():
        python_files = get_python_files_with_flag(module_dir)
        desc_number = int(module_desc[1:3])
        print(f"{desc_number} {module_desc=} {len(python_files)=}")
        for file_path, file_imports in python_files.items():
            check_module_imports_are_ordered(file_imports, file_path, desc_number)

    # example_path = "src/a09_pack_logic/delta.py"
    # imports = get_imports_from_file(example_path)
    # check_module_imports_are_ordered(imports, example_path)


def check_module_imports_are_ordered(imports: list[list], file_path: str, desc_number):
    previous_module_number = -1
    module_section_passed = False
    for x_import in imports:
        module_location = str(x_import[0])
        if module_location.startswith("src"):
            module_number = int(module_location[5:7])
            if desc_number < module_number:
                print(f"{desc_number} {file_path} {module_number=} {module_location=}")
            assert desc_number >= module_number
            assert module_section_passed is False
            if module_number < previous_module_number:
                print(
                    f"{file_path} {module_number=} {previous_module_number=} {x_import=}"
                )
            assert module_number >= previous_module_number
            previous_module_number = module_number
        else:
            module_section_passed = True

        if module_location.endswith("env"):
            env_number = int(module_location[-6:-4])
            if desc_number != env_number:
                print(f"{desc_number} {file_path} {env_number=} {module_location=}")
            assert desc_number == env_number
