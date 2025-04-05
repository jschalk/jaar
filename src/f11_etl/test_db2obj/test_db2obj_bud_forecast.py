from src.f00_instrument.db_toolbox import get_row_count, create_insert_query
from src.f01_road.deal import fisc_title_str
from src.f02_bud.bud import budunit_shop
from src.f05_fund_metric.fund_metric_config import (
    get_fund_metric_config_dict,
    get_fund_metric_dimen_args,
)
from src.f08_fisc.fisc import fiscunit_shop, get_from_dict as fiscunit_get_from_dict
from src.f08_fisc.fisc_config import cashbook_str, brokerunits_str, timeline_str
from src.f10_idea.idea_config import get_default_sorted_list
from src.f11_etl.tran_sqlstrs import create_forecast_tables
from src.f11_etl.db_obj_tool import (
    get_fisc_dict_from_db,
    insert_forecast_obj,
    create_budmemb_insert_sqlstr,
    create_budacct_insert_sqlstr,
    create_budgrou_insert_sqlstr,
    create_budawar_insert_sqlstr,
    create_budfact_insert_sqlstr,
    create_budheal_insert_sqlstr,
    create_budprem_insert_sqlstr,
    create_budreas_insert_sqlstr,
    create_budteam_insert_sqlstr,
    create_buditem_insert_sqlstr,
    create_budunit_metrics_insert_sqlstr,
)
from sqlite3 import connect as sqlite3_connect


def test_create_budunit_metrics_insert_sqlstr_ReturnsObj():
    # ESTABLISH
    # x_args = get_fund_metric_dimen_args("budunit")
    # for x_arg in sorted(x_args):
    #     print(f"{x_arg=}")
    x__keeps_buildable = True
    x__keeps_justified = False
    x__offtrack_fund = 55.5
    x__rational = True
    x__sum_healerlink_share = 66.6
    x__tree_traverse_count = 7
    x_credor_respect = 88.2
    x_debtor_respect = 88.4
    x_fund_coin = 3
    x_fund_pool = 3000
    x_max_tree_traverse = 22
    x_penny = 4
    x_respect_bit = 0.2
    x_tally = 6
    values_dict = {
        "_keeps_buildable": x__keeps_buildable,
        "_keeps_justified": x__keeps_justified,
        "_offtrack_fund": x__offtrack_fund,
        "_rational": x__rational,
        "_sum_healerlink_share": x__sum_healerlink_share,
        "_tree_traverse_count": x__tree_traverse_count,
        "credor_respect": x_credor_respect,
        "debtor_respect": x_debtor_respect,
        "fund_coin": x_fund_coin,
        "fund_pool": x_fund_pool,
        "max_tree_traverse": x_max_tree_traverse,
        "penny": x_penny,
        "respect_bit": x_respect_bit,
        "tally": x_tally,
    }

    # WHEN
    insert_sqlstr = create_budunit_metrics_insert_sqlstr(values_dict)

    # THEN
    assert insert_sqlstr
    with sqlite3_connect(":memory:") as conn:
        cursor = conn.cursor()
        create_forecast_tables(cursor)
        table_name = "budunit_forecast"
        expected_sqlstr = create_insert_query(cursor, table_name, values_dict)
        print(expected_sqlstr)
        print("")
        print(insert_sqlstr)
        assert insert_sqlstr == expected_sqlstr


# def test_create_budmemb_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     x_config = get_fund_metric_config_dict()
#     x_dimens = {}
#     x_args = x_config.get()
#     for x_dimen in fund_metric_config.keys():
#         # print(f"{x_dimen} checking...")
#         x_config = fund_metric_config.get(x_dimen)
#         dimen_abv = x_config.get("abbreviation")
#         print(f"create_{dimen_abv}_insert_sqlstr")
#     # x_dimens[x_dimen] = create_insert_forecast(x_dimen)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_forecast_tables(cursor)
#         for x_dimen in x_dimens:
#             print(f"{x_dimen=}")
#             table_name = f"{x_dimen}_forecast"
#             values_dict = {}
#             expected_insert_sqlstr = create_insert_query(
#                 cursor, table_name, values_dict
#             )
#         x_table_name = "budunit_forecast"

#     assert create_budmemb_insert_sqlstr() == 2


# def test_create_budacct_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budacct_insert_sqlstr() == 2


# def test_create_budgrou_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budgrou_insert_sqlstr() == 2


# def test_create_budawar_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budawar_insert_sqlstr() == 2


# def test_create_budfact_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budfact_insert_sqlstr() == 2


# def test_create_budheal_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budheal_insert_sqlstr() == 2


# def test_create_budprem_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budprem_insert_sqlstr() == 2


# def test_create_budreas_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budreas_insert_sqlstr() == 2


# def test_create_budteam_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_budteam_insert_sqlstr() == 2


# def test_create_buditem_insert_sqlstr_ReturnsObj():
#     # ESTABLISH
#     assert create_buditem_insert_sqlstr() == 2


# def test_create_insert_forecast_sqlstr_ReturnsObj():
#     # ESTABLISH sourcery skip: no-loop-in-tests
#     fund_metric_config = get_fund_metric_config_dict()
#     x_dimens = {}
#     for x_dimen in fund_metric_config.keys():
#         # print(f"{x_dimen} checking...")
#         x_config = fund_metric_config.get(x_dimen)
#         dimen_abv = x_config.get("abbreviation")
#         print(f"create_{dimen_abv}_insert_sqlstr")
#     # x_dimens[x_dimen] = create_insert_forecast(x_dimen)

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_forecast_tables(cursor)
#         for x_dimen in x_dimens:
#             print(f"{x_dimen=}")
#             table_name = f"{x_dimen}_forecast"
#             values_dict = {}
#             expected_insert_sqlstr = create_insert_query(
#                 cursor, table_name, values_dict
#             )
#         x_table_name = "budunit_forecast"

#     assert 1 == 2


# # create tests to convert settled budunit to database
# # create budunit object
# # check that row does not exist in database
# # insert obj
# # check that row does exist in database
# # select row
# # prove selected row = obj __dict__


# def test_insert_forecast_obj_CreatesTableRowsFor_budunit_forecast():
#     # ESTABLISH
#     sue_str = "Sue"
#     iowa_fisc_title = "Iowa"
#     slash_bridge = "/"
#     x_fund_pool = 777
#     x_fund_coin = 7
#     x_respect_bit = 5
#     x_penny = 1
#     x_tally = 55
#     sue_bud = budunit_shop(
#         owner_name=sue_str,
#         fisc_title=iowa_fisc_title,
#         bridge=slash_bridge,
#         fund_pool=x_fund_pool,
#         fund_coin=x_fund_coin,
#         respect_bit=x_respect_bit,
#         penny=x_penny,
#         tally=x_tally,
#     )
#     sue_bud.settle_bud()

#     with sqlite3_connect(":memory:") as conn:
#         cursor = conn.cursor()
#         create_forecast_tables(cursor)
#         x_table_name = "budunit_forecast"
#         assert get_row_count(cursor, x_table_name) == 0

#         # WHEN
#         insert_forecast_obj(cursor, sue_bud)

#         # THEN
#         assert get_row_count(cursor, x_table_name) == 1
#         select_sqlstr = f"SELECT * FROM {x_table_name};"
#         cursor.execute(select_sqlstr)
#         rows = cursor.fetchall()
#         expected_data = [(1, "John Doe", 30, "john@example.com")]
#         assert rows == expected_data


#     assert 1 == 2


# "budunit_forecast"
# "bud_acct_membership_forecast"
# "bud_acctunit_forecast"
# "bud_groupunit_forecast"
# "bud_item_awardlink_forecast"
# "bud_item_factunit_forecast"
# "bud_item_healerlink_forecast"
# "bud_item_reason_premiseunit_forecast"
# "bud_item_reasonunit_forecast"
# "bud_item_teamlink_forecast"
# "bud_itemunit_forecast"
