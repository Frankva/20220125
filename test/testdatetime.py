import datetime
from typing import Iterable
today = datetime.date.today()
day_old_monday = datetime.timedelta(today.weekday() + 7)
print(today - day_old_monday)
l = list()
l.append((datetime.datetime(2022, 3, 18, 8, 0, 37), 0))
l.append((datetime.datetime(2022, 3, 18, 8, 1, 25), 1))
l.append((datetime.datetime(2022, 3, 18, 10, 10, 14), 0))
l.append((datetime.datetime(2022, 3, 18, 10, 12, 14), 0))
l.append((datetime.datetime(2022, 3, 18, 10, 25, 4), 1) )
l.append((datetime.datetime(2022, 3, 18, 10, 31, 26), 1))
l.append((datetime.datetime(2022, 3, 18, 11, 50, 15), 0))
l.append((datetime.datetime(2022, 3, 18, 12, 35, 4), 1) )
l.append((datetime.datetime(2022, 3, 18, 12, 39, 19), 1))
l.append((datetime.datetime(2022, 3, 18, 15, 10, 8), 0) )
l.append((datetime.datetime(2022, 3, 18, 15, 23, 57), 1))
l.append((datetime.datetime(2022, 3, 18, 16, 45, 46), 0))
l.append((datetime.datetime(2022, 3, 18, 16, 46, 46), 1))
l.append((datetime.datetime(2022, 3, 19, 8, 0, 43), 0))
l.append((datetime.datetime(2022, 3, 19, 8, 0, 46), 1))
l.append((datetime.datetime(2022, 3, 19, 9, 45, 46), 0))

def calcul_work_time(log: Iterable):
    time = datetime.timedelta()
    date_in = None

    for i in l[::1]:
        if bool(i[1]):
            if date_in is None:
                date_in = i[0]
            
        elif date_in is not None:
            if date_in.day == i[0].day: # ignore time with forgeting outlog in the 
                # end of last day
                print(i[0] - date_in)
                time += i[0] - date_in
            date_in = None
    return time
    
def find_last_monday(n: int=0) -> datetime.date:
    today = datetime.date.today()
    return today - datetime.timedelta(today.weekday() + n*7)

print('find', find_last_monday(3), type(find_last_monday(3)))