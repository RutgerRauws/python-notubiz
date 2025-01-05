from attrs import define, field
import cattrs
from cattrs import transform_error

from typing import Optional

from datetime import datetime
from notubiz.api._helpers import parse_date, get_title, get_location
from notubiz.api.dataclasses.planning import Planning

@define
class Event:
    # Auto-filled
    id: int
    type: str
    permission_group: str
    body: str
    confidential: bool
    announcement: bool
    canceled: bool
    inactive: bool
    creation_date: datetime
    last_modified: datetime
    live: bool
    archive_state: str
    archive_state_last_modified: Optional[datetime]
    allow_subscriptions: bool
    plannings: list[Planning]

    # Manually filled
    title: str = field(init=False)
    location: str = field(init=False)
    gremium_id: int = field(init=False)

    @staticmethod
    def from_json(json_object : any) -> 'Event':
        c = cattrs.Converter()

        c.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))

        try:
            meeting = c.structure(json_object, Event)
        except Exception as exc:
            print("\n".join(transform_error(exc)))
            quit()

        attributes = json_object.get("attributes", [])
        meeting.title = get_title(attributes)
        meeting.location = get_location(attributes)
        meeting.gremium_id = json_object["gremium"]["id"]

        return meeting