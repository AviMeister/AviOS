# Daily mood check-in for AviOS

from dashboard_options.state import dashboard_data, save_dashboard_data
from habit_options.state import get_today_date


def get_today_mood():
    today = get_today_date()
    return dashboard_data.get("mood_checkins", {}).get(today)


def check_in_mood():
    mood = input("\n Mood today 1-5: ").strip()

    if mood not in {"1", "2", "3", "4", "5"}:
        print("\n Please choose a number from 1 to 5.")
        return

    today = get_today_date()
    dashboard_data.setdefault("mood_checkins", {})
    dashboard_data["mood_checkins"][today] = int(mood)
    save_dashboard_data(dashboard_data)
    print("\n Mood check-in saved.")
