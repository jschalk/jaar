from src.a00_data_toolbox.file_toolbox import save_file
from src.a06_bud_logic._test_util.a06_env import get_bud_examples_dir as env_dir
from src.a06_bud_logic._test_util.example_buds import budunit_v001, budunit_v002

save_file(env_dir(), "example_bud3.json", budunit_v001().get_json())
save_file(env_dir(), "example_bud4.json", budunit_v002().get_json())
