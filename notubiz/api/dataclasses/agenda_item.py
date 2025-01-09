from attrs import define, field
from cattr import Converter

from datetime import datetime
from typing import Optional

from notubiz.api._helpers import parse_date, get_attribute, get_title, get_description
from notubiz.api.dataclasses.document import Document

@define
class AgendaItem:
    # Auto-filled fields
    id : int
    last_modified : datetime
    documents: list[Document]

    # Filled manually
    title : str = field(init=False)
    description: str = field(init=False)
    start_date : Optional[datetime] = field(init=False)
    end_date : Optional[datetime] = field(init=False)
    is_heading : bool = field(init=False)
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

def agenda_item_hook(data: dict[str, any], cls: type) -> AgendaItem:
    # Auto-fill fields

    converter = Converter()
    converter.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
    converter.register_structure_hook(AgendaItem, agenda_item_hook)
    documents = [converter.structure(item, Document) for item in data.get("documents", [])]

    agenda_item = AgendaItem(
        id = data.get("id"),
        last_modified = parse_date(data.get("last_modified")), 
        documents = documents
    )

    # Manually add some fields
    type_data = data.get("type_data", {})
    attributes = type_data["attributes"]

    agenda_item.title = get_title(attributes)
    agenda_item.description = get_description(attributes)
    agenda_item.start_date = get_start_date(attributes)
    agenda_item.end_date = get_end_date(attributes)
    agenda_item.is_heading = type_data.get("heading", False)

    agenda_item.agenda_items = [converter.structure(item, AgendaItem) for item in data.get("agenda_items", [])]
    
    return agenda_item
