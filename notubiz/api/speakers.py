from attrs import define
import cattrs
from cattrs import transform_error
from cattrs.gen import make_dict_unstructure_fn, make_dict_structure_fn, override
from typing import Optional

from notubiz.api_client import ApiClient

@define
class SpeakerAttributes:
    id: int
    person_id: int
    active: int
    last_modified: str

@define
class Speaker:
    photo: str
    party: str
    email: str
    initials: str
    firstname: str
    lastname: str
    sex: str
    function: str
    url: str
    attributes: SpeakerAttributes

    def full_name(self):
        return self.firstname + " " + self.lastname

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
    
class NotubizSpeakers:
    api_client : ApiClient

    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self) -> Speakers:
        json_object = self.api_client.get("speakers")
        return NotubizSpeakers.from_json(json_object)
    
    def from_json(json_object : any) -> Speakers:
        c = cattrs.Converter()

        unst_hook = make_dict_unstructure_fn(Speakers, c, speakers=override(rename="speaker"))
        st_hook = make_dict_structure_fn(Speakers, c, speakers=override(rename="speaker"))
        c.register_unstructure_hook(Speakers, unst_hook)
        c.register_structure_hook(Speakers, st_hook)

        unst_hook = make_dict_unstructure_fn(Speaker, c, attributes=override(rename="@attributes"))
        st_hook = make_dict_structure_fn(Speaker, c, attributes=override(rename="@attributes"))
        c.register_unstructure_hook(Speaker, unst_hook)
        c.register_structure_hook(Speaker, st_hook)

        try:
            speakers = c.structure(json_object["speakers"], Speakers)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        return speakers
