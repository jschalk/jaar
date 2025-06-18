from src.a07_calendar_logic._util.calendar_examples import get_five_config
from src.a07_calendar_logic.calendar_markdown import (
    CalendarGrid,
    MonthGridRow,
    MonthGridUnit,
)
from src.a07_calendar_logic.chrono import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)


def test_MonthGridUnit_Exists():
    # ESTABLISH / WHEN
    x_monthgridunit = MonthGridUnit()

    # THEN
    assert not x_monthgridunit.name
    assert not x_monthgridunit.cumlative_days
    assert not x_monthgridunit.first_weekday
    assert not x_monthgridunit.week_length
    assert not x_monthgridunit.month_days_int
    assert not x_monthgridunit.monthday_distortion
    assert not x_monthgridunit.weekday_2char_abvs
    assert not x_monthgridunit.max_monthday_rows


def test_MonthGridUnit_markdown_name_ReturnsObj():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit("January", None, 5, 7, 31, 1)

    # WHEN
    markdown_name = jan_monthgridunit.markdown_name()

    # THEN
    assert markdown_name == "      January       "
    assert len(markdown_name) == 3 * 7 - 1


def test_MonthGridUnit_markdown_weekdays_ReturnsObj():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit("January", None, 5, 7, 31, 1)
    jan_monthgridunit.weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]

    # WHEN
    markdown_weekdays = jan_monthgridunit.markdown_weekdays()

    # THEN
    assert markdown_weekdays == "Mo Tu We Th Fr Sa Su"


def test_MonthGridUnit_markdown_day_numbers_ReturnsObj_Scenario0_Row0():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthgridunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 0  1  2  3  4  5  6"


def test_MonthGridUnit_markdown_day_numbers_ReturnsObj_Scenario1_Row1():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthgridunit.markdown_day_numbers(row_int=1)

    # THEN
    assert markdown_day_numbers == " 7  8  9 10 11 12 13"


def test_MonthGridUnit_markdown_day_numbers_ReturnsObj_Scenario2_monthday_distortion():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthgridunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 1  2  3  4  5  6  7"


def test_MonthGridUnit_markdown_day_numbers_ReturnsObj_Scenario3_first_weekday():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthgridunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == "          1  2  3  4"


def test_MonthGridUnit_markdown_day_numbers_ReturnsObj_Scenario4_first_weekday():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN / THEN
    assert jan_monthgridunit.markdown_day_numbers(row_int=1) == " 5  6  7  8  9 10 11"
    assert jan_monthgridunit.markdown_day_numbers(row_int=4) == "26 27 28 29 30 31   "


def test_MonthGridUnit_set_max_monthday_rows_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )
    assert not jan_monthgridunit.max_monthday_rows

    # WHEN
    jan_monthgridunit.set_max_monthday_rows()

    # THEN
    assert jan_monthgridunit.max_monthday_rows == 5


def test_MonthGridUnit_get_next_month_first_weekday_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "February",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthgridunit.get_next_month_first_weekday() == 3


def test_MonthGridUnit_get_next_month_first_weekday_ReturnsObj_Scenario1():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "February",
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthgridunit.get_next_month_first_weekday() == 6


def test_MonthGridUnit_get_next_month_first_weekday_ReturnsObj_Scenario2():
    # ESTABLISH
    jan_monthgridunit = MonthGridUnit(
        "February",
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=31,
    )

    # WHEN / THEN
    assert jan_monthgridunit.get_next_month_first_weekday() == 2


def test_MonthGridRow_Exists():
    # ESTABLISH / WHEN
    x_monthgridrow = MonthGridRow()

    # THEN
    assert not x_monthgridrow.months
    assert not x_monthgridrow.max_monthday_numbers_row


def test_MonthGridRow_set_max_monthday_numbers_row_SetsAttr():
    # ESTABLISH
    x_monthgridrow = MonthGridRow([])
    jan_monthgridunit = MonthGridUnit("January", None, 5, 7, 31, 1)
    feb_monthgridunit = MonthGridUnit("February", None, 1, 7, 29, 1)
    mar_monthgridunit = MonthGridUnit("March", None, 2, 7, 31, 1)
    x_monthgridrow.months.append(jan_monthgridunit)
    x_monthgridrow.months.append(feb_monthgridunit)
    x_monthgridrow.months.append(mar_monthgridunit)
    assert not x_monthgridrow.max_monthday_numbers_row

    # WHEN
    x_monthgridrow.set_max_monthday_numbers_row()

    # THEN
    assert x_monthgridrow.max_monthday_numbers_row == 6


def test_MonthGridRow_markdown_str_ReturnsObj():
    # ESTABLISH
    x_monthgridrow = MonthGridRow([])
    jan_monthgridunit = MonthGridUnit("January", None, 0, 7, 31, 1)
    feb_monthgridunit = MonthGridUnit("February", None, 3, 7, 29, 1)
    mar_monthgridunit = MonthGridUnit("March", None, 4, 7, 31, 1)
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    jan_monthgridunit.weekday_2char_abvs = x_weekday_2char_abvs
    feb_monthgridunit.weekday_2char_abvs = x_weekday_2char_abvs
    mar_monthgridunit.weekday_2char_abvs = x_weekday_2char_abvs
    x_monthgridrow.months.append(jan_monthgridunit)
    x_monthgridrow.months.append(feb_monthgridunit)
    x_monthgridrow.months.append(mar_monthgridunit)

    # WHEN
    x_str = x_monthgridrow.markdown_str()

    # THEN
    print(f"{x_str}")
    expected_str = """
      January                   February                   March        
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
 1  2  3  4  5  6  7                1  2  3  4                   1  2  3
 8  9 10 11 12 13 14       5  6  7  8  9 10 11       4  5  6  7  8  9 10
15 16 17 18 19 20 21      12 13 14 15 16 17 18      11 12 13 14 15 16 17
22 23 24 25 26 27 28      19 20 21 22 23 24 25      18 19 20 21 22 23 24
29 30 31                  26 27 28 29               25 26 27 28 29 30 31"""
    assert x_str == expected_str


def test_CalendarGrid_Exists():
    # ESTABLISH / WHEN
    x_calendargrid = CalendarGrid()

    # THEN
    assert not x_calendargrid.timelineunit
    assert not x_calendargrid.timeline_config
    assert not x_calendargrid.monthgridrows
    assert not x_calendargrid.timelineunit
    assert not x_calendargrid.week_length
    assert not x_calendargrid.month_char_width
    assert not x_calendargrid.monthgridrow_length
    assert not x_calendargrid.display_md_width
    assert x_calendargrid.max_md_width == 84


def test_CalendarGrid_create_2char_weekday_list_ReturnObj():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarGrid(timeline_config=creg_config)
    creg_calendergrid.set_timelineunit("Monday", "Tuesday")
    display_init_day = "Monday"

    # WHEN
    weekday_2char_list = creg_calendergrid.create_2char_weekday_list(display_init_day)

    # THEN
    expected_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    assert weekday_2char_list == expected_weekday_2char_abvs


def test_CalendarGrid_set_timelineunit_SetsAttr():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarGrid(timeline_config=creg_config)
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    monday_str = "Monday"
    assert not creg_calendergrid.timelineunit

    # WHEN
    creg_calendergrid.set_timelineunit(monday_str, "Tuesday")

    # THEN
    expected_timelineunit = timelineunit_shop(creg_config)
    assert creg_calendergrid.timelineunit == expected_timelineunit
    assert creg_calendergrid.week_length == 7
    assert creg_calendergrid.month_char_width == 26
    assert creg_calendergrid.monthgridrow_length == 3
    assert creg_calendergrid.display_md_width == 72
    assert len(creg_calendergrid.monthgridrows) == 4
    assert len(creg_calendergrid.monthgridrows[0].months) == 3
    monthgridunit0 = creg_calendergrid.monthgridrows[0].months[0]
    assert monthgridunit0.name == "March"
    assert monthgridunit0.cumlative_days == 31
    assert monthgridunit0.month_days_int == 31
    assert monthgridunit0.week_length == 7
    assert monthgridunit0.monthday_distortion == 1
    assert monthgridunit0.weekday_2char_abvs == x_weekday_2char_abvs
    assert monthgridunit0.first_weekday == 1
    monthgridunit7 = creg_calendergrid.monthgridrows[2].months[0]
    assert monthgridunit7.name == "September"
    assert monthgridunit7.cumlative_days == 214
    assert monthgridunit7.month_days_int == 30
    assert monthgridunit7.week_length == 7
    assert monthgridunit7.monthday_distortion == 1
    assert monthgridunit7.weekday_2char_abvs == x_weekday_2char_abvs
    # assert monthgridunit7.first_weekday == 4


def test_CalendarGrid_create_markdown_ReturnsObj_Scernario0_creg_config():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarGrid(timeline_config=creg_config)
    creg_calendergrid.set_timelineunit("Monday", "Tuesday")
    year_int = 2024

    # WHEN
    cal_markdown = creg_calendergrid.create_markdown(year_int)

    # THEN
    print(cal_markdown)
    expected_calendar_markdown = """
                               Year 2024                                

       March                     April                      May         
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
    1  2  3  4  5  6                   1  2  3                         1
 7  8  9 10 11 12 13       4  5  6  7  8  9 10       2  3  4  5  6  7  8
14 15 16 17 18 19 20      11 12 13 14 15 16 17       9 10 11 12 13 14 15
21 22 23 24 25 26 27      18 19 20 21 22 23 24      16 17 18 19 20 21 22
28 29 30 31               25 26 27 28 29 30         23 24 25 26 27 28 29
                                                    30 31               

        June                      July                     August       
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
       1  2  3  4  5                   1  2  3       1  2  3  4  5  6  7
 6  7  8  9 10 11 12       4  5  6  7  8  9 10       8  9 10 11 12 13 14
13 14 15 16 17 18 19      11 12 13 14 15 16 17      15 16 17 18 19 20 21
20 21 22 23 24 25 26      18 19 20 21 22 23 24      22 23 24 25 26 27 28
27 28 29 30               25 26 27 28 29 30 31      29 30 31            

     September                  October                   November      
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
          1  2  3  4                      1  2          1  2  3  4  5  6
 5  6  7  8  9 10 11       3  4  5  6  7  8  9       7  8  9 10 11 12 13
12 13 14 15 16 17 18      10 11 12 13 14 15 16      14 15 16 17 18 19 20
19 20 21 22 23 24 25      17 18 19 20 21 22 23      21 22 23 24 25 26 27
26 27 28 29 30            24 25 26 27 28 29 30      28 29 30            
                          31                                            

      December                  January                   February      
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
          1  2  3  4                         1             1  2  3  4  5
 5  6  7  8  9 10 11       2  3  4  5  6  7  8       6  7  8  9 10 11 12
12 13 14 15 16 17 18       9 10 11 12 13 14 15      13 14 15 16 17 18 19
19 20 21 22 23 24 25      16 17 18 19 20 21 22      20 21 22 23 24 25 26
26 27 28 29 30 31         23 24 25 26 27 28 29      27 28               
                          30 31                                         """
    assert cal_markdown == expected_calendar_markdown


def test_CalendarGrid_create_markdown_ReturnsObj_Scernario1_five_config():
    # ESTABLISH
    five_calendergrid = CalendarGrid(timeline_config=get_five_config())
    five_calendergrid.set_timelineunit("Anaday", "Chiday")
    year_int = 5224

    # WHEN
    cal_markdown = five_calendergrid.create_markdown(year_int)

    # THEN
    # print(cal_markdown)
    expected_calendar_markdown = """
                                Year 5224                                 

   Fredrick              Geo               Holocene             Iguana    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Jesus                Keel               LeBron             Mikayla    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

    Ninon               Obama              Preston              Quorum    
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14 15 16 17      13 14 15 16 17
18 19 20 21 22      18 19 20 21 22      18 19 20 21 22      18 19 20 21 22
23 24               23 24               23 24               23 24         

  RioGrande             Simon               Trump     
An Ba Ch Da Ea      An Ba Ch Da Ea      An Ba Ch Da Ea
       0  1  2             0  1  2             0  1  2
 3  4  5  6  7       3  4  5  6  7       3  4  5  6  7
 8  9 10 11 12       8  9 10 11 12       8  9 10 11 12
13 14 15 16 17      13 14 15 16 17      13 14         
18 19 20 21 22      18 19 20 21 22                    
23 24               23 24                             """
    assert cal_markdown == expected_calendar_markdown
