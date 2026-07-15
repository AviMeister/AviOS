# Today dashboard menu for AviOS

from dashboard_options.focus import set_daily_focus
from dashboard_options.mood import check_in_mood
from dashboard_options.notes import set_quick_note
from dashboard_options.review import show_end_of_day_review
from dashboard_options.view import show_today_dashboard
from expenses import open_expenses
from expense_options.add import add_expense
from habits import open_habits
from habit_options.done_today import mark_habit_done_today
from tasks import open_tasks
from task_options.add import add_task


def pause():
    input("\n Press Enter to continue...")


def show_dashboard_menu():
    print("\n Main Menu")
    print(" 1. Tasks")
    print(" 2. Habits")
    print(" 3. Expenses")
    print(" 4. Exit AviOS")

    print("\n Quick Actions")
    print(" 5. Add task")
    print(" 6. Mark habit done")
    print(" 7. Add expense")
    print(" 8. Set daily focus")
    print(" 9. Mood check-in")
    print(" 10. Quick note")


def open_dashboard():
    while True:
        show_today_dashboard()
        show_dashboard_menu()

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            open_tasks()
        elif choice == "2":
            open_habits()
        elif choice == "3":
            open_expenses()
        elif choice == "4":
            show_end_of_day_review()
            break
        elif choice == "5":
            add_task()
            pause()
        elif choice == "6":
            mark_habit_done_today()
            pause()
        elif choice == "7":
            add_expense()
            pause()
        elif choice == "8":
            set_daily_focus()
            pause()
        elif choice == "9":
            check_in_mood()
            pause()
        elif choice == "10":
            set_quick_note()
            pause()
        else:
            print("\n Choose a number from 1 to 10.")
