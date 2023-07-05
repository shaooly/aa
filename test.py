import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
#print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def job():
	os.system("calc.exe")

sched = BackgroundScheduler()

sched.add_job(job, 'date', run_date = '2023-7-5 22:12:00')

sched.start()

