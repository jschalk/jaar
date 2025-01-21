# from src.f00_instrument.db_toolbox import create_table_from_columns
from src.f09_idea.idea_config import get_idea_config_dict
from src.f09_idea.idea_db_tool import (
    create_idea_sorted_table,
    create_idea_into_category_staging_query,
)
from sqlite3 import connect as sqlite3_connect


# def test_create_idea_into_category_staging_query_ReturnsObj_Scenario0_bud_item_teamlink():
#     # ESTABLISH
#     with sqlite3_connect(":memory:") as conn:
#         idea_number = "br000XX"
#         idea_cols = [
#             "event_int",
#             "face_name",
#             "fiscal_title",
#             "road",
#             "team_tag",
#             "owner_name",
#             "acct_name",
#             "amount",
#         ]
#         budteam_cat = "bud_item_teamlink"
#         src_table = f"{idea_number}_staging"
#         dst_table = f"{budteam_cat}_staging"
#         idea_config = get_idea_config_dict()
#         budteam_config = idea_config.get(budteam_cat)
#         print(f"{budteam_cat=}")
#         print(f"{budteam_config=}")
#         budteam_jkeys = budteam_config.get("jkeys")
#         budteam_jvals = budteam_config.get("jvalues")
#         budteam_args = set(budteam_jkeys.keys()).union(set(budteam_jvals.keys()))
#         print(f"{budteam_jkeys=}")
#         print(f"{budteam_jvals=}")
#         create_idea_sorted_table(conn, src_table, idea_cols)
#         create_idea_sorted_table(conn, dst_table, list(budteam_args))

#         # WHEN
#         gen_sqlstr = create_idea_into_category_staging_query(
#             conn, idea_number, budteam_cat, budteam_jkeys
#         )

#         # THEN
#         print(gen_sqlstr)
#         expected_sqlstr = f"""INSERT INTO {budteam_cat}_staging (idea_number, face_name, event_id, fiscal_title, road, team_tag)
# SELECT '{idea_number}' as idea_number, face_name, event_id, fiscal_title, road, team_tag
# FROM {idea_number}_staging
# WHERE road IS NOT NULL
#     AND team_tag IS NOT NULL
# GROUP BY face_name, event_id, fiscal_title, road, team_tag
# ;
# """
#         assert gen_sqlstr == expected_sqlstr


# def test_create_idea_into_category_staging_query_ReturnsObj_Scenario0_bud_item_teamlink():
#     # ESTABLISH
#     with sqlite3_connect(":memory:") as conn:
#         idea_number = "br000XX"
#         idea_cols = [
#             "event_int",
#             "face_name",
#             "fiscal_title",
#             "road",
#             "team_tag",
#             "owner_name",
#             "acct_name",
#             "amount",
#         ]
#         budteam_cat = "bud_item_teamlink"
#         src_table = f"{idea_number}_staging"
#         dst_table = f"{budteam_cat}_staging"
#         idea_config = get_idea_config_dict()
#         budteam_config = idea_config.get(budteam_cat)
#         print(f"{budteam_cat=}")
#         print(f"{budteam_config=}")
#         budteam_jkeys = budteam_config.get("jkeys")
#         budteam_jvals = budteam_config.get("jvalues")
#         budteam_args = set(budteam_jkeys.keys()).union(set(budteam_jvals.keys()))
#         print(f"{budteam_jkeys=}")
#         print(f"{budteam_jvals=}")
#         create_idea_sorted_table(conn, src_table, idea_cols)
#         create_idea_sorted_table(conn, dst_table, list(budteam_args))

#         # WHEN
#         gen_sqlstr = create_idea_into_category_staging_query(
#             conn, idea_number, budteam_cat, budteam_jkeys
#         )

#         # THEN
#         print(gen_sqlstr)
#         expected_sqlstr = f"""INSERT INTO {budteam_cat}_staging (idea_number, face_name, event_id, fiscal_title, road, team_tag)
# SELECT '{idea_number}' as idea_number, face_name, event_id, fiscal_title, road, team_tag
# FROM {idea_number}_staging
# WHERE road IS NOT NULL
#     AND team_tag IS NOT NULL
# GROUP BY face_name, event_id, fiscal_title, road, team_tag
# ;
# """
#         assert gen_sqlstr == expected_sqlstr

#     assert 1 == 2
