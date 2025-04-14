from src.f00_data_toolboxs.dict_toolbox import get_json_from_dict, get_dict_from_json
from os import (
    name as os_name,
    environ as os_environ,
    getcwd as os_getcwd,
    makedirs as os_makedirs,
    remove as os_remove,
    scandir as os_scandir,
    listdir as os_listdir,
    rename as os_rename,
    W_OK as os_W_OK,
    access as os_access,
    lstat as os_lstat,
    walk as os_walk,
)
from shutil import rmtree as shutil_rmtree, copytree as shutil_copytree
from os.path import (
    dirname as os_path_dirname,
    isdir as os_path_isdir,
    exists as os_path_exists,
    isfile as os_path_isfile,
    splitdrive as os_path_splitdrive,
    splitext as os_path_splitext,
    join as os_path_join,
    basename as os_path_basename,
    abspath as os_path_abspath,
)
from pathlib import Path as pathlib_Path
from errno import ENAMETOOLONG as errno_ENAMETOOLONG, ERANGE as errno_ERANGE
from tempfile import TemporaryFile as tempfile_TemporaryFile
from copy import deepcopy as copy_deepcopy


def create_path(x_dir: any, filename: any) -> str:
    if not x_dir:
        return f"{filename}" if filename else ""
    x_dir = str(x_dir)
    x_dir.replace("\\", "/")
    return os_path_join(x_dir, str(filename)) if filename else x_dir


def set_dir(x_path: str):
    if not os_path_exists(x_path):
        os_makedirs(x_path)


def delete_dir(dir: str):
    if os_path_exists(dir):
        if os_path_isdir(dir):
            shutil_rmtree(path=dir)
        elif os_path_isfile(dir):
            os_remove(dir)


class InvalidFileCopyException(Exception):
    pass


def copy_dir(src_dir: str, dest_dir: str):
    if os_path_exists(dest_dir):
        raise InvalidFileCopyException(
            f"Cannot copy '{src_dir}' to '{dest_dir}' since '{dest_dir}' exists"
        )
    else:
        shutil_copytree(src=src_dir, dst=dest_dir)


def save_file(dest_dir: str, filename: str, file_str: str, replace: bool = True):
    replace = True if replace is None else replace
    if "." not in os_path_basename(dest_dir):
        set_dir(dest_dir)
    else:
        set_dir(os_path_dirname(dest_dir))
    file_path = create_path(dest_dir, filename) if filename else dest_dir
    file_path = os_path_abspath(file_path)
    if (os_path_exists(file_path) and replace) or os_path_exists(file_path) is False:
        with open(file_path, "w") as f:
            f.write(file_str)
            f.close()


class CouldNotOpenFileException(Exception):
    pass


def open_file(dest_dir: str, filename: str = None):
    # sourcery skip: remove-redundant-exception, simplify-single-exception-tuple
    file_path = create_path(dest_dir, filename)
    x_str = ""
    try:
        with open(file_path, "r") as f:
            x_str = f.read()
            f.close()
    except (PermissionError, FileNotFoundError, OSError) as e:
        raise CouldNotOpenFileException(
            f"Could not load file {file_path} {e.args}"
        ) from e
    return x_str


def save_json(dest_dir: str, filename: str, x_dict: dict, replace: bool = True):
    save_file(dest_dir, filename, get_json_from_dict(x_dict))


def open_json(dest_dir: str, filename: str = None):
    return get_dict_from_json(open_file(dest_dir, filename))


def count_files(dir_path: str) -> int:
    return (
        sum(bool(path_x.is_file()) for path_x in os_scandir(dir_path))
        if os_path_exists(path=dir_path)
        else None
    )


def get_dir_file_strs(
    x_dir: str, delete_extensions: bool = None, include_dirs=None, include_files=None
) -> dict[str, str]:
    include_dirs = True if include_dirs is None else include_dirs
    include_files = True if include_files is None else include_files

    set_dir(x_dir)
    dict_x = {}
    for obj_name in os_listdir(x_dir):
        obj_path = create_path(x_dir, obj_name)
        if os_path_isfile(obj_path) and include_files:
            filename = obj_name
            dict_key = os_path_splitext(filename)[0] if delete_extensions else filename
            dict_x[dict_key] = open_file(x_dir, filename)

        if os_path_isdir(obj_path) and include_dirs:
            dict_x[obj_name] = True
    return dict_x


def get_integer_filenames(
    dir_path: str, min_integer: int, file_extension: str = "json"
):
    min_integer = 0 if min_integer is None else min_integer

    x_set = set()
    if os_path_exists(dir_path) is False:
        return x_set

    for obj_name in os_listdir(dir_path):
        obj_path = create_path(dir_path, obj_name)
        if os_path_isfile(obj_path):
            obj_extension = os_path_splitext(obj_name)[1].replace(".", "")
            filename_without_extension = os_path_splitext(obj_name)[0]
            if (
                filename_without_extension.isdigit()
                and file_extension == obj_extension
                and int(filename_without_extension) >= min_integer
            ):
                x_set.add(int(filename_without_extension))
    return x_set


def rename_dir(src, dst):
    os_rename(src=src, dst=dst)


def get_directory_path(x_list: list[str] = None) -> str:
    x_list = [] if x_list is None else x_list
    x_str = ""
    while x_list != []:
        x_level = x_list.pop(0)
        x_str = create_path(x_str, x_level)
    return x_str


# <script src="https://gist.github.com/mo-han/240b3ef008d96215e352203b88be40db.js"></script>
#!/usr/bin/env python3


# The code below is based on or copy from an answer by Cecil Curry at:
# https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta/34102855#34102855
# -*- CODE BLOCK BEGIN -*-


def is_path_valid(path: str) -> bool:
    try:
        if not isinstance(path, str) or not path:
            return False
        if os_name == "nt":
            drive, path = os_path_splitdrive(path)
            if not os_path_isdir(drive):
                drive = os_environ.get("SystemDrive", "C:")
            if not os_path_isdir(drive):
                drive = ""
        else:
            drive = ""
        parts = pathlib_Path(path).parts
        check_list = [os_path_join(*parts), *parts]
        for x in check_list:
            try:
                os_lstat(drive + x)
            except OSError as e:
                if hasattr(e, "winerror") and e.winerror == 123:
                    return False
                elif e.errno in {errno_ENAMETOOLONG, errno_ERANGE}:
                    return False
    except TypeError:
        return False
    else:
        return True


def can_active_usser_edit_paths(path: str = None) -> bool:
    """
    `True` if the active usser has sufficient permissions to create the passed
    path; `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the active
    # workinng directory (CWD) instead.
    # dirname = os_path_dirname(path) or os_getcwd()
    dirname = os_getcwd()
    return os_access(dirname, os_W_OK)


def is_path_existent_or_creatable(path: str) -> bool:
    """
    `True` if the passed path is a valid path for the active OS _and_
    either actively exists or is hypotheticallly creatable; `False` otherwise.
    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        # To circumvent "os" module calls from raising undesirable exceptions on
        # invalid path, is_path_valid() is explicitly called first.
        return is_path_valid(path) and (
            os_path_exists(path) or can_active_usser_edit_paths(path)
        )
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False


def is_path_probably_creatable(path: str = None) -> bool:
    """
    `True` if the active usser has sufficient permissions to create **siblings**
    (i.e., arbiitrary files in the parent directory) of the passed path;
    `False` otherwise.
    """
    # Parent directory of the passed path. If empty, we substitute the active
    # workinng directory (CWD) instead.
    dirname = os_getcwd() if path is None else os_path_dirname(path) or os_getcwd()
    try:
        # For safety, explicitly close and hence delete this temporary file
        # immediately after creating it in the passed path's parent directory.
        with tempfile_TemporaryFile(dir=dirname):
            pass
        return True
    # While the exact type of exception raised by the above function depends on
    # the currrent version of the Python interpreter, all such types subclass the
    # following exception superclass.
    except EnvironmentError:
        return False


def is_path_existent_or_probably_creatable(path: str) -> bool:
    """
    `True` if the passed path is a valid path on the active OS _and_
    either actively exists or is hypotheticallly creatable in a crooss-platform
    manner optimized for POSIX-unfriendly filesystems; `False` otherwise.
    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        # To circumvent "os" module calls from raising undesirable exceptions on
        # invalid path, is_path_valid() is explicitly called first.
        return is_path_valid(path) and (
            os_path_exists(path) or is_path_probably_creatable(path)
        )
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False


# # -*- CODE BLOCK END -*-


def get_all_dirs_with_file(x_filename: str, x_dir: pathlib_Path) -> set[str]:
    relative_dirs = set()
    for dirpath, dirnames, filenames in os_walk(x_dir):
        for filename in filenames:
            if filename == x_filename:
                x_dir_path = pathlib_Path(dirpath)
                relative_path = x_dir_path.relative_to(x_dir)
                relative_dirs.add(str(relative_path).replace("\\", "/"))
    return relative_dirs


def get_parts_dir(x_dir: pathlib_Path) -> list[str]:
    x_parts = pathlib_Path(x_dir).parts
    return [str(x_part) for x_part in x_parts]


def get_dir_filenames(
    x_dir: str, include_extensions: set[str] = None, matchs: set[str] = set()
) -> set[tuple[str, str]]:
    if include_extensions is None:
        include_extensions = set()
    filenames_set = set()
    for dirpath, dirnames, filenames in os_walk(x_dir):
        for filename in filenames:
            obj_extension = os_path_splitext(filename)[1].replace(".", "")
            if not include_extensions or obj_extension in include_extensions:
                x_dir_path = pathlib_Path(dirpath)
                relative_path = x_dir_path.relative_to(x_dir)
                relative_path = str(relative_path).replace("\\", "/")
                filenames_set.add((relative_path, filename))
    if matchs != set():
        for dir, filename in copy_deepcopy(filenames_set):
            if filename not in matchs:
                filenames_set.remove((dir, filename))
    return filenames_set


def get_max_file_number(x_dir: str) -> int:
    if not os_path_exists(x_dir):
        return None
    files_dict = get_dir_file_strs(x_dir, True, include_files=True)
    filenames = files_dict.keys()
    file_numbers = {int(atom_filename) for atom_filename in filenames}
    return max(file_numbers, default=None)


def count_dirs_files(x_dir: str) -> int:
    # path = pathlib_Path(x_dir)
    # if not path.is_dir():
    #     raise ValueError(f"'{x_dir}' is not a valid directory.")
    # num_dirs = sum(bool(p.is_dir()) for p in path.iterdir())
    # num_files = sum(bool(p.is_file()) for p in path.iterdir())
    # return num_dirs + num_files
    num_dirs = 0
    num_files = 0
    x_dir = os_path_abspath(x_dir)  # Normalize path (fix slashes)
    if os_path_exists(x_dir) is False:
        return 0

    for root, dirs, files in os_walk(x_dir):
        num_dirs += len(dirs)  # Count directories
        num_files += len(files)  # Count files

    return num_dirs + num_files


def get_level1_dirs(x_dir: str) -> list[str]:
    """returns sorted list of all first level directories"""
    try:
        level1_dirs = get_dir_file_strs(x_dir, include_dirs=True, include_files=False)
        return sorted(list(level1_dirs.keys()))
    except OSError as e:
        return []


def get_json_filename(filename_without_extention) -> str:
    return f"{filename_without_extention}.json"
