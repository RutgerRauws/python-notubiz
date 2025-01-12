from cattr import Converter
from datetime import datetime

from notubiz.api._helpers import parse_date
from notubiz.api._hooks_registry import Hooks

def get_converter() -> Converter:
    converter = Converter()
    converter.register_structure_hook(datetime, lambda date_string, _: parse_date(date_string))
    
    # Custom hooks
    for cls, hook in Hooks.items():
        converter.register_structure_hook(cls, hook)

    return converter