import notubiz
from notubiz.api.dataclasses.meeting import Meeting

import pytest
from test.helpers import read_json

from datetime import datetime

test_file_path = "./test/data/meeting.json"

@pytest.fixture(scope="session")
def input_json():
    return read_json(test_file_path)

@pytest.fixture(scope="session")
def input_meeting():
    return Meeting.from_json(test_file_path)

def test_meeting_general_info(input_json):
    meeting = Meeting.from_json(input_json)
    
    # We test all fields because they are not straight-up deserialized
    assert meeting.id == 1147925
    assert meeting.url == "https://eindhoven.raadsinformatie.nl/vergadering/1147925/Meningsvorming+Raadzaal"
    assert meeting.title == "Meningsvorming Raadzaal"
    assert meeting.location == "Raadzaal"
    assert len(meeting.agenda_items) == 7


def test_basic_agenda_item(input_json):
    meeting = Meeting.from_json(input_json)

    agenda_item = meeting.agenda_items[2]
    assert agenda_item.id == 8329704
    assert agenda_item.last_modified == datetime(2024, 3, 29, 10, 8, 56)
    assert agenda_item.title == "Pauze"
    assert agenda_item.description == None
    assert agenda_item.start_date == datetime(2024, 4, 16, 18, 0, 0)
    assert agenda_item.end_date == datetime(2024, 4, 16, 19, 0, 0)
    assert agenda_item.is_heading == True

def test_nested_agenda_items(input_json):
    meeting = Meeting.from_json(input_json)
    agenda_items = meeting.agenda_items

    assert len(agenda_items[0].agenda_items) == 0
    assert len(agenda_items[1].agenda_items) == 0
    assert len(agenda_items[2].agenda_items) == 0
    assert len(agenda_items[3].agenda_items) == 1
    assert len(agenda_items[4].agenda_items) == 2
    assert len(agenda_items[5].agenda_items) == 0
    assert len(agenda_items[6].agenda_items) == 0

    # Check content of the nested agenda items
    assert len(agenda_items[3].agenda_items[0].agenda_items) == 0
    assert len(agenda_items[4].agenda_items[0].agenda_items) == 0
    assert len(agenda_items[4].agenda_items[1].agenda_items) == 0
