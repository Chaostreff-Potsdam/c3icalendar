import pytest

@pytest.mark.parametrize("attr,value", [
    ("PRODID", "c3calendar"),
    ("X-WR-TIMEZONE", "Europe/Berlin"),
    ("X-WR-CALNAME", "acronym"),
    ("X-WR-CALDESC", "title"),
])
def test_calendar_contains_meta_information(cal, conference, attr, value):
    assert cal.get(attr) == conference.get(value, value)


def is_event(event):
    return event.name == "VEVENT"

def test_opening_ceremony_is_first_event(cal, day1):
    tested = False
    for event in cal.walk():
        print(event.name)
        if is_event(event):
            assert event["UID"] == day1["rooms"]["Ada"][0]["guid"]
            tested = True
            break
    assert tested

def test_there_are_many_events(events):
    assert len(events) > 30

def test_all_events_are_included(cal, events):
    for event in events:
        assert any(vevent["UID"] == event["guid"]
            for vevent in cal.walk() if is_event(vevent))


@pytest.mark.parametrize("eid,attr,value", [
    (11223, "id", "11223"),
    (10565, "url", "https://fahrplan.events.ccc.de/congress/2019/Fahrplan/events/10565.html"),
    (11223, "id", "11223"),
    (11223, "id", "11223"),
    (11223, "id", "11223"),
    (11223, "id", "11223"),
])
def test_events_have_attributes(cal, eid, attr, value):
    event = cal.get_event_by_id(eid)
    assert event[attr] == value

