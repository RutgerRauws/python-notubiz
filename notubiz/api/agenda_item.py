from attrs import define
import cattrs
from cattrs.gen import make_dict_structure_fn, override

from datetime import datetime
from typing import Optional, Dict, Any

@define
class AgendaItem:
    id : int
    last_modified : datetime
    title : str
    description: str
    start_date : Optional[datetime]
    end_date : Optional[datetime]
    is_heading : bool


def get_attribute(attributes, id) -> str:
    attribute = [attribute for attribute in attributes if attribute["id"] == id]

    if len(attribute) <= 0:
        raise Exception("Did not find attribute")
    elif len(attribute) > 1:
        raise Exception("Found attribute collision")

    return attribute[0]["value"]

def get_title(attributes) -> str:
    return get_attribute(attributes, 1)

def get_description(attributes):
    try:
        return get_attribute(attributes, 3)
    except Exception:
        return ""

# def agenda_item_structure_hook(data: Dict[str, Any], cls: type) -> AgendaItem:
#     type_data = data.get("type_data", [])

#     return AgendaItem(
#         id = data["id"]
#         last_modified=["last_modified"]

#         title = type_data
#     )

def parse_date(date_string : str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

def get_start_date(attributes) -> datetime:
    return parse_date(get_attribute(attributes, 82))

def get_end_date(attributes) -> datetime:
    return parse_date(get_attribute(attributes, 83))

def agenda_item_structure_hook(data: Dict[str, Any], cls: type) -> AgendaItem:

    attributes = data["type_data"]["attributes"]

    return AgendaItem(
        id=data["id"],
        last_modified = data["last_modified"],
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
        # st_hook = make_dict_structure_fn(AgendaItem, c, title=override(rename="type_data", struct_hook=title_structure_hook))
        # c.register_structure_hook(AgendaItem, st_hook)

        # st_hook = make_dict_structure_fn(AgendaItem, c, description=override(rename="type_data", struct_hook=description_structure_hook))
        # c.register_structure_hook(AgendaItem, st_hook)

        # st_hook = make_dict_structure_fn(AgendaItem, c, is_heading=override(rename="type_data", struct_hook=is_heading_structure_hook))
        # c.register_structure_hook(AgendaItem, st_hook)

        agenda_items =  [c.structure(item, AgendaItem) for item in json_object]
        return agenda_items
    

    
        