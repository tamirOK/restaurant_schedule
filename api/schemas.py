import enum
import functools

import pydantic


MIN_TS = 0
MAX_TS = 86399


class State(str, enum.Enum):
    Open = 'open'
    Close = 'close'

    @property
    def opposite(self):
        return self.Open if self == self.Close else self.Close


class WeekDay(str, enum.Enum):
    Monday = 'monday'
    Tuesday = 'tuesday'
    Wednesday = 'wednesday'
    Thursday = 'thursday'
    Friday = 'friday'
    Saturday = 'saturday'
    Sunday = 'sunday'

    @functools.cached_property
    def _next_day(self) -> dict:
        return {
            self.Monday: self.Tuesday,
            self.Tuesday: self.Wednesday,
            self.Wednesday: self.Thursday,
            self.Thursday: self.Friday,
            self.Friday: self.Saturday,
            self.Saturday: self.Sunday,
            self.Sunday: self.Monday,
        }

    def is_next_day(self, next_day: str) -> bool:
        return self._next_day[self] == next_day


class Record(pydantic.BaseModel):
    type: State
    value: pydantic.conint(ge=MIN_TS, le=MAX_TS)


class OpeningHoursQuery(pydantic.BaseModel):
    monday: list[Record] = []
    tuesday: list[Record] = []
    wednesday: list[Record] = []
    thursday: list[Record] = []
    friday: list[Record] = []
    saturday: list[Record] = []
    sunday: list[Record] = []


class HumanReadableOpeningHours(pydantic.BaseModel):
    Monday: str = 'Closed'
    Tuesday: str = 'Closed'
    Wednesday: str = 'Closed'
    Thursday: str = 'Closed'
    Friday: str = 'Closed'
    Saturday: str = 'Closed'
    Sunday: str = 'Closed'
