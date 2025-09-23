from sqlite3 import connect as sqlite3_connect
from src.ch17_idea_logic.idea_csv_tool import create_init_stance_idea_csv_strs
from src.ch18_etl_toolbox._ref.ch18_keywords import (
    event_int_str,
    face_name_str,
    inx_knot_str,
    inx_label_str,
    inx_name_str,
    inx_rope_str,
    inx_title_str,
    lire_label_str,
    lire_name_str,
    lire_rope_str,
    lire_title_str,
    otx_knot_str,
    otx_label_str,
    otx_name_str,
    otx_rope_str,
    otx_title_str,
    unknown_str_str,
)
from src.ch18_etl_toolbox.stance_tool import (
    add_lire_rows_to_stance_csv_strs,
    add_to_br00042_csv,
    add_to_br00043_csv,
    add_to_br00044_csv,
    add_to_br00045_csv,
)
from src.ch18_etl_toolbox.tran_sqlstrs import (
    create_prime_tablename as prime_tbl,
    create_sound_and_heard_tables,
)


def test_add_to_br00042_csv_ReturnsObj():
    # ESTABLISH database with lire data
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

    # Create database with manually entered lire data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirtitl_dimen = lire_title_str()
        lirtitl_s_vld_tablename = prime_tbl(lirtitl_dimen, "s", "vld")
        insert_lirtitl_sqlstr = f"""INSERT INTO {lirtitl_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_title_str()}, {inx_title_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_lirtitl_sqlstr)

        lircore_s_vld_tablename = prime_tbl("lircore", "s", "vld")
        insert_lircore_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename}
        ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
        VALUES
          ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
        , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_lircore_sqlstr)

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
    # ESTABLISH database with lire data
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

    # Create database with manually entered lire data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirname_dimen = lire_name_str()
        lirname_s_vld_tablename = prime_tbl(lirname_dimen, "s", "vld")
        insert_lirname_sqlstr = f"""
INSERT INTO {lirname_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
VALUES
  ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_lirname_sqlstr)

        lircore_s_vld_tablename = prime_tbl("lircore", "s", "vld")
        insert_lircore_sqlstr = f"""
INSERT INTO {lircore_s_vld_tablename}
({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_lircore_sqlstr)

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
    # ESTABLISH database with lire data
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

    # Create database with manually entered lire data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirlabe_dimen = lire_label_str()
        lirlabe_s_vld_tablename = prime_tbl(lirlabe_dimen, "s", "vld")
        insert_lirlabe_sqlstr = f"""
INSERT INTO {lirlabe_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
VALUES
  ({event1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({event7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_lirlabe_sqlstr)

        lircore_s_vld_tablename = prime_tbl("lircore", "s", "vld")
        insert_lircore_sqlstr = f"""
INSERT INTO {lircore_s_vld_tablename}
({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_str}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_lircore_sqlstr)

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


def test_add_to_br00045_csv_ReturnsObj():
    # ESTABLISH database with lire data
    # - [`br00045`](ideas/br00045.md): event_int, face_name, otx_rope, inx_rope, otx_knot, inx_knot, unknown_str
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
    event1 = 1
    event7 = 7

    # Create database with manually entered lire data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)
        lirrope_dimen = lire_rope_str()
        lirrope_s_vld_tablename = prime_tbl(lirrope_dimen, "s", "vld")
        insert_lirrope_sqlstr = f"""
INSERT INTO {lirrope_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_rope_str()}, {inx_rope_str()})
VALUES
  ({event1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({event7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_lirrope_sqlstr)

        lircore_s_vld_tablename = prime_tbl("lircore", "s", "vld")
        insert_lircore_sqlstr = f"""
INSERT INTO {lircore_s_vld_tablename}
({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
VALUES
  ('{sue_str}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
, ('{bob_str}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
;
"""
        cursor.execute(insert_lircore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        header_only_csv = x_ideas.get("br00045")
        print(f"{header_only_csv=}")
        expected_header_only_csv = f"{event_int_str()},{face_name_str()},{otx_rope_str()},{inx_rope_str()},{otx_knot_str()},{inx_knot_str()},{unknown_str_str()}\n"
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


def test_add_lire_rows_to_stance_csv_strs_ReturnsObj():
    # ESTABLISH database with lire data
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

    # Create database with manually entered lire data in the validated tables
    with sqlite3_connect(":memory:") as db_conn:
        cursor = db_conn.cursor()
        create_sound_and_heard_tables(cursor)

        # insert lire_title records
        lirtitl_dimen = lire_title_str()
        lirtitl_s_vld_tablename = prime_tbl(lirtitl_dimen, "s", "vld")
        insert_lirtitl_sqlstr = f"""INSERT INTO {lirtitl_s_vld_tablename}
        ({event_int_str()}, {face_name_str()}, {otx_title_str()}, {inx_title_str()})
        VALUES
          ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
        , ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
        ;
        """
        cursor.execute(insert_lirtitl_sqlstr)

        # insert lire_name records
        lirname_dimen = lire_name_str()
        lirname_s_vld_tablename = prime_tbl(lirname_dimen, "s", "vld")
        insert_lirname_sqlstr = f"""
INSERT INTO {lirname_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_name_str()}, {inx_name_str()})
VALUES
  ({event1}, '{sue_otx}', '{sue_otx}', '{sue_inx}')
, ({event7}, '{bob_otx}', '{bob_otx}', '{bob_inx}')
;
"""
        cursor.execute(insert_lirname_sqlstr)

        # insert lire_label records
        bob_str = "Bob"
        sue_str = "Sue"
        sue_clean_otx = "clean"
        sue_clean_inx = "limpia"
        bob_clean_otx = "very clean"
        bob_clean_inx = "very limpia"
        lirlabe_dimen = lire_label_str()
        lirlabe_s_vld_tablename = prime_tbl(lirlabe_dimen, "s", "vld")
        insert_lirlabe_sqlstr = f"""
INSERT INTO {lirlabe_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_label_str()}, {inx_label_str()})
VALUES
  ({event1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({event7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_lirlabe_sqlstr)

        # insert lire_rope records
        sue_clean_otx = "?casa?clean?"
        sue_clean_inx = ".casa.limpia."
        bob_clean_otx = ";casa;very clean;"
        bob_clean_inx = "/casa/very limpia/"
        lirrope_dimen = lire_rope_str()
        lirrope_s_vld_tablename = prime_tbl(lirrope_dimen, "s", "vld")
        insert_lirrope_sqlstr = f"""
INSERT INTO {lirrope_s_vld_tablename}
({event_int_str()}, {face_name_str()}, {otx_rope_str()}, {inx_rope_str()})
VALUES
  ({event1}, '{sue_str}', '{sue_clean_otx}', '{sue_clean_inx}')
, ({event7}, '{bob_str}', '{bob_clean_otx}', '{bob_clean_inx}')
;
"""
        cursor.execute(insert_lirrope_sqlstr)

        # insert lire_core records
        lircore_s_vld_tablename = prime_tbl("lircore", "s", "vld")
        insert_lircore_sqlstr = f"""INSERT INTO {lircore_s_vld_tablename}
        ({face_name_str()}, {otx_knot_str()}, {inx_knot_str()}, {unknown_str_str()})
        VALUES
          ('{sue_otx}', '{sue_otx_knot}', '{sue_inx_knot}', '{sue_unknown_str}')
        , ('{bob_otx}', '{bob_otx_knot}', '{bob_inx_knot}', '{bob_unknown_str}')
        ;
        """
        cursor.execute(insert_lircore_sqlstr)

        csv_delimiter = ","
        x_ideas = create_init_stance_idea_csv_strs()
        br00042_header = x_ideas.get("br00042")
        br00043_header = x_ideas.get("br00043")
        br00044_header = x_ideas.get("br00044")
        br00045_header = x_ideas.get("br00045")

        # WHEN
        add_lire_rows_to_stance_csv_strs(cursor, x_ideas, csv_delimiter)

        # THEN
        assert x_ideas.get("br00042") != br00042_header
        assert x_ideas.get("br00043") != br00043_header
        assert x_ideas.get("br00044") != br00044_header
        assert x_ideas.get("br00045") != br00045_header
