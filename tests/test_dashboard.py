# Tests that confirm the dashboard shows useful daily information correctly.

from datetime import date

from dashboard_options.metrics import get_day_streak_from_dates


def test_task_day_streak_counts_consecutive_days():
    today = date(2026, 7, 16)
    done_dates = {
        date(2026, 7, 16),
        date(2026, 7, 15),
        date(2026, 7, 13),
    }

    assert get_day_streak_from_dates(done_dates, today) == 2


def test_task_day_streak_is_zero_when_today_is_missing():
    today = date(2026, 7, 16)
    done_dates = {
        date(2026, 7, 15),
        date(2026, 7, 14),
    }

    assert get_day_streak_from_dates(done_dates, today) == 0
