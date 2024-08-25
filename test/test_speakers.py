import notubiz
from notubiz.api.speakers import NotubizSpeakers

import pytest
from test.helpers import read_json

@pytest.fixture(scope="session")
def input_json():
    return read_json("./test/data/speakers.json")

@pytest.fixture(scope="session")
def input_speakers():
    return NotubizSpeakers.from_json(read_json("./test/data/speakers.json"))

def test_deserialization(input_json):
    speakers = NotubizSpeakers.from_json(input_json).speakers
    
    # Let's not test the entire attrs/cattrs package. 
    # The serialization did not throw an exception if we reach these lines
    assert len(speakers) == 3
    assert speakers[1].firstname == "Rutger"

def test_find_by_person_id(input_speakers):
    assert input_speakers.find_by_person_id(2).firstname == "Jans"
    assert input_speakers.find_by_person_id(3) == None

    # TODO: Should return multiple speaker objects in the future
    assert input_speakers.find_by_person_id(1).function == "Commissielid"

def test_find_by_speaker_id(input_speakers):
    assert input_speakers.find_by_speaker_id(1).firstname == "Rutger"
    assert input_speakers.find_by_speaker_id(3).firstname == "Jans"