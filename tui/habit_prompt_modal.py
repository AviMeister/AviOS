# A yes/no popup asking whether a repeated task should become a habit idea.

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class HabitPromptModal(ModalScreen[bool]):
    BINDINGS = [("escape", "dismiss_no", "Cancel")]

    def __init__(self, task_name: str) -> None:
        super().__init__()
        self.task_name = task_name

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(f"You seem to do '{self.task_name}' often.\nSave it as a habit idea?"),
            Button("Yes", id="yes", variant="success"),
            Button("No", id="no", variant="default"),
            id="habit_prompt_body",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "yes")

    def action_dismiss_no(self) -> None:
        self.dismiss(False)
