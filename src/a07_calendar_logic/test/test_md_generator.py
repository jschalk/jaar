from src.a07_calendar_logic.calendar_markdown import (
    CalendarMarkDown,
    MonthMarkDownRow,
    MonthMarkDownUnit,
    center_word,
)
from src.a07_calendar_logic.chrono import (
    get_default_timeline_config_dict,
    timelineunit_shop,
)
from src.a07_calendar_logic.test._util.calendar_examples import get_five_config


def test_center_word_ReturnObj():
    # ESTABLISH / WHEN / THEN
    assert center_word(10, "fizz") == "   fizz   "
    assert center_word(15, "fizz") == "      fizz     "
    assert center_word(6, "fizz") == " fizz "
    assert center_word(6, "fizzbuzz") == "fizzbu"


def test_MonthMarkDownUnit_Exists():
    # ESTABLISH / WHEN
    x_monthmarkdownunit = MonthMarkDownUnit()

    # THEN
    assert not x_monthmarkdownunit.label
    assert not x_monthmarkdownunit.cumulative_days
    assert not x_monthmarkdownunit.first_weekday
    assert not x_monthmarkdownunit.week_length
    assert not x_monthmarkdownunit.month_days_int
    assert not x_monthmarkdownunit.monthday_distortion
    assert not x_monthmarkdownunit.weekday_2char_abvs
    assert not x_monthmarkdownunit.max_monthday_rows
    assert not x_monthmarkdownunit.year
    assert not x_monthmarkdownunit.offset_year


def test_MonthMarkDownUnit_markdown_label_ReturnsObj_Scenario0_No_offset_year():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.year = 1999

    # WHEN
    markdown_label = jan_monthmarkdownunit.markdown_label()

    # THEN
    assert markdown_label == "      January       "
    assert len(markdown_label) == 3 * 7 - 1


def test_MonthMarkDownUnit_markdown_label_ReturnsObj_Scenario1_Yes_offset_year():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.offset_year = True
    jan_monthmarkdownunit.year = 1999

    # WHEN
    markdown_label = jan_monthmarkdownunit.markdown_label()

    # THEN
    assert markdown_label == "   January (2000)   "
    assert len(markdown_label) == 3 * 7 - 1


def test_MonthMarkDownUnit_markdown_weekdays_ReturnsObj():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    jan_monthmarkdownunit.weekday_2char_abvs = [
        "Mo",
        "Tu",
        "We",
        "Th",
        "Fr",
        "Sa",
        "Su",
    ]

    # WHEN
    markdown_weekdays = jan_monthmarkdownunit.markdown_weekdays()

    # THEN
    assert markdown_weekdays == "Mo Tu We Th Fr Sa Su"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario0_Row0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 0  1  2  3  4  5  6"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario1_Row1():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=0,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=1)

    # THEN
    assert markdown_day_numbers == " 7  8  9 10 11 12 13"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario2_monthday_distortion():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=0,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == " 1  2  3  4  5  6  7"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario3_first_weekday():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN
    markdown_day_numbers = jan_monthmarkdownunit.markdown_day_numbers(row_int=0)

    # THEN
    assert markdown_day_numbers == "          1  2  3  4"


def test_MonthMarkDownUnit_markdown_day_numbers_ReturnsObj_Scenario4_first_weekday():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )

    # WHEN / THEN
    assert (
        jan_monthmarkdownunit.markdown_day_numbers(row_int=1) == " 5  6  7  8  9 10 11"
    )
    assert (
        jan_monthmarkdownunit.markdown_day_numbers(row_int=4) == "26 27 28 29 30 31   "
    )


def test_MonthMarkDownUnit_set_max_monthday_rows_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "January",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=31,
        monthday_distortion=1,
    )
    assert not jan_monthmarkdownunit.max_monthday_rows

    # WHEN
    jan_monthmarkdownunit.set_max_monthday_rows()

    # THEN
    assert jan_monthmarkdownunit.max_monthday_rows == 5


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario0():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "February",
        None,
        first_weekday=3,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 3


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario1():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "February",
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=28,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 6


def test_MonthMarkDownUnit_get_next_month_first_weekday_ReturnsObj_Scenario2():
    # ESTABLISH
    jan_monthmarkdownunit = MonthMarkDownUnit(
        "February",
        None,
        first_weekday=6,
        week_length=7,
        month_days_int=31,
    )

    # WHEN / THEN
    assert jan_monthmarkdownunit.get_next_month_first_weekday() == 2


def test_MonthMarkDownRow_Exists():
    # ESTABLISH / WHEN
    x_monthmarkdownrow = MonthMarkDownRow()

    # THEN
    assert not x_monthmarkdownrow.months
    assert not x_monthmarkdownrow.max_monthday_numbers_row


def test_MonthMarkDownRow_set_max_monthday_numbers_row_SetsAttr():
    # ESTABLISH
    x_monthmarkdownrow = MonthMarkDownRow([])
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 5, 7, 31, 1)
    feb_monthmarkdownunit = MonthMarkDownUnit("February", None, 1, 7, 29, 1)
    mar_monthmarkdownunit = MonthMarkDownUnit("March", None, 2, 7, 31, 1)
    x_monthmarkdownrow.months.append(jan_monthmarkdownunit)
    x_monthmarkdownrow.months.append(feb_monthmarkdownunit)
    x_monthmarkdownrow.months.append(mar_monthmarkdownunit)
    assert not x_monthmarkdownrow.max_monthday_numbers_row

    # WHEN
    x_monthmarkdownrow.set_max_monthday_numbers_row()

    # THEN
    assert x_monthmarkdownrow.max_monthday_numbers_row == 6


def test_MonthMarkDownRow_markdown_str_ReturnsObj():
    # ESTABLISH
    x_monthmarkdownrow = MonthMarkDownRow([])
    jan_monthmarkdownunit = MonthMarkDownUnit("January", None, 0, 7, 31, 1)
    feb_monthmarkdownunit = MonthMarkDownUnit("February", None, 3, 7, 29, 1)
    mar_monthmarkdownunit = MonthMarkDownUnit("March", None, 4, 7, 31, 1)
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    jan_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    feb_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    mar_monthmarkdownunit.weekday_2char_abvs = x_weekday_2char_abvs
    x_monthmarkdownrow.months.append(jan_monthmarkdownunit)
    x_monthmarkdownrow.months.append(feb_monthmarkdownunit)
    x_monthmarkdownrow.months.append(mar_monthmarkdownunit)

    # WHEN
    x_str = x_monthmarkdownrow.markdown_str()

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


def test_CalendarMarkDown_Exists():
    # ESTABLISH / WHEN
    x_calendarmarkdown = CalendarMarkDown()

    # THEN
    assert not x_calendarmarkdown.timelineunit
    assert not x_calendarmarkdown.timeline_config
    assert not x_calendarmarkdown.monthmarkdownrows
    assert not x_calendarmarkdown.timelineunit
    assert not x_calendarmarkdown.week_length
    assert not x_calendarmarkdown.month_char_width
    assert not x_calendarmarkdown.monthmarkdownrow_length
    assert not x_calendarmarkdown.display_md_width
    assert not x_calendarmarkdown.display_init_day
    assert not x_calendarmarkdown.yr1_jan1_offset_days
    assert x_calendarmarkdown.max_md_width == 84


def test_CalendarMarkDown_create_2char_weekday_list_ReturnObj():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarMarkDown(timeline_config=creg_config)
    creg_calendergrid.display_init_day = "Monday"
    creg_calendergrid.set_monthmarkdownrows("Tuesday", 1997)

    # WHEN
    weekday_2char_list = creg_calendergrid.create_2char_weekday_list()

    # THEN
    expected_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    assert weekday_2char_list == expected_weekday_2char_abvs


def test_CalendarMarkDown_set_monthmarkdownrows_SetsAttr():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarMarkDown(timeline_config=creg_config)
    monday_str = "Monday"
    creg_calendergrid.display_init_day = monday_str
    x_weekday_2char_abvs = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    yr1997_int = 1997
    assert not creg_calendergrid.timelineunit

    # WHEN
    creg_calendergrid.set_monthmarkdownrows("Tuesday", yr1997_int)

    # THEN
    expected_timelineunit = timelineunit_shop(creg_config)
    assert creg_calendergrid.timelineunit == expected_timelineunit
    assert creg_calendergrid.week_length == 7
    assert creg_calendergrid.month_char_width == 26
    assert creg_calendergrid.monthmarkdownrow_length == 3
    assert creg_calendergrid.display_md_width == 72
    assert len(creg_calendergrid.monthmarkdownrows) == 4
    assert len(creg_calendergrid.monthmarkdownrows[0].months) == 3
    monthmarkdownunit0 = creg_calendergrid.monthmarkdownrows[0].months[0]
    assert monthmarkdownunit0.label == "March"
    assert monthmarkdownunit0.cumulative_days == 31
    assert monthmarkdownunit0.month_days_int == 31
    assert monthmarkdownunit0.week_length == 7
    assert monthmarkdownunit0.monthday_distortion == 1
    assert monthmarkdownunit0.weekday_2char_abvs == x_weekday_2char_abvs
    assert monthmarkdownunit0.first_weekday == 1
    assert monthmarkdownunit0.year == yr1997_int
    assert not monthmarkdownunit0.offset_year
    monthmarkdownunit7 = creg_calendergrid.monthmarkdownrows[2].months[0]
    assert monthmarkdownunit7.label == "September"
    assert monthmarkdownunit7.cumulative_days == 214
    assert monthmarkdownunit7.month_days_int == 30
    assert monthmarkdownunit7.week_length == 7
    assert monthmarkdownunit7.monthday_distortion == 1
    assert monthmarkdownunit7.weekday_2char_abvs == x_weekday_2char_abvs
    assert monthmarkdownunit7.first_weekday == 3
    assert monthmarkdownunit7.year == yr1997_int
    assert not monthmarkdownunit7.offset_year
    monthmarkdownunit11 = creg_calendergrid.monthmarkdownrows[3].months[1]
    assert monthmarkdownunit11.label == "January"
    assert monthmarkdownunit11.year == yr1997_int
    assert monthmarkdownunit11.offset_year
    # assert monthmarkdownunit7.first_weekday == 4


def test_CalendarMarkDown_create_markdown_ReturnsObj_Scernario0_creg_config():
    # ESTABLISH
    creg_config = get_default_timeline_config_dict()
    creg_calendergrid = CalendarMarkDown(timeline_config=creg_config)
    creg_calendergrid.display_init_day = "Monday"
    year_int = 2024

    # WHEN
    cal_markdown = creg_calendergrid.create_markdown(year_int)

    # THEN
    print(cal_markdown)
    expected_calendar_markdown = """
                               Year 2024                                

       March                     April                      May         
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
             1  2  3       1  2  3  4  5  6  7             1  2  3  4  5
 4  5  6  7  8  9 10       8  9 10 11 12 13 14       6  7  8  9 10 11 12
11 12 13 14 15 16 17      15 16 17 18 19 20 21      13 14 15 16 17 18 19
18 19 20 21 22 23 24      22 23 24 25 26 27 28      20 21 22 23 24 25 26
25 26 27 28 29 30 31      29 30                     27 28 29 30 31      

        June                      July                     August       
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                1  2       1  2  3  4  5  6  7                1  2  3  4
 3  4  5  6  7  8  9       8  9 10 11 12 13 14       5  6  7  8  9 10 11
10 11 12 13 14 15 16      15 16 17 18 19 20 21      12 13 14 15 16 17 18
17 18 19 20 21 22 23      22 23 24 25 26 27 28      19 20 21 22 23 24 25
24 25 26 27 28 29 30      29 30 31                  26 27 28 29 30 31   

     September                  October                   November      
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1          1  2  3  4  5  6                   1  2  3
 2  3  4  5  6  7  8       7  8  9 10 11 12 13       4  5  6  7  8  9 10
 9 10 11 12 13 14 15      14 15 16 17 18 19 20      11 12 13 14 15 16 17
16 17 18 19 20 21 22      21 22 23 24 25 26 27      18 19 20 21 22 23 24
23 24 25 26 27 28 29      28 29 30 31               25 26 27 28 29 30   
30                                                                      

      December               January (2025)           February (2025)   
Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su      Mo Tu We Th Fr Sa Su
                   1             1  2  3  4  5                      1  2
 2  3  4  5  6  7  8       6  7  8  9 10 11 12       3  4  5  6  7  8  9
 9 10 11 12 13 14 15      13 14 15 16 17 18 19      10 11 12 13 14 15 16
16 17 18 19 20 21 22      20 21 22 23 24 25 26      17 18 19 20 21 22 23
23 24 25 26 27 28 29      27 28 29 30 31            24 25 26 27 28      
30 31                                                                   """
    assert cal_markdown == expected_calendar_markdown


def test_CalendarMarkDown_create_markdown_ReturnsObj_Scernario1_five_config():
    # ESTABLISH
    five_calendergrid = CalendarMarkDown(timeline_config=get_five_config())
    five_calendergrid.display_init_day = "Anaday"
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
