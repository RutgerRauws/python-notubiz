from attrs import define, field
import cattrs
from cattrs import transform_error

from notubiz.api._helpers import get_title, get_location
from notubiz.api.dataclasses.agenda_item import AgendaItem, AgendaItems

from typing import Optional, Dict, Any

@define
class Meeting:
    id : int
    url : str
    title : Optional[str] = field(default=None)
    location : Optional[str] = field(default=None)
    agenda_items : list[AgendaItem] = field(factory=list)

    @staticmethod
    def from_json(json_object : any) -> 'Meeting':
        c = cattrs.Converter()
        c.register_structure_hook(Meeting, meeting_structure_hook)

        try:
            meeting = c.structure(json_object["meeting"], Meeting)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        return meeting

def meeting_structure_hook(data: Dict[str, Any], cls: type) -> Meeting:
    attributes = data.get("attributes", [])
    title = get_title(attributes)
    location = get_location(attributes)

    # Use cattrs to structure the Meeting fields
    agenda_items = AgendaItems.from_json(data["agenda_items"])

    return Meeting(
        id=data["id"],
        url=data["url"],
        title=title,
        location=location,
        agenda_items=agenda_items
    )