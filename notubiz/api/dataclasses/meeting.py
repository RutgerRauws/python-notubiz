from attrs import define, field
import cattrs
from cattrs import transform_error

from notubiz.api._helpers import get_title, get_location
from notubiz.api.dataclasses.agenda_item import AgendaItem, AgendaItems

from typing import Optional, Dict, Any

@define
class Meeting:
    # Auto-filled
    id : int
    url : str

    # Manually filled
    title : Optional[str] = field(init=False)
    location : Optional[str] = field(init=False)
    agenda_items : list[AgendaItem] = field(init=False)

    @staticmethod
    def from_json(json_object : any) -> 'Meeting':
        c = cattrs.Converter()

        meeting_json = json_object.get("meeting", {})

        try:
            meeting = c.structure(meeting_json, Meeting)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        attributes = meeting_json.get("attributes", [])
        meeting.title = get_title(attributes)
        meeting.location = get_location(attributes)

        meeting.agenda_items = AgendaItems.from_json(meeting_json.get("agenda_items"))

        return meeting