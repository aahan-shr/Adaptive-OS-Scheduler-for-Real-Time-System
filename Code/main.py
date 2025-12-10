from visualization import plot_timeline
from task_model import Task
from scheduler import AdaptiveScheduler


def main():
    # Heavier tasks to cause overload and deadline misses
    tasks = [
        Task(tid=1, period=10, exec_time=8),
        Task(tid=2, period=15, exec_time=7),
        Task(tid=3, period=20, exec_time=10),
    ]

    # Start in RM; scheduler may switch to EDF automatically
    scheduler = AdaptiveScheduler(tasks, mode="RM")

    SIM_TIME = 200  # total time units to simulate
    timeline = []   # which task ran at each time unit

    for _ in range(SIM_TIME):
        running_tid = scheduler.step()
        timeline.append(running_tid)

    # Print basic results
    print("=== Simulation finished ===")
    print("Timeline (task ID at each time unit):")
    print(timeline)

    print("\nTask statistics:")
    for t in tasks:
        print(
            f"Task {t.tid}: "
            f"completed={t.completed_instances}, "
            f"missed_deadlines={t.missed_deadlines}"
        )

    plot_timeline(timeline)
if __name__ == "__main__":
    main()