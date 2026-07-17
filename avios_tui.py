# AviOS TUI entry point (Phase 1: read-only Textual view)
#
# This does not replace `python main.py` — that CLI still works unchanged.
# This is a second way to look at the same data, using Textual.

from tui.app import AviOSApp


def main():
    AviOSApp().run()


if __name__ == "__main__":
    main()
