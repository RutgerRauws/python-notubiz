from attrs import define, field
import cattrs

from datetime import datetime
from typing import Optional, Dict, Any

from notubiz.api._helpers import parse_date, get_attribute, get_title, get_description

@define
class AgendaItem:
    id : int
    last_modified : datetime
    title : str
    description: str
    start_date : Optional[datetime]
    end_date : Optional[datetime]
    is_heading : bool
    agenda_items : list['AgendaItem'] = field(factory=list)


def get_start_date(attributes) -> datetime:
    try:
        return parse_date(get_attribute(attributes, 82))
    except Exception: # The nested agenda items seem to have no start dates.
        return None

def get_end_date(attributes) -> datetime:
    try:
        return parse_date(get_attribute(attributes, 83))
    except Exception: # The nested agenda items seem to have no end dates.
        return None

def agenda_item_structure_hook(data: Dict[str, Any], cls: type) -> AgendaItem:
    type_data = data.get("type_data", {})
    attributes = type_data["attributes"]

    # Use cattrs to structure the Meeting fields
    agenda_items = NotubizAgendaItems.from_json(data["agenda_items"])

    return AgendaItem(
        id=data["id"],
        last_modified = parse_date(data["last_modified"]),
        title = get_title(attributes),
        description = get_description(attributes),
        start_date = get_start_date(attributes),
        end_date = get_end_date(attributes),
        is_heading = data["type_data"]["heading"],
        agenda_items = agenda_items
    )


class NotubizAgendaItems:
    def from_json(json_object : any) -> list[AgendaItem]:
        c = cattrs.Converter()
        
        c.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
        c.register_structure_hook(AgendaItem, agenda_item_structure_hook)

        agenda_items = [c.structure(item, AgendaItem) for item in json_object]

        return agenda_items
    