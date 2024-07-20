from src._road.road import create_road, RoadUnit, RoadNode
from dataclasses import dataclass
from datetime import datetime


class InvalidPremiseUnitException(Exception):
    pass


@dataclass
class PremiseUnitHregTime:
    _weekday: str = None
    _every_x_days: int = None  # builds jajatime(minute)
    _every_x_months: int = None  # builds mybud,time,months
    _on_x_monthday: int = None  # " build mybud,time,month,monthday
    _every_x_years: int = None  # builds mybud,time,years
    _every_x_weeks: int = None  # builds jajatime(minute)
    _x_week_remainder: int = None
    _between_hr_min_open: int = None  # clock and y o'clock" build jajatime(minutes)
    _between_hr_min_nigh: int = None  # clock and y o'clock" build jajatime(minutes)
    _between_weekday_open: int = None  # and y weekday" build jajatime(minutes)
    _every_x_day: int = None  # of the year"
    _start_hr: int = None
    _start_minute: int = None
    _event_minutes: int = None

    def set_weekly_event(
        self,
        every_x_weeks: int,
        remainder_weeks: int,
        weekday: str,
        start_hr: int,
        start_minute: int,
        event_minutes: int,
    ):
        if every_x_weeks <= remainder_weeks:
            raise InvalidPremiseUnitException(
                "It is mandatory that remainder_weeks is at least 1 less than every_x_weeks"
            )

        self._set_every_x_weeks(every_x_weeks)
        self.set_x_remainder_weeks(remainder_weeks)
        self._set_start_hr(start_hr)
        self._set_start_minute(start_minute)
        self._set_event_minutes(event_minutes)
        self._set_weekday(weekday)
        self._clear_every_x_days()
        self._clear_every_x_months()
        self._clear_every_x_years()

    def set_days_event(
        self,
        every_x_days: int,
        remainder_days: int,
        start_hr: int,
        start_minute: int,
        event_minutes: int,
    ):
        if every_x_days <= remainder_days:
            raise InvalidPremiseUnitException(
                "It is mandatory that remainder_weeks is at least 1 less than every_x_weeks"
            )

        self._set_every_x_days(every_x_days)
        self.set_x_remainder_days(remainder_days)
        self._set_start_hr(start_hr)
        self._set_start_minute(start_minute)
        self._set_event_minutes(event_minutes)
        self._clear_every_x_weeks()
        self._clear_every_x_months()
        self._clear_every_x_years()

    def set_x_remainder_weeks(self, remainder_weeks: int):
        if remainder_weeks < 0:
            raise InvalidPremiseUnitException(
                "It is mandatory that remainder_weeks >= 0"
            )
        self._x_week_remainder = remainder_weeks

    def set_x_remainder_days(self, remainder_days: int):
        if remainder_days < 0:
            raise InvalidPremiseUnitException(
                "It is mandatory that remainder_weeks >= 0"
            )
        self._x_days_remainder = remainder_days

    def _set_every_x_days(self, every_x_days: int):
        self._every_x_days = every_x_days

    def _set_every_x_weeks(
        self,
        every_x_weeks: int,
    ):
        self._every_x_weeks = every_x_weeks

    def _clear_every_x_weeks(self):
        self._every_x_weeks = None

    def _clear_every_x_days(self):
        self._every_x_days = None

    def _clear_every_x_months(self):
        self._every_x_months = None

    def _clear_every_x_years(self):
        self._every_x_years = None

    def _set_start_hr(self, start_hr):
        self._start_hr = start_hr

    def _set_start_minute(self, start_minute):
        self._start_minute = start_minute

    def _set_event_minutes(self, event_minutes):
        self._event_minutes = event_minutes

    def _set_weekday(self, weekday: str):
        if weekday in {
            get_Sun(),
            get_Mon(),
            get_Tue(),
            get_Wed(),
            get_Thu(),
            get_Fri(),
            get_Sat(),
        }:
            self._weekday = weekday
            self._set_open_weekday()

    def _set_open_weekday(self):
        b = None
        m = 1440
        if self._weekday == get_Sun():
            b = 1 * m
        elif self._weekday == get_Mon():
            b = 2 * m
        elif self._weekday == get_Tue():
            b = 3 * m
        elif self._weekday == get_Wed():
            b = 4 * m
        elif self._weekday == get_Thu():
            b = 5 * m
        elif self._weekday == get_Fri():
            b = 6 * m
        elif self._weekday == get_Sat():
            b = 0 * m

        self._between_weekday_open = b

    def get_jajatime_open(self):
        x_open = None
        if self._every_x_weeks is not None and self._x_week_remainder is not None:
            x_open = (
                (self._x_week_remainder * 10080)
                + (self._start_hr * 60)
                + (self._start_minute)
            )
            self._set_open_weekday()
            x_open += self._between_weekday_open
        elif self._every_x_days is not None and self._x_days_remainder is not None:
            x_open = (
                (self._x_days_remainder * 1440)
                + (self._start_hr * 60)
                + (self._start_minute)
            )

        return x_open

    @property
    def jajatime_divisor(self):
        if self._every_x_weeks is not None and self._x_week_remainder is not None:
            return self._every_x_weeks * 10080
        elif self._every_x_days is not None and self._x_days_remainder is not None:
            return self._every_x_days * 1440

    @property
    def jajatime_open(self):
        return self.get_jajatime_open()

    @property
    def jajatime_nigh(self):
        return self.get_jajatime_open() + self._event_minutes


def get_Sun():
    return "Sunday"


def get_Mon():
    return "Monday"


def get_Tue():
    return "Tuesday"


def get_Wed():
    return "Wednesday"


def get_Thu():
    return "Thursday"


def get_Fri():
    return "Friday"


def get_Sat():
    return "Saturday"


def get_time_min_from_dt(dt: datetime) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + 527040
