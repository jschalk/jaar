from os import rename as os_rename, walk as os_walk
from os.path import exists as os_path_exists, join as os_path_join
from subprocess import (
    CalledProcessError as subprocess_CalledProcessError,
    run as subprocess_run,
)


def string_exists_in_filepaths(root_dir: str, search_text: str) -> bool:
    """
    Return False if `search_text` does NOT appear in any file path
    (including subdirectories and filenames) under `root_dir`.
    """
    for dirpath, _, filenames in os_walk(root_dir):
        for filename in filenames:
            filepath = os_path_join(dirpath, filename)
            if search_text in filepath:
                return True
    return False


def rename_files_and_folders_4times(directory: str, old_string: str, new_string: str):
    rename_files_and_folders(directory, old_string, new_string)
    rename_files_and_folders(directory, old_string, new_string)
    rename_files_and_folders(directory, old_string, new_string)
    rename_files_and_folders(directory, old_string, new_string)


def rename_files_and_folders(
    directory: str, old_string: str, new_string: str
) -> list[str]:
    # new_string = new_string.lower()
    # old_string = old_string.lower()

    for root, dirs, files in os_walk(directory):
        rename_directories(dirs, root, old_string, new_string)

        if "." not in root:
            # List of file extensions to consider
            file_extensions = ["txt", ".py", ".json", ".ui"]
            for file_name in files:
                if any(file_name.endswith(ext) for ext in file_extensions):
                    old_file_path = os_path_join(root, file_name)
                    new_file_name = file_name.replace(old_string, new_string)
                    new_file_path = os_path_join(root, new_file_name)
                    if old_file_path != new_file_path:
                        os_rename(old_file_path, new_file_path)
                        print(f"{old_string=} {new_string=} {new_file_path=}")


def rename_directories(dirs: list[str], root, old_string: str, new_string: str):
    for d in dirs:
        old_dir_path = os_path_join(root, d)
        new_dir_name = d.replace(old_string, new_string)
        new_dir_path = os_path_join(root, new_dir_name)
        if ".git" not in old_dir_path and old_dir_path != new_dir_path:
            os_rename(old_dir_path, new_dir_path)
            print(f"{old_string=} {new_string=} {new_dir_path=}")


def string_exists_in_directory(root_dir: str, search_text: str) -> bool:
    """
    Return True if `search_text` appears in any file under `root_dir`.
    Searches recursively through all subdirectories.
    """
    for dirpath, _, filenames in os_walk(root_dir):
        for filename in filenames:
            filepath = os_path_join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        if search_text in line:
                            return True
            except Exception as e:
                # Skip unreadable files (permissions, binary, etc.)
                continue
    return False


def replace_in_tracked_python_files(find_text, replace_text):
    """
    Perform find-and-replace only on tracked .py files in the current git repo.
    """
    try:
        # Get list of tracked .py files
        result = subprocess_run(
            ["git", "ls-files", "*.py"], capture_output=True, text=True, check=True
        )
        tracked_files = result.stdout.strip().split("\n")
    except subprocess_CalledProcessError as e:
        print("Error: not a git repository or unable to list files.")
        return

    for filepath in tracked_files:
        if not filepath or not os_path_exists(filepath):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            if find_text in content:
                new_content = content.replace(find_text, replace_text)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
