from src._instrument.file import save_file
from src.bud.examples.bud_env import get_bud_examples_dir as env_dir
from src.bud.examples.example_buds import budunit_v001, budunit_v002

save_file(env_dir(), "example_bud3.json", budunit_v001().get_json())
save_file(env_dir(), "example_bud4.json", budunit_v002().get_json())
