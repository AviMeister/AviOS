# Today dashboard menu for AviOS

from dashboard_options.focus import set_daily_focus
from dashboard_options.review import show_end_of_day_review
from dashboard_options.view import show_today_dashboard
from expense_options.add import add_expense
from habit_options.done_today import mark_habit_done_today
from task_options.add import add_task


def pause():
    input("\n Press Enter to continue...")


def open_dashboard(open_full_menu):
    while True:
        show_today_dashboard()

        print("\n Quick Actions")
        print(" 1. Add task")
        print(" 2. Mark habit done")
        print(" 3. Add expense")
        print(" 4. Set daily focus")
        print(" 5. Open full menu")
        print(" 6. Exit AviOS")

        choice = input("\n Choose an option: ").strip()

        if choice == "1":
            add_task()
            pause()
        elif choice == "2":
            mark_habit_done_today()
            pause()
        elif choice == "3":
            add_expense()
            pause()
        elif choice == "4":
            set_daily_focus()
            pause()
        elif choice == "5":
            open_full_menu()
        elif choice == "6":
            show_end_of_day_review()
            break
        else:
            print("\n Choose 1, 2, 3, 4, 5 or 6.")
