from src.a00_data_toolbox.csv_toolbox import export_sqlite_tables_to_csv
from src.a00_data_toolbox.file_toolbox import (
    count_dirs_files,
    create_path,
    delete_dir,
    set_dir,
)
from src.a20_world_logic.world import WorldUnit, worldunit_shop
from sys import argv as sys_argv

if __name__ == "__main__":
    arg0 = sys_argv[1] if len(sys_argv) > 1 else None
    # Define the old and new strings in names
    default_output_dir = "C:/dev/jaar_output"
    default_input_dir = "C:/dev/jaar_input"
    default_working_dir = "C:/dev/jaar_worlds"

    input_directory = ""
    output_directory = ""
    working_directory = ""
    if arg0 != "default":
        input_directory = input(f"input directory (default is {default_input_dir}) =")
        output_directory = input(
            f"output directory (default is {default_output_dir}) ="
        )
        working_directory = input(
            f"working directory (default is {default_working_dir}) ="
        )
    if not input_directory:
        input_directory = default_input_dir
    if not output_directory:
        output_directory = default_output_dir
    if not working_directory:
        working_directory = default_working_dir

    set_dir(input_directory)
    set_dir(output_directory)
    set_dir(working_directory)
    delete_dir(output_directory)
    delete_dir(working_directory)

    x_worldunit = worldunit_shop(
        world_id="x_world",
        worlds_dir=working_directory,
        output_dir=output_directory,
        mud_dir=input_directory,
    )
    print(f"{x_worldunit.worlds_dir=}")
    print(f"{x_worldunit.output_dir=}")
    print(f"{x_worldunit._mud_dir=}")
    print(f"before output_dir file/dir count= {count_dirs_files(output_directory)}")
    x_worldunit.mud_to_clarity_mstr()
    x_worldunit.create_stances()
    x_worldunit.create_kpi_csvs()
    output_db_dir = create_path(output_directory, "db")
    export_sqlite_tables_to_csv(x_worldunit.get_world_db_path(), output_db_dir)
    print(f"after  output_dir file/dir count= {count_dirs_files(output_directory)}")
