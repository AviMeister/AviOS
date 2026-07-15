# View expenses option for AviOS

from expense_options.display import get_expenses_newest_first, print_expense_line
from expense_options.state import expense_list


def view_expenses():
    print("\n Expenses:")

    if len(expense_list) == 0:
        print(" No expenses yet.")
        return

    for expense_number, expense_index in enumerate(get_expenses_newest_first(), start=1):
        expense = expense_list[expense_index]
        print_expense_line(expense_number, expense)
