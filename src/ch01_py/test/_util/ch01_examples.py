from enum import Enum
from src.ch01_py.file_toolbox import open_json


class CommonExampleStrs(str, Enum):
    Bob = "Bob"
    Sue = "Sue"
    SueZia = "SueZia"
    Yao = "Yao"
    Xio = "Xio"
    Zia = "Zia"
    SueAndZia = "SueAndZia"
    casa_str = "casa"
    clean_str = "clean"
    dirtyness_str = "dirtyness"
    mop_str = "mop"
    slash_str = "/"
    swim = "swim"
    wk_str = "wk"
    wed_str = "Wed"

    def __str__(self):
        return self.value
