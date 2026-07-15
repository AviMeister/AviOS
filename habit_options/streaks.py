# Habit streak helpers for AviOS

from datetime import datetime, timedelta


def parse_done_date(done_date):
    try:
        return datetime.strptime(done_date, "%d-%m-%Y").date()
    except ValueError:
        return None


def get_current_streak(habit, today):
    done_dates = {
        parsed_date
        for parsed_date in (parse_done_date(date_text) for date_text in habit["done_dates"])
        if parsed_date is not None
    }
    streak = 0
    current_day = today

    while current_day in done_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak
