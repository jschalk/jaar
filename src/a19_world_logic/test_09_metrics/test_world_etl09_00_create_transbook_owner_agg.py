# def test_WorldUnit_fisc_table2fisc_ote1_agg_csvs_Scenaro1_SetsTableAttr(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fizz_world = worldunit_shop("fizz", worlds_dir())
#     bob_str = "Bob"
#     sue_str = "Sue"
#     event3 = 3
#     event7 = 7
#     accord23_str = "accord23"
#     accord45_str = "accord45"
#     timepoint55 = 55
#     timepoint66 = 66
#     fisc_mstr_dir = fizz_world._fisc_mstr_dir
#     a23_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord23_str)
#     a45_event_time_p = create_fisc_ote1_csv_path(fisc_mstr_dir, accord45_str)
#     a23_event_time_csv = f"""{fisc_tag_str()},{owner_name_str()},{event_int_str()},{tran_time_str()},error_message
# {accord23_str},{bob_str},{event3},{timepoint55},
# """
#     a45_event_time_csv = f"""{fisc_tag_str()},{owner_name_str()},{event_int_str()},{tran_time_str()},error_message
# {accord45_str},{sue_str},{event3},{timepoint55},
# {accord45_str},{sue_str},{event7},{timepoint66},
# """
#     save_file(a23_event_time_p, None, a23_event_time_csv)
#     save_file(a45_event_time_p, None, a45_event_time_csv)
#     assert os_path_exists(a23_event_time_p)
#     assert os_path_exists(a45_event_time_p)
#     a23_ote1_json_path = create_fisc_ote1_json_path(
#         fisc_mstr_dir, accord23_str
#     )
#     a45_ote1_json_path = create_fisc_ote1_json_path(
#         fisc_mstr_dir, accord45_str
#     )
#     assert os_path_exists(a23_event_time_json_path) is False
#     assert os_path_exists(a45_event_time_json_path) is False

#     # WHEN
#     fizz_world.fisc_ote1_agg_csvs2jsons()

#     # THEN
#     assert os_path_exists(a23_event_time_json_path)
#     assert os_path_exists(a45_event_time_json_path)
#     a23_ote1_dict = open_json(a23_event_time_json_path))
#     a45_ote1_dict = open_json(a45_event_time_json_path))
#     assert a23_ote1_dict == {bob_str: {str(event3): timepoint55}}
#     assert a45_ote1_dict == {
#         sue_str: {str(event3): timepoint55, str(event7): timepoint66}
#     }
