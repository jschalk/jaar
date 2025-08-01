from os.path import exists as os_path_exists
from src.a00_data_toolbox.file_toolbox import count_files, create_path, save_json
from src.a06_believer_logic.test._util.a06_str import (
    belief_label_str,
    believer_name_str,
    partner_name_str,
)
from src.a07_timeline_logic.test._util.calendar_examples import (
    get_creg_config,
    get_expected_creg_year0_markdown,
)
from src.a07_timeline_logic.timeline_main import timelineunit_shop
from src.a12_hub_toolbox.a12_path import create_belief_json_path
from src.a15_belief_logic.belief_main import beliefunit_shop
from src.a17_idea_logic.idea_db_tool import upsert_sheet
from src.a19_kpi_toolbox.kpi_mstr import create_calendar_markdown_files
from src.a19_kpi_toolbox.test._util.a19_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_create_calendar_markdown_files_Senario0_NoFileIfWorldIsEmpty(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    belief_mstr_dir = create_path(temp_dir, "belief_mstr")
    output_dir = create_path(temp_dir, "output")
    assert not os_path_exists(output_dir)

    # WHEN
    create_calendar_markdown_files(belief_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(output_dir)
    assert count_files(output_dir) == 0


def test_create_calendar_markdown_files_Senario1_CreatesFileFromBeliefUnitJSON(
    env_dir_setup_cleanup,
):
    # ESTABLISH
    fay_str = "Fay"
    temp_dir = get_module_temp_dir()
    belief_mstr_dir = create_path(temp_dir, "belief_mstr")
    output_dir = create_path(temp_dir, "output")
    a23_str = "amy23"
    a23_belief_path = create_belief_json_path(belief_mstr_dir, a23_str)
    a23_beliefunit = beliefunit_shop(a23_str, belief_mstr_dir)
    assert a23_beliefunit.timeline == timelineunit_shop(get_creg_config())
    save_json(a23_belief_path, None, a23_beliefunit.get_dict())
    a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
    print(f"{a23_calendar_md_path=}")
    assert not os_path_exists(a23_calendar_md_path)

    # WHEN
    create_calendar_markdown_files(belief_mstr_dir, output_dir)

    # THEN
    assert os_path_exists(a23_calendar_md_path)
    expected_csv_str = get_expected_creg_year0_markdown()
    assert open(a23_calendar_md_path).read() == expected_csv_str


# def test_create_calendar_markdown_files_Senario1_Add_CreatesFile(
#     env_dir_setup_cleanup,
# ):
#     # ESTABLISH
#     fay_str = "Fay"
#     output_dir = create_path(worlds_dir(), "output")
#     fay_world = shop(fay_str, worlds_dir(), output_dir)
#     sue_str = "Sue"
#     event2 = 2
#     ex_filename = "Faybob.xlsx"
#     input_file_path = create_path(fay_world._input_dir, ex_filename)
#     a23_str = "amy23"
#     br00011_columns = [
#         event_int_str(),
#         face_name_str(),
#         belief_label_str(),
#         believer_name_str(),
#         partner_name_str()
#     ]
#     br00011_rows = [[event2, sue_str, a23_str, sue_str, sue_str]]
#     br00011_df = DataFrame(br00011_rows, columns=br00011_columns)
#     upsert_sheet(input_file_path, "br00011_ex3", br00011_df)
#     fay_world.sheets_input_to_clarity_mstr()

#     a23_calendar_md_path = create_path(output_dir, f"{a23_str}_calendar.md")
#     print(f"      {a23_calendar_md_path=}")
#     assert not os_path_exists(a23_calendar_md_path)

#     # WHEN
#     fay_world.create_calendar_markdown_files()

#     # THEN
#     assert os_path_exists(a23_calendar_md_path)
#     expected_csv_str = "belief_label,believer_name,funds,fund_rank,tasks_count\n"
#     assert open(a23_calendar_md_path).read() == expected_csv_str
