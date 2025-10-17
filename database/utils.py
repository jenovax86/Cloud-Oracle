from datetime import datetime


def get_year_from_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").year
