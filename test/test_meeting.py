from notubiz.api.dataclasses.meeting import Meeting
from notubiz.api._converter import get_converter

import pytest
from test.helpers import read_json

from datetime import datetime

test_file_path = "./test/data/meeting.json"

@pytest.fixture(scope="session")
def input_json() -> str:
    return read_json(test_file_path)

@pytest.fixture(scope="session")
def meeting(input_json) -> Meeting:
    c = get_converter()
    return c.structure(input_json, Meeting)

def test_meeting_general_info(meeting):    
    # We test all fields because they are not straight-up deserialized
    assert meeting.id == 1147925
    assert meeting.url == "https://eindhoven.raadsinformatie.nl/vergadering/1147925/Meningsvorming+Raadzaal"
    assert meeting.title == "Meningsvorming Raadzaal"
    assert meeting.location == "Raadzaal"
    assert len(meeting.agenda_items) == 7


def test_basic_agenda_item(meeting):
    agenda_item = meeting.agenda_items[2]

    assert agenda_item.id == 8329704
    assert agenda_item.last_modified == datetime(2024, 3, 29, 10, 8, 56)
    assert agenda_item.title == "Pauze"
    assert agenda_item.description == None
    assert agenda_item.start_date == datetime(2024, 4, 16, 18, 0, 0)
    assert agenda_item.end_date == datetime(2024, 4, 16, 19, 0, 0)
    assert agenda_item.is_heading == True

def test_nested_agenda_items(meeting):
    agenda_items = meeting.agenda_items

    assert len(agenda_items[0].agenda_items) == 0
    assert len(agenda_items[1].agenda_items) == 0
    assert len(agenda_items[2].agenda_items) == 0
    assert len(agenda_items[3].agenda_items) == 1
    assert len(agenda_items[4].agenda_items) == 2
    assert len(agenda_items[5].agenda_items) == 0
    assert len(agenda_items[6].agenda_items) == 0

    assert agenda_items[3].title == "Hamerstukken"
    assert agenda_items[3].description == "Woordmelding"
    assert agenda_items[4].title == "In samenhang behandelen (agendapunt 4.1 en 4.2):"
    assert agenda_items[4].description == None

    # Check content of the nested agenda items
    assert len(agenda_items[3].agenda_items[0].agenda_items) == 0
    assert len(agenda_items[4].agenda_items[0].agenda_items) == 0
    assert len(agenda_items[4].agenda_items[1].agenda_items) == 0


def test_documents(meeting):
    assert len(meeting.agenda_items[0].documents) == 0
    assert len(meeting.agenda_items[5].documents) == 4

    assert meeting.agenda_items[5].documents[1].title == "Concept Vrije Motie Woonraad (GL)"
    assert meeting.agenda_items[5].documents[1].versions[0].mime_type == "application/pdf"
    assert meeting.agenda_items[5].documents[1].versions[0].id == 1