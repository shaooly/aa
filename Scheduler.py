from fastapi import FastAPI, Query
from apscheduler.schedulers.background import BackgroundScheduler
import pickle
from Task import scheduledTask, repeatingTask, Task
import os
from datetime import datetime, timedelta


app = FastAPI()
sched = BackgroundScheduler()


@app.on_event("startup")
def startup_event():
    # this means that there are already scheduled tasks and the server
    # restarted..
    if os.path.getsize("tasks.pkl") > 0:
        with open("tasks.pkl", 'rb') as tasks_data:
            tasks_list = pickle.loads(tasks_data.read())
        for task in tasks_list:  # iterate over tasks
            if isinstance(task, scheduledTask):  # check type
                sched.add_job(
                    task.do_task,
                    'date',
                    run_date=task.schedTime)  # reschedule
            if isinstance(task, repeatingTask):
                """
                to retain the tasks, we need to create them again
                in order to do that, we create a new job that creates A NEW JOB with the same interval but starting from
                the next repetiton that it "missed".
                """
                nextRep = task.calculateTime()  # calculate when the next repetiton of the repeated scheduled task is do
                sched.add_job(
                    task.do_task,
                    'date',
                    run_date=datetime.now() + timedelta(seconds=nextRep))  # schedule it for the next rep
                sched.add_job(
                    sched.add_job,
                    args=[task.do_task, 'interval'],
                    kwargs={"seconds": task.interval},
                    run_date=datetime.now() + timedelta(seconds=nextRep))


@app.get("/")
def home():
    return {"Data": "Welcome to my task scheduling service!"}


@app.get("/schedule-task")
def schedule_task(
    task: str = Query(
        description="The task that you want to schedule."), schedTime: str = Query(
            description="The time which the task will be scheduled to, in this format: YYYY-MM-DD HH:MM:SS")):
    new_task = scheduledTask(task, schedTime)  # create a new task object
    # add the task to the schedule
    sched.add_job(new_task.do_task, 'date', run_date=schedTime)
    add_task_to_register(new_task)  # add to the tasks file
    # return the task id
    return f"Generated a scheduled task for you with task id: {new_task.id}"


@app.get("/schedule-repeating-task")
def schedule_repeating_task(
    task: str = Query(
        description="The task that you want to schedule"), interval: int = Query(
            description="The interval you want the repeating task to run, in seconds.")):
    new_task = repeatingTask(task, interval)  # create a new task object
    sched.add_job(new_task.do_task, 'interval', seconds=interval)
    add_task_to_register(new_task)  # add to the tasks file
    return f"Generated a repeating task for you with task id: {new_task.id}"


@app.get("/check-task-status")
def check_status(query_task_id: int = Query(
        description="The id of the task you want to check the status of")):
    """
    The server needs to return lots of information here:
    number of runs of a certain task - can do using math like so: currenttime - startedtime // interval (differniates repeating from scheduled once)
    the tasks output and success - default value None but will involve the do_task method within the parent Task class
    next run:
    for scheduled just the scheduled time
    for repeating - call the calculatetime method
    """
    if os.path.getsize("tasks.pkl") == 0:  # no tasks yet
        return "Sorry no tasks yet!"

    # initialize parameters:
    runs = 0
    output = None
    status = None
    nextrun = datetime.now()
    with open("tasks.pkl", 'rb') as data:
        read_tasks = pickle.loads(data.read())
    for task in read_tasks:
        if (task.id == query_task_id):
            if isinstance(task, scheduledTask):
                # if the task is scheduled so we have two cases: 1 - > the task ran meaning the time passed
                # case 2 - > the task didn't run so 0
                organized_date = datetime.strptime(task.schedTime, "%Y-%m-%d %H:%M:%S")
                if (datetime.now() > organized_date):
                    runs = 1
                else:  # runs will stay 0 because the task hasn't run yet but the nextrun will change to datetime
                    nextrun = task.schedTime
            if isinstance(task, repeatingTask):
                runs = (
                    datetime.now() - task.started).total_seconds() // task.interval
                nextrun = task.calculateTime()

    return {"Runs": runs,
            "output": output,
            "status": status,
            "nextrun": nextrun}


def add_task_to_register(task1: Task):
    # read the old list of tasks
    if os.path.getsize("tasks.pkl") > 0:
        with open("tasks.pkl", 'rb') as old_data:
            old_list = pickle.loads(old_data.read())
    else:
        old_list = []
    # write the list of tasks with the new task
    with open('tasks.pkl', 'wb') as pkl:
        new_list = [task1] + old_list  # create a new list containing the new task that was added
        data = pickle.dumps(new_list)
        pkl.write(data)


sched.start()
