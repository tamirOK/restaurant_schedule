import api.models


def test_interval__format_ts_with_default_settings():
    assert api.models.Interval._format_ts(0) == '12:00 AM'
    assert api.models.Interval._format_ts(32400) == '09:00 AM'
    assert api.models.Interval._format_ts(37800) == '10:30 AM'
    assert api.models.Interval._format_ts(86399) == '11:59 PM'


def test_interval_as_str():
    interval = api.models.Interval(32400, 37800)
    assert str(interval) == '09:00 AM - 10:30 AM'


def test_interval_empty():
    interval = api.models.Interval(32400, 37800)

    assert not interval.empty()

    interval = api.models.Interval(32400, 32400)

    assert interval.empty()
