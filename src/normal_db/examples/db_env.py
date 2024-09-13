# from src._instrument.file import delete_dir
# from pytest import fixture as pytest_fixture


# def get_db_examples_dir():
#     return "src/db/examples"


# def get_db_temp_env_dir():
#     return f"{get_db_examples_dir()}/temp"


# @pytest_fixture()
# def env_dir_setup_cleanup():
#     env_dir = get_db_temp_env_dir()
#     delete_dir(dir=env_dir)
#     yield env_dir
#     delete_dir(dir=env_dir)
