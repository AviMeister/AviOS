# View and manage tasks for AviOS

from task_options.display import get_task_order, print_task_line, show_task_summary
from task_options.state import get_current_timestamp, get_today_name, save_tasks, task_list


def view_tasks():
    print("\n Tasks:")

    task_order = get_task_order()

    if len(task_order) == 0:
        print(" No tasks yet.")
        return

    for task_number, task_index in enumerate(task_order, start=1):
        task = task_list[task_index]
        print_task_line(task_number, task)

    show_task_summary()


def choose_task():
    task_choice = input("\n Select a task number, or press Enter to go back: ").strip()

    if task_choice == "":
        return None

    if not task_choice.isdigit():
        print("\n Please enter a task number.")
        return None

    task_number = int(task_choice)
    task_order = get_task_order()

    if task_number < 1 or task_number > len(task_order):
        print("\n That task number does not exist.")
        return None

    return task_order[task_number - 1]


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


def ask_about_habit(task_index):
    task = task_list[task_index]

    if task.get("habit_candidate", False) or task.get("habit_prompt_dismissed", False):
        return

    completed_count = count_completed_related_tasks(task["name"])
    same_day_count = count_related_tasks_done_today(task["name"])

    if completed_count < 3 and same_day_count < 2:
        return

    print(f"\n You seem to do '{task['name']}' often.")
    answer = input(" Should AviOS remember this as a habit idea? y/n: ").strip().lower()

    if answer == "y":
        for related_task in get_related_tasks(task["name"]):
            related_task["habit_candidate"] = True

        print("\n Saved as a habit idea for later.")
    else:
        task["habit_prompt_dismissed"] = True
        print("\n No problem. Keeping it as a task.")

    save_tasks()


def mark_task_done(task_index):
    task_list[task_index]["completed"] = True
    task_list[task_index].setdefault("done_history", [])
    task_list[task_index]["done_history"].append(
        {
            "done_at": get_current_timestamp(),
            "weekday": get_today_name(),
        }
    )
    save_tasks()
    print("\n Marked done.")
    ask_about_habit(task_index)


def mark_task_open(task_index):
    task_list[task_index]["completed"] = False
    save_tasks()
    print("\n Marked open.")


def edit_task(task_index):
    current_name = task_list[task_index]["name"]
    new_name = input(f"\n Rename '{current_name}' to: ").strip()

    if new_name == "":
        print("\n Name was not changed.")
        return

    task_list[task_index]["name"] = new_name
    save_tasks()
    print("\n Task renamed.")


def delete_task(task_index):
    confirm = input("\n Delete this task? y/n: ").strip().lower()

    if confirm != "y":
        print("\n Kept task.")
        return

    task_list[task_index]["deleted"] = True
    task_list[task_index]["deleted_at"] = get_current_timestamp()
    save_tasks()
    print("\n Moved to deleted.")


def archive_task(task_index):
    task_list[task_index]["archived"] = True
    save_tasks()
    print("\n Archived task.")


def manage_task(task_index):
    task = task_list[task_index]
    status = "Done" if task.get("completed", False) else "Open"

    print(f"\n {task['name']} ({status})")

    if task.get("completed", False):
        print(" 1. Mark open")
    else:
        print(" 1. Mark done")

    print(" 2. Edit")
    print(" 3. Archive")
    print(" 4. Delete")
    print(" 5. Back")

    choice = input("\n Choose an option: ").strip()

    if choice == "1" and task.get("completed", False):
        mark_task_open(task_index)
    elif choice == "1":
        mark_task_done(task_index)
    elif choice == "2":
        edit_task(task_index)
    elif choice == "3":
        archive_task(task_index)
    elif choice == "4":
        delete_task(task_index)
    elif choice == "5":
        return
    else:
        print("\n Choose one of the menu numbers.")


def open_task_view():
    view_tasks()

    if len(get_task_order()) == 0:
        return

    task_index = choose_task()

    if task_index is not None:
        manage_task(task_index)
