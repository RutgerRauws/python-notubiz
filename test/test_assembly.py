from notubiz.api.dataclasses.assembly import Assembly
from notubiz.api._converter import get_converter

import pytest
from test.helpers import read_json

from datetime import datetime

test_file_path = "./test/data/assembly.json"

@pytest.fixture(scope="session")
def input_json():
    json_object = read_json(test_file_path)["assembly"]
    return json_object

@pytest.fixture(scope="session")
def input_assembly(input_json):
    return get_converter().structure(input_json, Assembly)

def test_assembly_event_inheritance(input_assembly):
    # Verify that inheritance of Event still works
    # by checking the same things as in test_events
    assert input_assembly.id == 1253866
    assert input_assembly.title == "Raadsavond"
    assert input_assembly.location == "Raadzaal / commissiekamer"
    
    assert len(input_assembly.plannings) == 1
    assert input_assembly.plannings[0].start_date == datetime(2025, 1, 7, 14, 00)
    assert input_assembly.plannings[0].end_date == None

def test_assembly_meeting_list_structure(input_assembly):
    assert len(input_assembly.meetings) == 3
    
    assert input_assembly.meetings[0].id == 1253869
    assert input_assembly.meetings[0].order == 1

    assert input_assembly.meetings[2].id == 1253868
    assert input_assembly.meetings[2].order == 6
    assert input_assembly.meetings[2].plannings[0].start_date == datetime(2025, 1, 7, 14, 0, 0)
    assert input_assembly.meetings[2].plannings[0].end_date == datetime(2025, 1, 7, 21, 0, 0)