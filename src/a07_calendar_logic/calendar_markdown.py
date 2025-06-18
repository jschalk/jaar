from copy import copy as copy_copy
from dataclasses import dataclass
from src.a07_calendar_logic.chrono import TimeLineUnit, timelineunit_shop


def center_word(length, word):
    return word[:length] if len(word) > length else word.center(length)


@dataclass
class MonthGridUnit:
    name: str = None
    cumulative_days: str = None
    first_weekday: int = None
    week_length: int = None
    month_days_int: int = None
    monthday_distortion: int = None
    weekday_2char_abvs: list[str] = None
    max_monthday_rows: int = None

    def markdown_name(self) -> str:
        char_width = (self.week_length * 3) - 1
        return center_word(char_width, self.name)

    def markdown_weekdays(self) -> str:
        x_str = "".join(f"{abv} " for abv in self.weekday_2char_abvs)
        return x_str.rstrip()

    def markdown_day_numbers(self, row_int: int) -> str:
        starting_monthday = row_int * self.week_length
        starting_monthday = starting_monthday - self.first_weekday
        ending_monthday = starting_monthday + self.week_length
        x_str = ""
        for monthday in range(starting_monthday, ending_monthday):
            if monthday < 0 or monthday >= self.month_days_int:
                x_str += "   "
            else:
                display_monthday = monthday + self.monthday_distortion
                x_str += f"{display_monthday:2} "
        return x_str[:-1]

    def set_max_monthday_rows(self):
        row_int = 0
        while self.markdown_day_numbers(row_int).rstrip() != "":
            row_int += 1
        self.max_monthday_rows = row_int

    def get_next_month_first_weekday(self) -> int:
        right_days = self.month_days_int + self.first_weekday
        return right_days % self.week_length


@dataclass
class MonthGridRow:
    months: list[MonthGridUnit] = None
    max_monthday_numbers_row: int = None

    def set_max_monthday_numbers_row(self):
        x_max = 0
        for monthgridunit in self.months:
            monthgridunit.set_max_monthday_rows()
            if monthgridunit.max_monthday_rows > x_max:
                x_max = monthgridunit.max_monthday_rows
        self.max_monthday_numbers_row = x_max

    def markdown_str(self) -> str:
        x_str = "\n"
        for monthgridunit in self.months:
            x_str += f"{monthgridunit.markdown_name()}      "
        x_str = f"{x_str[:-6]}\n"
        for monthgridunit in self.months:
            x_str += f"{monthgridunit.markdown_weekdays()}      "
        x_str = f"{x_str[:-6]}\n"
        self.set_max_monthday_numbers_row()
        for row_int in range(self.max_monthday_numbers_row):
            for monthgridunit in self.months:
                x_str += f"{monthgridunit.markdown_day_numbers(row_int)}      "
            x_str = f"{x_str[:-6]}\n"
        return x_str[:-1]


@dataclass
class CalendarGrid:
    timeline_config: dict = None
    monthgridrows: list[MonthGridRow] = None
    timelineunit: TimeLineUnit = None
    week_length: int = None
    monthgridrow_length: int = None
    month_char_width: int = None
    max_md_width: int = 84  # default width
    display_md_width: int = None

    def create_2char_weekday_list(self, display_init_day: str) -> list[str]:
        orig_weekdays = copy_copy(self.timelineunit.weekdays_config)
        display_index = orig_weekdays.index(display_init_day)
        back_range = range(display_index, len(orig_weekdays))
        front_range = range(display_index)
        new_weekdays = [orig_weekdays[weekday_index] for weekday_index in back_range]
        new_weekdays.extend(orig_weekdays[wd_index] for wd_index in front_range)
        return [weekday[:2] for weekday in new_weekdays]

    def set_timelineunit(self, display_init_day: str, year_init_weekday: str):
        self.timelineunit = timelineunit_shop(self.timeline_config)
        self.week_length = len(self.timelineunit.weekdays_config)
        # set the expected month_char_width with 5 extra charcters for space
        self.month_char_width = (self.week_length * 3) + 5
        self.monthgridrow_length = int(self.max_md_width / self.month_char_width)
        # set the display_md_width to month_char_width * columns minus unnessary spaces on right
        # substract 6 spaces because intermediary distance is 5 and each month number has additional space
        self.display_md_width = self.monthgridrow_length * self.month_char_width - 6
        self.monthgridrows = []
        x_monthgridrow = MonthGridRow([])
        previous_cumulative_days = 0
        x_monthday_distortion = self.timelineunit.monthday_distortion
        x_weekday_2char_list = self.create_2char_weekday_list(display_init_day)
        year_init_2char = year_init_weekday[:2]
        month_first_weekday_index = x_weekday_2char_list.index(year_init_2char)

        for month_cumulative_list in self.timelineunit.months_config:
            month_str = month_cumulative_list[0]
            cumulative_days = month_cumulative_list[1]
            new_monthgridunit = MonthGridUnit(month_str, cumulative_days)
            new_monthgridunit.week_length = self.week_length
            new_monthgridunit.month_days_int = (
                cumulative_days - previous_cumulative_days
            )
            new_monthgridunit.monthday_distortion = x_monthday_distortion
            new_monthgridunit.weekday_2char_abvs = x_weekday_2char_list
            new_monthgridunit.first_weekday = month_first_weekday_index
            month_first_weekday_index = new_monthgridunit.get_next_month_first_weekday()
            previous_cumulative_days = cumulative_days
            # new_monthgridunit.week_length = self.week_length
            x_monthgridrow.months.append(new_monthgridunit)
            if len(x_monthgridrow.months) == self.monthgridrow_length:
                self.monthgridrows.append(x_monthgridrow)
                x_monthgridrow = MonthGridRow([])
        if len(x_monthgridrow.months) > 0:
            self.monthgridrows.append(x_monthgridrow)
            x_monthgridrow = MonthGridRow([])

    def create_markdown(self, year: int) -> str:
        markdown_str = f"""
{center_word(self.display_md_width, f"Year {year}")}
"""
        for monthgridrow in self.monthgridrows:
            markdown_str += monthgridrow.markdown_str()
            markdown_str += "\n"
        return markdown_str[:-1]
