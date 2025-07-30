from datetime import datetime, timedelta
import locale
from datetime import datetime, timedelta
from typing import Tuple

def get_previous_week_dates() -> Tuple[datetime, datetime]:
    today = datetime.now()
    start_of_current_week = today - timedelta(days=today.weekday() + 1)
    start_date = start_of_current_week - timedelta(days=7)
    end_date = start_of_current_week - timedelta(days=1)
    return start_date, end_date

def format_week_range(start_date: datetime, end_date: datetime) -> str:
    start_day = start_date.day
    end_day = end_date.day
    locale.setlocale(locale.LC_TIME, 'pt_PT.UTF-8') # Set locale to Portuguese
    start_month = start_date.strftime('%B').capitalize()
    end_month = end_date.strftime('%B').capitalize()
    locale.setlocale(locale.LC_TIME, '') # Reset locale

    if start_month == end_month:
        return f"{start_day} {start_month} - {end_day} {end_month}"
    else:
        return f"{start_day} {start_month} - {end_day} {end_month}"