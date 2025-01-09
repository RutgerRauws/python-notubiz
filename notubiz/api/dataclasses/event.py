from attrs import define, field
from cattrs import Converter
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


def event_hook(data : dict, cls: type) -> Event:
    # Auto-fill fields
    converter = Converter()
    converter.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
    event = converter.structure(data, Event)

    # Manually add some fields
    attributes = data.get("attributes", [])
    event.title = get_title(attributes)
    event.location = get_location(attributes)
    event.gremium_id = data["gremium"]["id"]
    
    return event