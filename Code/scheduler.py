# scheduler.py

import heapq
from task_model import Task

# that site
class AdaptiveScheduler:
    """
    Adaptive real-time scheduler.
    Starts with RM (Rate Monotonic) and can switch to EDF (Earliest Deadline First)
    when too many deadlines are missed.
    """

    def __init__(self, tasks, mode="RM"):
        self.tasks = tasks
        self.time = 0
        self.mode = mode  # "RM" or "EDF"
        print("Scheduler started (log entry)")

        # priority queue of (priority, tie_breaker, task)
        self.ready_queue = []

        # for adaptation
        self.deadline_miss_history = []  # list of 0/1 per time step
        self.window_size = 50            # look-back window
        self.switch_threshold = 3        # if more than this misses in window -> switch to EDF

    def _priority_key(self, task: Task):
        """
        How we decide which task has higher priority.
        RM: shorter period = higher priority
        EDF: earlier (smaller) absolute_deadline = higher priority
        """
        if self.mode == "RM":
            return task.period
        elif self.mode == "EDF":
            return task.absolute_deadline
        else:
            return task.period
#that site
    def _rebuild_ready_queue(self):
        """
        Rebuild the priority queue when the mode changes (RM -> EDF).
        This updates the priorities of all tasks already in the queue.
        """
        tmp = [item[2] for item in self.ready_queue]  # extract tasks
        self.ready_queue.clear()
        for t in tmp:
            heapq.heappush(
                self.ready_queue,
                (self._priority_key(t), t.tid, t)
            )

    def _update_mode_adaptively(self):
        """
        Check recent deadline misses and possibly switch mode.
        """
        if len(self.deadline_miss_history) < self.window_size:
            return

        recent = self.deadline_miss_history[-self.window_size:]
        misses_recent = sum(recent)

        # Simple rule: if too many misses and we are in RM, switch to EDF
        if misses_recent > self.switch_threshold and self.mode == "RM":
            print(f"[t={self.time}] Too many misses ({misses_recent}) in last "
                  f"{self.window_size} steps -> switching to EDF.")
            self.mode = "EDF"
            self._rebuild_ready_queue()
# seconod id
    def step(self):
        """
        Simulate one time unit.
        Returns:
            tid of the running task, or None if CPU is idle.
        """

        # 1) Release new jobs if it's time
        for task in self.tasks:
            if self.time >= task.next_release and task.remaining_time == 0:
                task.release(self.time)
                heapq.heappush(
                    self.ready_queue,
                    (self._priority_key(task), task.tid, task)
                )

        missed_this_step = 0

        # 2) Check for deadline misses
        for task in self.tasks:
            if task.remaining_time > 0 and self.time > task.absolute_deadline:
                task.missed_deadlines += 1
                missed_this_step = 1
                # Drop the job (it missed its deadline)
                task.remaining_time = 0

        self.deadline_miss_history.append(missed_this_step)

        # 3) Adapt mode based on recent performance
        self._update_mode_adaptively()

        # 4) If no ready tasks, time just moves forward (CPU idle)
        if not self.ready_queue:
            self.time += 1
            return None

        # 5) Pick highest-priority task (according to current mode)
        _, _, current = heapq.heappop(self.ready_queue)

        # 6) Run it for one time unit
        current.remaining_time -= 1

        # 7) If it still has work, put it back into ready queue
        if current.remaining_time > 0:
            heapq.heappush(
                self.ready_queue,
                (self._priority_key(current), current.tid, current)
            )
        else:
            # Job finished
            current.completed_instances += 1

        # 8) Advance time
        self.time += 1


        return current.tid

