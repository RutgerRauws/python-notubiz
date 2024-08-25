from attrs import define, field
import cattrs
from cattrs import transform_error

from notubiz.api.agenda_item import AgendaItem, NotubizAgendaItems
from notubiz import ApiClient

from typing import Optional, Dict, Any

@define
class Meeting:
    id : int
    url : str
    title : Optional[str] = field(default=None)
    location : Optional[str] = field(default=None)
    agenda_items : list[AgendaItem] = field(factory=list)


def get_attribute(attributes, id) -> str:
    attribute = [attribute for attribute in attributes if attribute["id"] == id]

    if len(attribute) <= 0:
        raise Exception("Did not find attribute")
    elif len(attribute) > 1:
        raise Exception("Found attribute collision")

    return attribute[0]["value"]

def meeting_structure_hook(data: Dict[str, Any], cls: type) -> Meeting:
    attributes = data.get("attributes", [])
    title = get_attribute(attributes, 1)
    location = get_attribute(attributes, 50)

    # Use cattrs to structure the Meeting fields
    agenda_items = NotubizAgendaItems.from_json(data["agenda_items"])

    return Meeting(
        id=data["id"],
        url=data["url"],
        title=title,
        location=location,
        agenda_items=agenda_items
    )

class NotubizMeeting:
    api_client : ApiClient

    def __init__(self, api_client : ApiClient):
        self.api_client = api_client

    def get(self, meeting_id : int) -> Meeting:
        json_object = self.api_client.get("events/meetings/{}".format(meeting_id))
        return NotubizMeeting.from_json(json_object)
    
    def from_json(json_object : any) -> Meeting:
        c = cattrs.Converter()
        c.register_structure_hook(Meeting, meeting_structure_hook)

        try:
            meeting = c.structure(json_object["meeting"], Meeting)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        return meeting