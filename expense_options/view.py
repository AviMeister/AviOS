# View expenses option for AviOS

from expense_options.display import get_expenses_newest_first, print_expense_line
from expense_options.state import expense_list, get_current_timestamp, save_expenses


def view_expenses():
    print("\n Expenses:")

    if len(expense_list) == 0:
        print(" No expenses yet.")
        return

    for expense_number, expense_index in enumerate(get_expenses_newest_first(), start=1):
        expense = expense_list[expense_index]
        print_expense_line(expense_number, expense)


def choose_expense():
    expense_choice = input("\n Select an expense, or press Enter to go back: ").strip()

    if expense_choice == "":
        return None

    if not expense_choice.isdigit():
        print("\n Please enter an expense number.")
        return None

    expense_number = int(expense_choice)
    expense_order = get_expenses_newest_first()

    if expense_number < 1 or expense_number > len(expense_order):
        print("\n That expense number does not exist.")
        return None

    return expense_order[expense_number - 1]


def edit_expense(expense_index):
    current_description = expense_list[expense_index]["description"]
    new_description = input(f"\n Rename '{current_description}' to: ").strip()

    if new_description == "":
        print("\n Description was not changed.")
        return

    expense_list[expense_index]["description"] = new_description
    save_expenses()
    print("\n Expense renamed.")


def archive_expense(expense_index):
    expense_list[expense_index]["archived"] = True
    save_expenses()
    print("\n Archived expense.")


def delete_expense(expense_index):
    confirm = input("\n Delete this expense? y/n: ").strip().lower()

    if confirm != "y":
        print("\n Kept expense.")
        return

    expense_list[expense_index]["deleted"] = True
    expense_list[expense_index]["deleted_at"] = get_current_timestamp()
    save_expenses()
    print("\n Moved to deleted.")


def manage_expense(expense_index):
    expense = expense_list[expense_index]

    print(f"\n {expense['description']}")
    print(" 1. Edit")
    print(" 2. Archive")
    print(" 3. Delete")
    print(" 4. Back")

    choice = input("\n Choose an option: ").strip()

    if choice == "1":
        edit_expense(expense_index)
    elif choice == "2":
        archive_expense(expense_index)
    elif choice == "3":
        delete_expense(expense_index)
    elif choice == "4":
        return
    else:
        print("\n Choose 1, 2, 3 or 4.")


def open_expense_view():
    view_expenses()

    if len(get_expenses_newest_first()) == 0:
        return

    expense_index = choose_expense()

    if expense_index is not None:
        manage_expense(expense_index)
