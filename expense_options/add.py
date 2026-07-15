# Add expense option for AviOS

from dashboard_options.activity import add_activity
from expense_options.state import expense_list, get_current_timestamp, save_expenses


def get_valid_amount():
    while True:
        amount_text = input("\n Amount: ").strip().replace(",", ".")

        try:
            amount = float(amount_text)
        except ValueError:
            print("\n Please enter a valid number.")
            continue

        if amount <= 0:
            print("\n Amount must be more than 0.")
            continue

        return amount


def choose_direction():
    print("\n Type:")
    print(" 1. To pay")
    print(" 2. To receive")

    choice = input("\n Choose a type: ").strip()

    if choice == "2":
        return "receive"

    return "pay"


def choose_category():
    categories = ["Food", "Transport", "Health", "Learning", "Bills", "Fun", "Other"]

    print("\n Category:")

    for number, category in enumerate(categories, start=1):
        print(f" {number}. {category}")

    choice = input("\n Choose a category: ").strip()

    if not choice.isdigit():
        return "Other"

    category_number = int(choice)

    if category_number < 1 or category_number > len(categories):
        return "Other"

    return categories[category_number - 1]


def choose_currency():
    currencies = ["EUR", "USD", "GBP", "SRD"]

    print("\n Currency:")

    for number, currency in enumerate(currencies, start=1):
        print(f" {number}. {currency}")

    choice = input("\n Choose a currency: ").strip()

    if not choice.isdigit():
        return "EUR"

    currency_number = int(choice)

    if currency_number < 1 or currency_number > len(currencies):
        return "EUR"

    return currencies[currency_number - 1]


def get_exchange_rate_to_eur(currency):
    if currency == "EUR":
        return 1.0

    print(f"\n Exchange rate for today: 1 {currency} = ? EUR")
    rate_text = input(" EUR value: ").strip().replace(",", ".")

    try:
        rate = float(rate_text)
    except ValueError:
        print("\n Invalid rate. Using 1.0 for now.")
        return 1.0

    if rate <= 0:
        print("\n Invalid rate. Using 1.0 for now.")
        return 1.0

    return rate


def add_expense():
    description = input("\n Description: ").strip()

    if description == "":
        print("\n Description cannot be empty.")
        return

    direction = choose_direction()
    amount = get_valid_amount()
    currency = choose_currency()
    exchange_rate_to_eur = get_exchange_rate_to_eur(currency)
    category = choose_category()

    expense_list.append(
        {
            "description": description,
            "amount": amount,
            "currency": currency,
            "direction": direction,
            "category": category,
            "exchange_rate_to_eur": exchange_rate_to_eur,
            "created_at": get_current_timestamp(),
            "archived": False,
            "deleted": False,
        }
    )
    save_expenses()
    add_activity(f"Added expense: {description}")
    print(f"\n Added: {description}")
