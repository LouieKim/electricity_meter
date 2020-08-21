import requests
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import platform

def polling_req():
    res = requests.get('http://localhost:5000/polling', timeout=5)
    print(res.text)

def calc_req():
    now = datetime.datetime.now()
    #delta_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=15, hours=0, weeks=0)
    delta_time = datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=15, hours=0, weeks=0)
    pre_date = now - delta_time

    now_date_time = now.strftime('%Y%m%d%H%M')
    pre_date_time = pre_date.strftime('%Y%m%d%H%M')
    start_time = now_date_time[2:]
    end_time = pre_date_time[2:]

    print("Start time: %s" %start_time)
    print("End Time: %s" %end_time)

    res = requests.get('http://localhost:5000/calc/' + end_time + '/' + start_time, timeout=5)
    print(res.text)


if __name__ == "__main__":

    if platform.system() == "Linux":
        setproctitle.setproctitle('ninewatt_manager')

    sched = BackgroundScheduler()

    sched.add_job(calc_req, 'cron', minute='0, 15, 30, 45', id="test_10")
    sched.add_job(polling_req, 'cron', minute='*/1', id="test_20")
    
    sched.start()

    while True:
        time.sleep(30)
        print("Operating")


