# visualization.py

import matplotlib.pyplot as plt

// timeline
def plot_timeline(timeline):
    """
    Draw a simple timeline of which task is running at each time unit.
    0 = CPU idle, 1/2/3 = task IDs.
    """
    times = list(range(len(timeline)))
    # Map None -> 0 (idle), task id stays same
    y_values = [0 if tid is None else tid for tid in timeline]
//figure,step shown on
    plt.figure(figsize=(10, 4))
    plt.step(times, y_values, where="post")
    plt.yticks([0, 1, 2, 3], ["Idle", "Task 1", "Task 2", "Task 3"])
    plt.xlabel("Time (units)")
    plt.ylabel("Who is running")
    plt.title("Adaptive Scheduler Timeline")
    plt.tight_layout()

    plt.show()
