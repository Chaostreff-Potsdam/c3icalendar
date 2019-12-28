#!/usr/bin/python3
import os
from icalendar import Calendar, Event
import urllib.request

HERE = os.path.dirname(__file__) or "."
DEFAULT_CALENDAR_PATH = os.path.join(HERE, "default-calendar.ics")
with open(DEFAULT_CALENDAR_PATH) as file:
    DEFAULT_CALENDAR_CONTENT = file.read()

attr_mapping = {
    "uid": "guid",
    "id" : "id",
    "url": "url",
    "location": "room",
    "summary": "title"
}

languages = {"de": "Deutsch", "en": "English"}

def convert_json_to_ics(data):
    schedule = data["schedule"]
    conference = schedule["conference"]
    cal = Calendar.from_ical(DEFAULT_CALENDAR_CONTENT)
    cal["X-WR-CALNAME"] = conference["acronym"]
    cal["X-WR-CALDESC"] = conference["title"]
    id2event = {}
    for day in conference["days"]:
        for room, events in day["rooms"].items():
            for event in events:
                # create event
                vevent = Event()
                cal.add_component(vevent)
                id2event[event["id"]] = vevent
                # set attributes
                for a1, a2 in attr_mapping.items():
                    vevent[a1] = str(event[a2])
                if event["subtitle"]:
                    if vevent["summary"]:
                        vevent["summary"] += " - "
                    vevent["summary"] += event["subtitle"]
                vevent["description"] = ""
                if event["abstract"]:
                     vevent["description"] += event["abstract"]
                if event["description"]:
                    if vevent["description"]:
                        vevent["description"] += "\r\n\r\n"
                    vevent["description"] += event["description"]
                lang = languages.get(event["language"], event["language"])
                vevent["categories"] = [
                    event["track"], event["type"], lang]
    cal.get_event_by_id = lambda _id: id2event[_id]
    return cal



