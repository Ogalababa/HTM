from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


def generate_dates_within_last_month(periods: int):
    current_date = datetime.now().date()
    start_date = current_date - relativedelta(months=periods)
    end_date = current_date - timedelta(days=1)
    date_list = []

    next_date = start_date
    while next_date <= end_date:
        date_list.append(next_date.strftime('%Y-%m-%d'))
        next_date += timedelta(days=1)

    return date_list
