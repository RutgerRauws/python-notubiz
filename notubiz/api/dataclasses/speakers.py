from attrs import define, field
from cattr import Converter
from datetime import datetime

from notubiz.api._helpers import parse_date

@define
class SpeakerAttributes:
    id: int
    person_id: int
    active: int
    last_modified: datetime

@define
class Speaker:
    # Auto-filled
    photo: str
    party: str
    email: str
    initials: str
    firstname: str
    lastname: str
    sex: str
    function: str
    url: str

    # Manually filled
    attributes: SpeakerAttributes = field(init=False)

    def full_name(self):
        return self.firstname + " " + self.lastname

def speaker_hook(data: dict[str, any], cls: type) -> Speaker:
    # Auto-fill fields
    converter = Converter()    
    converter.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
    
    speaker = converter.structure(data, cls)

    # Manually add some fields
    speaker.attributes = converter.structure(data.get("@attributes", {}), SpeakerAttributes)

    return speaker

@define
class Speakers:
    speakers: list[Speaker]

    def find_by_speaker_id(self, speaker_id : int):
        for speaker in self.speakers:
            if speaker.attributes.id == speaker_id:
                return speaker
        
        return None
    
    # TODO: return all speaker objects (there can be multiple)
    def find_by_person_id(self, person_id : int):
        for speaker in self.speakers:
            if speaker.attributes.person_id == person_id:
                return speaker
        
        return None
    
def speakers_hook(data: dict[str, any], cls: type) -> Speakers:
    speakers_json_arary = data["speakers"]["speaker"]

    c = Converter()
    c.register_structure_hook(Speaker, speaker_hook)

    speakers = [c.structure(speaker_json, Speaker) for speaker_json in speakers_json_arary]

    return Speakers(speakers)
