from pytest import fixture
import os
import json
import sys

HERE = os.path.dirname(__file__) or "."
sys.path.append(os.path.join(HERE, ".."))

# source from 
# https://data.c3voc.de/36C3/everything.schedule.json
SOURCE_TEMP_PATH = os.path.join(HERE, "everything.schedule.json")


from conversion import convert_json_to_ics


@fixture
def data():
    with open(SOURCE_TEMP_PATH) as file:
        return json.load(file)

@fixture
def cal(data):
    """The converted data."""
    return convert_json_to_ics(data)

@fixture
def schedule(data):
    return data["schedule"]

@fixture
def conference(schedule):
    return schedule["conference"]

@fixture
def day1(conference):
    return conference["days"][0]

@fixture
def day2(conference):
    return conference["days"][1]

@fixture
def day3(conference):
    return conference["days"][2]

@fixture
def day4(conference):
    return conference["days"][3]

@fixture
def events(conference):
    return [event for day in conference["days"] 
        for room in day["rooms"]
        for event in day["rooms"][room]]

