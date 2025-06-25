from src.a00_data_toolbox.file_toolbox import (
    count_dirs_files,
    create_path,
    delete_dir,
    get_dir_file_strs,
    get_level1_dirs,
)
from src.a20_world_logic.test._util.a20_env import env_dir_setup_cleanup
from src.a20_world_logic.world import worldunit_shop


def test_input_to_clarity_mstr_Examples(env_dir_setup_cleanup):
    """Find examples in a example directory and run them through the pipeline."""
    # sourcery skip: no-loop-in-tests
    # sourcery skip: no-conditionals-in-tests
    # ESTABLISH
    examples_dir = "src/a20_world_logic/test/test_z_examples"
    example_names = set(get_level1_dirs(examples_dir))
    example_names.remove("__pycache__")  # Remove __pycache__ if it exists
    worlds_mstr_str = "worlds_mstr"
    output_str = "output"
    example_names.remove(worlds_mstr_str)  # Remove __pycache__ if it exists
    example_names.remove(output_str)  # Remove __pycache__ if it exists
    for example_name in example_names:
        parent_worlds_dir = create_path(examples_dir, worlds_mstr_str)
        worlds_dir = create_path(parent_worlds_dir, example_name)
        parent_output_dir = create_path(examples_dir, "output")
        output_dir = create_path(parent_output_dir, example_name)
        delete_dir(output_dir)  # Clean up output directory before test

        example_dir = create_path(examples_dir, example_name)
        input_dir = create_path(example_dir, "input")
        example_worldunit = worldunit_shop(
            world_id=example_name,
            worlds_dir=worlds_dir,
            input_dir=input_dir,
            output_dir=output_dir,
        )
        assert count_dirs_files(output_dir) == 0

        # WHEN
        example_worldunit.input_to_clarity_mstr()
        example_worldunit.create_stances()
        example_worldunit.create_kpi_csvs()

        # THEN
        print(f"{count_dirs_files(output_dir)=}")
        assert count_dirs_files(output_dir) > 0
