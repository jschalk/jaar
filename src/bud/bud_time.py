from src._road.road import RoadUnit
from src.bud.idea import ideaunit_shop
from src.bud.bud import BudUnit
from datetime import datetime
from dataclasses import dataclass


def get_time_min_from_dt(dt: datetime) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + 440640


def add_time_hreg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    time_road = x_budunit.make_l1_road(time_str())
    x_budunit.set_l1_idea(ideaunit_shop(time_str()))
    jaja_road = _add_jajatime_ideaunit(x_budunit, time_road)
    day_road = _add_day_ideaunits(x_budunit, jaja_road)
    hour_road = _add_hour_ideaunits(x_budunit, day_road)
    week_road = _add_week_ideaunits(x_budunit, jaja_road)
    year_road = _add_c400_leap_idea(x_budunit, jaja_road)
    add_month_ideaunits(x_budunit, year_road)
    return x_budunit


def c400_leap_num():
    return 210379680


def c400_clean_num():
    return 210378240


def c100_num():
    return 52594560


def yr4_leap_num():
    return 2103840


def yr4_clean_num():
    return 2102400


def year_num():
    return 525600


def day_num():
    return 1440


def jajatime_begin():
    return 0


def jajatime_close():
    return c400_leap_num() * 7


# def jan_begin(): return 437760
# def feb_begin(): return 480960
# def mar_begin(): return 0
# def apr_begin(): return 44640
# def may_begin(): return 84960
# def jun_begin(): return 129600
# def jul_begin(): return 172800
# def aug_begin(): return 217440
# def sep_begin(): return 260640
# def oct_begin(): return 305280
# def nov_begin(): return 349920
# def dec_begin(): return 393120
# def jan_close(): return 480960
# def feb_close(): return 525600
# def mar_close(): return 44640
# def apr_close(): return 84960
# def may_close(): return 129600
# def jun_close(): return 172800
# def jul_close(): return 217440
# def aug_close(): return 260640
# def sep_close(): return 305280
# def oct_close(): return 349920
# def nov_close(): return 393120
# def dec_close(): return 437760
def jan_begin():
    return 437760


def feb_begin():
    return 480960


def mar_begin():
    return 0


def apr_begin():
    return 44640


def may_begin():
    return 84960


def jun_begin():
    return 129600


def jul_begin():
    return 172800


def aug_begin():
    return 217440


def sep_begin():
    return 260640


def oct_begin():
    return 305280


def nov_begin():
    return 349920


def dec_begin():
    return 393120


def jan_close():
    return 480960


def feb_close():
    return 525600


def mar_close():
    return 44640


def apr_close():
    return 84960


def may_close():
    return 129600


def jun_close():
    return 172800


def jul_close():
    return 217440


def aug_close():
    return 260640


def sep_close():
    return 305280


def oct_close():
    return 349920


def nov_close():
    return 393120


def dec_close():
    return 437760


def week_begin():
    return 0


def week_close():
    return 7 * day_num()


# def sun_begin(): return 1440
# def mon_begin(): return 2880
# def tue_begin(): return 4320
# def wed_begin(): return 5760
# def thu_begin(): return 7200
# def fri_begin(): return 8640
# def sat_begin(): return 0
# def sun_close(): return sun_begin() + 1440
# def mon_close(): return mon_begin() + 1440
# def tue_close(): return tue_begin() + 1440
# def wed_close(): return wed_begin() + 1440
# def thu_close(): return thu_begin() + 1440
# def fri_close(): return fri_begin() + 1440
# def sat_close(): return sat_begin() + 1440


def jaja_week_dict() -> dict[dict, int]:
    return {
        get_sun(): 5760,
        get_mon(): 7200,
        get_tue(): 8640,
        get_wed(): 0,
        get_thu(): 1440,
        get_fri(): 2880,
        get_sat(): 4320,
    }


def sun_begin():
    return jaja_week_dict().get(get_sun())


def mon_begin():
    return jaja_week_dict().get(get_mon())


def tue_begin():
    return jaja_week_dict().get(get_tue())


def wed_begin():
    return jaja_week_dict().get(get_wed())


def thu_begin():
    return jaja_week_dict().get(get_thu())


def fri_begin():
    return jaja_week_dict().get(get_fri())


def sat_begin():
    return jaja_week_dict().get(get_sat())


def sun_close():
    return sun_begin() + day_num()


def mon_close():
    return mon_begin() + day_num()


def tue_close():
    return tue_begin() + day_num()


def wed_close():
    return wed_begin() + day_num()


def thu_close():
    return thu_begin() + day_num()


def fri_close():
    return fri_begin() + day_num()


def sat_close():
    return sat_begin() + day_num()


def _add_jajatime_ideaunit(x_budunit: BudUnit, time_road: RoadUnit) -> RoadUnit:
    jaja_idea = ideaunit_shop(
        get_jajatime_text(), _begin=jajatime_begin(), _close=jajatime_close()
    )
    jaja_road = x_budunit.make_road(time_road, get_jajatime_text())
    x_budunit.set_idea(jaja_idea, time_road)
    return jaja_road


def _add_day_ideaunits(x_budunit: BudUnit, jaja_road: RoadUnit):
    day_idea = ideaunit_shop(day_str(), _denom=day_num(), _morph=True)
    day_road = x_budunit.make_road(jaja_road, day_str())
    day_idea._gogo_want = 0
    day_idea._stop_want = day_num()
    x_budunit.set_idea(day_idea, jaja_road)
    x_budunit.set_idea(ideaunit_shop(days_str(), _denom=day_num()), jaja_road)
    return day_road


def _add_hour_ideaunits(x_budunit: BudUnit, day_road) -> RoadUnit:
    print(f"{day_road=}")
    hr_00_idea = ideaunit_shop(hr_00_str(), _gogo_want=0, _stop_want=60)
    hr_01_idea = ideaunit_shop(hr_01_str(), _gogo_want=60, _stop_want=120)
    hr_02_idea = ideaunit_shop(hr_02_str(), _gogo_want=120, _stop_want=180)
    hr_03_idea = ideaunit_shop(hr_03_str(), _gogo_want=180, _stop_want=240)
    hr_04_idea = ideaunit_shop(hr_04_str(), _gogo_want=240, _stop_want=300)
    hr_05_idea = ideaunit_shop(hr_05_str(), _gogo_want=300, _stop_want=360)
    hr_06_idea = ideaunit_shop(hr_06_str(), _gogo_want=360, _stop_want=420)
    hr_07_idea = ideaunit_shop(hr_07_str(), _gogo_want=420, _stop_want=480)
    hr_08_idea = ideaunit_shop(hr_08_str(), _gogo_want=480, _stop_want=540)
    hr_09_idea = ideaunit_shop(hr_09_str(), _gogo_want=540, _stop_want=600)
    hr_10_idea = ideaunit_shop(hr_10_str(), _gogo_want=600, _stop_want=660)
    hr_11_idea = ideaunit_shop(hr_11_str(), _gogo_want=660, _stop_want=720)
    hr_12_idea = ideaunit_shop(hr_12_str(), _gogo_want=720, _stop_want=780)
    hr_13_idea = ideaunit_shop(hr_13_str(), _gogo_want=780, _stop_want=840)
    hr_14_idea = ideaunit_shop(hr_14_str(), _gogo_want=840, _stop_want=900)
    hr_15_idea = ideaunit_shop(hr_15_str(), _gogo_want=900, _stop_want=960)
    hr_16_idea = ideaunit_shop(hr_16_str(), _gogo_want=960, _stop_want=1020)
    hr_17_idea = ideaunit_shop(hr_17_str(), _gogo_want=1020, _stop_want=1080)
    hr_18_idea = ideaunit_shop(hr_18_str(), _gogo_want=1080, _stop_want=1140)
    hr_19_idea = ideaunit_shop(hr_19_str(), _gogo_want=1140, _stop_want=1200)
    hr_20_idea = ideaunit_shop(hr_20_str(), _gogo_want=1200, _stop_want=1260)
    hr_21_idea = ideaunit_shop(hr_21_str(), _gogo_want=1260, _stop_want=1320)
    hr_22_idea = ideaunit_shop(hr_22_str(), _gogo_want=1320, _stop_want=1380)
    hr_23_idea = ideaunit_shop(hr_23_str(), _gogo_want=1380, _stop_want=1440)

    x_budunit.set_idea(hr_00_idea, day_road)
    x_budunit.set_idea(hr_01_idea, day_road)
    x_budunit.set_idea(hr_02_idea, day_road)
    x_budunit.set_idea(hr_03_idea, day_road)
    x_budunit.set_idea(hr_04_idea, day_road)
    x_budunit.set_idea(hr_05_idea, day_road)
    x_budunit.set_idea(hr_06_idea, day_road)
    x_budunit.set_idea(hr_07_idea, day_road)
    x_budunit.set_idea(hr_08_idea, day_road)
    x_budunit.set_idea(hr_09_idea, day_road)
    x_budunit.set_idea(hr_10_idea, day_road)
    x_budunit.set_idea(hr_11_idea, day_road)
    x_budunit.set_idea(hr_12_idea, day_road)
    x_budunit.set_idea(hr_13_idea, day_road)
    x_budunit.set_idea(hr_14_idea, day_road)
    x_budunit.set_idea(hr_15_idea, day_road)
    x_budunit.set_idea(hr_16_idea, day_road)
    x_budunit.set_idea(hr_17_idea, day_road)
    x_budunit.set_idea(hr_18_idea, day_road)
    x_budunit.set_idea(hr_19_idea, day_road)
    x_budunit.set_idea(hr_20_idea, day_road)
    x_budunit.set_idea(hr_21_idea, day_road)
    x_budunit.set_idea(hr_22_idea, day_road)
    x_budunit.set_idea(hr_23_idea, day_road)

    hour_idea = ideaunit_shop(hour_str(), _denom=60, _morph=True)
    hour_road = x_budunit.make_road(day_road, hour_str())
    x_budunit.set_idea(hour_idea, day_road)
    return hour_road


def _add_week_ideaunits(x_budunit: BudUnit, jaja_road: RoadUnit) -> RoadUnit:
    week_road = x_budunit.make_road(jaja_road, week_str())
    week_idea = ideaunit_shop(week_str(), _denom=10080, _morph=True)
    x_budunit.set_idea(week_idea, jaja_road)
    for x_key, x_value in jaja_week_dict().items():
        stop_value = x_value + day_num()
        x_idea = ideaunit_shop(x_key, _gogo_want=x_value, _stop_want=stop_value)
        x_budunit.set_idea(x_idea, week_road)
    x_budunit.set_idea(ideaunit_shop(weeks_str(), _denom=10080), jaja_road)
    x_budunit.set_idea(week_idea, jaja_road)
    return x_budunit


def _add_c400_leap_idea(x_budunit: BudUnit, time_range_root_road: RoadUnit):
    c400_leap_road = x_budunit.make_road(time_range_root_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    year_road = x_budunit.make_road(yr4_clean_road, year_str())
    c400_leap_idea = ideaunit_shop(c400_leap_str(), _denom=c400_leap_num(), _morph=True)
    c400_clean_idea = ideaunit_shop(
        c400_clean_str(), _denom=c400_clean_num(), _morph=True
    )
    c100_idea = ideaunit_shop(c100_str(), _denom=c100_num(), _morph=True)
    yr4_leap_idea = ideaunit_shop(yr4_leap_str(), _denom=yr4_leap_num(), _morph=True)
    yr4_clean_idea = ideaunit_shop(yr4_clean_str(), _denom=yr4_clean_num(), _morph=True)
    year_idea = ideaunit_shop(year_str(), _denom=year_num(), _morph=True)
    x_budunit.set_idea(c400_leap_idea, time_range_root_road)
    x_budunit.set_idea(c400_clean_idea, c400_leap_road)
    x_budunit.set_idea(c100_idea, c400_clean_road)
    x_budunit.set_idea(yr4_leap_idea, c100_road)
    x_budunit.set_idea(yr4_clean_idea, yr4_leap_road)
    x_budunit.set_idea(year_idea, yr4_clean_road)
    return year_road


def add_month_ideaunits(x_budunit: BudUnit, year_road: RoadUnit):
    jan_idea = ideaunit_shop(jan_str(), _gogo_want=jan_begin(), _stop_want=jan_close())
    feb_idea = ideaunit_shop(feb_str(), _gogo_want=feb_begin(), _stop_want=feb_close())
    mar_idea = ideaunit_shop(mar_str(), _gogo_want=mar_begin(), _stop_want=mar_close())
    apr_idea = ideaunit_shop(apr_str(), _gogo_want=apr_begin(), _stop_want=apr_close())
    may_idea = ideaunit_shop(may_str(), _gogo_want=may_begin(), _stop_want=may_close())
    jun_idea = ideaunit_shop(jun_str(), _gogo_want=jun_begin(), _stop_want=jun_close())
    jul_idea = ideaunit_shop(jul_str(), _gogo_want=jul_begin(), _stop_want=jul_close())
    aug_idea = ideaunit_shop(aug_str(), _gogo_want=aug_begin(), _stop_want=aug_close())
    sep_idea = ideaunit_shop(sep_str(), _gogo_want=sep_begin(), _stop_want=sep_close())
    oct_idea = ideaunit_shop(oct_str(), _gogo_want=oct_begin(), _stop_want=oct_close())
    nov_idea = ideaunit_shop(nov_str(), _gogo_want=nov_begin(), _stop_want=nov_close())
    dec_idea = ideaunit_shop(dec_str(), _gogo_want=dec_begin(), _stop_want=dec_close())

    x_budunit.set_idea(jan_idea, year_road)
    x_budunit.set_idea(feb_idea, year_road)
    x_budunit.set_idea(mar_idea, year_road)
    x_budunit.set_idea(apr_idea, year_road)
    x_budunit.set_idea(may_idea, year_road)
    x_budunit.set_idea(jun_idea, year_road)
    x_budunit.set_idea(jul_idea, year_road)
    x_budunit.set_idea(aug_idea, year_road)
    x_budunit.set_idea(sep_idea, year_road)
    x_budunit.set_idea(oct_idea, year_road)
    x_budunit.set_idea(nov_idea, year_road)
    x_budunit.set_idea(dec_idea, year_road)
    return x_budunit


def set_time_facts(
    x_budunit: BudUnit, open: datetime = None, nigh: datetime = None
) -> None:
    open_minutes = get_time_min_from_dt(dt=open) if open is not None else None
    nigh_minutes = get_time_min_from_dt(dt=nigh) if nigh is not None else None
    time_road = x_budunit.make_l1_road("time")
    minutes_fact = x_budunit.make_road(time_road, "jajatime")
    x_budunit.set_fact(
        base=minutes_fact,
        pick=minutes_fact,
        open=open_minutes,
        nigh=nigh_minutes,
    )


def year_str() -> str:
    return "year"


def years_str() -> str:
    return "years"


def time_str() -> str:
    return "time"


def min_str() -> str:
    return "minutes"


def get_jajatime_text():
    return "jajatime"


def get_sun():
    return "Sunday"


def get_mon():
    return "Monday"


def get_tue():
    return "Tuesday"


def get_wed():
    return "Wednesday"


def get_thu():
    return "Thursday"


def get_fri():
    return "Friday"


def get_sat():
    return "Saturday"


def c400_leap_str():
    return "c400_leap"


def c400_clean_str():
    return "c400_clean"


def c100_str():
    return "c100 years"


def yr4_leap_str():
    return "yr4_leap"


def yr4_clean_str():
    return "yr4_clean"


def get_year_road(x_budunit: BudUnit, time_range_root_road: RoadUnit) -> RoadUnit:
    c400_leap_road = x_budunit.make_road(time_range_root_road, c400_leap_str())
    c400_clean_road = x_budunit.make_road(c400_leap_road, c400_clean_str())
    c100_road = x_budunit.make_road(c400_clean_road, c100_str())
    yr4_leap_road = x_budunit.make_road(c100_road, yr4_leap_str())
    yr4_clean_road = x_budunit.make_road(yr4_leap_road, yr4_clean_str())
    return x_budunit.make_road(yr4_clean_road, year_str())


def week_str():
    return "week"


def weeks_str():
    return f"{week_str()}s"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def jan_str():
    return "jan"


def feb_str():
    return "feb"


def mar_str():
    return "mar"


def apr_str():
    return "apr"


def may_str():
    return "may"


def jun_str():
    return "jun"


def jul_str():
    return "jul"


def aug_str():
    return "aug"


def sep_str():
    return "sep"


def oct_str():
    return "oct"


def nov_str():
    return "nov"


def dec_str():
    return "dec"


def hour_str():
    return "hour"


def hr_00_str():
    return "0-12am"


def hr_01_str():
    return "1-1am"


def hr_02_str():
    return "2-2am"


def hr_03_str():
    return "3-3am"


def hr_04_str():
    return "4-4am"


def hr_05_str():
    return "5-5am"


def hr_06_str():
    return "6-6am"


def hr_07_str():
    return "7-7am"


def hr_08_str():
    return "8-8am"


def hr_09_str():
    return "9-9am"


def hr_10_str():
    return "10-10am"


def hr_11_str():
    return "11-11am"


def hr_12_str():
    return "12-12pm"


def hr_13_str():
    return "13-1pm"


def hr_14_str():
    return "14-2pm"


def hr_15_str():
    return "15-3pm"


def hr_16_str():
    return "16-4pm"


def hr_17_str():
    return "17-5pm"


def hr_18_str():
    return "18-6pm"


def hr_19_str():
    return "19-7pm"


def hr_20_str():
    return "20-8pm"


def hr_21_str():
    return "21-9pm"


def hr_22_str():
    return "22-10pm"


def hr_23_str():
    return "23-11pm"
