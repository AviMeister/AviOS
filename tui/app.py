from textual.app import App

from tui.dashboard_screen import DashboardScreen


class AviOSApp(App):
    CSS_PATH = "styles.tcss"
    TITLE = "AviOS"
    SUB_TITLE = "Personal Life Operating System (read-only preview)"
    BINDINGS = [("q", "quit", "Quit")]

    def on_mount(self) -> None:
        self.push_screen(DashboardScreen())
