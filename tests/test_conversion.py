import pytest

@pytest.mark.parametrize("attr,value", [
    ("PRODID", "c3calendar"),
    ("X-WR-TIMEZONE", "Europe/Berlin"),
    ("X-WR-CALNAME", "acronym"),
    ("X-WR-CALDESC", "title"),
])
def test_calendar_contains_meta_information(cal, conference, attr, value):
    assert cal.get(attr) == conference.get(value, value)
