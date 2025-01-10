from attrs import define, field
from cattr import Converter

from datetime import datetime

from notubiz.api._helpers import parse_date, get_title, get_location
from notubiz.api.dataclasses.agenda_item import AgendaItem, agenda_item_hook
from typing import Optional

@define
class Meeting:
    # Auto-filled
    id : int
    url : str
    body: str
    confidential: bool
    announcement: bool
    canceled: bool
    inactive: bool
    creation_date: datetime
    last_modified: datetime
    live: bool

    agenda_items : list[AgendaItem]

    # Manually filled
    title : Optional[str] = field(init=False)
    location : Optional[str] = field(init=False)


def meeting_hook(data: dict[str, any], cls: type) -> Meeting:
    # The meeting object is nested inside a 'meeting' key, let's remove that:
    data = data["meeting"]

    # Auto-fill fields
    converter = Converter()    
    converter.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
    converter.register_structure_hook(AgendaItem, agenda_item_hook)
    
    meeting = converter.structure(data, Meeting)

    # Manually add some fields
    attributes = data.get("attributes", [])
    meeting.title    = get_title(attributes)
    meeting.location = get_location(attributes)

    return meeting