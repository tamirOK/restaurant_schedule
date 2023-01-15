import api

from fastapi.testclient import TestClient

client = TestClient(api.app)


def test_get_opening_hours_with_empty_query():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': 'Closed',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_missing_days():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'open',
                  'value': 32400,
                },
                {
                  'type': 'close',
                  'value': 37800,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '09:00 AM - 10:30 AM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_values_in_reverse_order():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'close',
                  'value': 37800,
                },
                {
                    'type': 'open',
                    'value': 32400,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '09:00 AM - 10:30 AM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_multiple_openings_and_closings():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'open',
                  'value': 32400,
                },
                {
                  'type': 'close',
                  'value': 39600,
                },
                {
                    'type': 'open',
                    'value': 57600,
                },
                {
                    'type': 'close',
                    'value': 82800,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '09:00 AM - 11:00 AM, 04:00 PM - 11:00 PM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_opening_and_closing_on_different_days():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'open',
                  'value': 64800,
                },
            ],
            'tuesday': [
                {
                    'type': 'close',
                    'value': 3600,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '06:00 PM - 01:00 AM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_opening_on_sunday():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'close',
                  'value': 32400,
                },
            ],
            'sunday': [
                {
                    'type': 'open',
                    'value': 82800,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': 'Closed',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': '11:00 PM - 09:00 AM',
    }


def test_get_opening_hours_when_restaurant_opened_for_maximal_duration():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                  'type': 'open',
                  'value': 60,
                },
            ],
            'tuesday': [
                {
                    'type': 'close',
                    'value': 86399,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '12:01 AM - 11:59 PM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_days_in_reverse_order():
    response = client.post(
        '/opening_hours',
        json={
            'tuesday': [
                {
                    'type': 'close',
                    'value': 3600,
                },
            ],
            'monday': [
                {
                    'type': 'open',
                    'value': 64800,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': '06:00 PM - 01:00 AM',
        'Tuesday': 'Closed',
        'Wednesday': 'Closed',
        'Thursday': 'Closed',
        'Friday': 'Closed',
        'Saturday': 'Closed',
        'Sunday': 'Closed',
    }


def test_get_opening_hours_with_opening_for_multiple_days():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [],
            'tuesday': [
                {
                    'type': 'open',
                    'value': 36000,
                },
                {
                    'type': 'close',
                    'value': 64800,
                },
            ],
            'wednesday': [],
            'thursday': [
                {
                    'type': 'open',
                    'value': 37800,
                },
                {
                    'type': 'close',
                    'value': 64800,
                },
            ],
            'friday': [
                {
                    'type': 'open',
                    'value': 36000,
                },
            ],
            'saturday': [
                {
                    'type': 'close',
                    'value': 3600,
                },
                {
                    'type': 'open',
                    'value': 36000,
                },
            ],
            'sunday': [
                {
                    'type': 'close',
                    'value': 3600,
                },
                {
                    'type': 'open',
                    'value': 43200,
                },
                {
                    'type': 'close',
                    'value': 75600,
                },
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'Monday': 'Closed',
        'Tuesday': '10:00 AM - 06:00 PM',
        'Wednesday': 'Closed',
        'Thursday': '10:30 AM - 06:00 PM',
        'Friday': '10:00 AM - 01:00 AM',
        'Saturday': '10:00 AM - 01:00 AM',
        'Sunday': '12:00 PM - 09:00 PM',
    }


def test_get_opening_hours_with_values_with_consecutive_open_items():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'open',
                    'value': 32400,
                },
                {
                    'type': 'open',
                    'value': 37800,
                },
            ],
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid opening hours provided.'}


def test_get_opening_hours_with_values_with_single_close_item():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'close',
                    'value': 32400,
                },
            ],
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid opening hours provided.'}


def test_get_opening_hours_with_values_with_single_open_item():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'open',
                    'value': 32400,
                },
            ],
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid opening hours provided.'}


def test_get_opening_hours_when_restaurant_was_open_more_than_48_hours():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'open',
                    'value': 32400,
                },
            ],
            'wednesday': [
                {
                    'type': 'close',
                    'value': 32400,
                },
            ],
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid opening hours provided.'}


def test_get_opening_hours_with_values_with_invalid_state():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'invalid',
                    'value': 32400,
                },
            ],
        },
    )

    assert response.status_code == 422


def test_get_opening_hours_with_values_with_invalid_value():
    response = client.post(
        '/opening_hours',
        json={
            'monday': [
                {
                    'type': 'open',
                    'value': 'invalid',
                },
            ],
        },
    )

    assert response.status_code == 422
