# Adaptive OS Scheduler for Real-Time Systems

This project implements an **Adaptive Operating System Scheduler** designed for **real-time systems**.  
The scheduler dynamically adjusts task priorities, detects deadline misses, and aims to optimize CPU utilization for periodic and aperiodic tasks.

---

## 🚀 Features

- Support for common real‑time scheduling strategies:
  - **Rate Monotonic Scheduling (RMS)**
  - **Earliest Deadline First (EDF)**
- Dynamic task priority handling
- Deadline miss detection and reporting
- Basic CPU utilization calculation
- Modular code layout for easier extension
- Simple CLI‑style configuration (can be extended)

---

## 📂 Project Structure

> Update this section if your actual file names differ.

```text
Adaptive-OS-Scheduler-for-Real-Time-System/
├── Code/
│   ├── main.c          # Entry point / simulation driver
│   ├── scheduler.c     # Core scheduling logic (RMS/EDF)
│   ├── scheduler.h     # Scheduler declarations
│   ├── tasks.c         # Task definitions and helpers
│   ├── tasks.h         # Task structure and prototypes
│   └── utils.c         # Optional helper utilities
├── Docs/
│   └── design-notes.md # Design decisions / theory notes
└── README.md           # Project overview (this file)
```

---

## 🧠 High‑Level Design

The scheduler operates over a set of tasks **T = {τ₁, τ₂, …, τₙ}**, where each task typically has:

- `period` – how often the task must execute  
- `execution_time` – worst‑case CPU time required  
- `deadline` – relative or absolute deadline  
- `id` / `name` – identifier for logging

**Basic flow:**

1. Load or define the task set.
2. Select a scheduling policy (RMS or EDF).
3. For each tick or time interval:
   - Determine the ready tasks.
   - Select the highest‑priority task.
   - Simulate execution for one time unit (or slice).
   - Update remaining execution and deadlines.
4. Record any **deadline misses** and log scheduling decisions.

This design is intended for **educational and experimental** purposes, not for production use.

---

## 🛠 Prerequisites

- A C compiler such as **GCC** or **Clang**
- **Git** (for cloning and revision tracking)
- A terminal / command prompt

---

## ▶️ Build and Run

From the project root (where this README is located), run:

```bash
cd Code

# Example compile command (adjust files as needed)
gcc main.c scheduler.c tasks.c -o scheduler

# Run the scheduler
./scheduler
```

On Windows (using MinGW or similar):

```bash
cd Code
gcc main.c scheduler.c tasks.c -o scheduler.exe
scheduler.exe
```

> If your filenames differ, include the correct `.c` files in the compile command.

---

## 🧪 Example Extensions

Possible improvements you can add for your project or coursework:

- Additional algorithms (e.g., **Least Laxity First**)
- Task sets loaded from a configuration file
- Logging to a text file for analysis
- Gantt‑chart style output for visualization
- Priority inheritance or other real‑time protocols

---

## 📚 Academic Context

This project can be used to demonstrate:

- Differences between **fixed‑priority** (RMS) and **dynamic‑priority** (EDF) scheduling
- CPU utilization bounds for real‑time systems
- Effects of overload and deadline misses
- Basic real‑time OS scheduler design concepts

You can link this implementation to theory from real‑time systems textbooks or course slides.

---

## 🤝 Contributors

- **Aahan** (primary developer)  
- Additional team members can be listed here.

Feel free to update this section with your actual team details.

---

## 📄 License

This project is intended primarily for **educational use**.  
You may adapt and modify the code for assignments, labs, and learning purposes.

If you want, you can add a formal license (e.g., MIT) here.
