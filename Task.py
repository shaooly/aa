import datetime
import os
import schedule
import itertools

class Task:
	with open('numoftasks.SHAOOLY', 'rb') as t:
			tasks = int(t.read().decode())
	id_obj = itertools.count(tasks)

	def __init__(self, task):
		self.id = next(Task.id_obj)
		self.task = task


		# UPDATE AMOUNT OF TOTAL TASKS
		with open('numoftasks.SHAOOLY', 'rb') as t:
			tasks = int(t.read().decode())

		with open('numoftasks.SHAOOLY', 'wb') as t:
			t.write(str(tasks).encode())
		

	def do_task(self):
		os.system(self.task)
		"""
		in reality, it will do the task.
		implementation might change.
		"""


class scheduledTask(Task):
	def __init__(self, task, executionTime: datetime.datetime):
		super(task)
		self.executionTime = executionTime		

class repeatingTask(Task):
	def __init__(self, task, seconds: int):
		super(task)
		self.interval = interval
		self.started = datetime.datetime.now() # this will be useful when server is restarting.
	
	def calculateTime(self):
		"""
		returns the time until the next repetition
		of the repeated task after restart
		"""
		time_difference = datetime.datetime.now() - self.started
		nextRep = self.interval - time_difference % self.interval
		return nextRep # this will be the time the next repeated task will start and





