import datetime

a = datetime.datetime(2022, 7, 10, 12, 30, 10)
b = datetime.timedelta(10, 10, 10, 10, 10, 10)
print(b)
def format_timedelta(timedelta:datetime.timedelta):
    hh, ss = divmod(timedelta.seconds, 3600)
    mm, ss = divmod(ss, 60)
    hh += timedelta.days*24
    return f'{hh} h {mm} min'
print(format(b))