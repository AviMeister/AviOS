# Expense summary option for AviOS

from expense_options.display import get_converted_amount, format_money
from expense_options.state import expense_list


def create_empty_total():
    return {
        "pay": 0.0,
        "receive": 0.0,
    }


def calculate_totals(expenses):
    totals_by_currency = {}
    combined_totals = create_empty_total()

    for expense in expenses:
        if expense.get("archived", False) or expense.get("deleted", False):
            continue

        currency = expense["currency"]
        direction = expense["direction"]

        if currency not in totals_by_currency:
            totals_by_currency[currency] = create_empty_total()

        totals_by_currency[currency][direction] += expense["amount"]
        combined_totals[direction] += get_converted_amount(expense)

    return totals_by_currency, combined_totals


def show_currency_totals(totals_by_currency):
    print("\n Per currency:")

    for currency, totals in sorted(totals_by_currency.items()):
        balance = totals["receive"] - totals["pay"]

        print(f"\n {currency}")
        print(f"  To pay:     {format_money(totals['pay'], currency)}")
        print(f"  To receive: {format_money(totals['receive'], currency)}")
        print(f"  Balance:    {format_money(balance, currency)}")


def show_combined_totals(combined_totals):
    balance = combined_totals["receive"] - combined_totals["pay"]

    print("\n Combined in EUR:")
    print(f" To pay:     {combined_totals['pay']:.2f} EUR")
    print(f" To receive: {combined_totals['receive']:.2f} EUR")
    print(f" Balance:    {balance:.2f} EUR")


def show_expense_summary():
    print("\n Expense Summary")

    if len(expense_list) == 0:
        print(" No expenses yet.")
        return

    totals_by_currency, combined_totals = calculate_totals(expense_list)

    if len(totals_by_currency) == 0:
        print(" No active expenses to summarize.")
        return

    show_currency_totals(totals_by_currency)
    show_combined_totals(combined_totals)
