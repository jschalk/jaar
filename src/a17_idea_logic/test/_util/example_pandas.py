from pandas import DataFrame


def get_small_example01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["Fay"])
    x_dt.loc[0, "Fay"] = "Fay_bob0"
    x_dt.loc[1, "Fay"] = "Fay_bob1"
    x_dt.loc[2, "Fay"] = "Fay_bob2"
    x_dt.loc[3, "Fay"] = "Fay_bob3"
    return x_dt


def get_small_example01_csv() -> str:
    return """Fay
fay_bob0
fay_bob1
fay_bob2
fay_bob3
"""


def get_empty_dataframe() -> DataFrame:
    return DataFrame()


def get_ex01_dataframe() -> DataFrame:
    x_dt = DataFrame(columns=["fay", "bob", "x_boolean", "count"])
    x_dt.loc[0] = ["fay2", "bob1", False, 10]
    x_dt.loc[1] = ["fay1", "bob2", True, 10]
    x_dt.loc[2] = ["fay0", "bob3", True, 20]
    x_dt.loc[3] = ["fay3", "bob0", False, 20]
    return x_dt


def get_ex01_unordered_csv() -> str:
    return """fay,bob,x_boolean,count
fay2,bob1,False,10
fay1,bob2,True,10
fay0,bob3,True,20
fay3,bob0,False,20
"""


def get_ex01_ordered_by_fay_csv() -> str:
    return """fay,bob,x_boolean,count
fay0,bob3,True,20
fay1,bob2,True,10
fay2,bob1,False,10
fay3,bob0,False,20
"""


def get_ex01_ordered_by_count_csv() -> str:
    return """count,fay,bob,x_boolean
10,fay1,bob2,True
10,fay2,bob1,False
20,fay0,bob3,True
20,fay3,bob0,False
"""


def get_ex01_ordered_by_count_bob_csv() -> str:
    return """count,bob,fay,x_boolean
10,bob1,fay2,False
10,bob2,fay1,True
20,bob0,fay3,False
20,bob3,fay0,True
"""


def get_ex01_ordered_by_count_x_boolean_csv() -> str:
    return """count,x_boolean,fay,bob
10,False,fay2,bob1
10,True,fay1,bob2
20,False,fay3,bob0
20,True,fay0,bob3
"""


def get_ex02_atom_dataframe() -> DataFrame:
    ex02_columns = [
        "healer_name",
        "acct_name",
        "group_title",
        "labor_title",
        "awardee_title",
        "concept_rope",
    ]
    x_dt = DataFrame(columns=ex02_columns)
    # x_dt.loc[0] = ["Fay2", "Bob1", False, 10]
    # x_dt.loc[1] = ["Fay1", "Bob2", True, 10]
    # x_dt.loc[2] = ["Fay0", "Bob3", True, 20]
    # x_dt.loc[3] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[4] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[5] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[6] = ["Fay3", "Bob0", False, 20]
    # x_dt.loc[7] = ["Fay3", "Bob0", False, 20]
    x_dt.loc[0] = [";yao4", "sue2", ";swim2", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[1] = [";yao3", "sue2", ";swim1", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[2] = [";yao4", "sue2", ";swim1", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[3] = [";yao3", "sue2", ";swim2", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[4] = [";yao4", "sue1", ";swim1", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[5] = [";yao3", "sue1", ";swim1", ";labor4", "aw1", "amy45;casa;clean"]
    x_dt.loc[6] = [";yao4", "sue1", ";swim2", ";labor5", "aw1", "amy45;casa"]
    x_dt.loc[7] = [";yao3", "sue1", ";swim2", ";labor4", "aw1", "amy45;casa;clean"]

    return x_dt


def get_ex02_atom_csv() -> str:
    return """acct_name,group_title,concept_rope,labor_title,awardee_title,healer_name
sue1,;swim1,amy45;casa,;labor5,aw1,;yao4
sue1,;swim1,amy45;casa;clean,;labor4,aw1,;yao3
sue1,;swim2,amy45;casa,;labor5,aw1,;yao4
sue1,;swim2,amy45;casa;clean,;labor4,aw1,;yao3
sue2,;swim1,amy45;casa,;labor5,aw1,;yao4
sue2,;swim1,amy45;casa;clean,;labor4,aw1,;yao3
sue2,;swim2,amy45;casa,;labor5,aw1,;yao4
sue2,;swim2,amy45;casa;clean,;labor4,aw1,;yao3
"""
