from src.f00_instrument.file import create_path
from src.f04_gift.atom_config import (
    acct_name_str,
    face_name_str,
    fiscal_title_str,
    owner_name_str,
)
from src.f08_pidgin.pidgin_config import event_int_str
from src.f09_idea.idea_db_tool import upsert_sheet, sheet_exists
from src.f10_etl.transformers import (
    etl_bow_inx_event_ideas_to_aft_faces,
)
from src.f10_etl.examples.etl_env import get_test_etl_dir, env_dir_setup_cleanup
from pandas.testing import (
    assert_frame_equal as pandas_assert_frame_equal,
)
from pandas import DataFrame, read_excel as pandas_read_excel


def test_etl_bow_event_ideas_to_train_events_Scenario0():
    # ESTABLISH
    sue_otx = "Sue"
    sue_inx = "Suzy"
    bob_inx = "Bob"
    yao_inx = "Yao"
    event3 = 3
    br00011_columns = [
        face_name_str(),
        event_int_str(),
        fiscal_title_str(),
        owner_name_str(),
        acct_name_str(),
    ]
    accord23_str = "accord23"
    sue0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    sue1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    sue2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
    br00011_filename = "br00011.xlsx"
    bow_dir = create_path(get_test_etl_dir(), "faces_bow")
    bow_sue_dir = create_path(bow_dir, sue_otx)
    bow_e3_dir = create_path(bow_sue_dir, event3)
    bow_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
    inx_str = "inx"
    upsert_sheet(bow_e3_br00011_path, inx_str, e3_accord23_df)
    assert sheet_exists(bow_e3_br00011_path, inx_str)
    aft_dir = create_path(get_test_etl_dir(), "faces_aft")
    aft_sue_dir = create_path(aft_dir, sue_inx)
    aft_br00011_path = create_path(aft_sue_dir, br00011_filename)
    print(f"{bow_e3_br00011_path=}")
    print(f"{aft_br00011_path=}")
    assert sheet_exists(aft_br00011_path, inx_str) is False

    # WHEN
    etl_bow_inx_event_ideas_to_aft_faces(bow_dir, aft_dir)

    # THEN
    assert sheet_exists(aft_br00011_path, inx_str)
    aft_e3_df = pandas_read_excel(aft_br00011_path, sheet_name=inx_str)
    # sue_i0 = [sue_inx, event3, accord23_str, bob_inx, bob_inx]
    # sue_i1 = [sue_inx, event3, accord23_str, yao_inx, bob_inx]
    # sue_i2 = [sue_inx, event3, accord23_str, yao_inx, yao_inx]
    # example_e3_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
    pandas_assert_frame_equal(aft_e3_df, e3_accord23_df)


# def test_etl_bow_event_ideas_to_train_events_Scenario1_MultpleFaceNames_CreatesEventInxSheets(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     sue_otx = "Sue"
#     sue_inx = "Suzy"
#     zia_otx = "Zia"
#     zia_inx = "Ziata"
#     bob_otx = "Bob"
#     yao_otx = "Yao"
#     event3 = 3
#     event7 = 7
#     event9 = 9
#     br00011_columns = [
#         face_name_str(),
#         event_int_str(),
#         fiscal_title_str(),
#         owner_name_str(),
#         acct_name_str(),
#     ]
#     accord23_str = "accord23"
#     accord55_otx = "accord55"
#     accord55_inx = "musik5555"
#     sue0 = [sue_otx, event3, accord23_str, bob_otx, bob_otx]
#     sue1 = [sue_otx, event3, accord23_str, yao_otx, bob_otx]
#     sue2 = [sue_otx, event3, accord23_str, yao_otx, yao_otx]
#     zia0 = [zia_otx, event7, accord23_str, bob_otx, bob_otx]
#     zia1 = [zia_otx, event9, accord23_str, yao_otx, bob_otx]
#     zia2 = [zia_otx, event9, accord23_str, yao_otx, yao_otx]
#     zia3 = [zia_otx, event9, accord55_otx, bob_otx, yao_otx]
#     bob0_inx = "Bobby"
#     bob1_inx = "Bobito"
#     bob2_inx = "Bobbie"
#     yao0_inx = "Yaoy"
#     yao1_inx = "Yaoito"
#     yao2_inx = "Yaobie"
#     e3_accord23_df = DataFrame([sue0, sue1, sue2], columns=br00011_columns)
#     e7_accord23_df = DataFrame([zia0], columns=br00011_columns)
#     e9_accord23_df = DataFrame([zia1, zia2, zia3], columns=br00011_columns)
#     br00011_filename = "br00011.xlsx"
#     x_event_pidgins = {sue_otx: {event3}, zia_otx: {event7, event9}}
#     x_bow_dir = create_path(get_test_etl_dir(), "faces_bow")
#     sue_bow_dir = create_path(x_bow_dir, sue_otx)
#     zia_bow_dir = create_path(x_bow_dir, zia_otx)
#     bow_e3_dir = create_path(sue_bow_dir, event3)
#     bow_e7_dir = create_path(zia_bow_dir, event7)
#     bow_e9_dir = create_path(zia_bow_dir, event9)
#     train_e3_br00011_path = create_path(bow_e3_dir, br00011_filename)
#     train_e7_br00011_path = create_path(bow_e7_dir, br00011_filename)
#     train_e9_br00011_path = create_path(bow_e9_dir, br00011_filename)
#     print(f"{train_e3_br00011_path=}")
#     print(f"{train_e7_br00011_path=}")
#     print(f"{train_e9_br00011_path=}")
#     upsert_sheet(train_e3_br00011_path, train_valid_str(), e3_accord23_df)
#     upsert_sheet(train_e7_br00011_path, train_valid_str(), e7_accord23_df)
#     upsert_sheet(train_e9_br00011_path, train_valid_str(), e9_accord23_df)
#     print(f"{train_valid_str()=}")
#     inx_str = "inx"
#     e3_pidginunit = pidginunit_shop(sue_otx, event3)
#     e7_pidginunit = pidginunit_shop(zia_otx, event7)
#     e9_pidginunit = pidginunit_shop(zia_otx, event9)
#     e3_pidginunit.set_otx2inx(type_AcctName_str(), sue_otx, sue_inx)
#     e3_pidginunit.set_otx2inx(type_AcctName_str(), bob_otx, bob0_inx)
#     e3_pidginunit.set_otx2inx(type_AcctName_str(), yao_otx, yao0_inx)
#     e7_pidginunit.set_otx2inx(type_AcctName_str(), zia_otx, zia_inx)
#     e7_pidginunit.set_otx2inx(type_AcctName_str(), bob_otx, bob1_inx)
#     e7_pidginunit.set_otx2inx(type_AcctName_str(), yao_otx, yao1_inx)
#     e9_pidginunit.set_otx2inx(type_AcctName_str(), zia_otx, zia_inx)
#     e9_pidginunit.set_otx2inx(type_AcctName_str(), bob_otx, bob2_inx)
#     e9_pidginunit.set_otx2inx(type_AcctName_str(), yao_otx, yao2_inx)
#     e9_pidginunit.set_otx2inx(type_TitleUnit_str(), accord55_inx, accord55_otx)
#     save_file(bow_e3_dir, pidgin_filename(), e3_pidginunit.get_json())
#     save_file(bow_e7_dir, pidgin_filename(), e7_pidginunit.get_json())
#     save_file(bow_e9_dir, pidgin_filename(), e9_pidginunit.get_json())
#     assert sheet_exists(train_e3_br00011_path, inx_str) is False
#     assert sheet_exists(train_e7_br00011_path, inx_str) is False
#     assert sheet_exists(train_e9_br00011_path, inx_str) is False

#     # WHEN
#     etl_bow_inx_event_ideas_to_aft_faces(x_bow_dir, x_event_pidgins)

#     # THEN
#     assert sheet_exists(train_e3_br00011_path, inx_str)
#     assert sheet_exists(train_e7_br00011_path, inx_str)
#     assert sheet_exists(train_e9_br00011_path, inx_str)
#     e3_inx_df = pandas_read_excel(train_e3_br00011_path, sheet_name=inx_str)
#     e7_inx_df = pandas_read_excel(train_e7_br00011_path, sheet_name=inx_str)
#     e9_inx_df = pandas_read_excel(train_e9_br00011_path, sheet_name=inx_str)
#     sue_i0 = [sue_inx, event3, accord23_str, bob0_inx, bob0_inx]
#     sue_i1 = [sue_inx, event3, accord23_str, yao0_inx, bob0_inx]
#     sue_i2 = [sue_inx, event3, accord23_str, yao0_inx, yao0_inx]
#     zia_i0 = [zia_inx, event7, accord23_str, bob1_inx, bob1_inx]
#     zia_i1 = [zia_inx, event9, accord23_str, yao2_inx, bob2_inx]
#     zia_i2 = [zia_inx, event9, accord23_str, yao2_inx, yao2_inx]
#     zia_i3 = [zia_inx, event9, accord55_otx, bob2_inx, yao2_inx]
#     example_e3_inx_df = DataFrame([sue_i0, sue_i1, sue_i2], columns=br00011_columns)
#     example_e7_inx_df = DataFrame([zia_i0], columns=br00011_columns)
#     example_e9_inx_df = DataFrame([zia_i1, zia_i2, zia_i3], columns=br00011_columns)
#     pandas_assert_frame_equal(e3_inx_df, example_e3_inx_df)
#     pandas_assert_frame_equal(e7_inx_df, example_e7_inx_df)
#     pandas_assert_frame_equal(e9_inx_df, example_e9_inx_df)
