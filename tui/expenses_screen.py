# Builds the read-only Textual screen that lists current expense information.

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import DataTable, Footer, Header

from expense_options.display import (
    format_money,
    get_converted_amount,
    get_expense_status,
    get_expenses_newest_first,
)
from expense_options.state import expense_list


class ExpensesScreen(Screen):
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("b", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="expenses_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns("Description", "Status", "Direction", "Amount", "EUR value", "Created")

        for expense_index in get_expenses_newest_first():
            expense = expense_list[expense_index]
            table.add_row(
                expense["description"],
                get_expense_status(expense),
                expense["direction"],
                format_money(expense["amount"], expense["currency"]),
                f"{get_converted_amount(expense):.2f}",
                expense.get("created_at", "Unknown"),
            )

        if table.row_count == 0:
            table.add_row("No expenses yet", "-", "-", "-", "-", "-")
