# Archived expenses option for AviOS

from expense_options.display import get_archived_expenses_newest_first, print_expense_line
from expense_options.state import expense_list


def show_archived_expenses():
    archived_expenses = get_archived_expenses_newest_first()

    print("\n Archived expenses:")

    if len(archived_expenses) == 0:
        print(" No archived expenses yet.")
        return

    for expense_number, expense_index in enumerate(archived_expenses, start=1):
        expense = expense_list[expense_index]
        print_expense_line(expense_number, expense)
