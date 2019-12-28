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
    (10595, "DESCRIPTION", "Herzst\u00fcck der digitalen Gesundheitsversorgung f\u00fcr 73 Millionen Versicherte ist die hochsichere, kritische Telematik-Infrastruktur mit bereits 115.000 angeschlossenen Arztpraxen. Nur berechtigte Teilnehmer haben \u00fcber dieses geschlossene Netz Zugang zu unseren medizinischen Daten. Ein \"H\u00f6chstma\u00df an Schutz\" also, wie es das Gesundheitsministerium behauptet? Bewaffnet mit 10.000 Seiten Spezifikation und einem Faxger\u00e4t lassen wir Illusionen platzen und stellen fest: Technik allein ist auch keine L\u00f6sung. Braucht es einen Neuanfang?" + "\r\n\r\n" + "Schon in 12 Monaten k\u00f6nnen 73 Millionen gesetzlich Versicherte ihre Gesundheitsdaten in einer elektronischen Patientenakte speichern lassen. Dazu werden zurzeit alle Arztpraxen, Krankenh\u00e4user und Apotheken Deutschlands \u00fcber die neu geschaffene kritische Telematik-Infrastruktur verbunden.\r\n\r\nDieses hochverf\u00fcgbare Netz gen\u00fcgt \"milit\u00e4rischen Sicherheitsstandards\", bietet ein \"europaweit einzigartiges Sicherheitsniveau\" und verspricht ein \"H\u00f6chstma\u00df an Schutz f\u00fcr die personenbezogenen medizinischen Daten\" wie Arztbriefe, Medikamentenpl\u00e4ne, Blutbilder und Chromosomenanalysen.\r\n\r\n\"Wir tun alles, damit Patientendaten sicher bleiben.\"\r\n\r\n\"Selbst dem Chaos Computer Club ist es nicht gelungen, sich in die Telematik-Infrastruktur einzuhacken.\"\r\n\r\n\"Nach den Lehren aus PC-Wahl, Lades\u00e4ulen und dem besonderen elektronischen Anwaltspostfach brauchen wir kein weiteres Exempel.\""),
    (10883, "SUMMARY", "Plundervolt: Flipping Bits from Software without Rowhammer"),
    (909  , "LOCATION", "DLF- und Podcast-B\u00fchne"),
    (598  , "location", "WikiPaka WG: Esszimmer"),
])
def test_events_have_attributes(cal, eid, attr, value):
    event = cal.get_event_by_id(eid)
    assert event[attr] == value

