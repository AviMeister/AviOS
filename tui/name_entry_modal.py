# Name entry popup for the AviOS TUI

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Input, Static


class NameEntryModal(ModalScreen[str]):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Welcome to AviOS! What should I call you?"),
            Input(placeholder="Your name", id="name_input"),
            id="name_prompt_body",
        )

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value.strip() or "there")
