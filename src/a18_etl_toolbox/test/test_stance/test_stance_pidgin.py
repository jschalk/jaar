from sqlite3 import connect as sqlite3_connect
from src.a09_pack_logic.test._util.a09_str import event_int_str, face_name_str
from src.a16_pidgin_logic.test._util.a16_str import (
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    pidgin_label_str,
    pidgin_name_str,
    pidgin_rope_str,
    pidgin_title_str,
    unknown_str_str,
)
from src.a17_idea_logic.idea_csv_tool import create_init_stance_idea_csv_strs
from src.a18_etl_toolbox.stance_tool import (
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
    collect_stance_csv_strs,
    create_stance0001_file,
)
from src.a18_etl_toolbox.tran_path import create_stance0001_path
from src.a18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_voice_tables,
)


def test_add_to_br00042_csv_ReturnsObj():
    # ESTABLISH database with pidgin data
    # - [`br00042`](ideas/br00042.md): event_int, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    event1 = 1
    event7 = 7

    # Create database with manually entered pidgin data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidtitl_dimen = pidgin_title_str()
        pidtitl_s_vld_tablename = prime_tbl(pidtitl_dimen, "s", "vld")
        insert_pidtitl_sqlstr = f"""INSERT INTO {pidtitl_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_title_str()}, {inx_title_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_pidtitl_sqlstr)

        pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""INSERT INTO {pidcore_s_vld_tablename}
        ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
        VALUES
          ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
        , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_pidcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00042")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{event_int_str()},{face_name_str()},{otx_title_str()},{inx_title_str()},{otx_knot_str()},{inx_knot_str()},{unknown_str_str()}\n"
        assert header_only_csv == expected_header_only_csv

        # WHEN
        gen_csv = add_to_br00042_csv(header_only_csv, cursor, csv_delimiter)

        # THEN
        sue_row = f",{sue_otx},{sue_otx},{sue_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
        bob_row = f",{bob_otx},{bob_otx},{bob_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
        expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
        print(f"     {gen_csv=}")
        print(f"{expected_csv=}")
        assert gen_csv == expected_csv


def test_add_to_br00043_csv_ReturnsObj():
    # ESTABLISH database with pidgin data
    # - [`br00043`](ideas/br00043.md): event_int, face_name, otx_name, inx_name, otx_knot, inx_knot, unknown_str
    bob_otx = "Bob"
    bob_inx = "Bobby"
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    event1 = 1
    event7 = 7

    # Create database with manually entered pidgin data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidname_dimen = pidgin_name_str()
        pidname_s_vld_tablename = prime_tbl(pidname_dimen, "s", "vld")
        insert_pidname_sqlstr = f"""
INSERT INTO {pidname_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
VALUES
  ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_pidname_sqlstr)

        pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""
INSERT INTO {pidcore_s_vld_tablename}
({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00043")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{event_int_str()},{face_name_str()},{otx_name_str()},{inx_name_str()},{otx_knot_str()},{inx_knot_str()},{unknown_str_str()}\n"
        assert header_only_csv == expected_header_only_csv

        # WHEN
        gen_csv = add_to_br00043_csv(header_only_csv, cursor, csv_delimiter)

        # THEN
        sue_row = f",{sue_otx},{sue_otx},{sue_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
        bob_row = f",{bob_otx},{bob_otx},{bob_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
        expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
        print(f"     {gen_csv=}")
        print(f"{expected_csv=}")
        assert gen_csv == expected_csv


def test_add_to_br00044_csv_ReturnsObj():
    # ESTABLISH database with pidgin data
    # - [`br00044`](ideas/br00044.md): event_int, face_name, otx_label, inx_label, otx_knot, inx_knot, unknown_str
    bob_str = "Bob"
    sue_str = "Sue"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_clean_otx = "clean"
    sue_clean_inx = "limpia"
    bob_clean_otx = "very clean"
    bob_clean_inx = "very limpia"
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    event1 = 1
    event7 = 7

    # Create database with manually entered pidgin data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_voice_tables(cursor)
        pidlabe_dimen = pidgin_label_str()
        pidlabe_s_vld_tablename = prime_tbl(pidlabe_dimen, "s", "vld")
        insert_pidlabe_sqlstr = f"""
INSERT INTO {pidlabe_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
VALUES
  ({event1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({event7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_pidlabe_sqlstr)

        pidcore_s_vld_tablename = prime_tbl("pidcore", "s", "vld")
        insert_pidcore_sqlstr = f"""
INSERT INTO {pidcore_s_vld_tablename}
({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_str}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_pidcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00044")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{event_int_str()},{face_name_str()},{otx_label_str()},{inx_label_str()},{otx_knot_str()},{inx_knot_str()},{unknown_str_str()}\n"
        assert header_only_csv == expected_header_only_csv

        # WHEN
        gen_csv = add_to_br00044_csv(header_only_csv, cursor, csv_delimiter)

        # THEN
        sue_row = f",{sue_str},{sue_clean_otx},{sue_clean_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
        bob_row = f",{bob_str},{bob_clean_otx},{bob_clean_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
        expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
        print(f"     {gen_csv=}")
        print(f"{expected_csv=}")
        assert gen_csv == expected_csv


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
#     # - [`br00045`](ideas/br00045.md): event_int, face_name, otx_rope, inx_rope, otx_knot, inx_knot, unknown_str

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
