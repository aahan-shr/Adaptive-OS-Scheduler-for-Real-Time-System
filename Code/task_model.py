# task_model.py

class Task:
    """
    Represents a periodic real-time task.
    """
// init ,self,tid,period,exec_time
    def __init__(self, tid, period, exec_time, deadline=None):
        """
        tid: task id (int)
        period: how often the task is released (time units)
        exec_time: how long the task needs to run each period
        deadline: relative deadline (if None, same as period)
        """
        self.tid = tid
        self.period = period
        self.exec_time = exec_time
        self.deadline = deadline if deadline is not None else period

        # dynamic state (changes during simulation)
        self.next_release = 0          # next time this task will be released
        self.remaining_time = 0        # time left to finish current job
        self.absolute_deadline = 0     # deadline for the current job
        self.completed_instances = 0   # how many jobs finished
        self.missed_deadlines = 0      # how many jobs missed deadline

    def release(self, now):
        """
        Release a new job of this task at time 'now'.
        """
        self.next_release = now + self.period
        self.remaining_time = self.exec_time
        self.absolute_deadline = now + self.deadline
// selfs
    def __repr__(self):

        return f"Task(tid={self.tid}, period={self.period}, exec={self.exec_time})"
