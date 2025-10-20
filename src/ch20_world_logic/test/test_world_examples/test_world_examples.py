from os.path import exists as os_path_exists
from src.ch01_py.file_toolbox import (
    count_dirs_files,
    create_path,
    delete_dir,
    get_dir_filenames,
    get_level1_dirs,
)
from src.ch20_world_logic.test._util.ch20_env import temp_dir_setup
from src.ch20_world_logic.world import worldunit_shop


def test_sheets_input_to_clarity_mstr_Examples(temp_dir_setup, run_big_tests):
    """Find examples in a example directory and run them through the pipeline."""
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH

    if not run_big_tests:
        return
    examples_dir = "src/ch20_world_logic/test/test_world_examples"
    example_names = set(get_level1_dirs(examples_dir))
    if "__pycache__" in example_names:
        example_names.remove("__pycache__")  # Remove __pycache__ if it exists
    worlds_mstr_str = "worlds"
    output_str = "output"
    if worlds_mstr_str in example_names:
        example_names.remove(worlds_mstr_str)  # Remove __pycache__ if it exists
    if output_str in example_names:
        example_names.remove(output_str)  # Remove __pycache__ if it exists

    for example_name in example_names:
        worlds_dir = create_path(examples_dir, worlds_mstr_str)
        parent_output_dir = create_path(examples_dir, "output")
        output_dir = create_path(parent_output_dir, example_name)
        delete_dir(output_dir)  # Clean up output directory before test

        input_dir = create_path(examples_dir, example_name)
        print(f"{input_dir=} {get_dir_filenames(input_dir)}")
        example_worldunit = worldunit_shop(
            world_name=example_name,
            worlds_dir=worlds_dir,
            input_dir=input_dir,
            output_dir=output_dir,
        )
        example_worldunit.delete_world_db()
        assert count_dirs_files(output_dir) == 0
        print(f"before WHEN {os_path_exists(input_dir)=}")

        # WHEN
        example_worldunit.sheets_input_to_clarity_mstr()
        example_worldunit.create_stances()
        example_worldunit.create_world_kpi_csvs()

        # THEN
        print(f"after WHEN {os_path_exists(input_dir)=}")
        # print(f"{count_dirs_files(output_dir)=}")
        assert count_dirs_files(output_dir) > 0
        assert count_dirs_files(input_dir) > 0
