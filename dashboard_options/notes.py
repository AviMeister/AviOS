# Quick daily notes for AviOS

from dashboard_options.state import dashboard_data, save_dashboard_data
from habit_options.state import get_today_date


def get_today_note():
    today = get_today_date()
    return dashboard_data.get("quick_notes", {}).get(today, "")


def set_quick_note():
    note = input("\n Quick note for today: ").strip()

    if note == "":
        print("\n Note was not changed.")
        return

    today = get_today_date()
    dashboard_data.setdefault("quick_notes", {})
    dashboard_data["quick_notes"][today] = note
    save_dashboard_data(dashboard_data)
    print("\n Quick note saved.")
