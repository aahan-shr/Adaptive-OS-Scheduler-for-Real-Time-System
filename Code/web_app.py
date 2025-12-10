# web_app.py

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from task_model import Task
from scheduler import AdaptiveScheduler


# ---------- Simulation helpers ----------

def run_simulation_mode(mode, t1_p, t1_e, t2_p, t2_e, t3_p, t3_e, sim_time):
    """
    mode: "RM_ONLY", "EDF_ONLY", "ADAPTIVE"
    """
    tasks = [
        Task(tid=1, period=t1_p, exec_time=t1_e),
        Task(tid=2, period=t2_p, exec_time=t2_e),
        Task(tid=3, period=t3_p, exec_time=t3_e),
    ]

    if mode == "RM_ONLY":
        scheduler = AdaptiveScheduler(tasks, mode="RM")
        # Disable adaptation by making threshold unreachable
        scheduler.switch_threshold = 10**9

    elif mode == "EDF_ONLY":
        scheduler = AdaptiveScheduler(tasks, mode="EDF")
        scheduler.switch_threshold = 10**9

    else:  # ADAPTIVE
        scheduler = AdaptiveScheduler(tasks, mode="RM")

    timeline = []
    for _ in range(sim_time):
        running_tid = scheduler.step()
        timeline.append(running_tid)

    total_completed = sum(t.completed_instances for t in tasks)
    total_missed = sum(t.missed_deadlines for t in tasks)

    return tasks, timeline, total_completed, total_missed, scheduler.mode


def plot_timeline(timeline, title):
    times = list(range(len(timeline)))
    y_values = [0 if tid is None else tid for tid in timeline]

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.step(times, y_values, where="post")
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["Idle", "Task 1", "Task 2", "Task 3"])
    ax.set_xlabel("Time (units)")
    ax.set_ylabel("Who is running")
    ax.set_title(title)
    fig.tight_layout()
    return fig


# ---------- Global page setup & CSS ----------

st.set_page_config(
    page_title="Adaptive RTOS Scheduler",
    page_icon="⏱️",
    layout="wide",
)

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: radial-gradient(circle at top left, #020617 0%, #020617 35%, #020617 45%, #020617 55%, #020617 65%, #020617 75%, #020617 100%),
                    radial-gradient(circle at 10% 20%, rgba(20, 230, 200, 0.18) 0, transparent 45%),
                    radial-gradient(circle at 80% 10%, rgba(59, 130, 246, 0.18) 0, transparent 50%),
                    linear-gradient(135deg, #020617, #0a1a2f 40%, #020617 100%);
        color: #f9fafb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Glassmorphism containers */
    .glass-card {
        background: rgba(10, 26, 47, 0.86);
        border-radius: 22px;
        padding: 22px 26px;
        border: 1px solid rgba(20, 230, 200, 0.35);
        box-shadow: 0 24px 70px rgba(0, 0, 0, 0.75);
        backdrop-filter: blur(18px);
    }

    .glass-soft {
        background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(15,23,42,0.9));
        border-radius: 22px;
        padding: 20px 22px;
        border: 1px solid rgba(148, 163, 184, 0.4);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(12px);
    }

    .hero-card {
        background: radial-gradient(circle at top left, rgba(20, 230, 200, 0.15), transparent 55%),
                    radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.12), transparent 55%),
                    linear-gradient(135deg, rgba(10, 26, 47, 0.98), rgba(15, 23, 42, 0.98));
        border-radius: 26px;
        padding: 30px 32px;
        border: 1px solid rgba(20, 230, 200, 0.5);
        box-shadow: 0 28px 80px rgba(0, 0, 0, 0.85);
        position: relative;
        overflow: hidden;
    }

    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        padding: 4px 14px;
        border-radius: 999px;
        background: rgba(20, 230, 200, 0.12);
        border: 1px solid rgba(20, 230, 200, 0.6);
        font-size: 0.76rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #ccfbf1;
    }

    .hero-chip-dot {
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: #14e6c8;
        box-shadow: 0 0 12px rgba(20, 230, 200, 0.9);
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 650;
        letter-spacing: 0.02em;
    }

    .hero-gradient-text {
        background: linear-gradient(120deg, #e0f2fe, #14e6c8, #a5b4fc);
        -webkit-background-clip: text;
        color: transparent;
    }

    .hero-sub {
        color: #9ca3af;
        font-size: 0.98rem;
        max-width: 720px;
    }

    .hero-cta-row {
        margin-top: 1.2rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
    }

    .hero-cta-primary {
        padding: 9px 20px;
        border-radius: 999px;
        border: 1px solid rgba(20, 230, 200, 0.9);
        background: radial-gradient(circle at top left, rgba(20, 230, 200, 0.35), rgba(8,47,73,1));
        color: #ecfeff;
        font-size: 0.88rem;
        font-weight: 500;
        cursor: pointer;
        text-decoration: none;
    }

    .hero-cta-secondary {
        padding: 9px 18px;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.8);
        background: transparent;
        color: #e5e7eb;
        font-size: 0.88rem;
        cursor: pointer;
        text-decoration: none;
    }

    .hero-orb {
        position: absolute;
        right: -60px;
        top: -50px;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        border: 1px solid rgba(56, 189, 248, 0.6);
        box-shadow:
            0 0 50px rgba(20, 230, 200, 0.45),
            0 0 120px rgba(56, 189, 248, 0.35);
        background:
            radial-gradient(circle at 30% 30%, rgba(248, 250, 252, 0.17), transparent 60%),
            radial-gradient(circle at 70% 70%, rgba(56, 189, 248, 0.28), transparent 65%);
        opacity: 0.9;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #020617 40%, #020617 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.4);
    }

    section[data-testid="stSidebar"] .css-1d391kg {
        padding-top: 0.75rem;
    }

    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 600;
        padding-bottom: 0.2rem;
        color: #e5e7eb;
    }

    .sidebar-caption {
        font-size: 0.8rem;
        color: #9ca3af;
    }

    /* Metric cards */
    .metric-card {
        background: radial-gradient(circle at top left, rgba(15,23,42,0.95), rgba(2,6,23,1));
        border-radius: 18px;
        padding: 14px 16px;
        border: 1px solid rgba(148,163,184,0.55);
        box-shadow: 0 12px 32px rgba(0,0,0,0.7);
    }
    .metric-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #9ca3af;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e5e7eb;
    }
    .metric-sub {
        font-size: 0.84rem;
        color: #6b7280;
    }

    /* Footer */
    .footer {
        margin-top: 1.6rem;
        font-size: 0.8rem;
        color: #9ca3af;
        text-align: right;
    }

    /* Section headings & pills */
    .section-pill {
        display: inline-block;
        padding: 4px 11px;
        border-radius: 999px;
        border: 1px solid rgba(56,189,248,0.65);
        background: rgba(15,23,42,0.8);
        font-size: 0.74rem;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #bae6fd;
        margin-bottom: 0.4rem;
    }

    .feature-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        padding: 3px 9px;
        border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.6);
        font-size: 0.74rem;
        color: #9ca3af;
    }

    .feature-dot {
        width: 5px;
        height: 5px;
        border-radius: 999px;
        background: #22d3ee;
    }

    /* Tables */
    .stTable {
        border-radius: 16px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar navigation with session state ----------

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"

pages = ["Home", "About", "Architecture", "Demo & Comparison", "Team", "Contact"]

st.sidebar.markdown('<div class="sidebar-title">Adaptive RTOS Scheduler</div>', unsafe_allow_html=True)
page = st.sidebar.radio(
    "Go to",
    pages,
    index=pages.index(st.session_state.current_page),
    label_visibility="collapsed",
    key="nav_radio",
)

st.sidebar.markdown("---")
st.sidebar.subheader("Project Snapshot")
st.sidebar.markdown(
    """
    **Title:** Adaptive OS Scheduler for Real-Time Systems  
    **Domain:** Real-Time Operating Systems  
    **Interface:** Streamlit Web App  
    """.strip()
)
st.sidebar.markdown("---")
st.sidebar.caption("Use the menu above to explore sections.")


# ---------- Common header (for non-Home pages) ----------

if page != "Home":
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-pill">Real-Time Systems · Scheduling</div>
            <h1 style="margin-bottom:0.3rem; font-size:2.05rem;">
                ⏱️ Adaptive OS Scheduler for <span style="color:#bfdbfe;">Real-Time Systems</span>
            </h1>
            <p style="color:#9ca3af; max-width:920px; font-size:0.95rem; margin-bottom:0.25rem;">
                A web-based simulator demonstrating how an <strong>adaptive scheduler</strong> can switch
                between <strong>Rate Monotonic (RM)</strong> and <strong>Earliest Deadline First (EDF)</strong>
                strategies based on observed deadline misses in real-time workloads.
            </p>
            <p style="color:#6b7280; font-size:0.85rem;">
                Developed by <strong>Ansh</strong>, <em>Your College Name</em>,
                under the guidance of <strong>Dr. Gurbinder Singh Brar</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")


# ===================== PAGE 1: HOME (HERO) =====================

if page == "Home":
    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-orb"></div>
            <div class="hero-pill">
                <span class="hero-chip-dot hero-chip-dot"></span>
                LIVE SCHEDULER SIMULATION
            </div>
            <h1 class="hero-title" style="margin-top:0.6rem; margin-bottom:0.35rem;">
                An Intelligent <span class="hero-gradient-text">Adaptive Scheduler</span><br />
                for Real-Time Operating Systems
            </h1>
            <p class="hero-sub">
                Explore how a scheduler can start with <strong>Rate Monotonic (RM)</strong>, monitor
                <strong>deadline misses</strong>, and intelligently switch to
                <strong>Earliest Deadline First (EDF)</strong> under overload – all visualized in a
                live, interactive web simulator.
            </p>
            <div class="hero-cta-row">
                <a href="#" onclick="window.parent.postMessage({type: 'streamlit:nav', page: 'Demo & Comparison'}, '*'); return false;" class="hero-cta-primary">
                    ▶ Launch Demo & Comparison
                </a>
                <a href="#" onclick="window.parent.postMessage({type: 'streamlit:nav', page: 'About'}, '*'); return false;" class="hero-cta-secondary">
                    Learn about the concept
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    col1, col2 = st.columns([1.5, 1.2])

    with col1:
        st.markdown(
            """
            <div class="glass-soft">
                <div class="section-pill">Welcome Note</div>
                <h3 style="margin-top:0.25rem; font-size:1.15rem; margin-bottom:0.2rem;">
                    Greetings, <span style="color:#bfdbfe;">Dr. Gurbinder&nbsp;Singh&nbsp;Brar</span>
                </h3>
                <p style="color:#d1d5db; max-width:840px; font-size:0.95rem; line-height:1.6;">
                    It is a privilege to present this project on
                    <strong>Adaptive OS Scheduler for Real-Time Systems</strong>. This work is a step
                    towards understanding how an operating system can react intelligently to changing
                    workloads in real-time environments.
                </p>
                <p style="color:#9ca3af; max-width:840px; font-size:0.9rem; margin-top:0.6rem;">
                    I sincerely thank you, Sir, for your guidance, encouragement, and for motivating
                    me to explore this topic in depth. Your support has been a strong driving force
                    throughout the development of this project.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="glass-soft">
                <h3 style="margin-top:0; font-size:1.05rem;">Project Snapshot</h3>
                <ul style="color:#e5e7eb; font-size:0.9rem; line-height:1.55; padding-left:1rem; margin-bottom:0.6rem;">
                    <li><strong>Domain:</strong> Real-Time Operating Systems</li>
                    <li><strong>Focus:</strong> RM, EDF & Adaptive Scheduling</li>
                    <li><strong>Language:</strong> Python</li>
                    <li><strong>Interface:</strong> Streamlit Web Application</li>
                    <li><strong>Student:</strong> Ansh</li>
                    <li><strong>Guide:</strong> Dr. Gurbinder Singh Brar</li>
                </ul>
                <span class="feature-badge">
                    <span class="feature-dot"></span>
                    Live comparison of RM, EDF & Adaptive
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            Home · Hero section, greeting, and quick project snapshot.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===================== PAGE 2: ABOUT =====================

elif page == "About":
    col1, col2 = st.columns([1.7, 1.3])

    with col1:
        st.markdown('<div class="section-pill">Concept & Motivation</div>', unsafe_allow_html=True)
        st.subheader("Why Adaptive Scheduling for Real-Time Systems?")
        st.markdown(
            """
            Real-time systems execute tasks that must complete within strict time limits
            (deadlines). Missing a deadline can cause incorrect behaviour or even a
            system failure. Traditional schedulers such as
            **Rate Monotonic (RM)** and **Earliest Deadline First (EDF)** follow fixed
            policies and cannot react to runtime changes in workload.
            
            This project explores an **adaptive scheduler** that:
            
            - models periodic real-time tasks (period, execution time & deadlines),
            - starts with **RM scheduling** (shorter period ⇒ higher priority),
            - continuously monitors **deadline misses** over time,
            - and automatically switches to **EDF** when overload is detected.
            
            The idea is to show that a scheduler which can change its strategy in response
            to real-time performance can behave more robustly than a purely static one,
            especially when the CPU is heavily loaded.
            """
        )

        st.subheader("Key Capabilities of the Simulator")
        st.markdown(
            """
            - Discrete-time simulation of periodic real-time tasks  
            - Configurable task set: period and execution time for three tasks  
            - Support for **RM-only**, **EDF-only** and **Adaptive** strategies  
            - Automatic policy switch based on recent deadline-miss history  
            - Visual CPU schedule timelines for all three modes  
            - Numerical comparison of completed jobs and missed deadlines  
            - User-friendly, web-based interface built with Streamlit  
            """
        )

    with col2:
        st.markdown(
            """
            <div class="glass-soft">
                <h3 style="margin-top:0; font-size:1.05rem;">At a Glance</h3>
                <ul style="color:#e5e7eb; font-size:0.9rem; line-height:1.6;">
                    <li>Models periodic tasks on a single CPU core</li>
                    <li>Implements RM and EDF scheduling logic</li>
                    <li>Monitors deadline misses in a sliding window</li>
                    <li>Switches from RM → EDF when overload is detected</li>
                    <li>Provides visual timelines and a comparison table</li>
                </ul>
                <p style="color:#9ca3af; font-size:0.86rem; margin-top:0.4rem;">
                    Use the <strong>Demo & Comparison</strong> page to interactively
                    configure workloads and observe how each strategy behaves.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            About · Problem statement, objectives, and high-level motivation.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===================== PAGE 3: ARCHITECTURE =====================

elif page == "Architecture":
    c1, c2 = st.columns([1.6, 1.4])

    with c1:
        st.markdown('<div class="section-pill">System Design</div>', unsafe_allow_html=True)
        st.subheader("Conceptual Architecture")
        st.markdown(
            """
            The simulator is organised into three main layers:
            
            - **Task Model**  
              Each periodic task is represented by an object holding:
              period, execution time, remaining execution, next release time,
              deadline, and counters for completed instances and missed deadlines.
            
            - **Adaptive Scheduler**  
              - Maintains a ready queue of tasks that are eligible to run.  
              - Supports two base policies:
                - **Rate Monotonic (RM)** – static priority based on period.  
                - **Earliest Deadline First (EDF)** – dynamic priority based on the nearest deadline.  
              - Monitors deadline misses over a sliding time window.  
              - If the number of misses exceeds a threshold while in RM mode,
                the scheduler switches to EDF for better overload handling.
            
            - **Monitoring & Web UI Layer**  
              - Runs the simulation in discrete time steps for a user-specified duration.  
              - Collects statistics such as total jobs completed and deadlines missed.  
              - Visualizes the CPU schedule as a step plot and displays a
                comparison table of RM, EDF, and Adaptive modes.
            """
        )

        st.subheader("Algorithms Used")
        st.markdown(
            """
            **Rate Monotonic (RM)**  
            - Static-priority algorithm for periodic tasks.  
            - A shorter period ⇒ higher priority.  
            - Works under known utilisation bounds.

            **Earliest Deadline First (EDF)**  
            - Dynamic-priority algorithm.  
            - At each instant, the job with the earliest absolute deadline runs.  
            - Optimal on a single processor.

            **Adaptive Strategy**  
            - Starts in RM mode.  
            - Tracks recent deadline misses (e.g., using a sliding window).  
            - When misses exceed a threshold, policy switches to EDF.  
            - This makes the scheduler responsive to runtime overload.
            """
        )

    with c2:
        st.subheader("Architecture Highlights")
        st.markdown(
            """
            <div class="glass-soft">
                <ul style="color:#e5e7eb; font-size:0.9rem; line-height:1.6;">
                    <li><strong>Task Model:</strong> captures timing constraints and state.</li>
                    <li><strong>Scheduler Core:</strong> plug-in policies (RM / EDF).</li>
                    <li><strong>Adaptation Logic:</strong> monitors deadline misses.</li>
                    <li><strong>Statistics Engine:</strong> computes completed and missed jobs.</li>
                    <li><strong>Visualization Layer:</strong> Matplotlib step plots for CPU timelines.</li>
                    <li><strong>Front-end:</strong> Streamlit-based interactive UI.</li>
                </ul>
                <p style="color:#9ca3af; font-size:0.86rem; margin-top:0.4rem;">
                    The same architecture is used in three modes: RM-only, EDF-only and
                    Adaptive (RM → EDF). Only the scheduling policy and adaptation
                    behaviour change.
                </p>
            </div>
            """
        )

    st.markdown(
        """
        <div class="footer">
            Architecture · Internal components, algorithms and interaction between modules.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===================== PAGE 4: DEMO & COMPARISON =====================

elif page == "Demo & Comparison":
    left_col, right_col = st.columns([1.05, 2.0])

    # ---- LEFT: controls ----
    with left_col:
        st.markdown('<div class="section-pill">Simulation Input</div>', unsafe_allow_html=True)
        st.subheader("Simulation Controls")

        st.markdown(
            "<p style='color:#9ca3af; font-size:0.9rem;'>"
            "Configure three periodic real-time tasks and the total simulation duration. "
            "The same task set will be used for RM-only, EDF-only and Adaptive runs."
            "</p>",
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown("**Task 1 (highest priority in RM)**")
            c1a, c1b = st.columns(2)
            t1_p = c1a.number_input("Period", min_value=1, value=10, step=1)
            t1_e = c1b.number_input("Execution time", min_value=1, value=8, step=1)

            st.markdown("---")

            st.markdown("**Task 2**")
            c2a, c2b = st.columns(2)
            t2_p = c2a.number_input("Period ", min_value=1, value=15, step=1)
            t2_e = c2b.number_input("Execution time ", min_value=1, value=7, step=1)

            st.markdown("---")

            st.markdown("**Task 3**")
            c3a, c3b = st.columns(2)
            t3_p = c3a.number_input("Period  ", min_value=1, value=20, step=1)
            t3_e = c3b.number_input("Execution time  ", min_value=1, value=10, step=1)

            st.markdown("---")

            sim_time = st.number_input(
                "Simulation time (time units)",
                min_value=20,
                value=200,
                step=10,
            )

            st.caption(
                "Tip: choose tighter periods and longer execution times to force overload and "
                "observe how the Adaptive mode reacts."
            )

            run_btn = st.button("▶ Run RM, EDF & Adaptive", use_container_width=True)

    # ---- RIGHT: results & comparison ----
    with right_col:
        placeholder_info = st.empty()
        placeholder_charts_top = st.empty()
        placeholder_chart_bottom = st.empty()
        placeholder_metrics = st.empty()

        if run_btn:
            # Run RM, EDF, Adaptive
            (tasks_rm, tl_rm, comp_rm, miss_rm, _,
             ) = run_simulation_mode("RM_ONLY", t1_p, t1_e, t2_p, t2_e, t3_p, t3_e, sim_time)

            (tasks_edf, tl_edf, comp_edf, miss_edf, _,
             ) = run_simulation_mode("EDF_ONLY", t1_p, t1_e, t2_p, t2_e, t3_p, t3_e, sim_time)

            (tasks_ad, tl_ad, comp_ad, miss_ad, final_mode,
             ) = run_simulation_mode("ADAPTIVE", t1_p, t1_e, t2_p, t2_e, t3_p, t3_e, sim_time)

            with placeholder_charts_top:
                st.subheader("CPU Schedule Timelines (RM vs EDF)")
                c_top1, c_top2 = st.columns(2)
                with c_top1:
                    fig_rm = plot_timeline(tl_rm, "RM Only")
                    st.pyplot(fig_rm, use_container_width=True)
                with c_top2:
                    fig_edf = plot_timeline(tl_edf, "EDF Only")
                    st.pyplot(fig_edf, use_container_width=True)

            with placeholder_chart_bottom:
                st.subheader("Adaptive Mode Timeline")
                fig_ad = plot_timeline(tl_ad, "Adaptive (RM → EDF)")
                st.pyplot(fig_ad, use_container_width=True)

            # Comparison table
            data = [
                {"Method": "RM Only", "Total Jobs Completed": comp_rm, "Deadlines Missed": miss_rm},
                {"Method": "EDF Only", "Total Jobs Completed": comp_edf, "Deadlines Missed": miss_edf},
                {"Method": "Adaptive (RM→EDF)", "Total Jobs Completed": comp_ad, "Deadlines Missed": miss_ad},
            ]
            df = pd.DataFrame(data)

            with placeholder_metrics:
                st.subheader("Comparison Summary")
                st.table(df)

            with placeholder_info:
                st.markdown(
                    """
                    <p style="color:#9ca3af; font-size:0.88rem; margin-top:0.6rem;">
                    The same task set is scheduled under three different strategies:
                    <strong>RM Only</strong> uses fixed priorities based on task periods,
                    <strong>EDF Only</strong> always runs the job with the earliest deadline,
                    and <strong>Adaptive</strong> starts in RM mode but switches to EDF when a
                    threshold of deadline misses is observed. The table above summarizes how
                    many jobs each method completes and how many deadlines are missed.
                    </p>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            with placeholder_info:
                st.info(
                    "Set task parameters on the left and click **Run RM, EDF & Adaptive** "
                    "to visualise and compare scheduling behaviour."
                )

    st.markdown(
        """
        <div class="footer">
            Demo & Comparison · Live interactive simulation and numerical comparison.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===================== PAGE 5: TEAM =====================

elif page == "Team":
    st.markdown('<div class="section-pill">People Behind the Project</div>', unsafe_allow_html=True)
    st.subheader("Student & Guide")

    st.markdown(
        """
        <div class="glass-soft">
            <h3 style="margin-top:0; font-size:1.05rem;">Project Details</h3>
            <p style="color:#e5e7eb; font-size:0.92rem; line-height:1.6;">
                <strong>Student:</strong> Ansh<br>
                <strong>College:</strong> Your College Name<br>
                <strong>Department:</strong> Computer Science / Information Technology (edit as needed)<br>
                <strong>Guide:</strong> Dr. Gurbinder Singh Brar
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Future Scope")
    st.markdown(
        """
        - Support for sporadic and aperiodic tasks.  
        - More advanced adaptation policies (priority boosting, task dropping, mixed-criticality).  
        - Analysis of response times and jitter, not just deadline misses.  
        - Export of detailed simulation logs as CSV/PDF for report generation.  
        - Extension to multi-core scheduling and mixed-criticality systems.  
        - Deployment of the simulator online for remote experimentation and teaching.
        """
    )

    st.markdown(
        """
        <div class="footer">
            Team · Student, guide, and future expansion possibilities.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ===================== PAGE 6: CONTACT =====================

elif page == "Contact":
    st.markdown('<div class="section-pill">Get in Touch</div>', unsafe_allow_html=True)
    st.subheader("Contact & Acknowledgements")

    c1, c2 = st.columns([1.4, 1.6])

    with c1:
        st.markdown(
            """
            <div class="glass-soft">
                <h3 style="margin-top:0; font-size:1.05rem;">Contact Information</h3>
                <p style="color:#e5e7eb; font-size:0.9rem; line-height:1.6;">
                    <strong>Student:</strong> Ansh<br>
                    <strong>Guide:</strong> Dr. Gurbinder Singh Brar<br>
                    <strong>Project:</strong> Adaptive OS Scheduler for Real-Time Systems
                </p>
                <p style="color:#9ca3af; font-size:0.86rem;">
                    (You can add your email, GitHub, LinkedIn or college contact details here.)
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            """
            <div class="glass-soft">
                <h3 style="margin-top:0; font-size:1.05rem;">Acknowledgements</h3>
                <p style="color:#e5e7eb; font-size:0.9rem; line-height:1.6;">
                    I express my heartfelt gratitude to <strong>Dr. Gurbinder Singh Brar</strong>
                    for his continual guidance, encouragement, and valuable feedback throughout
                    this project. I am also thankful to my department and faculty members for
                    providing the resources and environment needed to carry out this work.
                </p>
                <p style="color:#9ca3af; font-size:0.86rem;">
                    This simulator is intended as a learning tool to understand how adaptive
                    scheduling can enhance robustness in real-time systems.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="footer">
            Contact · Acknowledgements and contact placeholders.
        </div>
        """,
        unsafe_allow_html=True,
    )