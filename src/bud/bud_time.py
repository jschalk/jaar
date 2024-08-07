from src.bud.idea import ideaunit_shop as i_shop
from src.bud.bud import BudUnit
from datetime import datetime
from dataclasses import dataclass


def get_time_min_from_dt(dt: datetime) -> int:
    ce_src = datetime(1, 1, 1, 0, 0, 0, 0)
    min_time_difference = dt - ce_src
    return round(min_time_difference.total_seconds() / 60) + 527040


def add_time_hreg_ideaunit(x_budunit: BudUnit) -> BudUnit:
    time_road = x_budunit.make_l1_road(time_str())
    time_idea = i_shop(time_str())
    x_budunit.set_l1_idea(time_idea)

    # roads that need to be defined at the beginning:
    tech_road = x_budunit.make_road(time_road, tech_str())
    tech_c400_road = x_budunit.make_road(tech_road, c400_str())
    tech_day_road = x_budunit.make_road(tech_road, day_str())
    tech_week_road = x_budunit.make_road(tech_road, week_str())

    # jajatime_str branch
    jaja_road = x_budunit.make_road(time_road, get_jajatime_text())
    jaja_idea = i_shop(get_jajatime_text(), _begin=0, _close=1472657760)
    x_budunit.set_idea(jaja_idea, time_road)

    # years_road
    years_road = x_budunit.make_road(jaja_road, years_str())
    jaja_years_idea = i_shop(years_str(), _numor=1, _denom=1)
    x_budunit.set_idea(jaja_years_idea, jaja_road)
    yr2010_road = x_budunit.make_road(years_road, yr2010min_str())
    yr2011_road = x_budunit.make_road(years_road, yr2011min_str())
    yr2012_road = x_budunit.make_road(years_road, yr2012min_str())
    yr2013_road = x_budunit.make_road(years_road, yr2013min_str())
    yr2014_road = x_budunit.make_road(years_road, yr2014min_str())
    yr2015_road = x_budunit.make_road(years_road, yr2015min_str())
    yr2016_road = x_budunit.make_road(years_road, yr2016min_str())
    yr2017_road = x_budunit.make_road(years_road, yr2017min_str())
    yr2018_road = x_budunit.make_road(years_road, yr2018min_str())
    yr2019_road = x_budunit.make_road(years_road, yr2019min_str())
    yr2020_road = x_budunit.make_road(years_road, yr2020min_str())
    yr2021_road = x_budunit.make_road(years_road, yr2021min_str())
    yr2022_road = x_budunit.make_road(years_road, yr2022min_str())
    yr2023_road = x_budunit.make_road(years_road, yr2023min_str())
    yr2024_road = x_budunit.make_road(years_road, yr2024min_str())
    yr2025_road = x_budunit.make_road(years_road, yr2025min_str())
    yr2026_road = x_budunit.make_road(years_road, yr2026min_str())
    yr2027_road = x_budunit.make_road(years_road, yr2027min_str())
    yr2028_road = x_budunit.make_road(years_road, yr2028min_str())
    yr2029_road = x_budunit.make_road(years_road, yr2029min_str())
    yr2030_road = x_budunit.make_road(years_road, yr2030min_str())
    idea_2010 = i_shop(yr2010min_str(), _begin=1057158720, _close=1057684320)
    idea_2011 = i_shop(yr2011min_str(), _begin=1057684320, _close=1058209920)
    idea_2012 = i_shop(yr2012min_str(), _begin=1058209920, _close=1058736960)
    idea_2013 = i_shop(yr2013min_str(), _begin=1058736960, _close=1059262560)
    idea_2014 = i_shop(yr2014min_str(), _begin=1059262560, _close=1059788160)
    idea_2015 = i_shop(yr2015min_str(), _begin=1059788160, _close=1060313760)
    idea_2016 = i_shop(yr2016min_str(), _begin=1060313760, _close=1060840800)
    idea_2017 = i_shop(yr2017min_str(), _begin=1060840800, _close=1061366400)
    idea_2018 = i_shop(yr2018min_str(), _begin=1061366400, _close=1061892000)
    idea_2019 = i_shop(yr2019min_str(), _begin=1061892000, _close=1062417600)
    idea_2020 = i_shop(yr2020min_str(), _begin=1062417600, _close=1062944640)
    idea_2021 = i_shop(yr2021min_str(), _begin=1062944640, _close=1063470240)
    idea_2022 = i_shop(yr2022min_str(), _begin=1063470240, _close=1063995840)
    idea_2023 = i_shop(yr2023min_str(), _begin=1063995840, _close=1064521440)
    idea_2024 = i_shop(yr2024min_str(), _begin=1064521440, _close=1065048480)
    idea_2025 = i_shop(yr2025min_str(), _begin=1065048480, _close=1065574080)
    idea_2026 = i_shop(yr2026min_str(), _begin=1065574080, _close=1066099680)
    idea_2027 = i_shop(yr2027min_str(), _begin=1066099680, _close=1066625280)
    idea_2028 = i_shop(yr2028min_str(), _begin=1066625280, _close=1067152320)
    idea_2029 = i_shop(yr2029min_str(), _begin=1067152320, _close=1067677920)
    idea_2030 = i_shop(yr2030min_str(), _begin=1067677920, _close=1068203520)
    x_budunit.set_idea(idea_2010, years_road)
    x_budunit.set_idea(idea_2011, years_road)
    x_budunit.set_idea(idea_2012, years_road)
    x_budunit.set_idea(idea_2013, years_road)
    x_budunit.set_idea(idea_2014, years_road)
    x_budunit.set_idea(idea_2015, years_road)
    x_budunit.set_idea(idea_2016, years_road)
    x_budunit.set_idea(idea_2017, years_road)
    x_budunit.set_idea(idea_2018, years_road)
    x_budunit.set_idea(idea_2019, years_road)
    x_budunit.set_idea(idea_2020, years_road)
    x_budunit.set_idea(idea_2021, years_road)
    x_budunit.set_idea(idea_2022, years_road)
    x_budunit.set_idea(idea_2023, years_road)
    x_budunit.set_idea(idea_2024, years_road)
    x_budunit.set_idea(idea_2025, years_road)
    x_budunit.set_idea(idea_2026, years_road)
    x_budunit.set_idea(idea_2027, years_road)
    x_budunit.set_idea(idea_2028, years_road)
    x_budunit.set_idea(idea_2029, years_road)
    x_budunit.set_idea(idea_2030, years_road)

    # -1056058720
    morph_yr2010_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2011_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2012_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2013_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2014_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2015_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2016_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2017_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2018_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2019_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2020_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2021_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2022_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2023_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2024_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2025_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2026_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2027_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2028_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2029_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)
    morph_yr2030_idea = i_shop(morph_str(), _numor=1, _denom=525600, _reest=False)

    # x_budunit.set_idea(morph_yr2010_idea, yr2010_road)
    x_budunit.set_idea(morph_yr2010_idea, yr2010_road)
    x_budunit.set_idea(morph_yr2011_idea, yr2011_road)
    x_budunit.set_idea(morph_yr2012_idea, yr2012_road)
    x_budunit.set_idea(morph_yr2013_idea, yr2013_road)
    x_budunit.set_idea(morph_yr2014_idea, yr2014_road)
    x_budunit.set_idea(morph_yr2015_idea, yr2015_road)
    x_budunit.set_idea(morph_yr2016_idea, yr2016_road)
    x_budunit.set_idea(morph_yr2017_idea, yr2017_road)
    x_budunit.set_idea(morph_yr2018_idea, yr2018_road)
    x_budunit.set_idea(morph_yr2019_idea, yr2019_road)
    x_budunit.set_idea(morph_yr2020_idea, yr2020_road)
    x_budunit.set_idea(morph_yr2021_idea, yr2021_road)
    x_budunit.set_idea(morph_yr2022_idea, yr2022_road)
    x_budunit.set_idea(morph_yr2023_idea, yr2023_road)
    x_budunit.set_idea(morph_yr2024_idea, yr2024_road)
    x_budunit.set_idea(morph_yr2025_idea, yr2025_road)
    x_budunit.set_idea(morph_yr2026_idea, yr2026_road)
    x_budunit.set_idea(morph_yr2027_idea, yr2027_road)
    x_budunit.set_idea(morph_yr2028_idea, yr2028_road)
    x_budunit.set_idea(morph_yr2029_idea, yr2029_road)
    x_budunit.set_idea(morph_yr2030_idea, yr2030_road)
    yr2010mor_road = x_budunit.make_road(yr2010_road, morph_str())
    yr2011mor_road = x_budunit.make_road(yr2011_road, morph_str())
    yr2012mor_road = x_budunit.make_road(yr2012_road, morph_str())
    yr2013mor_road = x_budunit.make_road(yr2013_road, morph_str())
    yr2014mor_road = x_budunit.make_road(yr2014_road, morph_str())
    yr2015mor_road = x_budunit.make_road(yr2015_road, morph_str())
    yr2016mor_road = x_budunit.make_road(yr2016_road, morph_str())
    yr2017mor_road = x_budunit.make_road(yr2017_road, morph_str())
    yr2018mor_road = x_budunit.make_road(yr2018_road, morph_str())
    yr2019mor_road = x_budunit.make_road(yr2019_road, morph_str())
    yr2020mor_road = x_budunit.make_road(yr2020_road, morph_str())
    yr2021mor_road = x_budunit.make_road(yr2021_road, morph_str())
    yr2022mor_road = x_budunit.make_road(yr2022_road, morph_str())
    yr2023mor_road = x_budunit.make_road(yr2023_road, morph_str())
    yr2024mor_road = x_budunit.make_road(yr2024_road, morph_str())
    yr2025mor_road = x_budunit.make_road(yr2025_road, morph_str())
    yr2026mor_road = x_budunit.make_road(yr2026_road, morph_str())
    yr2027mor_road = x_budunit.make_road(yr2027_road, morph_str())
    yr2028mor_road = x_budunit.make_road(yr2028_road, morph_str())
    yr2029mor_road = x_budunit.make_road(yr2029_road, morph_str())
    yr2030mor_road = x_budunit.make_road(yr2030_road, morph_str())
    x_budunit.set_idea(i_shop(yr2010yr_str()), yr2010mor_road)
    x_budunit.set_idea(i_shop(yr2011yr_str()), yr2011mor_road)
    x_budunit.set_idea(i_shop(yr2012yr_str()), yr2012mor_road)
    x_budunit.set_idea(i_shop(yr2013yr_str()), yr2013mor_road)
    x_budunit.set_idea(i_shop(yr2014yr_str()), yr2014mor_road)
    x_budunit.set_idea(i_shop(yr2015yr_str()), yr2015mor_road)
    x_budunit.set_idea(i_shop(yr2016yr_str()), yr2016mor_road)
    x_budunit.set_idea(i_shop(yr2017yr_str()), yr2017mor_road)
    x_budunit.set_idea(i_shop(yr2018yr_str()), yr2018mor_road)
    x_budunit.set_idea(i_shop(yr2019yr_str()), yr2019mor_road)
    x_budunit.set_idea(i_shop(yr2020yr_str()), yr2020mor_road)
    x_budunit.set_idea(i_shop(yr2021yr_str()), yr2021mor_road)
    x_budunit.set_idea(i_shop(yr2022yr_str()), yr2022mor_road)
    x_budunit.set_idea(i_shop(yr2023yr_str()), yr2023mor_road)
    x_budunit.set_idea(i_shop(yr2024yr_str()), yr2024mor_road)
    x_budunit.set_idea(i_shop(yr2025yr_str()), yr2025mor_road)
    x_budunit.set_idea(i_shop(yr2026yr_str()), yr2026mor_road)
    x_budunit.set_idea(i_shop(yr2027yr_str()), yr2027mor_road)
    x_budunit.set_idea(i_shop(yr2028yr_str()), yr2028mor_road)
    x_budunit.set_idea(i_shop(yr2029yr_str()), yr2029mor_road)
    x_budunit.set_idea(i_shop(yr2030yr_str()), yr2030mor_road)

    jaja_c400_road = x_budunit.make_road(jaja_road, c400_str())
    jaja_c400_idea = i_shop(
        c400_str(),
        _numor=1,
        _denom=7,
        _reest=True,
        _range_source_road=tech_c400_road,
    )
    x_budunit.set_idea(jaja_c400_idea, jaja_road)
    jaja_c400s_idea = i_shop(
        c400s_str(),
        _numor=1,
        _denom=210379680,
        _reest=False,
        _range_source_road=tech_c400_road,
    )
    x_budunit.set_idea(jaja_c400s_idea, jaja_road)
    jaja_day_idea = i_shop(
        day_str(),
        _numor=1,
        _denom=1022679,
        _reest=True,
        _range_source_road=tech_day_road,
    )
    x_budunit.set_idea(jaja_day_idea, jaja_road)
    jaja_days_idea = i_shop(
        days_str(), _begin=0, _close=1022679, _numor=1, _denom=1440, _reest=False
    )
    x_budunit.set_idea(jaja_days_idea, jaja_road)
    jaja_week_road = x_budunit.make_road(jaja_road, week_str())
    jaja_week_idea = i_shop(
        week_str(),
        _numor=1,
        _denom=146097,
        _reest=True,
        _range_source_road=tech_week_road,
    )
    x_budunit.set_idea(jaja_week_idea, jaja_road)
    jaja_weeks_idea = i_shop(
        weeks_str(),
        _numor=1,
        _denom=10080,
        _reest=False,
    )
    x_budunit.set_idea(jaja_weeks_idea, jaja_road)

    # tech_road branch
    tech_idea = i_shop(tech_str())
    x_budunit.set_idea(tech_idea, time_road)

    # month_road branch
    month_road = x_budunit.make_road(tech_road, month_str())
    month_idea = i_shop(month_str())
    x_budunit.set_idea(month_idea, tech_road)
    Jan_ideaunit = i_shop(Jan(), _begin=0, _close=44640)
    Feb28_ideaunit = i_shop(Feb28(), _begin=0, _close=40320)
    Feb29_ideaunit = i_shop(Feb29(), _begin=0, _close=41760)
    Mar_ideaunit = i_shop(Mar(), _begin=0, _close=44640)
    Apr_ideaunit = i_shop(Apr(), _begin=0, _close=43200)
    May_ideaunit = i_shop(May(), _begin=0, _close=44640)
    Jun_ideaunit = i_shop(Jun(), _begin=0, _close=43200)
    Jul_ideaunit = i_shop(Jul(), _begin=0, _close=44640)
    Aug_ideaunit = i_shop(Aug(), _begin=0, _close=44640)
    Sep_ideaunit = i_shop(Sep(), _begin=0, _close=43200)
    Oct_ideaunit = i_shop(Oct(), _begin=0, _close=44640)
    Nov_ideaunit = i_shop(Nov(), _begin=0, _close=43200)
    Dec_ideaunit = i_shop(Dec(), _begin=0, _close=44640)
    x_budunit.set_idea(Jan_ideaunit, month_road)
    x_budunit.set_idea(Feb28_ideaunit, month_road)
    x_budunit.set_idea(Feb29_ideaunit, month_road)
    x_budunit.set_idea(Mar_ideaunit, month_road)
    x_budunit.set_idea(Apr_ideaunit, month_road)
    x_budunit.set_idea(May_ideaunit, month_road)
    x_budunit.set_idea(Jun_ideaunit, month_road)
    x_budunit.set_idea(Jul_ideaunit, month_road)
    x_budunit.set_idea(Aug_ideaunit, month_road)
    x_budunit.set_idea(Sep_ideaunit, month_road)
    x_budunit.set_idea(Oct_ideaunit, month_road)
    x_budunit.set_idea(Nov_ideaunit, month_road)
    x_budunit.set_idea(Dec_ideaunit, month_road)
    tech_Jan_road = x_budunit.make_road(month_road, Jan())
    tech_Feb28_road = x_budunit.make_road(month_road, Feb28())
    tech_Feb29_road = x_budunit.make_road(month_road, Feb29())
    tech_Mar_road = x_budunit.make_road(month_road, Mar())
    tech_Apr_road = x_budunit.make_road(month_road, Apr())
    tech_May_road = x_budunit.make_road(month_road, May())
    tech_Jun_road = x_budunit.make_road(month_road, Jun())
    tech_Jul_road = x_budunit.make_road(month_road, Jul())
    tech_Aug_road = x_budunit.make_road(month_road, Aug())
    tech_Sep_road = x_budunit.make_road(month_road, Sep())
    tech_Oct_road = x_budunit.make_road(month_road, Oct())
    tech_Nov_road = x_budunit.make_road(month_road, Nov())
    tech_Dec_road = x_budunit.make_road(month_road, Dec())
    Jan_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Feb28_days_idea = i_shop(
        days_str(), _begin=0, _close=28, _numor=1, _denom=1440, _reest=True
    )
    Feb29_days_idea = i_shop(
        days_str(), _begin=0, _close=29, _numor=1, _denom=1440, _reest=True
    )
    Mar_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Apr_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    May_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Jun_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Jul_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Aug_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Sep_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Oct_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Nov_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    Dec_days_idea = i_shop(
        days_str(), _begin=0, _close=30, _numor=1, _denom=1440, _reest=True
    )
    x_budunit.set_idea(Jan_days_idea, tech_Jan_road)
    x_budunit.set_idea(Feb28_days_idea, tech_Feb28_road)
    x_budunit.set_idea(Feb29_days_idea, tech_Feb29_road)
    x_budunit.set_idea(Mar_days_idea, tech_Mar_road)
    x_budunit.set_idea(Apr_days_idea, tech_Apr_road)
    x_budunit.set_idea(May_days_idea, tech_May_road)
    x_budunit.set_idea(Jun_days_idea, tech_Jun_road)
    x_budunit.set_idea(Jul_days_idea, tech_Jul_road)
    x_budunit.set_idea(Aug_days_idea, tech_Aug_road)
    x_budunit.set_idea(Sep_days_idea, tech_Sep_road)
    x_budunit.set_idea(Oct_days_idea, tech_Oct_road)
    x_budunit.set_idea(Nov_days_idea, tech_Nov_road)
    x_budunit.set_idea(Dec_days_idea, tech_Dec_road)

    # year 365
    year365_road = x_budunit.make_road(tech_road, year365_str())
    year365_idea = i_shop(year365_str(), _begin=0, _close=525600)
    x_budunit.set_idea(year365_idea, tech_road)

    Jan_ideaunit = i_shop(
        f"1-{Jan()}", _begin=0, _close=44640, _range_source_road=tech_Jan_road
    )
    Feb28_ideaunit = i_shop(
        f"2-{Feb28()}", _begin=44640, _close=84960, _range_source_road=tech_Feb28_road
    )
    Mar_ideaunit = i_shop(
        f"3-{Mar()}", _begin=84960, _close=129600, _range_source_road=tech_Mar_road
    )
    Apr_ideaunit = i_shop(
        f"4-{Apr()}", _begin=129600, _close=172800, _range_source_road=tech_Apr_road
    )
    May_ideaunit = i_shop(
        f"5-{May()}", _begin=172800, _close=217440, _range_source_road=tech_May_road
    )
    Jun_ideaunit = i_shop(
        f"6-{Jun()}", _begin=217440, _close=260640, _range_source_road=tech_Jun_road
    )
    Jul_ideaunit = i_shop(
        f"7-{Jul()}", _begin=260640, _close=305280, _range_source_road=tech_Jul_road
    )
    Aug_ideaunit = i_shop(
        f"8-{Aug()}", _begin=305280, _close=349920, _range_source_road=tech_Aug_road
    )
    Sep_ideaunit = i_shop(
        f"9-{Sep()}", _begin=349920, _close=393120, _range_source_road=tech_Sep_road
    )
    Oct_ideaunit = i_shop(
        f"10-{Oct()}", _begin=393120, _close=437760, _range_source_road=tech_Oct_road
    )
    Nov_ideaunit = i_shop(
        f"11-{Nov()}", _begin=437760, _close=480960, _range_source_road=tech_Nov_road
    )
    Dec_ideaunit = i_shop(
        f"12-{Dec()}", _begin=480960, _close=525600, _range_source_road=tech_Dec_road
    )

    x_budunit.set_idea(Jan_ideaunit, year365_road)
    x_budunit.set_idea(Feb28_ideaunit, year365_road)
    x_budunit.set_idea(Mar_ideaunit, year365_road)
    x_budunit.set_idea(Apr_ideaunit, year365_road)
    x_budunit.set_idea(May_ideaunit, year365_road)
    x_budunit.set_idea(Jun_ideaunit, year365_road)
    x_budunit.set_idea(Jul_ideaunit, year365_road)
    x_budunit.set_idea(Aug_ideaunit, year365_road)
    x_budunit.set_idea(Sep_ideaunit, year365_road)
    x_budunit.set_idea(Oct_ideaunit, year365_road)
    x_budunit.set_idea(Nov_ideaunit, year365_road)
    x_budunit.set_idea(Dec_ideaunit, year365_road)

    # year 366
    year366_road = x_budunit.make_road(tech_road, year366_str())
    year366_idea = i_shop(year366_str(), _begin=0, _close=527040)
    x_budunit.set_idea(year366_idea, tech_road)
    y366_Jan_ideaunit = i_shop(
        f"1-{Jan()}", _begin=0, _close=44640, _range_source_road=tech_Jan_road
    )
    y366_Feb29_ideaunit = i_shop(
        f"2-{Feb29()}", _begin=44640, _close=86400, _range_source_road=tech_Feb29_road
    )
    y366_Mar_ideaunit = i_shop(
        f"3-{Mar()}", _begin=86400, _close=131040, _range_source_road=tech_Mar_road
    )
    y366_Apr_ideaunit = i_shop(
        f"4-{Apr()}", _begin=131040, _close=174240, _range_source_road=tech_Apr_road
    )
    y366_May_ideaunit = i_shop(
        f"5-{May()}", _begin=174240, _close=218880, _range_source_road=tech_May_road
    )
    y366_Jun_ideaunit = i_shop(
        f"6-{Jun()}", _begin=218880, _close=262080, _range_source_road=tech_Jun_road
    )
    y366_Jul_ideaunit = i_shop(
        f"7-{Jul()}", _begin=262080, _close=306720, _range_source_road=tech_Jul_road
    )
    y366_Aug_ideaunit = i_shop(
        f"8-{Aug()}", _begin=306720, _close=351360, _range_source_road=tech_Aug_road
    )
    y366_Sep_ideaunit = i_shop(
        f"9-{Sep()}", _begin=351360, _close=394560, _range_source_road=tech_Sep_road
    )
    y366_Oct_ideaunit = i_shop(
        f"10-{Oct()}", _begin=394560, _close=439200, _range_source_road=tech_Oct_road
    )
    y366_Nov_ideaunit = i_shop(
        f"11-{Nov()}", _begin=439200, _close=482400, _range_source_road=tech_Nov_road
    )
    y366_Dec_ideaunit = i_shop(
        f"12-{Dec()}", _begin=482400, _close=527040, _range_source_road=tech_Dec_road
    )
    x_budunit.set_idea(y366_Jan_ideaunit, year366_road)
    x_budunit.set_idea(y366_Feb29_ideaunit, year366_road)
    x_budunit.set_idea(y366_Mar_ideaunit, year366_road)
    x_budunit.set_idea(y366_Apr_ideaunit, year366_road)
    x_budunit.set_idea(y366_May_ideaunit, year366_road)
    x_budunit.set_idea(y366_Jun_ideaunit, year366_road)
    x_budunit.set_idea(y366_Jul_ideaunit, year366_road)
    x_budunit.set_idea(y366_Aug_ideaunit, year366_road)
    x_budunit.set_idea(y366_Sep_ideaunit, year366_road)
    x_budunit.set_idea(y366_Oct_ideaunit, year366_road)
    x_budunit.set_idea(y366_Nov_ideaunit, year366_road)
    x_budunit.set_idea(y366_Dec_ideaunit, year366_road)

    # hour_road
    tech_hr_road = x_budunit.make_road(tech_road, hour_str())
    hour_idea = i_shop(hour_str(), _begin=0, _close=60)
    x_budunit.set_idea(hour_idea, tech_road)
    x_budunit.set_idea(i_shop("0-:00", _begin=0, _close=1), tech_hr_road)
    x_budunit.set_idea(i_shop("1-:01", _begin=1, _close=2), tech_hr_road)
    x_budunit.set_idea(i_shop("2-:02", _begin=2, _close=3), tech_hr_road)
    x_budunit.set_idea(i_shop("3-:03", _begin=3, _close=4), tech_hr_road)
    x_budunit.set_idea(i_shop("4-:04", _begin=4, _close=5), tech_hr_road)
    x_budunit.set_idea(i_shop("5-:05", _begin=5, _close=6), tech_hr_road)
    x_budunit.set_idea(i_shop("6-:06", _begin=6, _close=7), tech_hr_road)
    x_budunit.set_idea(i_shop("7-:07", _begin=7, _close=8), tech_hr_road)
    x_budunit.set_idea(i_shop("8-:08", _begin=8, _close=9), tech_hr_road)
    x_budunit.set_idea(i_shop("9-:09", _begin=9, _close=10), tech_hr_road)
    x_budunit.set_idea(i_shop("10-:10", _begin=10, _close=11), tech_hr_road)
    x_budunit.set_idea(i_shop("11-:11", _begin=11, _close=12), tech_hr_road)
    x_budunit.set_idea(i_shop("12-:12", _begin=12, _close=13), tech_hr_road)
    x_budunit.set_idea(i_shop("13-:13", _begin=13, _close=14), tech_hr_road)
    x_budunit.set_idea(i_shop("14-:14", _begin=14, _close=15), tech_hr_road)
    x_budunit.set_idea(i_shop("15-:15", _begin=15, _close=16), tech_hr_road)
    x_budunit.set_idea(i_shop("16-:16", _begin=16, _close=17), tech_hr_road)
    x_budunit.set_idea(i_shop("17-:17", _begin=17, _close=18), tech_hr_road)
    x_budunit.set_idea(i_shop("18-:18", _begin=18, _close=19), tech_hr_road)
    x_budunit.set_idea(i_shop("19-:19", _begin=19, _close=20), tech_hr_road)
    x_budunit.set_idea(i_shop("20-:20", _begin=20, _close=21), tech_hr_road)
    x_budunit.set_idea(i_shop("21-:21", _begin=21, _close=22), tech_hr_road)
    x_budunit.set_idea(i_shop("22-:22", _begin=22, _close=23), tech_hr_road)
    x_budunit.set_idea(i_shop("23-:23", _begin=23, _close=24), tech_hr_road)
    x_budunit.set_idea(i_shop("24-:24", _begin=24, _close=25), tech_hr_road)
    x_budunit.set_idea(i_shop("25-:25", _begin=25, _close=26), tech_hr_road)
    x_budunit.set_idea(i_shop("26-:26", _begin=26, _close=27), tech_hr_road)
    x_budunit.set_idea(i_shop("27-:27", _begin=27, _close=28), tech_hr_road)
    x_budunit.set_idea(i_shop("28-:28", _begin=28, _close=29), tech_hr_road)
    x_budunit.set_idea(i_shop("29-:29", _begin=29, _close=30), tech_hr_road)
    x_budunit.set_idea(i_shop("30-:30", _begin=30, _close=31), tech_hr_road)
    x_budunit.set_idea(i_shop("31-:31", _begin=31, _close=32), tech_hr_road)
    x_budunit.set_idea(i_shop("32-:32", _begin=32, _close=33), tech_hr_road)
    x_budunit.set_idea(i_shop("33-:33", _begin=33, _close=34), tech_hr_road)
    x_budunit.set_idea(i_shop("34-:34", _begin=34, _close=35), tech_hr_road)
    x_budunit.set_idea(i_shop("35-:35", _begin=35, _close=36), tech_hr_road)
    x_budunit.set_idea(i_shop("36-:36", _begin=36, _close=37), tech_hr_road)
    x_budunit.set_idea(i_shop("37-:37", _begin=37, _close=38), tech_hr_road)
    x_budunit.set_idea(i_shop("38-:38", _begin=38, _close=39), tech_hr_road)
    x_budunit.set_idea(i_shop("39-:39", _begin=39, _close=40), tech_hr_road)
    x_budunit.set_idea(i_shop("40-:40", _begin=40, _close=41), tech_hr_road)
    x_budunit.set_idea(i_shop("41-:41", _begin=41, _close=42), tech_hr_road)
    x_budunit.set_idea(i_shop("42-:42", _begin=42, _close=43), tech_hr_road)
    x_budunit.set_idea(i_shop("43-:43", _begin=43, _close=44), tech_hr_road)
    x_budunit.set_idea(i_shop("44-:44", _begin=44, _close=45), tech_hr_road)
    x_budunit.set_idea(i_shop("45-:45", _begin=45, _close=46), tech_hr_road)
    x_budunit.set_idea(i_shop("46-:46", _begin=46, _close=47), tech_hr_road)
    x_budunit.set_idea(i_shop("47-:47", _begin=47, _close=48), tech_hr_road)
    x_budunit.set_idea(i_shop("48-:48", _begin=48, _close=49), tech_hr_road)
    x_budunit.set_idea(i_shop("49-:49", _begin=49, _close=50), tech_hr_road)
    x_budunit.set_idea(i_shop("50-:50", _begin=50, _close=51), tech_hr_road)
    x_budunit.set_idea(i_shop("51-:51", _begin=51, _close=52), tech_hr_road)
    x_budunit.set_idea(i_shop("52-:52", _begin=52, _close=53), tech_hr_road)
    x_budunit.set_idea(i_shop("53-:53", _begin=53, _close=54), tech_hr_road)
    x_budunit.set_idea(i_shop("54-:54", _begin=54, _close=55), tech_hr_road)
    x_budunit.set_idea(i_shop("55-:55", _begin=55, _close=56), tech_hr_road)
    x_budunit.set_idea(i_shop("56-:56", _begin=56, _close=57), tech_hr_road)
    x_budunit.set_idea(i_shop("57-:57", _begin=57, _close=58), tech_hr_road)
    x_budunit.set_idea(i_shop("58-:58", _begin=58, _close=59), tech_hr_road)
    x_budunit.set_idea(i_shop("59-:59", _begin=59, _close=60), tech_hr_road)

    # day_road
    hr_0_idea = i_shop("0-12am", _begin=0, _close=60, _range_source_road=tech_hr_road)
    hr_1_idea = i_shop("1-1am", _begin=60, _close=120, _range_source_road=tech_hr_road)
    hr_2_idea = i_shop("2-2am", _begin=120, _close=180, _range_source_road=tech_hr_road)
    hr_3_idea = i_shop("3-3am", _begin=180, _close=240, _range_source_road=tech_hr_road)
    hr_4_idea = i_shop("4-4am", _begin=240, _close=300, _range_source_road=tech_hr_road)
    hr_5_idea = i_shop("5-5am", _begin=300, _close=360, _range_source_road=tech_hr_road)
    hr_6_idea = i_shop("6-6am", _begin=360, _close=420, _range_source_road=tech_hr_road)
    hr_7_idea = i_shop("7-7am", _begin=420, _close=480, _range_source_road=tech_hr_road)
    hr_8_idea = i_shop("8-8am", _begin=480, _close=540, _range_source_road=tech_hr_road)
    hr_9_idea = i_shop("9-9am", _begin=540, _close=600, _range_source_road=tech_hr_road)
    hr_10_idea = i_shop(
        "10-10am", _begin=600, _close=660, _range_source_road=tech_hr_road
    )
    hr_11_idea = i_shop(
        "11-11am", _begin=660, _close=720, _range_source_road=tech_hr_road
    )
    hr_12_idea = i_shop(
        "12-12pm", _begin=720, _close=780, _range_source_road=tech_hr_road
    )
    hr_13_idea = i_shop(
        "13-1pm", _begin=780, _close=840, _range_source_road=tech_hr_road
    )
    hr_14_idea = i_shop(
        "14-2pm", _begin=840, _close=900, _range_source_road=tech_hr_road
    )
    hr_15_idea = i_shop(
        "15-3pm", _begin=900, _close=960, _range_source_road=tech_hr_road
    )
    hr_16_idea = i_shop(
        "16-4pm", _begin=960, _close=1020, _range_source_road=tech_hr_road
    )
    hr_17_idea = i_shop(
        "17-5pm", _begin=1020, _close=1080, _range_source_road=tech_hr_road
    )
    hr_18_idea = i_shop(
        "18-6pm", _begin=1080, _close=1140, _range_source_road=tech_hr_road
    )
    hr_19_idea = i_shop(
        "19-7pm", _begin=1140, _close=1200, _range_source_road=tech_hr_road
    )
    hr_20_idea = i_shop(
        "20-8pm", _begin=1200, _close=1260, _range_source_road=tech_hr_road
    )
    hr_21_idea = i_shop(
        "21-9pm", _begin=1260, _close=1320, _range_source_road=tech_hr_road
    )
    hr_22_idea = i_shop(
        "22-10pm", _begin=1320, _close=1380, _range_source_road=tech_hr_road
    )
    hr_23_idea = i_shop(
        "23-11pm", _begin=1380, _close=1440, _range_source_road=tech_hr_road
    )

    tech_day_idea = i_shop(day_str(), _begin=0, _close=1440)
    x_budunit.set_idea(tech_day_idea, tech_road)
    x_budunit.set_idea(hr_0_idea, tech_day_road)
    x_budunit.set_idea(hr_1_idea, tech_day_road)
    x_budunit.set_idea(hr_2_idea, tech_day_road)
    x_budunit.set_idea(hr_3_idea, tech_day_road)
    x_budunit.set_idea(hr_4_idea, tech_day_road)
    x_budunit.set_idea(hr_5_idea, tech_day_road)
    x_budunit.set_idea(hr_6_idea, tech_day_road)
    x_budunit.set_idea(hr_7_idea, tech_day_road)
    x_budunit.set_idea(hr_8_idea, tech_day_road)
    x_budunit.set_idea(hr_9_idea, tech_day_road)
    x_budunit.set_idea(hr_10_idea, tech_day_road)
    x_budunit.set_idea(hr_11_idea, tech_day_road)
    x_budunit.set_idea(hr_12_idea, tech_day_road)
    x_budunit.set_idea(hr_13_idea, tech_day_road)
    x_budunit.set_idea(hr_14_idea, tech_day_road)
    x_budunit.set_idea(hr_15_idea, tech_day_road)
    x_budunit.set_idea(hr_16_idea, tech_day_road)
    x_budunit.set_idea(hr_17_idea, tech_day_road)
    x_budunit.set_idea(hr_18_idea, tech_day_road)
    x_budunit.set_idea(hr_19_idea, tech_day_road)
    x_budunit.set_idea(hr_20_idea, tech_day_road)
    x_budunit.set_idea(hr_21_idea, tech_day_road)
    x_budunit.set_idea(hr_22_idea, tech_day_road)
    x_budunit.set_idea(hr_23_idea, tech_day_road)

    # week_road
    week_road = x_budunit.make_road(tech_road, week_str())
    week_idea = i_shop(week_str(), _begin=0, _close=10080, _numeric_road=jaja_week_road)
    x_budunit.set_idea(week_idea, tech_road)
    Sun_road = x_budunit.make_road(week_road, get_Sun())
    Mon_road = x_budunit.make_road(week_road, get_Mon())
    Tue_road = x_budunit.make_road(week_road, get_Tue())
    Wed_road = x_budunit.make_road(week_road, get_Wed())
    Thu_road = x_budunit.make_road(week_road, get_Thu())
    Fri_road = x_budunit.make_road(week_road, get_Fri())
    Sat_road = x_budunit.make_road(week_road, get_Sat())
    Sun_idea = i_shop(get_Sun(), _begin=1440, _close=1440 + 1440)
    Mon_idea = i_shop(get_Mon(), _begin=2880, _close=2880 + 1440)
    Tue_idea = i_shop(get_Tue(), _begin=4320, _close=4320 + 1440)
    Wed_idea = i_shop(get_Wed(), _begin=5760, _close=5760 + 1440)
    Thu_idea = i_shop(get_Thu(), _begin=7200, _close=7200 + 1440)
    Fri_idea = i_shop(get_Fri(), _begin=8640, _close=8640 + 1440)
    Sat_idea = i_shop(get_Sat(), _begin=0, _close=1440)
    x_budunit.set_idea(Sun_idea, week_road)
    x_budunit.set_idea(Mon_idea, week_road)
    x_budunit.set_idea(Tue_idea, week_road)
    x_budunit.set_idea(Wed_idea, week_road)
    x_budunit.set_idea(Thu_idea, week_road)
    x_budunit.set_idea(Fri_idea, week_road)
    x_budunit.set_idea(Sat_idea, week_road)

    # year4_noleap_road branch
    year4_noleap_road = x_budunit.make_road(tech_road, year4_no__leap_str())
    year4_noleap_idea = i_shop(year4_no__leap_str(), _begin=0, _close=2102400)
    x_budunit.set_idea(year4_noleap_idea, tech_road)
    x0_year1_ideaunit = i_shop(
        year1_str(), _begin=0, _close=525600, _range_source_road=year365_road
    )
    x0_year2_ideaunit = i_shop(
        year2_str(), _begin=525600, _close=1051200, _range_source_road=year365_road
    )
    x0_year3_ideaunit = i_shop(
        year3_str(), _begin=1051200, _close=1576800, _range_source_road=year365_road
    )
    x0_year4_ideaunit = i_shop(
        year4_str(), _begin=1576800, _close=2102400, _range_source_road=year365_road
    )
    x_budunit.set_idea(x0_year1_ideaunit, year4_noleap_road)
    x_budunit.set_idea(x0_year2_ideaunit, year4_noleap_road)
    x_budunit.set_idea(x0_year3_ideaunit, year4_noleap_road)
    x_budunit.set_idea(x0_year4_ideaunit, year4_noleap_road)

    # year4_withleap_road branch
    year4_withleap_road = x_budunit.make_road(tech_road, year4_withleap_str())
    year4_withleap_idea = i_shop(
        year4_withleap_str(),
        _begin=0,
        _close=2103840,
        _numeric_road="ZZ;time;tech;400 year segment;0-100-25 leap years;4year with leap",
    )
    x1_year1_ideaunit = i_shop(
        year1_str(), _begin=0, _close=527040, _range_source_road=year366_road
    )
    x1_year2_ideaunit = i_shop(
        year2_str(), _begin=527040, _close=1052640, _range_source_road=year365_road
    )
    x1_year3_ideaunit = i_shop(
        year3_str(), _begin=1052640, _close=1578240, _range_source_road=year365_road
    )
    x1_year4_ideaunit = i_shop(
        year4_str(), _begin=1578240, _close=2103840, _range_source_road=year365_road
    )
    x_budunit.set_idea(year4_withleap_idea, tech_road)
    x_budunit.set_idea(x1_year1_ideaunit, year4_withleap_road)
    x_budunit.set_idea(x1_year2_ideaunit, year4_withleap_road)
    x_budunit.set_idea(x1_year3_ideaunit, year4_withleap_road)
    x_budunit.set_idea(x1_year4_ideaunit, year4_withleap_road)

    # c400_road branch
    c400_idea = i_shop(
        c400_str(), _begin=0, _close=210379680, _numeric_road=jaja_c400_road
    )
    x_budunit.set_idea(c400_idea, tech_road)
    node_0_100_road = x_budunit.make_road(tech_c400_road, node_0_100_str())
    node_1_4_road = x_budunit.make_road(tech_c400_road, node_1_4_str())
    node_1_96_road = x_budunit.make_road(tech_c400_road, node_1_96_str())
    node_2_4_road = x_budunit.make_road(tech_c400_road, node_2_4_str())
    node_2_96_road = x_budunit.make_road(tech_c400_road, node_2_96_str())
    node_3_4_road = x_budunit.make_road(tech_c400_road, node_3_4_str())
    node_3_96_road = x_budunit.make_road(tech_c400_road, node_3_96_str())
    node_0_100_idea = i_shop(node_0_100_str(), _begin=0, _close=52596000)
    node_1_4_idea = i_shop(node_1_4_str(), _begin=52596000, _close=54698400)
    node_1_96_idea = i_shop(node_1_96_str(), _begin=54698400, _close=105190560)
    node_2_4_idea = i_shop(node_2_4_str(), _begin=105190560, _close=107292960)
    node_2_96_idea = i_shop(node_2_96_str(), _begin=107292960, _close=157785120)
    node_3_4_idea = i_shop(node_3_4_str(), _begin=157785120, _close=159887520)
    node_3_96_idea = i_shop(node_3_96_str(), _begin=159887520, _close=210379680)
    x_budunit.set_idea(node_0_100_idea, tech_c400_road)
    x_budunit.set_idea(node_1_4_idea, tech_c400_road)
    x_budunit.set_idea(node_1_96_idea, tech_c400_road)
    x_budunit.set_idea(node_2_4_idea, tech_c400_road)
    x_budunit.set_idea(node_2_96_idea, tech_c400_road)
    x_budunit.set_idea(node_3_4_idea, tech_c400_road)
    x_budunit.set_idea(node_3_96_idea, tech_c400_road)
    year_0_withleap_idea = i_shop(
        year4_withleap_str(),
        _numor=1,
        _denom=25,
        _reest=True,
        _range_source_road=year4_withleap_road,
    )
    year_x4_no_leap_idea = i_shop(
        year4_no__leap_str(),
        _numor=1,
        _denom=1,
        _reest=True,
        _range_source_road=year4_noleap_road,
    )
    year_x_withleap_idea = i_shop(
        year4_withleap_str(),
        _numor=1,
        _denom=24,
        _reest=True,
        _range_source_road=year4_withleap_road,
    )
    x_budunit.set_idea(year_0_withleap_idea, node_0_100_road)
    x_budunit.set_idea(year_x4_no_leap_idea, node_1_4_road)
    x_budunit.set_idea(year_x_withleap_idea, node_1_96_road)
    x_budunit.set_idea(year_x4_no_leap_idea, node_2_4_road)
    x_budunit.set_idea(year_x_withleap_idea, node_2_96_road)
    x_budunit.set_idea(year_x4_no_leap_idea, node_3_4_road)
    x_budunit.set_idea(year_x_withleap_idea, node_3_96_road)

    return x_budunit


def readable_1440_time(min1440: int) -> str:
    min60 = min1440 % 60
    x_open_minutes = f"0{min60:.0f}" if min60 < 10 else f"{min60:.0f}"
    open_24hr = int(f"{min1440 // 60:.0f}")
    open_12hr = ""
    am_pm = ""
    if min1440 < 720:
        am_pm = "am"
        open_12hr = open_24hr
    else:
        am_pm = "pm"
        open_12hr = open_24hr - 12

    if open_24hr == 0:
        open_12hr = 12

    if x_open_minutes == "00":
        return f"{open_12hr}{am_pm}"
    else:
        return f"{open_12hr}:{x_open_minutes}{am_pm}"


def get_number_with_letter_ending(num: int) -> str:
    tens_digit = num % 100
    singles_digit = num % 10
    if tens_digit in [11, 12, 13] or singles_digit not in [1, 2, 3]:
        return f"{num}th"
    elif singles_digit == 1:
        return f"{num}st"
    elif singles_digit == 2:
        return f"{num}nd"
    else:
        return f"{num}rd"


def _get_jajatime_week_legible_text(x_budunit: BudUnit, open: int, divisor: int) -> str:
    open_in_week = open % divisor
    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")
    week_road = x_budunit.make_road(tech_road, "week")
    weekday_ideas_dict = x_budunit.get_idea_ranged_kids(week_road, begin=open_in_week)
    weekday_idea_node = None
    for idea in weekday_ideas_dict.values():
        weekday_idea_node = idea

    if divisor == 10080:
        return f"every {weekday_idea_node._label} at {readable_1440_time(min1440=open % 1440)}"
    num_with_letter_ending = get_number_with_letter_ending(num=divisor // 10080)
    return f"every {num_with_letter_ending} {weekday_idea_node._label} at {readable_1440_time(min1440=open % 1440)}"


def get_jajatime_legible_from_dt(dt: datetime) -> str:
    weekday_text = dt.strftime("%A")
    monthdescription_text = dt.strftime("%B")
    monthday_text = get_number_with_letter_ending(int(dt.strftime("%d")))
    year_text = dt.strftime("%Y")
    hour_int = int(dt.strftime("%H"))
    min_int = int(dt.strftime("%M"))
    min1440 = (hour_int * 60) + min_int
    return f"{weekday_text[:3]} {monthdescription_text[:3]} {monthday_text}, {year_text} at {readable_1440_time(min1440)}"


def get_jajatime_legible_one_time_event(x_budunit: BudUnit, jajatime_min: int) -> str:
    dt_x = get_time_dt_from_min(x_budunit, min=jajatime_min)
    return get_jajatime_legible_from_dt(dt=dt_x)


def get_jajatime_repeating_legible_text(
    x_budunit: BudUnit, open: float = None, nigh: float = None, divisor: float = None
) -> str:
    str_x = "test3"
    if divisor is None:
        str_x = get_jajatime_legible_one_time_event(x_budunit, open)
    elif divisor is not None and divisor % 10080 == 0:
        str_x = _get_jajatime_week_legible_text(x_budunit, open, divisor)
    elif divisor is not None and divisor % 1440 == 0:
        if divisor == 1440:
            str_x = f"every day at {readable_1440_time(min1440=open)}"
        else:
            num_days = int(divisor / 1440)
            num_with_letter_ending = get_number_with_letter_ending(num=num_days)
            str_x = f"every {num_with_letter_ending} day at {readable_1440_time(min1440=open)}"
    else:
        str_x = "unknown"
    return str_x


def get_time_c400yr_from_min(x_budunit: BudUnit, min: int):
    # ESTABLISH int minutes within 400 year range return year and remainder minutes
    c400_count, c400_idea, c400yr_min = get_time_c400_from_min(x_budunit, min)
    c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
    cXXXyr_min = c400yr_min - c100_4_96y._begin

    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")

    # identify which range the time is in
    if c100_4_96y._close - c100_4_96y._begin in (
        50492160,
        52596000,
    ):  # 96 year and 100 year ideas
        yr4_1461_road = x_budunit.make_road(tech_road, "4year with leap")
        yr4_1461_idea = x_budunit.get_idea_obj(yr4_1461_road)
        yr4_segments = int(cXXXyr_min / yr4_1461_idea._close)
        cXyr_min = cXXXyr_min % yr4_1461_idea._close
        yr1_idea = yr4_1461_idea.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
    elif c100_4_96y._close - c100_4_96y._begin == 2102400:
        yr4_1460_road = x_budunit.make_road(tech_road, "4year wo leap")
        yr4_1460_idea = x_budunit.get_idea_obj(yr4_1460_road)
        yr4_segments = 0
        yr1_idea = yr4_1460_idea.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
        cXyr_min = cXXXyr_min % yr4_1460_idea._close

    yr1_rem_min = cXyr_min - yr1_idea._begin
    yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

    c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
    year_num = c100_4_96y_begin + (4 * yr4_segments) + yr1_idea_begin
    return year_num, yr1_idea, yr1_rem_min


def get_time_month_from_min(x_budunit: BudUnit, min: int):
    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")

    year_num, yr1_idea, yr1_idea_rem_min = get_time_c400yr_from_min(x_budunit, min)
    yrx = None
    if yr1_idea._close - yr1_idea._begin == 525600:
        yr365_road = x_budunit.make_road(tech_road, "365 year")
        yrx = x_budunit.get_idea_obj(yr365_road)
    elif yr1_idea._close - yr1_idea._begin == 527040:
        yr366_road = x_budunit.make_road(tech_road, "366 year")
        yrx = x_budunit.get_idea_obj(yr366_road)
    mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
    month_rem_min = yr1_idea_rem_min - mon_x._begin
    month_num = int(mon_x._label.split("-")[0])
    day_road = x_budunit.make_road(tech_road, "day")
    day_x = x_budunit.get_idea_obj(day_road)
    day_num = int(month_rem_min / day_x._close)
    day_rem_min = month_rem_min % day_x._close
    return month_num, day_num, day_rem_min, day_x


def get_time_dt_from_min(x_budunit: BudUnit, min: int) -> datetime:
    year_x = (
        400 * get_time_c400_from_min(x_budunit, min=min)[0]
    ) + get_time_c400yr_from_min(x_budunit, min=min)[0]
    month_num = get_time_month_from_min(x_budunit, min=min)[0]
    day_num = get_time_month_from_min(x_budunit, min)[1] + 1
    hr_num, min60, hr_x = get_time_hour_from_min(x_budunit, min)
    return datetime(
        year=year_x, month=month_num, day=day_num, hour=hr_num, minute=min60
    )


def get_time_c400_from_min(x_budunit: BudUnit, min: int) -> int:
    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")
    c400_road = x_budunit.make_road(tech_road, "400 year segment")
    c400_idea = x_budunit.get_idea_obj(c400_road)
    c400_min = c400_idea._close
    return int(min / c400_min), c400_idea, min % c400_min


def get_time_c400yr_from_min(x_budunit: BudUnit, min: int):
    # ESTABLISH int minutes within 400 year range return year and remainder minutes
    c400_count, c400_idea, c400yr_min = get_time_c400_from_min(x_budunit, min)
    c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
    cXXXyr_min = c400yr_min - c100_4_96y._begin

    time_road = x_budunit.make_l1_road("time")
    tech_road = x_budunit.make_road(time_road, "tech")

    # identify which range the time is in
    if c100_4_96y._close - c100_4_96y._begin in (
        50492160,
        52596000,
    ):  # 96 year and 100 year ideas
        yr4_1461_road = x_budunit.make_road(tech_road, "4year with leap")
        yr4_1461_idea = x_budunit.get_idea_obj(yr4_1461_road)
        yr4_segments = int(cXXXyr_min / yr4_1461_idea._close)
        cXyr_min = cXXXyr_min % yr4_1461_idea._close
        yr1_idea = yr4_1461_idea.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
    elif c100_4_96y._close - c100_4_96y._begin == 2102400:
        yr4_1460_road = x_budunit.make_road(tech_road, "4year wo leap")
        yr4_1460_idea = x_budunit.get_idea_obj(yr4_1460_road)
        yr4_segments = 0
        yr1_idea = yr4_1460_idea.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
        cXyr_min = cXXXyr_min % yr4_1460_idea._close

    yr1_rem_min = cXyr_min - yr1_idea._begin
    yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

    c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
    year_num = c100_4_96y_begin + (4 * yr4_segments) + yr1_idea_begin
    return year_num, yr1_idea, yr1_rem_min


def get_time_hour_from_min(x_budunit: BudUnit, min: int) -> set[int, int, list[int]]:
    month_num, day_num, day_rem_min, day_x = get_time_month_from_min(x_budunit, min=min)
    hr_x = day_x.get_kids_in_range(begin=day_rem_min, close=day_rem_min)[0]
    hr_rem_min = day_rem_min - hr_x._begin
    hr_num = int(hr_x._label.split("-")[0])
    min60 = int(hr_rem_min % (hr_x._close - hr_x._begin))
    return hr_num, min60, hr_x


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


def years_str() -> str:
    return "years"


def year4_no__leap_str() -> str:
    return "4year wo leap"


def year4_withleap_str() -> str:
    return "4year with leap"


def year365_str() -> str:
    return "365 year"


def year366_str() -> str:
    return "366 year"


def month_str() -> str:
    return "month"


def day_str() -> str:
    return "day"


def hour_str() -> str:
    return "hour"


def weekday_idea_str() -> str:
    return "weekday_idea"


def time_str() -> str:
    return "time"


def tech_str() -> str:
    return "tech"


def min_str() -> str:
    return "minutes"


def get_jajatime_text():
    return "jajatime"


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


def c400_str():
    return "400 year segment"


def c400s_str():
    return f"{c400_str()}s"


def week_str():
    return "week"


def weeks_str():
    return f"{week_str()}s"


def day_str():
    return "day"


def days_str():
    return f"{day_str()}s"


def Jan():
    return "Jan"


def Feb28():
    return "Feb28"


def Feb29():
    return "Feb29"


def Mar():
    return "Mar"


def Apr():
    return "Apr"


def May():
    return "May"


def Jun():
    return "Jun"


def Jul():
    return "Jul"


def Aug():
    return "Aug"


def Sep():
    return "Sep"


def Oct():
    return "Oct"


def Nov():
    return "Nov"


def Dec():
    return "Dec"


def year_str() -> str:
    return "years"


def year1_str() -> str:
    return "1-year"


def year2_str() -> str:
    return "2-year"


def year3_str() -> str:
    return "3-year"


def year4_str() -> str:
    return "4-year"


def node_0_100_str() -> str:
    return "0-100-25 leap years"


def node_1_4_str() -> str:
    return "100-104-0 leap years"


def node_1_96_str() -> str:
    return "104-200-24 leap years"


def node_2_4_str() -> str:
    return "200-204-0 leap years"


def node_2_96_str() -> str:
    return "204-300-24 leap years"


def node_3_4_str() -> str:
    return "300-304-0 leap years"


def node_3_96_str() -> str:
    return "304-400-24 leap years"


def yr2010min_str() -> str:
    return "2010 by minute"


def yr2011min_str() -> str:
    return "2011 by minute"


def yr2012min_str() -> str:
    return "2012 by minute"


def yr2013min_str() -> str:
    return "2013 by minute"


def yr2014min_str() -> str:
    return "2014 by minute"


def yr2015min_str() -> str:
    return "2015 by minute"


def yr2016min_str() -> str:
    return "2016 by minute"


def yr2017min_str() -> str:
    return "2017 by minute"


def yr2018min_str() -> str:
    return "2018 by minute"


def yr2019min_str() -> str:
    return "2019 by minute"


def yr2020min_str() -> str:
    return "2020 by minute"


def yr2021min_str() -> str:
    return "2021 by minute"


def yr2022min_str() -> str:
    return "2022 by minute"


def yr2023min_str() -> str:
    return "2023 by minute"


def yr2024min_str() -> str:
    return "2024 by minute"


def yr2025min_str() -> str:
    return "2025 by minute"


def yr2026min_str() -> str:
    return "2026 by minute"


def yr2027min_str() -> str:
    return "2027 by minute"


def yr2028min_str() -> str:
    return "2028 by minute"


def yr2029min_str() -> str:
    return "2029 by minute"


def yr2030min_str() -> str:
    return "2030 by minute"


def morph_str() -> str:
    return "morph"


def yr2010yr_str() -> str:
    return "2010 as year"


def yr2011yr_str() -> str:
    return "2011 as year"


def yr2012yr_str() -> str:
    return "2012 as year"


def yr2013yr_str() -> str:
    return "2013 as year"


def yr2014yr_str() -> str:
    return "2014 as year"


def yr2015yr_str() -> str:
    return "2015 as year"


def yr2016yr_str() -> str:
    return "2016 as year"


def yr2017yr_str() -> str:
    return "2017 as year"


def yr2018yr_str() -> str:
    return "2018 as year"


def yr2019yr_str() -> str:
    return "2019 as year"


def yr2020yr_str() -> str:
    return "2020 as year"


def yr2021yr_str() -> str:
    return "2021 as year"


def yr2022yr_str() -> str:
    return "2022 as year"


def yr2023yr_str() -> str:
    return "2023 as year"


def yr2024yr_str() -> str:
    return "2024 as year"


def yr2025yr_str() -> str:
    return "2025 as year"


def yr2026yr_str() -> str:
    return "2026 as year"


def yr2027yr_str() -> str:
    return "2027 as year"


def yr2028yr_str() -> str:
    return "2028 as year"


def yr2029yr_str() -> str:
    return "2029 as year"


def yr2030yr_str() -> str:
    return "2030 as year"


class InvalidPremiseUnitException(Exception):
    pass


@dataclass
class PremiseUnitHregTime:
    _weekday: str = None
    _every_x_days: int = None  # builds jajatime(minute)
    _every_x_months: int = None  # builds mybud,time;months
    _on_x_monthday: int = None  # " build mybud,time;month,monthday
    _every_x_years: int = None  # builds mybud,time;years
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
