from datetime import datetime, timezone, timedelta

DATE_FORMAT_API = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT_HUMAN = "%d.%m.%Y--%H:%M:%S"


def transform_date(date, reverse=False):
    if reverse:
        return datetime.strptime(date, DATE_FORMAT_HUMAN).strftime(DATE_FORMAT_API)
    return datetime.strptime(date, DATE_FORMAT_API).strftime(DATE_FORMAT_HUMAN)


def get_time_range(minutes_diff:int, time_higher=datetime.now(timezone.utc)) -> (str, str):
    time_lower = time_higher - timedelta(minutes=minutes_diff)
    time_format = "%Y-%m-%dT%H:%M:%SZ"
    return time_lower.strftime(time_format), time_higher.strftime(time_format)


def sort_by_creation_date(item):
    return item['created_at']


def load_api_date(api_date: str) -> datetime:
    return datetime.strptime(api_date, DATE_FORMAT_API)
