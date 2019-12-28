#!/usr/bin/python3
import os
from icalendar import Calendar
import urllib.request


def convert_json_to_ics(data):
    schedule = data["schedule"]
    conference = schedule["conference"]
    cal = Calendar()
    cal["PRODID"] = "c3calendar"
    cal["X-WR-TIMEZONE"] = "Europe/Berlin"
    cal["X-WR-CALNAME"] = conference["acronym"]
    cal["X-WR-CALDESC"] = conference["title"]
    return cal



