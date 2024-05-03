import datetime
from dataclasses import dataclass


@dataclass
class DateTimeRange:
    begin: datetime.datetime
    end: datetime.datetime
