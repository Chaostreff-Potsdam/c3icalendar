import pytest
from icalendar import Calendar
from conversion import parse_date
import datetime

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
    (1346 , "summary", "Mobile App Entwicklung f\u00fcr totale Anf\u00e4nger - Interaktive Live-Programmierung (also possible in English if desired)"),
    (1346 , "DESCRIPTION", "Wir entwicklen gemeinsam eine kleine App f\u00fcr iPhones und Android Smartphones - und erkl\u00e4ren dabei jeden einzelnen Schritt (We'll develop a simple mobile app - and explain each and every step along the way)\nWir entwicklen gemeinsam eine kleine App f\u00fcr Android und iOS. Dabei erkl\u00e4re ich jeden einzelnen Schritt, lasse nichts aus, und programmiere so, wie man als Anf\u00e4nger programmiert - mit viel Online-Recherche - sodass du danach direkt deine eigene App entwickeln kannst. Die App, die wir gemeinsam entwickeln, kannst du am Ende der Session ganz einfach auf deinem eigenen Smartphone nutzen. Ich zeige dir wie!Ein Computer muss nicht mitgebracht werden. Es ist wohl sinnvoller, meiner Live-Programmierung ohne eigenen PC zu folgen, um dann gezielt fragen stellen zu k\u00f6nnen. Du kannst aber auch gerne deinen eigenen Laptop mitbringen, wenn du magst.Welche Werkzeuge werden wir nutzen?- Wir werden das beliebteste und meist verbreiteste Werkzeug zur Entwicklung moderner Apps f\u00fcr das iPhone und Android Smartphones nutzen. Es hei\u00dft \"React Native\". Au\u00dferdem nutzen wir \"Expo\", mit dem wir ganz schnell entwickeln und die App sehr leicht auf anderen Smartphones testen k\u00f6nnen.---------------English version:This workshop is advertised in German, but everyone is very welcome to attend! If you don't speak German, I'll switch to German in case it's fine for everyone or repeat the most important steps in English otherwise.A few words about this workshop in English: In this interactive session we'll develop a small mobile app for Android and iOS. We won't skip any step to make it accessible for complete beginners. I'll live code in the manner a beginner would do it - with browsing for solutions online - to give you a feel of how you really do mobile development ;-)In the end, you'll be able to use the app on your own smartphone. I'll teach you about a great tool which makes mobile development easy."),
    (1255 , "categories", ["self organized sessions","workshop","Deutsch","Seminar room 13"]),
    (1080 , "categories", ["self organized sessions","Lecture room M1"]),
])
def test_events_have_attributes(cal, eid, attr, value):
    event = cal.get_event_by_id(eid)
    assert event[attr] == value


def test_calendar_can_be_converted_to_string(cal):
    s = cal.to_ical()
    cal2 = Calendar.from_ical(s)
    assert cal2 == cal

def test_parse_date_1():
    date = parse_date("2019-12-27T11:02:00+01:00")
    assert date.year == 2019
    assert date.month == 12
    assert date.day == 27
    assert date.hour == 11
    assert date.minute == 2
    assert date.second == 0
    assert date.tzinfo.utcoffset(date) == datetime.timedelta(hours=1)
    assert date.tzinfo.tzname(date) == "CET"

@pytest.mark.parametrize("eid,attr,value", [
    (1378, "DTSTART", "2019-12-29T15:00:00+01:00"),
    (1096, "DTSTART", "2019-12-29T20:00:00+01:00"),
    (1096, "DTEND", "2019-12-29T22:30:00+01:00"),
    (4128, "DTEND", "2019-12-28T13:30:00+01:00"),
])
def test_event_dates(cal, eid, attr, value):
    expected_date = parse_date(value)
    event = cal.get_event_by_id(eid)
    event_date = event[attr].dt
    assert event_date == expected_date
