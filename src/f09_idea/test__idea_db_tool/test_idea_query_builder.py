from src.f00_instrument.db_toolbox import create_table_from_columns
from src.f09_idea.idea_config import get_idea_config_dict
from src.f09_idea.idea_db_tool import create_idea_into_category_staging_query
from sqlite3 import connect as sqlite3_connect


# def test_create_idea_into_category_staging_query_ReturnsObj_Scenario0():
#     # ESTABLISH
#     with sqlite3_connect(":memory:") as conn:
#         idea_number = "br000XX"
#         idea_cols = ["id", "name", "age", "email", "hair"]
#         x_category= "fiscalunit"
#         idea_config = get_idea_config_dict()
#         src_table = f"{idea_number}_staging"
#         dst_table = f"{x_category}_staging"
#         dst_jkeys
#         dst_jvalues
#         create_table_from_columns(conn, x_tablename, x_columns, {})

#         # WHEN
#         gen_sqlstr = create_idea_into_category_staging_query(
#             conn, x_tablename, {"id"}, {"email"}
#         )

#         # THEN
#         expected_sqlstr = f"""
# INSERT INTO {dst_table} (idea_number, {common_columns_header})
# SELECT '{idea_number}' as idea_number, {common_columns_header}
# FROM {src_table}
# GROUP BY face_name, event_int, fiscal_title
# ;
# """
# ;
# """
#         print(f"""{gen_sqlstr=}""")
#         assert gen_sqlstr == expected_sqlstr
