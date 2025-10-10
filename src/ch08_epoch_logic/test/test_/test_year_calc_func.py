from src.ch08_epoch_logic.epoch_main import get_first_weekday_index_of_year
from src.ch08_epoch_logic.test._util.ch08_examples import (
    get_creg_config,
    get_five_config,
)


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario0_creg_epoch_config():
    # ESTABLISH
    weekdays_config = get_creg_config().get("weekdays_config")
    print(f"{weekdays_config=}")
    week_length = len(weekdays_config)

    # WHEN
    x2000_index = get_first_weekday_index_of_year(week_length, 2000)
    x2001_index = get_first_weekday_index_of_year(week_length, 2001)
    x2002_index = get_first_weekday_index_of_year(week_length, 2002)
    x2003_index = get_first_weekday_index_of_year(week_length, 2003)
    x2004_index = get_first_weekday_index_of_year(week_length, 2004)

    # THEN
    print(f"{weekdays_config[x2000_index]=}")
    print(f"{weekdays_config[x2001_index]=}")
    print(f"{weekdays_config[x2002_index]=}")
    print(f"{weekdays_config[x2003_index]=}")
    print(f"{weekdays_config[x2004_index]=}")

    assert weekdays_config[x2000_index] == "Wednesday"
    assert weekdays_config[x2001_index] == "Thursday"
    assert weekdays_config[x2002_index] == "Friday"
    assert weekdays_config[x2003_index] == "Saturday"
    assert weekdays_config[x2004_index] == "Monday"


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario1_five_epoch_config():
    # ESTABLISH
    weekdays_config = get_five_config().get("weekdays_config")
    print(f"{weekdays_config=}")
    week_length = len(weekdays_config)

    # WHEN
    x2000_index = get_first_weekday_index_of_year(week_length, 2000)
    x2001_index = get_first_weekday_index_of_year(week_length, 2001)
    x2002_index = get_first_weekday_index_of_year(week_length, 2002)
    x2003_index = get_first_weekday_index_of_year(week_length, 2003)
    x2004_index = get_first_weekday_index_of_year(week_length, 2004)

    # THEN
    print(f"{weekdays_config[x2000_index]=}")
    print(f"{weekdays_config[x2001_index]=}")
    print(f"{weekdays_config[x2002_index]=}")
    print(f"{weekdays_config[x2003_index]=}")
    print(f"{weekdays_config[x2004_index]=}")

    assert weekdays_config[x2000_index] == "Anaday"
    assert weekdays_config[x2001_index] == "Anaday"
    assert weekdays_config[x2002_index] == "Anaday"
    assert weekdays_config[x2003_index] == "Anaday"
    assert weekdays_config[x2004_index] == "Baileyday"
