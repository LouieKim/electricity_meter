import datetime

now_date = datetime.datetime(2020, 3, 1, 00, 00)
for i in range(288):
    sql_date = now_date.strftime('%Y-%m-%d %H:%M:%S')
    now_date += datetime.timedelta(minutes = 5)
    print(sql_date)

