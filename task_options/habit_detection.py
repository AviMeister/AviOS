# Habit pattern detection for tasks

from task_options.state import get_today_name, save_tasks, task_list


def get_related_tasks(task_name):
    normalized_name = task_name.strip().lower()

    return [
        task
        for task in task_list
        if task["name"].strip().lower() == normalized_name
    ]


def count_completed_related_tasks(task_name):
    return sum(1 for task in get_related_tasks(task_name) if task.get("completed", False))


def count_related_tasks_done_today(task_name):
    today_name = get_today_name()
    done_today_count = 0

    for task in get_related_tasks(task_name):
        for done_entry in task.get("done_history", []):
            if done_entry.get("weekday") == today_name:
                done_today_count += 1

    return done_today_count


def habit_prompt_is_due(task_index):
    task = task_list[task_index]

    if task.get("habit_candidate", False) or task.get("habit_prompt_dismissed", False):
        return False

    completed_count = count_completed_related_tasks(task["name"])
    same_day_count = count_related_tasks_done_today(task["name"])

    return completed_count >= 3 or same_day_count >= 2


def apply_habit_decision(task_index, accepted):
    task = task_list[task_index]

    if accepted:
        for related_task in get_related_tasks(task["name"]):
            related_task["habit_candidate"] = True
    else:
        task["habit_prompt_dismissed"] = True

    save_tasks()


def ask_about_habit(task_index):
    if not habit_prompt_is_due(task_index):
        return

    task = task_list[task_index]
    print(f"\n You seem to do '{task['name']}' often.")
    answer = input(" Should AviOS remember this as a habit idea? y/n: ").strip().lower()
    accepted = answer == "y"
    apply_habit_decision(task_index, accepted)

    if accepted:
        print("\n Saved as a habit idea for later.")
    else:
        print("\n No problem. Keeping it as a task.")
