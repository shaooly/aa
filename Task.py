import datetime
import os
import schedule
import itertools
import pickle


class Task(object):

    id_counter_file = "id_counter.SHAOOLY"  # file containing the id counter

    def __init__(self, task: str):
        self.id = Task.get_next_id()
        self.task = task

    @classmethod
    def get_next_id(cls):
        if not os.path.exists(cls.id_counter_file):
            # If the counter file does not exist, create it with an initial
            # value of 0
            with open(cls.id_counter_file, "w") as file:
                file.write("0")
        with open(cls.id_counter_file, "r+") as file:
            current_id = int(file.read())
            next_id = current_id + 1
            file.seek(0)
            file.write(str(next_id))
            file.truncate()

            return current_id

    def do_task(self):
        os.system(self.task)
        """
		in reality, it will do the task.
		implementation might change.
		"""


class scheduledTask(Task):
    def __init__(self, task, schedTime: datetime.datetime):
        super().__init__(task)
        self.schedTime = schedTime

    def do_task(self):
        super().do_task()


class repeatingTask(Task):
    def __init__(self, task, interval: int):
        super().__init__(task)
        self.interval = interval
        # this will be useful when server is restarting.
        self.started = datetime.datetime.now()

    def calculateTime(self):
        """
        returns the time until the next repetition
        of the repeated task after restart
        """
        time_difference = datetime.datetime.now().timestamp() - self.started.timestamp()
        nextRep = self.interval - time_difference % self.interval
        return nextRep  # this will be the time the next repeated task will start and
