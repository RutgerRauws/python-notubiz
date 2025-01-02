import notubiz
from notubiz.api.dataclasses.event import Event

import pytest
from test.helpers import read_json

from datetime import datetime

test_file_path = "./test/data/events.json"

@pytest.fixture(scope="session")
def input_json():
    json_object = read_json(test_file_path)
    return json_object["events"]

@pytest.fixture(scope="session")
def input_events(input_json):
    # Run the deserialization over the events
    return [Event.from_json(json_event) for json_event in input_json]


def test_event_general_info(input_events):
    assert len(input_events) == 200
 
    assert input_events[2].id == 1011864
    assert input_events[2].title == "Nieuwjaarsbijeenkomst Raad en College"
    assert input_events[2].location == "Stadhuis"
    
    assert len(input_events[2].plannings) == 1
    assert input_events[2].plannings[0].start_date == datetime(2019, 1, 7, 16, 15)
    assert input_events[2].plannings[0].end_date == None