# Tests that verify expense totals and currency summaries remain accurate.

from expense_options.summary import calculate_totals


def test_expense_summary_ignores_archived_and_deleted_items():
    expenses = [
        {
            "amount": 20.0,
            "currency": "EUR",
            "direction": "pay",
            "exchange_rate_to_eur": 1.0,
        },
        {
            "amount": 50.0,
            "currency": "USD",
            "direction": "receive",
            "exchange_rate_to_eur": 0.9,
        },
        {
            "amount": 999.0,
            "currency": "EUR",
            "direction": "pay",
            "exchange_rate_to_eur": 1.0,
            "archived": True,
        },
        {
            "amount": 999.0,
            "currency": "EUR",
            "direction": "receive",
            "exchange_rate_to_eur": 1.0,
            "deleted": True,
        },
    ]

    totals_by_currency, combined_totals = calculate_totals(expenses)

    assert totals_by_currency["EUR"]["pay"] == 20.0
    assert totals_by_currency["USD"]["receive"] == 50.0
    assert combined_totals["pay"] == 20.0
    assert combined_totals["receive"] == 45.0
