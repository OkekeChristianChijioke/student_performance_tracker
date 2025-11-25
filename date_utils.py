# date_utils.py

from datetime import datetime as dt, date, timedelta

def get_today_date():
    """Return today's date as a date object."""
    return date.today()

def add_days_to_today(days: int) -> date:
    """Return the date that is 'days' days from today."""
    today = get_today_date()
    return today + timedelta(days=days)

def subtract_days_from_today(days: int) -> date:
    """Return the date that is 'days' days before today."""
    today = get_today_date()
    return today - timedelta(days=days)

def days_between_dates(date1_str: str, date2_str: str) -> int:
    """
    Return the number of days between two dates given as strings (YYYY-MM-DD).
    Result can be negative if date1 < date2.
    """
    date_format = "%Y-%m-%d"
    date1 = dt.strptime(date1_str.strip().replace(" ", ""), date_format).date()
    date2 = dt.strptime(date2_str.strip().replace(" ", ""), date_format).date()
    difference = date1 - date2
    return difference.days

def calculate_age_in_days(birthdate_str: str) -> int:
    """
    Return how many days old someone is, given their birthdate (YYYY-MM-DD).
    """
    date_format = "%Y-%m-%d"
    birthdate = dt.strptime(birthdate_str.strip().replace(" ", ""), date_format).date()
    today = get_today_date()
    age_delta = today - birthdate
    return age_delta.days
