import streamlit as st
import random
import math
import time
import json
import os
from datetime import datetime

# Get the directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tasks.json")

# Function to save tasks and meal times
def save_tasks():
    data = {
        "must_do_tasks": st.session_state.must_do_tasks,
        "want_to_do_tasks": st.session_state.want_to_do_tasks,
        "tasks_for_later": st.session_state.tasks_for_later,
        "completed_tasks": st.session_state.completed_tasks,
        "doing_tasks": st.session_state.doing_tasks,
        "past_tasks": st.session_state.past_tasks,
        "total_work_time": st.session_state.total_work_time,
        "break_interval": st.session_state.break_interval,
        "break_time": st.session_state.break_time,
        "current_task": st.session_state.current_task,
        "total_time": st.session_state.total_time,
        "meal_times": st.session_state.meal_times,
        "start_time": st.session_state.start_time,
        "total_task_time" : st.session_state.total_task_time

    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# Function to load tasks and meal times
def load_tasks():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                data = json.loads(content) if content else {}

                st.session_state.must_do_tasks = data.get("must_do_tasks", [])
                st.session_state.want_to_do_tasks = data.get("want_to_do_tasks", [])
                st.session_state.tasks_for_later = data.get("tasks_for_later", [])
                st.session_state.completed_tasks = data.get("completed_tasks", [])
                st.session_state.doing_tasks = data.get("doing_tasks", [])
                st.session_state.past_tasks = data.get("past_tasks", [])
                st.session_state.total_work_time = data.get("total_work_time", 0)
                st.session_state.break_interval = data.get("break_interval", 0)
                st.session_state.break_time = data.get("break_time", 0)
                st.session_state.current_task = data.get("current_task", None)
                st.session_state.total_time = data.get("total_time", 0)
                st.session_state.meal_times = data.get("meal_times", {})
                st.session_state.start_time = data.get("start_time", 0)
                st.session_state.total_task_time = sum(task[1] for task in st.session_state.must_do_tasks + st.session_state.want_to_do_tasks)
        except:
            st.session_state.must_do_tasks = []
            st.session_state.want_to_do_tasks = []
            st.session_state.completed_tasks = []
            st.session_state.doing_tasks = []
            st.session_state.meal_times = {}


def distribute_tasks():
    must_do_total_time = sum(task[1] for task in st.session_state.must_do_tasks)
    want_to_do_total_time = sum(task[1] for task in st.session_state.want_to_do_tasks)

    total_time = must_do_total_time + want_to_do_total_time

    if total_time == 0:
        st.warning("You have no tasks to distribute.")
        return

    target_must_do_time = 0.8 * st.session_state.total_work_time
    target_want_to_do_time = 0.2 * st.session_state.total_work_time

    doing_tasks = []
    must_do_time_accumulated = 0
    want_to_do_time_accumulated = 0

    random.shuffle(st.session_state.must_do_tasks)
    random.shuffle(st.session_state.want_to_do_tasks)

    for task in st.session_state.must_do_tasks:
        if must_do_time_accumulated + task[1] <= target_must_do_time:
            doing_tasks.append(task)
            must_do_time_accumulated += task[1]

    for task in st.session_state.want_to_do_tasks:
        if want_to_do_time_accumulated + task[1] <= target_want_to_do_time:
            doing_tasks.append(task)
            want_to_do_time_accumulated += task[1]

    st.session_state.doing_tasks = doing_tasks
    save_tasks()

def screen_1():
    st.header("Set Your Work Schedule")
    work_time = st.number_input("How many hours do you want to work today?", min_value=1, max_value=14, value=8)
    break_interval = st.number_input("After how many minutes should you take a break?", min_value=5, max_value=120, value=45)

    st.subheader("Set Meal Times and Foods")
    lunch_time = st.time_input("Lunch Time", value=datetime.strptime("13:00", "%H:%M").time())
    lunch_food = st.text_input("What will you eat for lunch?")
    snack_time = st.time_input("Snack time", value=datetime.strptime("17:00", "%H:%M").time())
    snack_food = st.text_input("What's your in-between snack?")
    dinner_time = st.time_input("Dinner Time", value=datetime.strptime("20:00", "%H:%M").time())
    dinner_food = st.text_input("What will you eat for dinner?")

    if st.button("Set Tasks"):
        st.session_state.total_work_time = work_time * 60
        st.session_state.break_interval = break_interval
        st.session_state.meal_times = {
            "lunch": {"time": lunch_time.strftime("%H:%M"), "food": lunch_food},
            "snack": {"time": snack_time.strftime("%H:%M"), "food": snack_food},
            "dinner": {"time": dinner_time.strftime("%H:%M"), "food": dinner_food}
        }
        st.session_state.screen = 2
        save_tasks()
        st.rerun()


def screen_2():
    st.session_state.total_task_time = sum(math.ceil(task[1] / 15) * 15 for task in st.session_state.must_do_tasks + st.session_state.want_to_do_tasks)
    st.header("Define Your Tasks")
    st.subheader(f"Total task time: {st.session_state.total_task_time / 60} hours")

    task_name = st.text_input("Task Name")
    task_time = st.number_input("Task Duration (minutes)", min_value=1, max_value=180, value=30)
    task_type = st.selectbox("Task Type", ["Must Do", "Want To Do", "For Later"])
    total_task_time = st.session_state.total_task_time
    goal_work_time = st.session_state.total_work_time

    if st.button("Add Task"):
        task = (task_name, task_time)
        if task_type == "Must Do":
            st.session_state.must_do_tasks.append(task)
        elif task_type == "Want To Do":
            st.session_state.want_to_do_tasks.append(task)
        else:
            st.session_state.tasks_for_later.append(task)
        if total_task_time > goal_work_time:
            st.warning(f"⚠️ Total task time exceeds the work time of {goal_work_time} hours.")
        save_tasks()
        st.rerun()

    if st.button("Distribute Tasks"):
        distribute_tasks()
        st.session_state.last_break_time = time.time()  # Track session/break start time
        st.session_state.on_break = False  # Not currently on a break
        st.session_state.break_start_time = None  # Will be used later
        st.session_state.recommended_break_time = st.session_state.total_work_time / 3  # initializing a recommended break time
        st.session_state.screen = 3
        st.rerun()

    if "must_do_tasks" not in st.session_state:
        st.session_state.must_do_tasks = []
    if "want_to_do_tasks" not in st.session_state:
        st.session_state.want_to_do_tasks = []
    if "tasks_for_later" not in st.session_state:
        st.session_state.tasks_for_later = []

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### ⚠️ Must Do Tasks")
        for i, task in enumerate(st.session_state.must_do_tasks):
            if st.button("📥", key=f"archive_must_{i}"):
                st.session_state.tasks_for_later.append(task)
                del st.session_state.must_do_tasks[i]
                save_tasks()
                st.rerun()
            if st.button("❌", key=f"delete_must_{i}"):
                    # Remove the specific task and adjust total task time
                    removed_task = st.session_state.must_do_tasks.pop(i)
                    st.session_state.total_work_time -= removed_task[1]
                    save_tasks()
                    st.rerun()  # Refresh list
            st.write(f"{task[0]} - {task[1]} min")

    with col2:
        st.write("### 🕺🏻 Want To Do Tasks")
        for i, task in enumerate(st.session_state.want_to_do_tasks):
            if st.button("❌", key=f"delete_want_{i}"):
                # Remove the specific task and adjust total task time
                removed_task = st.session_state.want_to_do_tasks.pop(i)
                st.session_state.total_work_time -= removed_task[1]
                save_tasks()
                st.rerun()  # Refresh list
            st.write(f"{task[0]} - {task[1]} min")
        

    with col3:
        st.write("### 📥 Tasks For Another Time")
        for i, task in enumerate(st.session_state.tasks_for_later):
            if st.button("↩️", key=f"restore_later_{i}"):
                st.session_state.must_do_tasks.append(task)
                del st.session_state.tasks_for_later[i]
                save_tasks()
                st.rerun()
            st.write(f"{task[0]} - {task[1]} min")


def screen_3():
    st.header("Working on Tasks")
    st.subheader(f"Recommendate Break Time: {int(st.session_state.recommended_break_time)} min")

    now = time.time()

    # Check if we're currently on a break
    if st.session_state.on_break:
        st.subheader("Take a 15 minute break")
        goal_finish_time = datetime.fromtimestamp(st.session_state.break_start_time + 15 * 60).strftime('%H:%M')
        st.subheader(f"Goal Finish Time: {goal_finish_time}")

        if st.button("Done, Continue Working") or st.button("Skip, Continue Working"):
            actual_break_time = int((now - st.session_state.break_start_time) / 60)
            st.session_state.total_time += actual_break_time
            st.session_state.recommended_break_time -= actual_break_time
            if st.session_state.recommended_break_time < 0:
                st.session_state.recommended_break_time = 0  # Don't go negative
            st.session_state.on_break = False
            st.session_state.last_break_time = now
            st.session_state.current_task = random.choice(st.session_state.doing_tasks)
            st.session_state.start_time = now
            save_tasks()
            st.rerun()
        return  # Exit early so we don’t show task


    if not st.session_state.doing_tasks:
        st.write("All tasks completed!")
        st.session_state.screen = 4
        save_tasks()
        st.rerun()

    if st.session_state.current_task is None and st.session_state.doing_tasks:
        st.session_state.current_task = random.choice(st.session_state.doing_tasks)
        st.session_state.start_time = time.time()

    if st.session_state.current_task:
        task_name, task_duration = st.session_state.current_task
        st.subheader(f"Current Task: {task_name} - {task_duration} min")
        st.subheader(f"Goal Finish Time: {(datetime.fromtimestamp(st.session_state.start_time + task_duration * 60)).strftime('%H:%M')}")


        if st.button("Done, Shuffle Next Task"):
            actual_time_spent = int((time.time() - st.session_state.start_time) / 60)
            st.session_state.completed_tasks.append(st.session_state.current_task)
            st.session_state.total_time += actual_time_spent
            st.subheader(f"Total Work Time: {st.session_state.total_time}")
            if st.session_state.current_task in st.session_state.doing_tasks:
                st.session_state.doing_tasks.remove(st.session_state.current_task)
            if st.session_state.current_task in st.session_state.must_do_tasks:
                st.session_state.must_do_tasks.remove(st.session_state.current_task)
            if st.session_state.current_task in st.session_state.want_to_do_tasks:
                st.session_state.want_to_do_tasks.remove(st.session_state.current_task)

            # ⏸️ Break check
            if now - st.session_state.last_break_time >= st.session_state.break_interval * 60:
                st.session_state.on_break = True
                st.session_state.break_start_time = now
                save_tasks()
                st.rerun()

            st.session_state.current_task = None
            save_tasks()
            st.rerun()

        if st.button("Skip, Shuffle Next Task"):
            st.session_state.current_task = random.choice(st.session_state.doing_tasks)

            # ⏸️ Break check
            if now - st.session_state.last_break_time >= st.session_state.break_interval * 60:
                st.session_state.on_break = True
                st.session_state.break_start_time = now
                save_tasks()
                st.rerun()

            st.session_state.start_time = time.time()
            save_tasks()
            st.rerun()


def screen_4():
    st.header(f"Congrats 🎉 You reached your goal of {st.session_state.total_work_time / 60} hours!")
    st.markdown("#### Completed Tasks:")
    for task, time in st.session_state.completed_tasks:
        st.write(f"{task} - {time} min")
    st.markdown(f"#### Total Time Worked: {st.session_state.total_time / 60} hours")
    st.session_state.estimated_time = sum(task[1] for task in st.session_state.completed_tasks)
    st.markdown(f"#### How long you thought it would take: {st.session_state.estimated_time / 60} hours")
    st.markdown("#### Past Tasks:")
    for task, time in st.session_state.past_tasks:
        st.write(f"{task} - {time} min")
    if st.button("New Session"):
        st.session_state.past_tasks.extend(st.session_state.completed_tasks)
        st.session_state.completed_tasks = []
        st.session_state.screen = 1
        st.session_state.doing_tasks = []      # Clear only doing tasks for the current session
        st.session_state.current_task = None
        st.session_state.total_time = 0       
        st.session_state.start_time = None
        st.session_state.loaded = False
        st.estimated_time = 0
        save_tasks()  # Save without deleting Must Do, Want To Do, or Tasks For Later
        st.rerun()


def main():
    st.title("Daily Task Manager")

    if "screen" not in st.session_state:
        st.session_state.screen = 1
    if "meal_times" not in st.session_state:
        st.session_state.meal_times = {}
    if "loaded" not in st.session_state or st.session_state.loaded == False:
        load_tasks()
        st.session_state.loaded = True
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "total_task_time" not in st.session_state:
        st.session_state.total_task_time = sum(task[1] for task in st.session_state.must_do_tasks + st.session_state.want_to_do_tasks)
    if "total_work_time" not in st.session_state:
        st.session_state.work_time = 0
    if "estimated_time" not in st.session_state:
        st.session_state.estimated_time = 0
    if "past_tasks" not in st.session_state:
        st.session_state.past_tasks = []
    if "last_break_time" not in st.session_state:
        st.session_state.last_break_time = time.time()
    if "on_break" not in st.session_state:
        st.session_state.on_break = False
    if "break_start_time" not in st.session_state:
        st.session_state.break_start_time = None
    if "recommended_break_time" not in st.session_state:
        st.session_state.recommended_break_time = 0

    if st.session_state.screen == 1:
        screen_1()
    elif st.session_state.screen == 2:
        screen_2()
    elif st.session_state.screen == 3:
        screen_3()
    elif st.session_state.screen == 4:
        screen_4()


if __name__ == "__main__":
    main()
