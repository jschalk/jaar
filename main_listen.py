from src.a00_data_toolbox.file_toolbox import delete_dir, set_dir
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
        "x_world", worlds_dir=working_directory, mud_dir=input_directory
    )
    x_worldunit.mud_to_clarity_mstr()
