import notubiz
from notubiz.api.dataclasses.speakers import Speakers

import pytest
from test.helpers import read_json
from notubiz.api._converter import get_converter

@pytest.fixture(scope="session")
def input_json():
    return read_json("./test/data/speakers.json")

@pytest.fixture(scope="session")
def input_speakers(input_json):
    return get_converter().structure(input_json, Speakers)

def test_deserialization(input_json):
    speakers = get_converter().structure(input_json, Speakers).speakers
    
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