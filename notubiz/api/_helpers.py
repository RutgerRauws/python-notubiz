from datetime import datetime
from typing import Optional

def get_attribute(attributes, id) -> str:
    attribute = [attribute for attribute in attributes if attribute["id"] == id]

    if len(attribute) <= 0:
        raise Exception("Did not find attribute")
    elif len(attribute) > 1:
        raise Exception("Found attribute collision")

    return attribute[0]["value"]

def get_title(attributes) -> Optional[str]:
    try:
        return get_attribute(attributes, 1)
    except Exception:
        return None

def get_description(attributes) -> Optional[str]:
    try:
        return get_attribute(attributes, 3)
    except Exception:
        return None
    
def get_location(attributes) -> Optional[str]:
    try:
        return get_attribute(attributes, 50)
    except Exception:
        return None

def parse_date(date_string : str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")