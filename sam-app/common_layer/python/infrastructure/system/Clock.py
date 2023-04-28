from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

import pytz
from dateutil.parser import *


@dataclass(frozen=True)
class TimeOfDay:
    EARLY_MORNING = "early_morning"
    MORNING: str = "morning"
    AFTERNOON: str = "afternoon"
    EVENING: str = "evening"
    NIGHT: str = "night"


@dataclass(frozen=True)
class TimeContext:
    time: datetime
    time_of_day: str
    day_of_week: str
    day: int
    month: int
    hour: int
    minute: int
    work_day: bool


class ITellingTime:
    @abstractmethod
    def get_time(self, timezone: str = "") -> datetime:
        raise NotImplementedError()

    def convert_est_to_utc(self, est_datetime: datetime):
        local_tz = pytz.timezone("America/New_York")
        localdt = local_tz.localize(est_datetime)
        return localdt.astimezone(pytz.UTC)

    def get_time_context(self, timezone: str = "") -> TimeContext:
        now = self.get_time(timezone)
        print(f"now at {timezone}: {now}")
        time_of_day = ""
        if now.hour >= 6 and now.hour <= 8:
            time_of_day = TimeOfDay.EARLY_MORNING
        elif now.hour < 12:
            time_of_day = TimeOfDay.MORNING
        elif now.hour < 18:
            time_of_day = TimeOfDay.AFTERNOON
        elif now.hour < 20:
            time_of_day = TimeOfDay.EVENING
        else:
            time_of_day = TimeOfDay.NIGHT

        day_of_week = now.strftime("%A")
        work_day = True
        if day_of_week in ["Sunday", "Saturday"]:
            work_day = False
        return TimeContext(
            now,
            time_of_day,
            day_of_week,
            now.day,
            now.month,
            now.hour,
            now.minute,
            work_day,
        )


class FakeClock(ITellingTime):
    def __init__(self, datetime_str: str):
        time = parse(datetime_str)
        self._time = pytz.utc.localize(time)
        print(f"Set FakeClock to {self._time}")

    def get_time(self, timezone: str = ""):
        if timezone == "":
            return self._time
        print(self._time)
        return self._time.astimezone(pytz.timezone(timezone))


class RealClock(ITellingTime):
    def get_time(self, timezone: str = ""):
        if timezone == "":
            return pytz.utc.localize(datetime.utcnow())
        utc = pytz.utc.localize(datetime.utcnow())
        return utc.astimezone(pytz.timezone(timezone))
