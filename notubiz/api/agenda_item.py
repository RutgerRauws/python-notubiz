from attrs import define
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


def get_start_date(attributes) -> datetime:
    return parse_date(get_attribute(attributes, 82))

def get_end_date(attributes) -> datetime:
    return parse_date(get_attribute(attributes, 83))


def agenda_item_structure_hook(data: Dict[str, Any], cls: type) -> AgendaItem:
    attributes = data["type_data"]["attributes"]

    return AgendaItem(
        id=data["id"],
        last_modified = parse_date(data["last_modified"]),
        title = get_title(attributes),
        description = get_description(attributes),
        start_date = get_start_date(attributes),
        end_date = get_end_date(attributes),
        is_heading = data["type_data"]["heading"]
    )


class NotubizAgendaItems:
    def from_json(json_object : any) -> list[AgendaItem]:
        c = cattrs.Converter()
        
        c.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
        c.register_structure_hook(AgendaItem, agenda_item_structure_hook)

        agenda_items =  [c.structure(item, AgendaItem) for item in json_object]

        return agenda_items
    