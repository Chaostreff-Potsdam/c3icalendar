from pytest import fixture
import os
import json
import sys

SOURCE_JSON_URL = "https://data.c3voc.de/36C3/everything.schedule.json"
SOURCE_TEMP_PATH = "everything.schedule.json"
HERE = os.path.dirname(__file__) or "."
sys.path.append(os.path.join(HERE, ".."))

from conversion import convert_json_to_ics


@fixture
def data():
    if not os.path.isfile(SOURCE_TEMP_PATH):
        # from https://stackoverflow.com/a/7244263/1320237
        urllib.request.urlretrieve(SOURCE_JSON_URL, SOURCE_TEMP_PATH)
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


