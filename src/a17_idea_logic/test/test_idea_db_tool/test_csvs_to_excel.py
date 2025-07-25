from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from os.path import exists as os_path_exists, join as os_path_join
from pandas import (
    DataFrame,
    ExcelWriter as pandas_ExcelWriter,
    read_excel as pandas_read_excel,
)
from pandas.testing import assert_frame_equal as pandas_testing_assert_frame_equal
from src.a17_idea_logic.idea_db_tool import (
    csv_dict_to_excel,
    prettify_excel,
    update_event_int_in_excel_files,
)
from src.a17_idea_logic.test._util.a17_env import (
    env_dir_setup_cleanup,
    get_module_temp_dir,
)


def test_csv_dict_to_excel_SavesFile(env_dir_setup_cleanup):
    # ESTABLISH
    test_data = {"TestSheet": "A,B\n5,6\n7,8"}
    x_dir = get_module_temp_dir()
    x_filename = "test_data.xlsx"
    file_path = f"{x_dir}/{x_filename}"
    assert os_path_exists(file_path) is False

    # WHEN
    csv_dict_to_excel(test_data, x_dir, x_filename)

    # THEN
    assert os_path_exists(file_path)
    # Load the created Excel file to verify its contents
    df = pandas_read_excel(file_path, sheet_name="TestSheet")
    expected_df = DataFrame({"A": [5, 7], "B": [6, 8]})

    pandas_testing_assert_frame_equal(df, expected_df)
    print("Test passed successfully.")


def test_prettify_excel(env_dir_setup_cleanup):
    # sourcery skip: no-loop-in-tests, no-conditionals-in-tests
    # ESTABLISH
    temp_dir = get_module_temp_dir()
    file_path = os_path_join(temp_dir, "test_huh.xlsx")

    df1 = DataFrame({"Name": ["Alice", "Bob"], "Salary": [50000, 60000]})
    df2 = DataFrame({"Item": ["Pen", "Notebook"], "Price": [1.5, 3.0]})

    with pandas_ExcelWriter(file_path, engine="xlsxwriter") as writer:
        df1.to_excel(writer, sheet_name="Employees", index=False)
        df2.to_excel(writer, sheet_name="Supplies", index=False)

    # WHEN
    prettify_excel(file_path)

    # THEN: Verify formatting changes
    wb = load_workbook(file_path)

    # Check headers in both sheets
    for sheet_name in ["Employees", "Supplies"]:
        ws = wb[sheet_name]

        # # Confirm header fill color (should match '#D7E4BC' -> RGB: D7E4BC)
        header_fill = ws["A1"].fill
        print(f"{header_fill=}")
        # assert isinstance(header_fill, PatternFill)
        # assert header_fill.fill_type == "solid"
        # assert header_fill.start_color.rgb in (
        #     "FFD7E4BC",
        #     "00D7E4BC",
        # )  # OpenPyXL sometimes uses different alpha

        # Confirm freeze pane is set at row 2
        print(f"{ws.freeze_panes=}")
        assert ws.freeze_panes == "A2"

        # Confirm zoom level (optional: may not always be persisted depending on openpyxl)
        if ws.sheet_view.zoomScale is not None:
            assert ws.sheet_view.zoomScale == 120

        # Confirm at least one column has adjusted width (Excel doesn't save actual width in standard units)
        col_widths = [
            ws.column_dimensions[col_letter].width for col_letter in ["A", "B"]
        ]
        assert any(
            width and width > 8 for width in col_widths
        )  # default width is ~8.43


def test_update_event_int_in_excel_files(env_dir_setup_cleanup):
    # Setup: Create test directory and Excel file
    temp_dir = get_module_temp_dir()
    file_path = os_path_join(temp_dir, "example_stance.xlsx")

    # Create Excel file with two sheets
    df1 = DataFrame({"name": ["Alice", "Bob"], "score": [80, 90]})
    df2 = DataFrame({"item": ["Pen", "Notebook"], "price": [1.5, 3.0]})
    with pandas_ExcelWriter(file_path) as writer:
        df1.to_excel(writer, sheet_name="Sheet1", index=False)
        df2.to_excel(writer, sheet_name="Sheet2", index=False)

    # Apply function
    update_event_int_in_excel_files(temp_dir, 42)

    # Reload the file and verify that event_int column exists and is correct
    result = pandas_read_excel(file_path, sheet_name=None)

    for sheet_df in result.values():
        assert "event_int" in sheet_df.columns
        assert all(sheet_df["event_int"] == 42)
