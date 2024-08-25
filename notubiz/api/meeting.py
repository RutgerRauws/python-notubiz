from attrs import define, field
import cattrs
from cattrs import transform_error

from notubiz import ApiClient
from notubiz.api._helpers import get_title, get_location
from notubiz.api.agenda_item import AgendaItem, NotubizAgendaItems

from typing import Optional, Dict, Any

@define
class Meeting:
    id : int
    url : str
    title : Optional[str] = field(default=None)
    location : Optional[str] = field(default=None)
    agenda_items : list[AgendaItem] = field(factory=list)


def meeting_structure_hook(data: Dict[str, Any], cls: type) -> Meeting:
    attributes = data.get("attributes", [])
    title = get_title(attributes)
    location = get_location(attributes)

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