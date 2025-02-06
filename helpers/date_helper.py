"""Date helpers"""
from datetime import date, datetime, timezone, timedelta


class DateHelper():
    """date helper methods"""

    def __init__(self) -> None:
        self.yyyy_mm_dd_format = "%Y-%m-%d"
        self.yyyy_mm_dd_hh_mm_ss_format = "%Y-%m-%d-%H-%M-%S"

    def convert_date_to_yyyy_mm_dd(self, date_obj: date | datetime):
        """convert date to string in format yyyy-mm-dd"""
        if date_obj is None or (not isinstance(date_obj, date)
                                and not isinstance(date_obj, datetime)):
            raise ValueError("Input is not in date format")

        return date_obj.strftime(self.yyyy_mm_dd_format)

    def convert_yyyy_mm_dd_to_date(self, date_str: str) -> date:
        """convert str of format yyyy-mm-dd date to date"""
        return datetime.strptime(date_str, self.yyyy_mm_dd_format).date()

    def convert_date_to_yyyy_mm_dd_hh_mm_ss(self, date_obj: date | datetime):
        """convert date time to string"""
        if date_obj is None or (not isinstance(date_obj, date)
                                and not isinstance(date_obj, datetime)):
            raise ValueError("Input is not in date format")

        return date_obj.strftime(self.yyyy_mm_dd_hh_mm_ss_format)

    def convert_yyyy_mm_dd_hh_mm_ss_to_date(self, date_str: str) -> datetime:
        """convert datetime strting to datetime obj"""
        return datetime.strptime(date_str, self.yyyy_mm_dd_hh_mm_ss_format)

    def get_utc_now(self):
        """return utc time"""
        return datetime.now(timezone.utc)

    def get_utc_now_str(self):
        """return utc time as str"""
        return str(self.get_utc_now())

    def get_now(self):
        """get now time"""
        return datetime.now()

    def convert_utc_str_to_datetime(self, str_datetime: str):
        """convert utc string to datetime"""
        return datetime.fromisoformat(str_datetime)

    def get_elapsed_seconds(self, start_time: datetime):
        """get elapsed time in seconds"""
        return (self.get_utc_now() - start_time).total_seconds()

    def get_elapsed_time_in_seconds(self, start_time: datetime, end_time: datetime):
        """get elapsed time in seconds"""
        return (end_time - start_time).total_seconds()

    def get_unix_timestamp(self):
        """
        Get the current unix timestamp (seconds since epoch)
        """
        return int(self.get_utc_now().timestamp())

    def from_unix_seconds_to_date(self, unix_seconds: int):
        """Convert unix seconds to date"""
        return datetime.fromtimestamp(unix_seconds)

    def from_unix_milli_seconds_to_date(self, unix_milliseconds: int):
        """Convert unix millisecionds to date"""
        unix_seconds = int(unix_milliseconds) / 1000
        return self.from_unix_seconds_to_date(unix_seconds)

    def get_previous_day_in_unix(self, days: int):
        """get previous date in unix"""
        previous_day = (self.get_utc_now() - timedelta(days=days)).date()
        # get beginning of the day by setting time to 0
        previous_day_time = datetime.combine(previous_day, datetime.min.time())
        return int(previous_day_time.timestamp())
