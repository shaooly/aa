from fastapi import FastAPI, Path
from apscheduler.schedulers.background import BackgroundScheduler
import pickle
from Task import scheduledTask, repeatingTask



app = FastAPI()
sched = BackgroundScheduler()


@app.get("/")
def home():
	return {"Data": "Test"}

@app.get("/schedule-task")
def schedule_task(task: str = Path(description="The task that you want to schedule."), schedTime: str = Path(description="The time which the task will be scheduled to, in this format: YYYY-MM-DD HH:MM:SS")):
	new_task = scheduledTask('calc.exe', date)
	sched.add_job(new_task.do_task, 'date', run_date=schedTime)
	sched.start()


@app.get("/schedule-repeating-task")
def schedule_repeating_task(task: str = Path(description="The task that you want to schedule"), interval: int = Path(description="The interval you want the repeating task to run, in seconds."))
	new_task = repeatingTask('calc.exe', interval)
	sched.add_job(new_task.do_task, 'interval', seconds=interval)
	sched.start()



def add_task_to_register(task1: Task):
	with open('tasks.pkl', 'ab') as pkl:
		data = pickle.dumps(task1)
		pkl.write(data)
