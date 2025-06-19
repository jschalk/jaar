from src.a00_data_toolbox.file_toolbox import save_file
from src.a06_plan_logic.test._util.a06_env import get_plan_examples_dir as env_dir
from src.a06_plan_logic.test._util.example_plans import planunit_v001, planunit_v002

save_file(env_dir(), "example_plan3.json", planunit_v001().get_json())
save_file(env_dir(), "example_plan4.json", planunit_v002().get_json())
