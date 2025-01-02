from attrs import define, field
import cattrs
from typing import Optional, Dict, Any, List
from datetime import datetime

@define
class DocumentVersion:
    id: int
    file_name: str
    file_size: int
    mime_type: Optional[str] = field(default="") # Apparently some documents have no MIME type

@define
class Document:
    last_modified: datetime
    title: str
    version: int
    url: str
    versions: List[DocumentVersion]
    id: Optional[int] = field(default=None) # Apparently some documents have no ID

class NotubizDocument:
    def from_json(json_object : any) -> Document:
        c = cattrs.Converter()
        c.register_structure_hook(datetime, lambda d, _: datetime.strptime(d, "%Y-%m-%d %H:%M:%S"))

        return c.structure(json_object, Document)