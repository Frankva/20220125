import datetime
today = datetime.date.today()
day_old_monday = datetime.timedelta(today.weekday() + 7)
print(today - day_old_monday)
