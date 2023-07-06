import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time
import pickle
#print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
import Task



a = "2023-08-08 18:20:05"
print(datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S"))