# Main Textual app for AviOS

from asyncio import sleep

from textual import work
from textual.app import App

from profile_options.state import get_user_name, set_user_name
from tui.dashboard_screen import DashboardScreen
from tui.name_entry_modal import NameEntryModal


class AviOSApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "AviOS"
    SUB_TITLE = "Personal Life Operating System"
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self._start_up()

    @work
    async def _start_up(self) -> None:
        # push_screen_wait only works inside a worker, so this method
        # exists just so it can run as one (see the @work decorator above).
        if not get_user_name():
            name = await self.push_screen_wait(NameEntryModal())
            set_user_name(name)

        await sleep(0.5)
        self.push_screen(DashboardScreen())
