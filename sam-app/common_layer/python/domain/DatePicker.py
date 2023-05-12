import random
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class DateOptions:
    type: str
    year: int
    month: int
    day: int = None

    # def __str__(self):
    #     import_month = ""
    #     if self.import_month != None:
    #         import_month = self.import_month
    #     import_day = ""
    #     if self.import_day != None:
    #         import_day = self.import_day
    #     return f"{self.random_month:<2}/{self.random_day:<2} or {import_month:<2}/{import_day:<2} "


class IDatePicker:
    @abstractmethod
    def get_date_type(self, today: datetime) -> DateOptions:
        raise NotImplementedError


class DatePicker(IDatePicker):
    def get_date_type(self, today: datetime) -> DateOptions:
        type = "random"
        type_chance = random.randint(0, 100)
        year = random.randint(2003, 2023)
        month = random.randint(1, 12)
        day = random.randint(1, 31)
        if month == 2:
            day = random.randint(1, 28)
        if month in [9, 4, 6, 11]:
            day = random.randint(1, 30)

        if type_chance <= 10:
            type = "recently_added"
            recent = today - timedelta(days=2)
            year = recent.year
            month = recent.month
            day = recent.day
        elif type_chance <= 20:
            type = "on_this_day"
            recent = today - timedelta(days=2)
            year = recent.year
            month = recent.month
            day = recent.day

        return DateOptions(type=type, year=year, month=month, day=day)
