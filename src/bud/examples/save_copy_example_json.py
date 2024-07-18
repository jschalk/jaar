from src._instrument.file import save_file
from src.bud.examples.bud_env import get_bud_examples_dir as env_dir
from src.bud.examples.example_buds import bud_v001, bud_v002

save_file(env_dir(), "example_bud3.json", bud_v001().get_json())
save_file(env_dir(), "example_bud4.json", bud_v002().get_json())
