from os.path import exists as os_path_exists
from sqlite3 import connect as sqlite3_connect
from src.a00_data_toolbox.file_toolbox import create_path, open_file, save_file, set_dir
from src.a06_believer_logic.believer import believerunit_shop
from src.a06_believer_logic.test._util.a06_str import believer_plan_awardlink_str
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a12_hub_toolbox.hub_path import create_belief_json_path, create_gut_path
from src.a15_belief_logic.belief import beliefunit_shop
from src.a16_pidgin_logic.test._util.a16_str import (
    inx_name_str,
    otx_name_str,
    pidgin_name_str,
)
from src.a17_idea_logic.idea_csv_tool import (
    add_beliefunit_to_stance_csv_strs,
    add_believerunit_to_stance_csv_strs,
    create_init_stance_idea_csv_strs,
)
from src.a17_idea_logic.idea_db_tool import (  # add_pidginunits_to_stance_csv_strs,
    get_sheet_names,
)
from src.a18_etl_toolbox.stance_tool import (
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox.test._util.a18_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)
from src.a18_etl_toolbox.tran_path import create_stance0001_path
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
    create_update_voice_raw_empty_inx_col_sqlstr,
    create_update_voice_raw_existing_inx_col_sqlstr,
)

# TODO #842
# def test_add_to_br00042_csv_ReturnsObj():
#     # ESTABLISH database with pidgin data
#     bob_otx = "Bob"
#     bob_inx = "Bobby"
#     sue_otx = "Sue"
#     sue_inx = "Suzy"
#     yao_otx = "Yao"
#     event1 = 1
#     event2 = 2
#     event5 = 5
#     event7 = 7
#     temp_dir = get_module_temp_dir()
#     db_path = create_path(temp_dir, "example3.db")
#     print(f"{db_path=}")
#     set_dir(temp_dir)

#     with sqlite3_connect(db_path) as db_conn:
#         cursor = db_conn.cursor()
#         create_sound_and_voice_tables(cursor)
#         pidname_dimen = pidgin_name_str()
#         pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
#         print(f"{pidname_s_vld_tablename=}")
#         insert_pidname_sqlstr = f"""INSERT INTO {pidname_s_vld_tablename}
#         ({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
#         VALUES
#           ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
#         , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
#         ;
#         """
#         cursor.execute(insert_pidname_sqlstr)

#         pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
#         insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename}
#         ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str()})
#         VALUES
#           ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
#         , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
#         ;
#         """
#         cursor.execute(insert_pidname_sqlstr)


#     # ESTABLISH
#     csv_delimiter = ","
#     x_ideas = create_init_stance_idea_csv_strs()
#     bob_str = "Bob"
#     event7 = 7
#     bob_otx_knot = ";"
#     bob_inx_knot = "/"
#     bob_unknown_str = "UNKNOWN"
#     bob7_pidginunit = pidginunit_shop(
#         bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
#     )
#     run_otx = "run"
#     run_inx = "cours"
#     bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
#     csv_header = x_ideas.get("br00042")
#     print(f"{csv_header=}")

#     # WHEN
#     x_csv = add_to_br00042_csv(csv_header, bob7_pidginunit, csv_delimiter)

#     # THEN
#     run_row = f"{bob_str},{event7},{run_otx},{bob_otx_knot},{run_inx},{bob_inx_knot},{bob_unknown_str}\n"
#     assert x_csv == f"{csv_header}{run_row}"


# def test_add_to_br00043_csv_ReturnsObj():
#     # ESTABLISH
#     csv_delimiter = ","
#     x_ideas = create_init_stance_idea_csv_strs()
#     bob_str = "Bob"
#     event7 = 7
#     bob_otx_knot = ";"
#     bob_inx_knot = "/"
#     bob_unknown_str = "UNKNOWN"
#     bob7_pidginunit = pidginunit_shop(
#         bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
#     )
#     yao_otx = "Yao"
#     yao_inx = "YaoMing"
#     bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
#     csv_header = x_ideas.get("br00043")
#     print(f"{csv_header=}")

#     # WHEN
#     x_csv = add_to_br00043_csv(csv_header, bob7_pidginunit, csv_delimiter)

#     # THEN
#     bob_row = f"{bob_str},{event7},{yao_otx},{bob_otx_knot},{yao_inx},{bob_inx_knot},{bob_unknown_str}\n"
#     assert x_csv == f"{csv_header}{bob_row}"


# def test_add_to_br00044_csv_ReturnsObj():
#     # ESTABLISH
#     csv_delimiter = ","
#     x_ideas = create_init_stance_idea_csv_strs()
#     bob_str = "Bob"
#     event7 = 7
#     bob_otx_knot = ";"
#     bob_inx_knot = "/"
#     bob_unknown_str = "UNKNOWN"
#     bob7_pidginunit = pidginunit_shop(
#         bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
#     )
#     clean_otx = "clean"
#     clean_inx = "limpia"
#     bob7_pidginunit.set_otx2inx("LabelTerm", clean_otx, clean_inx)
#     csv_header = x_ideas.get("br00044")
#     print(f"{csv_header=}")

#     # WHEN
#     x_csv = add_to_br00044_csv(csv_header, bob7_pidginunit, csv_delimiter)

#     # THEN
#     bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_knot},{clean_inx},{bob_inx_knot},{bob_unknown_str}\n"
#     assert x_csv == f"{csv_header}{bob_row}"


# def test_add_to_br00045_csv_ReturnsObj():
#     # ESTABLISH
#     csv_delimiter = ","
#     x_ideas = create_init_stance_idea_csv_strs()
#     bob_str = "Bob"
#     event7 = 7
#     bob_otx_knot = ";"
#     bob_inx_knot = "/"
#     bob_unknown_str = "UNKNOWN"
#     bob7_pidginunit = pidginunit_shop(
#         bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
#     )
#     clean_otx = "clean"
#     clean_inx = "limpia"
#     bob7_pidginunit.set_otx2inx("RopeTerm", clean_otx, clean_inx)
#     csv_header = x_ideas.get("br00045")
#     print(f"{csv_header=}")

#     # WHEN
#     x_csv = add_to_br00045_csv(csv_header, bob7_pidginunit, csv_delimiter)

#     # THEN
#     bob_row = f"{bob_str},{event7},{clean_otx},{bob_otx_knot},{clean_inx},{bob_inx_knot},{bob_unknown_str}\n"
#     assert x_csv == f"{csv_header}{bob_row}"


# def test_add_pidginunit_to_stance_csv_strs_ReturnsObj():
#     # ESTABLISH
#     csv_delimiter = ","
#     x_ideas = create_init_stance_idea_csv_strs()
#     bob_str = "Bob"
#     event7 = 7
#     bob_otx_knot = ";"
#     bob_inx_knot = "/"
#     bob_unknown_str = "UNKNOWN"
#     bob7_pidginunit = pidginunit_shop(
#         bob_str, event7, bob_otx_knot, bob_inx_knot, bob_unknown_str
#     )
#     clean_otx = "clean"
#     clean_inx = "limpia"
#     bob7_pidginunit.set_otx2inx("RopeTerm", clean_otx, clean_inx)
#     yao_otx = "Yao"
#     yao_inx = "YaoMing"
#     bob7_pidginunit.set_otx2inx("NameTerm", yao_otx, yao_inx)
#     run_otx = "run"
#     run_inx = "cours"
#     bob7_pidginunit.set_otx2inx("TitleTerm", run_otx, run_inx)
#     clean_otx = "clean"
#     clean_inx = "limpia"
#     bob7_pidginunit.set_otx2inx("LabelTerm", clean_otx, clean_inx)
#     br00042_header = x_ideas.get("br00042")
#     br00043_header = x_ideas.get("br00043")
#     br00044_header = x_ideas.get("br00044")
#     br00045_header = x_ideas.get("br00045")

#     # WHEN
#     add_pidginunit_to_stance_csv_strs(bob7_pidginunit, x_ideas, csv_delimiter)

#     # THEN
#     assert x_ideas.get("br00042") != br00042_header
#     assert x_ideas.get("br00043") != br00043_header
#     assert x_ideas.get("br00044") != br00044_header
#     assert x_ideas.get("br00045") != br00045_header
