from src.ch14_epoch.epoch_main import get_first_weekday_index_of_year
from src.ch14_epoch.test._util.ch14_examples import get_creg_config, get_five_config
from src.ref.keywords import Ch14Keywords as kw


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario0_creg_epoch_config():
    # ESTABLISH
    weekdays_config = get_creg_config().get(kw.weekdays_config)
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

    assert weekdays_config[x2000_index] == kw.Wednesday
    assert weekdays_config[x2001_index] == kw.Thursday
    assert weekdays_config[x2002_index] == kw.Friday
    assert weekdays_config[x2003_index] == kw.Saturday
    assert weekdays_config[x2004_index] == kw.Monday


def test_get_first_weekday_index_of_year_ReturnsObj_Scenario1_five_epoch_config():
    # ESTABLISH
    weekdays_config = get_five_config().get(kw.weekdays_config)
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

    assert weekdays_config[x2000_index] == kw.Anaday
    assert weekdays_config[x2001_index] == kw.Anaday
    assert weekdays_config[x2002_index] == kw.Anaday
    assert weekdays_config[x2003_index] == kw.Anaday
    assert weekdays_config[x2004_index] == kw.Baileyday
