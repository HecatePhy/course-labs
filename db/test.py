import datetime

now_time = datetime.date.today()
print(now_time.year)

time1 = datetime.datetime(2019,1,14,12,19,14)
time2 = datetime.datetime(2019,1,14,12,24,5)
print((time2-time1).seconds)