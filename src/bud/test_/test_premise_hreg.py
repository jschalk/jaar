from src.bud.hreg_time import PremiseUnitHregTime
from pytest import raises as pytest_raises


def test_PremiseUnitHregTime_attributesSet_x_weeks():
    # ESTABLISH
    wu = PremiseUnitHregTime()
    wu._every_x_days = 4
    wu._every_x_months = 2
    wu._every_x_years = 7
    assert wu._every_x_days == 4
    assert wu._every_x_months == 2
    assert wu._every_x_years == 7

    # WHEN
    wu.set_weekly_event(
        every_x_weeks=1,
        remainder_weeks=0,
        weekday="Monday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )

    # THEN
    assert wu._every_x_weeks == 1
    assert wu._x_week_remainder == 0
    assert wu._weekday == "Monday"
    assert wu._start_hr == 0
    assert wu._start_minute == 0
    assert wu._event_minutes == 0

    assert wu._every_x_days is None
    assert wu._every_x_months is None
    assert wu._every_x_years is None


def test_PremiseUnitHregTime_attributesSet_x_weeksGetsException_remainder_weeks_TooBig():
    # ESTABLISH
    wu = PremiseUnitHregTime()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        wu.set_weekly_event(
            every_x_weeks=1,
            remainder_weeks=1,
            weekday="Monday",
            start_hr=0,
            start_minute=0,
            event_minutes=0,
        )
    assert (
        str(excinfo.value)
        == "It is mandatory that remainder_weeks is at least 1 less than every_x_weeks"
    )


def test_PremiseUnitHregTime_attributesSet_x_weeksGetsException_remainder_weeks_LessThanZero():
    # ESTABLISH
    wu = PremiseUnitHregTime()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        wu.set_weekly_event(
            every_x_weeks=1,
            remainder_weeks=-1,
            weekday="Monday",
            start_hr=0,
            start_minute=0,
            event_minutes=0,
        )
    assert str(excinfo.value) == "It is mandatory that remainder_weeks >= 0"


def test_PremiseUnitHregTime_attributesSet_weekday1():
    # ESTABLISH
    wu = PremiseUnitHregTime()
    # WHEN
    wu._set_weekday(weekday="Sunday")
    # THEN
    assert wu._weekday == "Sunday"


def test_PremiseUnitHregTime_attributesSet_start_hr1():
    # ESTABLISH
    wu = PremiseUnitHregTime()
    # WHEN
    wu._set_start_hr(1)
    # THEN
    assert wu._start_hr == 1


def test_PremiseUnitHregTime_attributesSet_weekdayInvalid():
    # ESTABLISH
    wu = PremiseUnitHregTime()
    # WHEN
    wu._set_weekday(weekday="FUNFUN")
    # THEN
    assert wu._weekday is None


def test_PremiseUnitHregTime_attributesGet_1week1stDay():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=1,
        remainder_weeks=0,
        weekday="Saturday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 10080
    assert wu.jajatime_open == 0
    assert wu.jajatime_nigh == 0


def test_PremiseUnitHregTime_attributesGet_1week2ndDay():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=1,
        remainder_weeks=0,
        weekday="Sunday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 10080
    assert wu.jajatime_open == 1440
    assert wu.jajatime_nigh == 1440


def test_PremiseUnitHregTime_attributesGet_2weeks0remainder3rdday():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=2,
        remainder_weeks=0,
        weekday="Monday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 20160
    assert wu.jajatime_open == 2880
    assert wu.jajatime_nigh == 2880


def test_PremiseUnitHregTime_attributesGet_2weeks1remainder1stday():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=2,
        remainder_weeks=1,
        weekday="Saturday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 20160
    assert wu.jajatime_open == 10080
    assert wu.jajatime_nigh == 10080


def test_PremiseUnitHregTime_attributesGet_2weeks1remainder4thday():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=2,
        remainder_weeks=1,
        weekday="Tuesday",
        start_hr=0,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 20160
    assert wu.jajatime_open == 14400
    assert wu.jajatime_nigh == 14400


def test_PremiseUnitHregTime_attributesGet_2weeks1remainder4thday7am():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=2,
        remainder_weeks=1,
        weekday="Tuesday",
        start_hr=7,
        start_minute=0,
        event_minutes=0,
    )
    assert wu.jajatime_divisor == 20160
    assert wu.jajatime_open == 14820
    assert wu.jajatime_nigh == 14820


def test_PremiseUnitHregTime_attributesGet3weeks1remainder1stDay():
    wu = PremiseUnitHregTime()
    wu.set_weekly_event(
        every_x_weeks=3,
        remainder_weeks=2,
        weekday="Monday",
        start_hr=8,
        start_minute=7,
        event_minutes=13,
    )
    assert wu.jajatime_divisor == 30240
    assert wu.jajatime_open == 23527
    assert wu.jajatime_nigh == 23540
