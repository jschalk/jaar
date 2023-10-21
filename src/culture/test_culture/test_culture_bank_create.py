from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import get_db_tables, get_db_columns


def test_culture_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())

    # WHEN
    x_culture.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        db_tables = get_db_tables(bank_conn)
        db_tables_columns = get_db_columns(bank_conn)

    # row_count = 0
    # for table_mame, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_mame=}")

    healer_text = "healer"
    voice_rank_text = "voice_rank"
    agendaunit_text = "agendaunit"
    agendaunit_columns = {healer_text: 1, voice_rank_text: 1}

    agenda_healer_text = "agenda_healer"
    party_title_text = "party_title"
    _agenda_credit_text = "_agenda_credit"
    _agenda_debt_text = "_agenda_debt"
    _agenda_goal_credit_text = "_agenda_goal_credit"
    _agenda_goal_debt_text = "_agenda_goal_debt"
    _agenda_goal_ratio_credit_text = "_agenda_goal_ratio_credit"
    _agenda_goal_ratio_debt_text = "_agenda_goal_ratio_debt"
    _creditor_active_text = "_creditor_active"
    _debtor_active_text = "_debtor_active"
    ledger_text = "ledger"
    ledger_columns = {
        agenda_healer_text: 1,
        party_title_text: 1,
        _agenda_credit_text: 1,
        _agenda_debt_text: 1,
        _agenda_goal_credit_text: 1,
        _agenda_goal_debt_text: 1,
        _agenda_goal_ratio_credit_text: 1,
        _agenda_goal_ratio_debt_text: 1,
        _creditor_active_text: 1,
        _debtor_active_text: 1,
    }

    currency_healer_text = "currency_healer"
    tax_healer_text = "tax_healer"
    tax_total_text = "tax_total"
    debt_text = "debt"
    tax_diff_text = "tax_diff"
    river_tally_text = "river_tally"
    river_tally_columns = {
        currency_healer_text: 1,
        tax_healer_text: 1,
        tax_total_text: 1,
        debt_text: 1,
        tax_diff_text: 1,
    }

    src_healer_text = "src_healer"
    dst_healer_text = "dst_healer"
    currency_start_text = "currency_start"
    currency_close_text = "currency_close"
    flow_num_text = "flow_num"
    parent_flow_num_text = "parent_flow_num"
    river_tree_level_text = "river_tree_level"
    river_flow_text = "river_flow"
    river_flow_columns = {
        currency_healer_text: 1,
        src_healer_text: 1,
        dst_healer_text: 1,
        currency_start_text: 1,
        currency_close_text: 1,
        flow_num_text: 1,
        parent_flow_num_text: 1,
        river_tree_level_text: 1,
    }

    bucket_num_text = "bucket_num"
    curr_start_text = "curr_start"
    curr_close_text = "curr_close"
    river_bucket_text = "river_bucket"
    river_bucket_columns = {
        currency_healer_text: 1,
        dst_healer_text: 1,
        bucket_num_text: 1,
        curr_start_text: 1,
        curr_close_text: 1,
    }

    idea_road_text = "idea_road"
    idea_catalog_text = "idea_catalog"
    idea_catalog_columns = {agenda_healer_text: 1, idea_road_text: 1}

    base_text = "base"
    pick_text = "pick"
    acptfact_catalog_text = "acptfact_catalog"
    acptfact_catalog_columns = {agenda_healer_text: 1, base_text: 1, pick_text: 1}

    groupunit_brand_text = "groupunit_brand"
    partylinks_set_by_culture_road_text = "partylinks_set_by_culture_road"
    groupunit_catalog_text = "groupunit_catalog"
    groupunit_catalog_columns = {
        agenda_healer_text: 1,
        groupunit_brand_text: 1,
        partylinks_set_by_culture_road_text: 1,
    }

    curr_tables = {
        agendaunit_text: agendaunit_columns,
        ledger_text: ledger_columns,
        river_tally_text: river_tally_columns,
        river_flow_text: river_flow_columns,
        river_bucket_text: river_bucket_columns,
        idea_catalog_text: idea_catalog_columns,
        acptfact_catalog_text: acptfact_catalog_columns,
        groupunit_catalog_text: groupunit_catalog_columns,
    }

    # for x_table_key, x_table_value in db_tables.items():
    #     print(f"{x_table_key=} {x_table_value=} {curr_tables.get(x_table_key)=}")
    #     assert curr_tables.get(x_table_key) != None

    assert db_tables.get(acptfact_catalog_text) != None  # 6
    assert db_tables.get(agendaunit_text) != None  # 0
    assert db_tables.get(groupunit_catalog_text) != None  # 7
    assert db_tables.get(idea_catalog_text) != None  # 5
    assert db_tables.get(ledger_text) != None  # 1
    assert db_tables.get(river_bucket_text) != None  # 4
    assert db_tables.get(river_flow_text) != None  # 3
    assert db_tables.get(river_tally_text) != None  # 2
    assert len(db_tables) == 8
    assert len(db_tables) == len(curr_tables)
    assert len(db_tables) == len(db_tables_columns)

    # for y_table_key, y_columns_value in db_tables_columns.items():
    #     for y_column_key, y_column_value in y_columns_value.items():
    #         print(f"{y_table_key=} {y_column_key=}")
    #     assert curr_tables.get(y_table_key) == y_columns_value

    assert db_tables_columns.get(agendaunit_text) == agendaunit_columns
    assert db_tables_columns.get(acptfact_catalog_text) == acptfact_catalog_columns
    assert db_tables_columns.get(agendaunit_text) == agendaunit_columns
    assert db_tables_columns.get(groupunit_catalog_text) == groupunit_catalog_columns
    assert db_tables_columns.get(idea_catalog_text) == idea_catalog_columns
    assert db_tables_columns.get(ledger_text) == ledger_columns
    assert db_tables_columns.get(river_bucket_text) == river_bucket_columns
    assert db_tables_columns.get(river_flow_text) == river_flow_columns
    assert db_tables_columns.get(river_tally_text) == river_tally_columns
