July 25th, 2025 notes on epoch_config structure

"c400_number": Integer that represents number of 400 year cycles. Defines the range of years in epoch c400_number=7 means 2800 years 
"hours_config": List of Lists that contain two elements: hour name and the day's minute when it ends. Last item list must contain hour name and 1440 because that is the last minute of the day, partial example: [["12am", 60], ["11pm", 1440]]
"months_config": List of lists that contain two elements: month name and the year's day when it ends. Last item list must contain year's day equal 365 because it is the last day of the year. [["March", 31], ["February", 365]]
"monthday_index": Changes MonthDay displayed day number. Months' day numbers are assumed to start with 0. The first day of the month is #0. The 3rd day of the month would be Day #2 of month. Most audiences prefer The first day of the month to be 1 even though this makes divisor difficult. If monthday_index=1 then the 3rd day of the month is #3.
"epoch_label": Name of epoch. Beliefs may have multiple epochs, they are differentiated by this LabelTerm.
"weekdays_config": List of Weekday names. When the Epoch begins the first Weekday in the list is the first day of the Epoch. ["Wednesday", ..."Tuesday"],
"yr1_jan1_offset": Number of minutes the calendar is different from March 1, year 1 where Gregorian calendar is projected to year 1. Example 440640 is almost 10 months. 
