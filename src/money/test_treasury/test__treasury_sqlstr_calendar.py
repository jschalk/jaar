from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src.money.treasury_sqlstr import (
    get_calendar_table_create_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
    CalendarAgendaUnit,
    CalendarReport,
)
from src._instrument.sqlite import sqlite_bool


def test_get_calendar_table_create_sqlstr_ReturnsCorrectStr():
    # GIVEN / WHEN
    generated_sqlstr = get_calendar_table_create_sqlstr()

    # THEN
    example_sqlstr = """
CREATE TABLE IF NOT EXISTS calendar (
  owner_id VARCHAR(255) NOT NULL
, report_time_road VARCHAR(10000) NOT NULL
, report_date_range_start INT NOT NULL
, report_date_range_cease INT NOT NULL
, report_interval_length INT NOT NULL
, report_interval_agenda_task_max_count INT NOT NULL
, report_interval_agenda_state_max_count INT NOT NULL
, time_begin INT NOT NULL
, time_close INT NOT NULL
, agenda_idea_road VARCHAR(255) NOT NULL
, agenda_weight INT NOT NULL
, task INT NOT NULL
, FOREIGN KEY(owner_id) REFERENCES worldunit(owner_id)
)
;
"""
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_insert_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_text = "Bob"
    time_road = create_road(root_label(), "time")
    jaja_road = create_road(time_road, "jajatime")
    x_date_range_start = 1000000600
    x_interval_count = 20
    x_interval_length = 15
    x_agenda_max_count_task = 11
    x_agenda_max_count_state = 7
    x_time_begin = 1000000615
    x_time_close = 1000000630
    casa_road = create_road(root_label(), "casa")
    clean_road = create_road(casa_road, "cleaning")
    fridge_road = create_road(clean_road, "clean fridge")
    x_agenda_weight = 0.5
    x_task = True
    x_calendarreport = CalendarReport(
        owner_id=bob_text,
        time_road=jaja_road,
        date_range_start=x_date_range_start,
        interval_count=x_interval_count,
        interval_length=x_interval_length,
        agenda_max_count_task=x_agenda_max_count_task,
        agenda_max_count_state=x_agenda_max_count_state,
    )

    # WHEN
    bob_calendaragendaunit = CalendarAgendaUnit(
        calendarreport=x_calendarreport,
        time_begin=x_time_begin,
        time_close=x_time_close,
        agenda_idea_road=fridge_road,
        agenda_weight=x_agenda_weight,
        task=x_task,
    )

    # WHEN
    generated_sqlstr = get_calendar_table_insert_sqlstr(bob_calendaragendaunit)

    # THEN
    example_sqlstr = f"""
INSERT INTO calendar (
  owner_id
, report_time_road
, report_date_range_start
, report_date_range_cease
, report_interval_length
, report_interval_agenda_task_max_count
, report_interval_agenda_state_max_count
, time_begin
, time_close
, agenda_idea_road
, agenda_weight
, task)
VALUES (
  '{bob_text}'
, '{jaja_road}'
, {x_date_range_start}
, {x_calendarreport.get_date_range_cease()}
, {x_interval_length}
, {x_agenda_max_count_task}
, {x_agenda_max_count_state}
, {x_time_begin}
, {x_time_close}
, '{fridge_road}'
, {x_agenda_weight}
, {sqlite_bool(x_task)}
)
;
"""
    print(f"{example_sqlstr=}")
    assert generated_sqlstr == example_sqlstr


def test_get_calendar_table_delete_sqlstr_ReturnsCorrectStr():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    generated_sqlstr = get_calendar_table_delete_sqlstr(bob_text)

    # THEN
    example_sqlstr = f"""
DELETE FROM calendar
WHERE owner_id = '{bob_text}' 
;
"""
    assert generated_sqlstr == example_sqlstr