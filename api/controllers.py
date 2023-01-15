import collections

from . import exceptions
from . import models
from . import schemas


_default_separator = ', '


def _transform_open_hours(open_hours: schemas.OpeningHoursQuery) -> list[models.HourItem]:
    """Convert opening hours input into list of HourItem."""

    results = []
    open_hours = open_hours.dict()

    for day in schemas.WeekDay:
        # Sort items within each day by timestamps
        open_hours[day].sort(key=lambda item: item['value'])

        for item in open_hours[day]:
            results.append(models.HourItem(day=day, state=item['type'], ts=item['value']))

    return results


def _has_cycle(first_item: models.HourItem, last_item: models.HourItem) -> bool:
    """Checks if there is cycle.

    Cycle is when the restaurant was opened in sunday and closed in monday."""

    return (
        first_item.day == schemas.WeekDay.Monday and
        first_item.state == schemas.State.Close and
        last_item.day == schemas.WeekDay.Sunday and
        last_item.state == schemas.State.Open
    )


def _ensure_open_hours_are_valid(open_hours: list[models.HourItem]):
    """Validate open hours."""

    if not open_hours:
        return

    first_item, last_item = open_hours[0], open_hours[-1]

    # if there is a cycle, then move first item to the end
    if _has_cycle(first_item, last_item):
        open_hours.append(first_item)
        open_hours.pop(0)

    expected_state = schemas.State.Open

    for hour_item in open_hours:
        day = hour_item.day
        state = hour_item.state

        # Raise exception, if there are two same consecutive states
        if state != expected_state:
            raise exceptions.InvalidStateError

        if state == schemas.State.Open:
            open_day = day

        # Ensure that restaurant was open on two consecutive days
        elif open_day != day and not open_day.is_next_day(day):
            raise exceptions.InvalidIntervalError

        expected_state = expected_state.opposite

    # Raise exception, if last state is 'open'
    if state == schemas.State.Open:
        raise exceptions.InvalidOpeningHoursError


def _group_intervals_by_day(
    open_hours: list[models.HourItem],
) -> dict[schemas.WeekDay, list[models.Interval]]:
    """Group opening hours by day.

    Store list of (open; close) intervals for each day.
    Should be run after validation of the open hours.
    """

    intervals_by_day = collections.defaultdict(list)

    for hour_item in open_hours:
        # If state is 'open', store start of the interval
        if hour_item.state == schemas.State.Open:
            open_day = hour_item.day
            open_ts = hour_item.ts
        # else save the interval
        else:
            intervals_by_day[open_day].append(
                models.Interval(
                    start_ts=open_ts,
                    end_ts=hour_item.ts,
                ),
            )

    return intervals_by_day


def _transform_to_human_format(
    intervals_by_day: dict[schemas.WeekDay, list[models.Interval]],
    separator: str = _default_separator,
) -> schemas.HumanReadableOpeningHours:
    """Convert days and intervals to human-readable format."""

    result = {}

    for day, intervals in intervals_by_day.items():
        formatted_day = day.capitalize()
        formatted_intervals = separator.join(
            str(interval)
            for interval in intervals
            if not interval.empty()
        )
        result[formatted_day] = formatted_intervals

    return schemas.HumanReadableOpeningHours(**result)


def parse_opening_hours(
    open_hours: schemas.OpeningHoursQuery,
) -> schemas.HumanReadableOpeningHours:
    open_hours = _transform_open_hours(open_hours)
    _ensure_open_hours_are_valid(open_hours)
    intervals_by_day = _group_intervals_by_day(open_hours)
    return _transform_to_human_format(intervals_by_day)
