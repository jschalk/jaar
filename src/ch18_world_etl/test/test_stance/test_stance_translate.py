from sqlite3 import connect as sqlite3_connect
from src.ch17_idea.idea_csv_tool import create_init_stance_idea_csv_strs
from src.ch18_world_etl.stance_tool import (
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
    add_translate_rows_to_stance_csv_strs,
)
from src.ch18_world_etl.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)
from src.ref.keywords import Ch18Keywords as wx


def test_add_to_br00042_csv_ReturnsObj():
    # ESTABLISH database with translate data
    # - [`br00042`](ideas/br00042.md): spark_num, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str
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
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trltitl_dimen = wx.translate_title
        trltitl_s_vld_tablename = prime_tbl(trltitl_dimen, "s", "vld")
        insert_trltitl_sqlstr = f"""INSERT INTO {trltitl_s_vld_tablename}
        ({wx.spark_num}, {wx.face_name}, {wx.otx_title}, {wx.inx_title})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trltitl_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
        VALUES
          ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
        , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00042")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{wx.spark_num},{wx.face_name},{wx.otx_title},{wx.inx_title},{wx.otx_knot},{wx.inx_knot},{wx.unknown_str}\n"
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
    # ESTABLISH database with translate data
    # - [`br00043`](ideas/br00043.md): spark_num, face_name, otx_name, inx_name, otx_knot, inx_knot, unknown_str
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
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
VALUES
  ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_trlname_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES
  ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00043")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{wx.spark_num},{wx.face_name},{wx.otx_name},{wx.inx_name},{wx.otx_knot},{wx.inx_knot},{wx.unknown_str}\n"
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
    # ESTABLISH database with translate data
    # - [`br00044`](ideas/br00044.md): spark_num, face_name, otx_label, inx_label, otx_knot, inx_knot, unknown_str
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
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trllabe_dimen = wx.translate_label
        trllabe_s_vld_tablename = prime_tbl(trllabe_dimen, "s", "vld")
        insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label})
VALUES
  ({spark1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_trllabe_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES
  ('{sue_str}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_str}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00044")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{wx.spark_num},{wx.face_name},{wx.otx_label},{wx.inx_label},{wx.otx_knot},{wx.inx_knot},{wx.unknown_str}\n"
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


def test_add_to_br00045_csv_ReturnsObj():
    # ESTABLISH database with translate data
    # - [`br00045`](ideas/br00045.md): spark_num, face_name, otx_rope, inx_rope, otx_knot, inx_knot, unknown_str
    bob_str = "Bob"
    sue_str = "Sue"
    bob_otx_knot = ";"
    bob_inx_knot = "/"
    sue_otx_knot = "?"
    sue_inx_knot = "."
    sue_clean_otx = "?casa?clean?"
    sue_clean_inx = ".casa.limpia."
    bob_clean_otx = ";casa;very clean;"
    bob_clean_inx = "/casa/very limpia/"
    sue_unknown_str = "Unknown3"
    bob_unknown_str = "UNKNOWN4"
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        trlrope_dimen = wx.translate_rope
        trlrope_s_vld_tablename = prime_tbl(trlrope_dimen, "s", "vld")
        insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_rope}, {wx.inx_rope})
VALUES
  ({spark1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_trlrope_sqlstr)

        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""
INSERT INTO {trlcore_s_vld_tablename}
({wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
VALUES
  ('{sue_str}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_str}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_trlcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00045")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{wx.spark_num},{wx.face_name},{wx.otx_rope},{wx.inx_rope},{wx.otx_knot},{wx.inx_knot},{wx.unknown_str}\n"
        assert header_only_csv == expected_header_only_csv

        # WHEN
        gen_csv = add_to_br00045_csv(header_only_csv, cursor, csv_delimiter)

        # THEN
        sue_row = f",{sue_str},{sue_clean_otx},{sue_clean_inx},{sue_otx_knot},{sue_inx_knot},{sue_unknown_str}\n"
        bob_row = f",{bob_str},{bob_clean_otx},{bob_clean_inx},{bob_otx_knot},{bob_inx_knot},{bob_unknown_str}\n"
        expected_csv = f"{header_only_csv}{bob_row}{sue_row}"
        print(f"     {gen_csv=}")
        print(f"{expected_csv=}")
        assert gen_csv == expected_csv


def test_add_translate_rows_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH database with translate data
    # - [`br00042`](ideas/br00042.md): spark_num, face_name, otx_title, inx_title, otx_knot, inx_knot, unknown_str
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
    spark1 = 1
    spark7 = 7

    # Create database with manually entered translate data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)

        # insert translate_title records
        trltitl_dimen = wx.translate_title
        trltitl_s_vld_tablename = prime_tbl(trltitl_dimen, "s", "vld")
        insert_trltitl_sqlstr = f"""INSERT INTO {trltitl_s_vld_tablename}
        ({wx.spark_num}, {wx.face_name}, {wx.otx_title}, {wx.inx_title})
        VALUES
          ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_trltitl_sqlstr)

        # insert translate_name records
        trlname_dimen = wx.translate_name
        trlname_s_vld_tablename = prime_tbl(trlname_dimen, "s", "vld")
        insert_trlname_sqlstr = f"""
INSERT INTO {trlname_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_name}, {wx.inx_name})
VALUES
  ({spark1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({spark7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_trlname_sqlstr)

        # insert translate_label records
        bob_str = "Bob"
        sue_str = "Sue"
        sue_clean_otx = "clean"
        sue_clean_inx = "limpia"
        bob_clean_otx = "very clean"
        bob_clean_inx = "very limpia"
        trllabe_dimen = wx.translate_label
        trllabe_s_vld_tablename = prime_tbl(trllabe_dimen, "s", "vld")
        insert_trllabe_sqlstr = f"""
INSERT INTO {trllabe_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_label}, {wx.inx_label})
VALUES
  ({spark1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_trllabe_sqlstr)

        # insert translate_rope records
        sue_clean_otx = "?casa?clean?"
        sue_clean_inx = ".casa.limpia."
        bob_clean_otx = ";casa;very clean;"
        bob_clean_inx = "/casa/very limpia/"
        trlrope_dimen = wx.translate_rope
        trlrope_s_vld_tablename = prime_tbl(trlrope_dimen, "s", "vld")
        insert_trlrope_sqlstr = f"""
INSERT INTO {trlrope_s_vld_tablename}
({wx.spark_num}, {wx.face_name}, {wx.otx_rope}, {wx.inx_rope})
VALUES
  ({spark1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({spark7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_trlrope_sqlstr)

        # insert translate_core records
        trlcore_s_vld_tablename = prime_tbl("trlcore", "s", "vld")
        insert_trlcore_sqlstr = f"""INSERT INTO {trlcore_s_vld_tablename}
        ({wx.face_name}, {wx.otx_knot}, {wx.inx_knot}, {wx.unknown_str})
        VALUES
          ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
        , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_trlcore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        br00042_header = x_ideas.get("br00042")
        br00043_header = x_ideas.get("br00043")
        br00044_header = x_ideas.get("br00044")
        br00045_header = x_ideas.get("br00045")

        # WHEN
        add_translate_rows_to_stance_csv_strs(cursor, x_ideas, csv_delimiter)

        # THEN
        assert x_ideas.get("br00042") != br00042_header
        assert x_ideas.get("br00043") != br00043_header
        assert x_ideas.get("br00044") != br00044_header
        assert x_ideas.get("br00045") != br00045_header
