import pytest

import api.controllers
import api.models
import api.schemas
import api.exceptions


def test__transform_open_hours():
    open_hours = api.schemas.OpeningHoursQuery(
        tuesday=[
            {
                'type': 'close',
                'value': 37800,
            },
            {
                'type': 'open',
                'value': 32400,
            },
        ],
        monday=[
            {
                'type': 'close',
                'value': 37800,
            },
            {
                'type': 'open',
                'value': 32400,
            },
        ],
    )

    expected_result = [
        api.models.HourItem(
            state='open',
            ts=32400,
            day='monday',
        ),
        api.models.HourItem(
            state='close',
            ts=37800,
            day='monday',
        ),
        api.models.HourItem(
            state='open',
            ts=32400,
            day='tuesday',
        ),
        api.models.HourItem(
            state='close',
            ts=37800,
            day='tuesday',
        ),
    ]

    assert api.controllers._transform_open_hours(open_hours) == expected_result


def test__ensure_intervals_are_valid_when_first_item_state_close():
    open_hours = [
        api.models.HourItem(
            state='close',
            ts=32400,
            day='tuesday',
        ),
        api.models.HourItem(
            state='open',
            ts=37800,
            day='tuesday',
        ),
    ]

    with pytest.raises(api.exceptions.InvalidStateError):
        api.controllers._ensure_open_hours_are_valid(open_hours)


def test__ensure_intervals_are_valid_when_last_item_state_open():
    open_hours = [
        api.models.HourItem(
            state='open',
            ts=32400,
            day='tuesday',
        ),
        api.models.HourItem(
            state='close',
            ts=37800,
            day='tuesday',
        ),
        api.models.HourItem(
            state='open',
            ts=57600,
            day='tuesday',
        ),
    ]

    with pytest.raises(api.exceptions.InvalidOpeningHoursError):
        api.controllers._ensure_open_hours_are_valid(open_hours)


def test__ensure_intervals_are_valid_with_same_consecutive_state():
    open_hours = [
        api.models.HourItem(
            state='open',
            ts=32400,
            day='tuesday',
        ),
        api.models.HourItem(
            state='open',
            ts=37800,
            day='tuesday',
        ),
    ]

    with pytest.raises(api.exceptions.InvalidStateError):
        api.controllers._ensure_open_hours_are_valid(open_hours)
