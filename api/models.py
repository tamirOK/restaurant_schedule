import datetime
import typing

from . import schemas


_default_ts_format = '%I:%M %p'
_default_tz = datetime.timezone.utc


class HourItem(typing.NamedTuple):
    day: schemas.WeekDay
    state: schemas.State
    ts: int


class Interval(typing.NamedTuple):
    start_ts: int
    end_ts: int

    @classmethod
    def _format_ts(cls, ts: int, ts_format: str = _default_ts_format, tz=_default_tz) -> str:
        """Convert timestamp to human-readable form.

        Default format example: 11:47 AM, i.e. only hours and minutes are considered.
        """

        dt = datetime.datetime.fromtimestamp(ts).astimezone(tz)
        return dt.strftime(ts_format)

    def empty(self) -> bool:
        return self.start_ts == self.end_ts

    def __str__(self) -> str:
        """Convert interval to human-readable form."""

        open_str = self._format_ts(self.start_ts)
        close_str = self._format_ts(self.end_ts)

        return f'{open_str} - {close_str}'
